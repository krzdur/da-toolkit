import pandas as pd
from sqlalchemy import create_engine

from google.cloud import bigquery
from google.oauth2 import service_account

import config


class Redshift:

    def __init__(self, login=config.login, password=config.password):
        self.login = login
        self.password = password
        self.engine = None
        self.connect()

    def connect(self):
        self.engine = create_engine(
            'postgresql://{0}:{1}@redshift.z-dn.net:5439/prod'.format(self.login, self.password),
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
                a table you want to append you df to; must contain schema name e.g "krzysztof_durbajlo.test_table"
        """
        schema, table = table.split('.')
        df.to_sql(table, self.engine, index=False, if_exists='append', schema=schema)


class BigQuery:

    def __init__(self, project='brainly-bi'):
        self.client = None
        self.project = project
        self.connect()

    def connect(self):
        credentials = service_account.Credentials.from_service_account_file(
            config.gc_account)
        self.client = bigquery.Client(project=self.project, credentials=credentials)

    def query(self, query):
        query_job = self.client.query(query)  # API request
        results = query_job.result()  # Waits for query to finish
        df = results.to_dataframe()
        return df