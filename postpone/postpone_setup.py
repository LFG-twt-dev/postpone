import click
import os
import subprocess
from dotenv import load_dotenv

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
def postpone_setup():
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

if __name__ == '__main__':
    postpone_setup()
