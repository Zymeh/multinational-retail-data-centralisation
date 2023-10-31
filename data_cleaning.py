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
