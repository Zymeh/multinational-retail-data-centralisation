import yaml
from sqlalchemy import create_engine

class DatabaseConnector:
    ''' This class is used to connect and upload to the various databases we are using.

        Methods:
            read_db_creds (): This method is used to read the database credentials used to access the databases.
            init_db_engine (): This method is used to create an engine that connects to the various databases.
            upload_to_db (): This method is used to upload the cleaned data to the database.

    '''

    def __init__(self, file_path):
        ''' This initialises the instance of the class based on the credentials supplied.

        Args:
            file_path (`str`): This is the filepath for the credentials.
        '''
        self.file = file_path

    class NotYAMLFileError(Exception):
        "definining a custom exception for when the file isnt a YAML file."
        pass

    def read_db_creds(self):
        ''' This method is used to read the credentials from the YAML file.

        Here, we first check if the filepath is correct. If it is, the file is read and loaded. If not, an error is thrown accordingly.
        
            Raises:
                NotYAMLFileError: If the file is not in YAML format.
                FileNotFoundError: If the specified file cannot be found.
                TypeError: If the `file` argument is not a string.
                ValueError: If there is an issue with loading the YAML file.
                yaml.YAMLError: If there is a YAML syntax error in the file.
                AttributeError: If there is an issue with the data type.

        Returns:
            cred_dict (`dict`): This is a dictionary which contains the credentials to be used to connect to the RDS database.

        '''

        try:
            if not self.file.endswith('.yaml') and not self.file.endswith('.yml'):
                raise self.NotYAMLFileError("File is not a YAML file.")

            with open(self.file, 'r') as file:
                cred_dict = yaml.load(file, Loader=yaml.FullLoader)
            return cred_dict

        except (FileNotFoundError, TypeError, self.NotYAMLFileError, ValueError, yaml.YAMLError, AttributeError) as e:
            print(f'Error: {e}, please check your file path, format, and content.')

    def init_db_engine(self):
        ''' This method is used to connect to the RDS database.

        Firstly, we use the method `read_db_creds` to get a dictionary of credentials.
        Then, we assign the values for each key to a variable. These variables are 
        then used when we create the engine.

        Returns:
            engine_for_exraction: This is an engine which is used when extracting data.
        
        '''

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
        '''This method is used to upload the cleaned dataframe to a database.

        Args:
            cleaned_dataframe (`dataframe`): This is the clean dataframe we 
            want to upload.
            table_name (`str`): This is what we would like to call the table 
            once uploaded to the database.

        Here, we simply connect to the database by supplying `create_engine` 
        with the correct credentials. We then use this engine to create a 
        connection so that we can upload the cleaned dataframes to.
        
        '''
        
        DATABASE_TYPE = 'postgresql'
        DBAPI = 'psycopg2'
        HOST = 'localhost'
        USER = 'postgres'
        PASSWORD = ''
        DATABASE = 'sales_data'
        PORT = 5432
        engine_for_uploading = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}", future=True)

        with engine_for_uploading.begin() as connection_to_sales_data:
            cleaned_dataframe.to_sql(table_name, con=connection_to_sales_data, if_exists='replace')