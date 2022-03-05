# Data Analytics toolkit

Python library optimizing some manual tasks of Data Analysts.

I built it to automate routine tasks related to connecting to databases are running statistical checks for experiments.


## Installation
1. Install the library by running this code:

```
# it's nice to start with creating a virtual environment (but is not required).
python -m venv my_env

pip install git+https://github.com/krzdur/da-toolkit.git
```

2. Create your own `config.py` file. It will contain your Redshift credentials and 
Google Cloud service account json. Follow the
example in `config-TEMPLATE.py` and put it into your working directory (the main 
catalog that you work in).
```python
# redshift credentials
login='your-login'
password='your-password'

# Google Cloud service_account.json path
gc_account = './path/to_the_file.json'
```
   
3. (optional) To query BigQuery data, you will need a service account key (json file) with appropriate
credentials.

## Use cases

Currently, the library optimizes two types of tasks:
* connecting and querying 2 types of databases: AWS Redshift & GCP BigQuery;
* running basic statistical checks (z-test) for experiments (A/B tests) metrics, both for proportions and means.

To find out more take a look at [the examples](https://github.com/krzdur/da-toolkit/tree/master/examples).

## Contribution

Everyone is free and welcome to fork and use the code.