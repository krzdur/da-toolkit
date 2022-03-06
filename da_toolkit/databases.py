import pandas as pd
from sqlalchemy import create_engine

from google.cloud import bigquery
from google.oauth2 import service_account

import os

from da_toolkit.config import Config
Config.load('config.env')


class Redshift:

    def __init__(self):
        self.db_url = os.getenv('RDS_HOST')
        self.db_port = os.getenv('RDS_PORT')
        self.db_name = os.getenv('RDS_NAME')
        self.engine = create_engine(
            'postgresql://{0}:{1}/{2}'.format(self.db_url, self.db_port, self.db_name),
            isolation_level="AUTOCOMMIT")

    def query(self, query):
        df = pd.read_sql_query(sql=query, con=self.engine)
        return df

    def append(self, df, table):
        """Appends a dataframe to a pointed Redshift table. The user has to have update access
        Arguments:
            df :
                a Pandas DataFrame you want to add to Redshift
            table :
                a table you want to append you df to; must contain schema name e.g "schema_name.test_table"
        """
        schema, table = table.split('.')
        df.to_sql(table, self.engine, index=False, if_exists='append', schema=schema)


class BigQuery:

    def __init__(self):
        self.client = None
        self.project = os.getenv('GCP_PROJECT_NAME')
        self.service_account = os.getenv('SERVICE_ACCOUNT_FILE')
        self.connect()

    def connect(self):
        credentials = service_account.Credentials.from_service_account_file(
            self.service_account)
        self.client = bigquery.Client(project=self.project, credentials=credentials)

    def query(self, query):
        query_job = self.client.query(query)  # API request
        df = query_job.result()\
            .to_dataframe()  # Waits for query to finish
        return df