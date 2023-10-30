class DatabaseConnector:
    def __init__(self, file_path):
        self.file = file_path

    class NotYAMLFileError(Exception):
        "definining a custom exception for when the file isnt a YAML file."
        pass

    def read_db_creds(self):
        import os
        import yaml


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

    def init_db_engine(self):
        from sqlalchemy import create_engine

        credentials = read_db_creds()

        DATABASE_TYPE = 'postgresql'
        DBAPI = 'psycopg2'
        HOST = credentials["RDS_HOST"]
        USER = credentials["RDS_USER"]
        PASSWORD = credentials["RDS_PASSWORD"]
        DATABASE = credentials["RDS_DATABASE"]
        PORT = credentials["RDS_PORT"] 

        engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}", future=True)





