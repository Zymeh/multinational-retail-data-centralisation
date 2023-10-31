from sqlalchemy import create_engine
import os
import yaml

class DatabaseConnector:

    def __init__(self, file_path):
        self.file = file_path

    class NotYAMLFileError(Exception):
        "definining a custom exception for when the file isnt a YAML file."
        pass

    def read_db_creds(self): #reads the creds stored in the YAML file

        try:
            if not self.file.endswith('.yaml') and not self.file.endswith('.yml'):
                raise self.NotYAMLFileError("File is not a YAML file.")

            with open(self.file, 'r') as file:
                cred_dict = yaml.load(file, Loader=yaml.FullLoader)
            return cred_dict

        except FileNotFoundError as e:
            print(f'FileNotFoundError: {e}, please make sure you are using the correct file path.')
        except TypeError as e:
            print(f'TypeError: {e}, please make sure you are using a string for the file name.')
        except self.NotYAMLFileError as e:
            print(f'Error: please make sure you are using a YAML file')
        except ValueError as e:
            print(f'ValueError: {e}, please make sure you are trying to load a file')
        except yaml.YAMLError as e:
            print(f'YAMLError: {e}, please make sure your YAML file is in the correct syntax and/or has the correct structure')
        except AttributeError:
            print(f'AttributeError: please use the correct data type')

    def init_db_engine(self): #creating engine to be used when getting database from RDS

        credentials = self.read_db_creds()

        DATABASE_TYPE = 'postgresql'
        DBAPI = 'psycopg2'
        HOST = credentials["RDS_HOST"]
        USER = credentials["RDS_USER"]
        PASSWORD = credentials["RDS_PASSWORD"]
        DATABASE = credentials["RDS_DATABASE"]
        PORT = credentials["RDS_PORT"] 

        engine_for_extraction = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}", future=True)

        return engine_for_extraction

    def upload_to_db(self, cleaned_dataframe, table_name): 
        
        DATABASE_TYPE = 'postgresql'
        DBAPI = 'psycopg2'
        HOST = 'localhost'
        USER = 'postgres'
        PASSWORD = 'QaB94cE#'
        DATABASE = 'sales_data'
        PORT = 5432
        engine_for_uploading = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}", future=True)

        with engine_for_uploading.begin() as connection_to_sales_data:
            cleaned_dataframe.to_sql(table_name, con=connection_to_sales_data, if_exists='replace')