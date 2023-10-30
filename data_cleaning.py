#%%
import database_utils
import data_extractor
import pandas as pd
class DataCleaning:

    def __init__(self):
        pass

    def clean_user_data(self):

        de = data_extractor.DataExtractor('db_creds.yaml')
        df = de.read_rds_table('legacy_users')

        condition = df['first_name'] == "NULL"
        df = df.drop(df[condition].index)
        df['first_name'] = df['first_name'].astype('string')

        df['address'] = df['address'].str.replace('\n', ', ')
        df['address'] = df['address'].astype('string')

        df['country_code'] = df['country_code'].str.replace('GGB', 'GB')
        df['country_code'] = df['country_code'].astype('string')

        df['phone_number'] = df['phone_number'].str.replace('-', ' ')
        df['phone_number'] = df['phone_number'].str.replace('.', ' ')
        df['phone_number'] = df['phone_number'].astype('string')

        strange_list = ['I7G4DMDZOZ', 'AJ1ENKS3QL', 'XGI7FM0VBJ', 'S0E37H52ON', 'XN9NGL5C0B', '50KUU3PQUF', 'EWE3U0DZIV', 'GMRBOMI0O1', 'YOTSVPRBQ7', '5EFAFD0JLI', 'PNRMPSYR1J', 'RQRB7RMTAD', '3518UD5CE8', '7ZNO5EBALT', 'T4WBZSW0XI']
        condition = df['country'].isin(strange_list)
        df = df.drop(df[condition].index)

        df['date_of_birth'] = pd.to_datetime(df['date_of_birth'], format='mixed')
        df['join_date'] = pd.to_datetime(df['join_date'], format='mixed')

        return df