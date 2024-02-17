# Postpone

Postpone is a Python library for simplifying the deployment of serverless functions as a service. It streamlines the process of connecting with AWS, creating a Lambda function, setting up a rule, and configuring triggers, all with just a few simple commands.

## Features

- **Easy Deployment**: Deploy serverless functions effortlessly with just two commands.
- **AWS Integration**: Seamlessly integrates with AWS services for robust serverless functionality.
- **Automated Setup**: Handles Lambda function creation, rule setup, and trigger configuration automatically.
- **Open Source**: Postpone is an open-source project, that welcomes contributions and feedback from the community.

## Installation

1. Put your credentials in the .env file then,

2. You can compile Postpone via bash:

    ```bash
        python3 setup.py sdist bdist_wheel
    ```

3. Then install it via: 
    ```bash
    pip install <generated_file_name>
    ```

## Usage

Compile Postpone.

Create your serverless function with Python and save it in a file, e.g., my_function.py.

Configure your AWS using:
```
postpone-setup
```

Deploy your function using the postpone deploy command:
```
postpone-deploy
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)