from game_apis.data_flow import DataFlow
from sqlalchemy import create_engine, event
import yaml

class SQLFlow(DataFlow):
    ID = 'SQL_CREDS'

    def __init__(self, config, sandbox=False, local_config=False):
        super().__init__(config, sandbox, local_config)

        self.db_user = self.config['db_user']
        self.db_pass = self.config['db_pass']
        self.db_server = self.config['db_server']
        self.db_name = self.config['db_name']


    def load(self, df, tablename, **kwags):
        # use event listener to increase the speed of executemany
        @event.listens_for(self.conn, 'before_cursor_execute')
        def receive_before_cursor_execute(conn, cursor, statement, params, context, executemany):
            if executemany:
                cursor.fast_executemany = True

        df.to_sql(
                name = tablename,
                schema = schema,
                con = self.conn,
                **kwags
            )


class PostgresSQLFlow(SQLFlow):
    def __init__(self, config, sandbox=False, local_config=False):
        super().__init__(config, sandbox, local_config)

        self.conn = create_engine(
            'postgresql+psycopg2://{0}:{1}@{2}/{3}?'.\
            format(
                self.db_user,
                self.db_pass,
                self.db_server,
                self.db_name
            )
        )

class MSSQLFlow(SQLFlow):
    def __init__(self, config, sandbox=False, local_config=False):
        super().__init__(config, sandbox, local_config)

        self.conn = create_engine(
            'mssql+pyodbc://{0}:{1}@{2}/{3}?'
            'driver=SQL+Server+Native+Client+11.0'.\
            format(
                self.db_user,
                self.db_pass,
                self.db_server,
                self.db_name
            )
        )
