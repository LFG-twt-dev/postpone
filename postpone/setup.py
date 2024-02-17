from setuptools import setup, find_packages
print(find_packages())
setup(
    name='aws-cli-setup',
    version='5.0',
    packages=['postpone'],
    include_package_data=True,
    install_requires=[
        'click',
        'python-dotenv',
    ],
    entry_points='''
        [console_scripts]
        aws-cli-setup=postpone.aws_cli_setup:configure_aws
        aws-cli-deploy=postpone.aws_cli_setup:additional_aws_tasks
    ''',
)
