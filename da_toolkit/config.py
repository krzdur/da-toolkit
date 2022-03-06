from getpass import getpass
from pathlib import Path

from dotenv import load_dotenv


class Config:

    def __init__(self):
        self.f = open('config.env', 'w')

    def get_bq_creds(self):
        """ Getting credentials for BigQuery"""
        proceed = input("Do you want to configure your BigQuery credentials? [y/n]")

        if proceed.lower() == 'y':
            service_acc = input('Currently, BigQuery authentication is only available via service accounts. \n'
                                'Put the path to your service account .json in here:')
            project = input('Provide Google Cloud Platform project name:\t')

            self.f.write('SERVICE_ACCOUNT_FILE={}\n'.format(Path(service_acc)))
            self.f.write('GCP_PROJECT_NAME={}\n'.format(project))
        elif proceed.lower() == 'n':
            pass
        else:
            raise ValueError('Please answer "y" or "no"')

    def get_redshift_creds(self):
        """ Getting credentials for AWS Redshift"""
        proceed = input("Do you want to configure your AWS Redshift credentials? [y/n]")
        if proceed.lower() == 'y':
            host = input('Provide host address:\t')
            name = input('What is the database name?\t')
            port = (input('You can change the port number. The default is set to 5439.\t') or 5439)
            login = input('Provide your Redshift user name:\t')
            password = getpass('Password:\t')

            self.f.write('RDS_HOST=\'{0}:{1}@{2}\'\n'.format(login, password, host, port, name))
            self.f.write('RDS_PORT=\'{}\'\n'.format(port))
            self.f.write('RDS_NAME=\'{}\'\n'.format(name))
        elif proceed.lower() == 'n':
            pass
        else:
            raise ValueError('Please answer "y" or "no"')

    @staticmethod
    def load(path='.../config.env'):
        load_dotenv(path)
