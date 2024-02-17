import click
import os
import subprocess
from dotenv import load_dotenv
import json
import postpone.policy  # Make sure this module and the policy attribute exist
import uuid

def is_aws_cli_installed():
    """Check if AWS CLI is installed by trying to get its version."""
    try:
        result = subprocess.run(["aws", "--version"], capture_output=True, text=True, check=True)
        print(f"AWS CLI is installed. Version info:\n{result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print("AWS CLI is not installed or not found in PATH.")
        return False
    except FileNotFoundError:
        print("AWS CLI is not installed or not found in PATH.")
        return False
    except Exception:
        print("Random exception",Exception)
        return False
    
def install_aws_cli():
    if is_aws_cli_installed():
        print("AWS CLI is already installed.")
        return

    # The rest of your original installation logic here...
    if os.name == 'posix':
        os_info = os.uname()
        if os_info.sysname == 'Linux':
            arch = os_info.machine
            if arch == 'x86_64':
                download_url = "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip"
            elif arch == 'aarch64':
                download_url = "https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip"
            else:
                raise ValueError("Unsupported architecture")
            install_cmd = "unzip awscliv2.zip && sudo ./aws/install"
        elif os_info.sysname == 'Darwin':
            download_url = "https://awscli.amazonaws.com/AWSCLIV2.pkg"
            install_cmd = "sudo installer -pkg AWSCLIV2.pkg -target /"
        else:
            raise ValueError("Unsupported POSIX system")

        curl_cmd = f"curl '{download_url}' -o 'awscliv2.zip'"
        subprocess.run(curl_cmd, shell=True, check=True)
        subprocess.run(install_cmd, shell=True, check=True)

    elif os.name == 'nt':
        download_url = "https://awscli.amazonaws.com/AWSCLIV2.msi"
        install_cmd = "msiexec.exe /i AWSCLIV2.msi"
        subprocess.run(f"curl '{download_url}' -o 'AWSCLIV2.msi'", shell=True, check=True)
        subprocess.run(install_cmd, shell=True, check=True)
    else:
        raise ValueError("Unsupported operating system")

@click.command()
def configure_aws():
    load_dotenv()
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    default_region = os.getenv("AWS_DEFAULT_REGION")
    default_output = os.getenv("AWS_DEFAULT_OUTPUT")

    # Install AWS CLI
    install_aws_cli()

    # Configure AWS CLI
    subprocess.run(f"aws configure set aws_access_key_id {aws_access_key_id}", shell=True)
    subprocess.run(f"aws configure set aws_secret_access_key {aws_secret_access_key}", shell=True)
    subprocess.run(f"aws configure set default.region {default_region}", shell=True)
    subprocess.run(f"aws configure set default.output {default_output}", shell=True)
    policy_string = json.dumps(postpone.policy.policy)
    role_uuid = uuid.uuid4()

    # Common AWS tasks
    
    subprocess.run(f"aws iam create-role --role-name {role_uuid} --assume-role-policy-document '{policy_string}'", shell=True)
    subprocess.run(f"aws iam attach-role-policy --role-name {role_uuid}  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole", shell=True)

# Function to create a new Lambda function
def create_lambda_function(function_name, zip_file_location, handler, runtime, role_arn):
    subprocess.run(f"aws lambda create-function --function-name {function_name} "
                   f"--zip-file fileb://{zip_file_location} "
                   f"--handler {handler} "
                   f"--runtime {runtime} "
                   f"--role {role_arn}", shell=True, check=True)

# ... (other functions)

# Command to perform additional AWS tasks
@click.command()
@click.option('--function-name', prompt='Enter Lambda Function Name', required=True, show_default=True)
@click.option('--zip-file-location', prompt='Enter Zip File Location', required=True, show_default=True)
@click.option('--handler', prompt='Enter Lambda Handler', default='index.handler', show_default=True)
@click.option('--runtime', prompt='Enter Lambda Runtime', default='python3.8', show_default=True)
@click.option('--role-arn', prompt='Enter IAM Role ARN', required=True, show_default=True)
def additional_aws_tasks(function_name, zip_file_location, handler, runtime, role_arn):
    create_lambda_function(function_name, zip_file_location, handler, runtime, role_arn)
    # Add other tasks as needed (e.g., update_lambda_function, list_lambda_functions, create_new_rule, etc.)

# ... (other functions)

if __name__ == '__main__':
    configure_aws()
    additional_aws_tasks()
