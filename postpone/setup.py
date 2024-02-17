from setuptools import setup, find_packages
print(find_packages())
setup(
    name='postpone',
    version='1.0',
    packages=['postpone'],
    include_package_data=True,
    install_requires=[
        'click',
        'python-dotenv',
    ],
    entry_points='''
        [console_scripts]
        postpone-setup=postpone.aws_cli_setup:postpone_configure
        postpone-deploy=postpone.aws_cli_setup:postpone_deploy
    ''',
)
