from setuptools import setup, find_packages

setup(
    name='aws-cli-setup',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'python-dotenv',
    ],
    entry_points='''
        [console_scripts]
        aws-cli-setup=aws_cli_setup:configure_aws
    ''',
)