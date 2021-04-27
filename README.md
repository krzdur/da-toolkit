# Data Analytics toolkit

---

Python library optimizing some manual task of  krzdurData Analysts


## Installation
1. Install the library by running this code:

```
# would be nice to start with creating a virtual environment (but is not required).
python -m venv my_env

pip install git+https://github.com/brainly/da-toolkit.git
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
credentials. If you don't know how to get it, reach out to one of your fellow analysts.



To start off take a look at [the examples](https://github.com/brainly/da-toolkit/tree/master/examples).

## Contribution

Every Data Analyst is invited to contribute to the project. :)