# Data Analyst toolkit

Python library optimizing some manual tasks of Data Analysts.

I built it to automate routine tasks related to connecting to databases are running statistical checks for experiments.


## Installation
1. Install the library by running this code:

```
# it's nice to start with creating a virtual environment (but is not required).
python -m venv my_env

pip install git+https://github.com/krzdur/da-toolkit.git
```

2. Create configuration file by running:
```terminal
python -m da_toolkit
```
The installer will ask you a couple of simple questions that will help you to
setup database connections. (To query BigQuery data, you will need a service account key (json file) with appropriate
credentials)
```bash
Do you want to configure your AWS Redshift credentials? [y/n]
```
This step is optional if you don't want to use this feature.

After going through the instructions you should see `da_toolkit_config.env` file created.
It stores the credentials provided and will load them as environment variables.

## Use cases

Currently, the library optimizes two types of tasks:
* connecting and querying 2 types of databases: AWS Redshift & GCP BigQuery;
* running basic statistical checks (z-test) for experiments (A/B tests) metrics, both for proportions and means.

To find out more take a look at [the examples](https://github.com/krzdur/da-toolkit/tree/master/examples).

## Contribution

Everyone is free and welcome to fork and reuse the code.