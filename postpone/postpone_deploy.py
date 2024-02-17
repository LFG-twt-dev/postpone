import click
import os
import subprocess
from dotenv import load_dotenv
import json
import postpone.policy  # Make sure this module and the policy attribute exist
import uuid
import time

# Function to create a new Lambda function
def create_lambda_function(function_name, zip_file_location, handler, runtime, role_arn):
    result= subprocess.run(f"aws lambda create-function --function-name {function_name} "
                   f"--zip-file fileb://{zip_file_location} "
                   f"--handler {handler} "
                   f"--runtime {runtime} "
                   f'--role "{role_arn}"', text=True, check=True,capture_output=True,shell=True)
    
    function_details = json.loads(result.stdout)
        # Extract the Function ARN
    function_arn = function_details['FunctionArn']
    return function_arn

def set_lambda_rule(function_arn,rule_name):
    target_details=subprocess.run(f'aws events put-targets --rule {rule_name} --targets "Id"={uuid.uuid4()},"Arn"="{function_arn}" --output json',capture_output=True,shell=True)
    return target_details

def setup_trigger(function_name,rule_name):
    
    result = subprocess.run(f'aws lambda add-permission --function-name "{function_name}" --action "lambda:InvokeFunction" --principal events.amazonaws.com --statement-id MyEvent --source-arn $(aws events describe-rule --name "{rule_name}"  --query "Arn" --output "text") --output "json"', capture_output=True, text=True,shell=True)

    # Output the result or handle errors
    if result.returncode == 0:
        print("Permission added successfully.")
        print(result.stdout)
    else:
        print("Error adding permission:")
        print(result)
        print(result.stderr)
    return result



# Command to perform additional AWS tasks
@click.command()
@click.option('--file-name', prompt='Enter Lambda File Name', required=True, default="lambda_function", show_default=True)
@click.option('--handler', prompt='Enter Lambda Handler', default='lambda_function.handler', show_default=True)
@click.option('--runtime', prompt='Enter Lambda Runtime', default='python3.8', show_default=True)
@click.option('--minutes', prompt='After how many minutes do you want to run the job', required=True, default=2, show_default=True)
def postpone_deploy(file_name, handler, runtime, minutes):
    policy_string = json.dumps(postpone.policy.policy)
    role_uuid = str(uuid.uuid4()).replace('-','')
    role_data = subprocess.run(f"aws iam create-role --role-name {role_uuid} --assume-role-policy-document '{policy_string}'", shell=True, text=True, capture_output=True)
    role_data_json = json.loads(role_data.stdout)
    role_arn = role_data_json["Role"]["Arn"]
    time.sleep(3)
    subprocess.run(f"aws iam attach-role-policy --role-name {role_uuid}  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole", shell=True,text=True, capture_output=True)
    subprocess.run(['zip', "./lambda.zip", "./"+file_name+".py"], check=True)
    time.sleep(3)
    function_name=str(uuid.uuid4()).replace('-','')
    function_arn=create_lambda_function(function_name, "lambda.zip", handler, runtime, role_arn)
    rate_unit="minute"
    if(int(minutes)>1):
        rate_unit="minutes"
    if(int(minutes)<0):
        return "invalid time"
    time.sleep(3)
    rule_name=str(uuid.uuid4()).replace('-','')
    subprocess.run(f'aws events put-rule --schedule-expression "rate({minutes} {rate_unit})" --name {rule_name}',text=True, capture_output=True,shell=True)
    time.sleep(3)
    set_lambda_rule(function_arn,rule_name)
    time.sleep(3)
    result=setup_trigger(function_name,rule_name)

if __name__ == '__main__':
    postpone_deploy()
