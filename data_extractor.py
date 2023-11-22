import requests
import validators
import pandas as pd
from sqlalchemy import inspect
import tabula
import boto3
from database_utils import DatabaseConnector


class DataExtractor:
    ''' This class is used to extract data from various sources.

        Methods: 
            list_db_tables (): This method retrieves table names from the 
            RDS database.
            read_rds_table (`str`): This method returns the specified table 
            (as a `dataframe`) from the RDS database.
            retrieve_pdf_data (`str`): This method returns a `dataframe` 
            corresponding to the table in a PDF.
            list_number_of_stores (): This method gives us the number of stores.
            retrieve_stores_data (): This method retrieves data for each store
              and returns a dataframe.
            extract_from_s3 (`str`): This method retrieves a table from the S3 bucket.
    
        Attributes: 
            file (`str`): A YAML file containing database credentials.
            rds_db_con (`DatabaseConnector`): An instance of the DatabaseConnector 
            class for database connections.
            engine (sqlalchemy.engine.Engine): An SQLAlchemy database engine 
            for database connections.
            headers_stores (`dict`): HTTP request headers for accessing store data.

    '''

    def __init__(self):
        ''' This is used to initialise the class.

        '''
        
        self.file = 'db_creds.yaml'
        self.rds_db_con = DatabaseConnector(self.file)
        self.engine = self.rds_db_con.init_db_engine()
        self.headers_stores = {
            "Content-Type": "application/json",
            "x-api-key": "<insert_key_here>"
        }

    def list_db_tables(self):
        '''This method is used to get the table names from the RDS database.

        This method uses the SQLAlchemy inspector to inspect the connected 
        database and obtain a list of table names from the RDS database.

        Returns:
            table_names (`list` of `str`): This is a list of the RDS database table 
            names we are interested in.
        
        '''

        with self.engine.begin() as connection:
            inspector = inspect(connection)

            table_names = inspector.get_table_names()

        return table_names

    def read_rds_table(self, table):
        '''This method retrieves the specified table from the RDS database.

        This method reads data from the specified table in the RDS database 
        using the SQLAlchemy `pd.read_sql_table` function.

        Args:
            table (`str`): The name of the table we want to retrieve.

        Returns:
            df (`dataframe`): The table which has been converted into a dataframe.
        
        '''
        
        with self.engine.begin() as connection:
            df = pd.read_sql_table(table, connection)

        return df
    
    def retrieve_pdf_data(self, link):
        ''' Retrieves tabular data from a PDF document available at the specified URL.

        This method fetches tabular data from a PDF document via the provided URL. 
        We validate the URL. If the URL is correct, the dataframe is returned. 
        If the URL is invalid, None is retured.

        Args:
            link (`str`): The URL of the PDF document to extract data from.

        Raises:
            ValidationError: Raised if the provided URL is invalid.

        Returns:
            pdf_data (`dataframe`) or `None`: A DataFrame containing extracted 
            tabular data from the PDF or None in case of an invalid URL.
        
        '''

        class ValidationError(Exception):
            pass

        try:
            if not validators.url(link):
                raise ValidationError
        except ValidationError:
            print(f'The URL ({link}) you have provided is invalid, please try again.')
            return
   
        pdf_data = tabula.read_pdf(link, pages='all',multiple_tables=True)

        pdf_data = pd.concat(pdf_data, ignore_index=True)

        return pdf_data

    def list_number_of_stores(self):
        ''' This method fetchs and returns the total number of stores from an API.

        This method sends a HTTP GET request to an API to obtain the total number 
        of stores. We then extract and return the number of stores from the API response.

        Returns:
            number_of_stores (`int`): The total number of stores.
        
        '''

        url = " https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores"
        response = requests.get(url, headers=self.headers_stores).json()
        number_of_stores = response['number_stores']

        return number_of_stores

    def retrieve_stores_data(self):
        '''This method retrieves data for each store and return it as a dataframe.

        This method fetches data for each store from a remote API and constructs it 
        into a dataframe. We use the `number_of_stores` method to get the numbers of 
        stores. We then iteratively retrieve data for each store, and then combine it into a dataframe.

        Return:
           store_data (`dataframe`): A dataframe containing data for each store.
        
        '''

        number_of_stores = DataExtractor().list_number_of_stores()

        store_data = pd.DataFrame()

        for store_number in range(number_of_stores):

            url = f'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/{store_number}'

            response = requests.get(url, headers=self.headers_stores).json()

            df_for_store = pd.DataFrame([response])
            store_data = pd.concat([store_data, df_for_store], ignore_index=True)
        
        store_data = store_data.set_index('index')

        return store_data

    def extract_from_s3(self, link):
        ''' This method retrieves a table from an S3 bucket and return it as a dataframe.

        This method fetches a table from an S3 bucket using the provided S3 URL, 
        downloads it, and returns the table data as a dataframe. It supports both CSV and JSON formats.

        Args:
            link (`str`): The S3 URL of the table to extract.

        Returns:
            df (`dataframe`): A dataframe containing the table data from the S3 bucket.

        '''

        link_parts = link.split('/')

        s3 = boto3.client('s3')
        s3.download_file('data-handling-public', link_parts[-1], link_parts[-1])

        if '.csv' in link_parts[-1]:
            df = pd.read_csv(link_parts[-1])

        elif '.json' in link_parts[-1]:
            df = pd.read_json(link_parts[-1])

        return df