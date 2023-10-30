class DataExtractor:

    def __init__(self, file_path):
        import database_utils
        self.file = file_path
        self.db_con = database_utils.DatabaseConnector(self.file)
        self.engine = self.db_con.init_db_engine()

    def list_db_tables(self): #lists tables
        from sqlalchemy import MetaData, inspect

        inspector = inspect(self.engine)

        return inspector.get_table_names()

    def read_rds_table(self, table):
        import pandas as pd

        df = pd.read_sql_table(table, self.engine)
        return df
