import click
import os
import subprocess
from dotenv import load_dotenv
import json
import postpone.policy

# Function to install AWS CLI based on OS
def install_aws_cli():
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
        install_cmd = "msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi"
        subprocess.run(install_cmd, shell=True, check=True)
    else:
        raise ValueError("Unsupported operating system")

# Command to configure AWS CLI using .env file
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
    policy_string=json.dumps(postpone.policy.policy)

    # Common AWS tasks
    subprocess.run("aws iam create-role --role-name lambda-ex --assume-role-policy-document"+policy_string, shell=True)
    subprocess.run("aws iam attach-role-policy --role-name lambda-ex --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole", shell=True)

if __name__ == '__main__':
    configure_aws()
