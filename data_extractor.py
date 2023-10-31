from database_utils import DatabaseConnector
import tabula
import validators
import pandas as pd
class DataExtractor:

    def __init__(self):
        
        self.file = 'db_creds.yaml'
        self.rds_db_con = DatabaseConnector(self.file)
        self.engine = self.rds_db_con.init_db_engine()

    def list_db_tables(self): #lists tables
        from sqlalchemy import MetaData, inspect

        inspector = inspect(self.engine)

        return inspector.get_table_names()

    def read_rds_table(self, table): #sql table to pandas dataframe
        

        df = pd.read_sql_table(table, self.engine)
        return df
    
    def retrieve_pdf_data(self, link):
        class ValidationError(Exception):
            pass

        try:
            if not validators.url(link):
                raise ValidationError
        except ValidationError:
            print(f'The URL ({link}) you have provided is invalid, please try again.')
   
        pdf_data = tabula.read_pdf(link, pages='all',multiple_tables=True)

        df = pd.concat(pdf_data, ignore_index=True)

        return df
    