import data_extractor
import pandas as pd
class DataCleaning:

    def __init__(self):
        self.de = data_extractor.DataExtractor()

    def clean_user_data(self):

        df = de.read_rds_table('legacy_users')

        df = df.set_index('index')

        condition = df['first_name'] == "NULL" #dropping nulls
        df = df.drop(df[condition].index)
        df['first_name'] = df['first_name'].astype('string')

        df['address'] = df['address'].str.replace('\n', ', ') #formatting addresses
        df['address'] = df['address'].astype('string')

        df['country_code'] = df['country_code'].str.replace('GGB', 'GB')
        df['country_code'] = df['country_code'].astype('string') #removing input errors

        df['phone_number'] = df['phone_number'].str.replace('-', ' ') #correctly formatting phone numbers
        df['phone_number'] = df['phone_number'].str.replace('.', ' ')
        df['phone_number'] = df['phone_number'].astype('string')

        strange_list = ['I7G4DMDZOZ', 'AJ1ENKS3QL', 'XGI7FM0VBJ', 'S0E37H52ON', 'XN9NGL5C0B', '50KUU3PQUF', 'EWE3U0DZIV', 'GMRBOMI0O1', 'YOTSVPRBQ7', '5EFAFD0JLI', 'PNRMPSYR1J', 'RQRB7RMTAD', '3518UD5CE8', '7ZNO5EBALT', 'T4WBZSW0XI'] # here we drop the wrongly filled rows
        condition = df['country'].isin(strange_list)
        df = df.drop(df[condition].index) 

        df['date_of_birth'] = pd.to_datetime(df['date_of_birth'], format='mixed')
        df['join_date'] = pd.to_datetime(df['join_date'], format='mixed')

        return df

    def clean_card_data(self):

        card_data = self.de.retrieve_pdf_data('https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf')

        card_data.reset_index(drop=True)

        strange_entries = ['NB71VBAHJE','WJVMUO4QX6', 'JRPRLPIBZ2', 'TS8A81WFXV', 'JCQMU8FN85', '5CJH7ABGDR', 'DE488ORDXY', 'OGJTXI6X1H', '1M38DYQTZV', 'DLWF2HANZF', 'XGZBYBYGUW', 'UA07L7EILH', 'BU9U947ZGV', '5MFWFBZRM9']
        condition = card_data['card_provider'].isin(strange_entries)
        card_data = card_data.drop(card_data[condition].index)

        card_data['card_provider'] = card_data['card_provider'].astype('string')

        condition = card_data['card_number'] == 'NULL'
        card_data = card_data.drop(card_data[condition].index)

        card_data['card_number'] = card_data['card_number'].astype('string')
        card_data['card_number'] = card_data['card_number'].str.replace('?', '')
        card_data['card_number'] = card_data['card_number'].str.replace('???', '')
        card_data['card_number'] = card_data['card_number'].str.replace('????', '')

        card_data['expiry_date'] = pd.to_datetime(card_data['expiry_date'], format='%m/%y').dt.strftime('%y-%m')

        card_data['date_payment_confirmed'] = pd.to_datetime(card_data['date_payment_confirmed'], format='mixed')

        return card_data

    def clean_store_data(self):

        store_data = self.de.retrieve_stores_data()

        condition = store_data['address'] == 'NULL'
        store_data = store_data.drop(store_data[condition].index)
        store_data['address'] = store_data['address'].str.replace('\n', ', ')
        store_data['address'] = store_data['address'].astype('string')

        strange_entries = ['YELVM536YT','FP8DLXQVGH','HMHIFNLOBN','F3AO8V2LHU','OH20I92LX3','OYVW925ZL8','B3EH2ZGQAV']
        condition = store_data['country_code'].isin(strange_entries)
        store_data = store_data.drop(store_data[condition].index)
        store_data['country_code'] = store_data['country_code'].astype('string')

        store_data['longitude'] = store_data['longitude'].astype('float32', errors='ignore')

        store_data = store_data.drop('lat', axis=1)

        store_data['locality'] = store_data['locality'].astype('string')

        store_data['store_code'] = store_data['store_code'].astype('string')

        store_data['staff_numbers'] = store_data['staff_numbers'].astype('int32', errors='ignore')

        store_data['opening_date'] = pd.to_datetime(store_data['opening_date'], format='mixed', errors='ignore')

        store_data['latitude'] = store_data['latitude'].astype('float32', errors='ignore')

        store_data['continent'] = store_data['continent'].str.replace('ee', '')
        store_data['continent'] = store_data['continent'].astype('string')

        store_data.replace('N/A', pd.NA, inplace=True)

        store_data = store_data.reset_index(drop=True)

        return store_data
    
    def clean_orders_data(self):

        orders_data = self.de.read_rds_table('orders_table')

        orders_data = orders_data.drop('level_0', axis=1)
        orders_data = orders_data.drop('first_name', axis=1)
        orders_data = orders_data.drop('last_name', axis=1)
        orders_data = orders_data.drop('1', axis=1)
        
        orders_data['card_number'] = orders_data['card_number'].astype('string')
        orders_data['store_code'] = orders_data['store_code'].astype('string')
        orders_data['product_code'] = orders_data['product_code'].astype('string')
        orders_data['user_uuid'] = orders_data['user_uuid'].astype('string')
        orders_data['date_uuid'] = orders_data['date_uuid'].astype('string')

        return orders_data