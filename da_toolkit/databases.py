import pandas as pd
from sqlalchemy import create_engine

from da_toolkit import config


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
