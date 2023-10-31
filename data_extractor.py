from database_utils import DatabaseConnector
import tabula
import validators
import pandas as pd
import requests
import boto3
class DataExtractor:

    def __init__(self):
        
        self.file = 'db_creds.yaml'
        self.rds_db_con = DatabaseConnector(self.file)
        self.engine = self.rds_db_con.init_db_engine()
        self.headers_stores = {
            "Content-Type": "application/json",
            "x-api-key": "yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX"
        }

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

    def list_number_of_stores(self):

        url = " https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores"
        response = requests.get(url, headers=self.headers_stores).json()
        number_of_stores = response['number_stores']

        return number_of_stores

    def retrieve_stores_data(self):

        number_of_stores = DataExtractor().list_number_of_stores()

        store_data = pd.DataFrame()

        for store_number in range(number_of_stores):

            url = f'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/{store_number}'

            response = requests.get(url, headers=self.headers_stores).json()

            df_for_store = pd.DataFrame([response])
            store_data = pd.concat([store_data, df_for_store], ignore_index=True)
        
        store_data = store_data.set_index('index')

        return store_data

    def extract_from_s3(self):

        s3 = boto3.client('s3')
        s3.download_file('data-handling-public', 'products.csv', 'product_details.csv')

        product_details = pd.read_csv('product_details.csv')

        return product_details