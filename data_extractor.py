class DataExtractor:

    def __init__(self, file_path):
        import database_utils
        self.file = file_path
        self.db_con = database_utils.DatabaseConnector(self.file)

    def list_db_tables(self):
        from sqlalchemy import MetaData, inspect

        engine = self.db_con.init_db_engine()
        inspector = inspect(engine)

        return inspector.get_table_names()

        

db = DataExtractor('db_creds.yaml')

print(db.list_db_tables())