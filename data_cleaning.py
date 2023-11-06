import data_extractor
import pandas as pd
import re
class DataCleaning:
    ''' This class used to clean the data we have extracted from various sources.

        Methods:
            clean_user_data (): This method is used to clean the user data.
            clean_card_data (): This method is used to clean card details.
            clean_store_data (): This method is used to cleam the store data.
            convert_product_weights(`dataframe`): This method is used to convert the products weights into kilograms.
            clean_products_data (): This method is used to clean the products data.
            clean_date_time_data (): This method is used to clean the date time data.
    
    '''

    def __init__(self):
        ''' This initialises the instance of the class.

        Inside, we are calling the `DataExtractor` class from the `data_extractor` module and assigning it `self` for later use in the class.
        
        '''
        self.de = data_extractor.DataExtractor()

    def clean_user_data(self):
        '''This is a method to clean the user data.

        Here, we are using the `read_rds_table` method from the `data_extractor` module to extract the table `legacy` users from the RDS database. We then set up a condition to drop all the rows where there are `'NULL'` values. For this, I simply dropped the rows where `'NULL'` was in the `first_name` as these rows contained `'NULL'` values in all columns. Then, we made a list called `strange_entries`. We obtained these by looking up unique values in the `country` column as there are only 3 countries. These are rows that contain corrupted data. We then dropped the rows which contained these values and the `'NULL'` values. Next, in the address column, we replaced the `\n` with `, ` just to make it easier to read. After this, in the `country_code` column, we then replaced `'GGB'` with `'GB'` as this was an input error. In the `phone_number` column, we got rid of the `.` and `-` as these do not really matter.  Finally, we formatted the `birth_date` and `join_date` columns to display the dates correctly.  

        Returns:
            user_data (`dataframe`): This is the cleaned dataframe.

        '''

        user_data = self.de.read_rds_table('legacy_users')

        user_data = user_data.set_index('index')

        strange_entries = ['I7G4DMDZOZ', 'AJ1ENKS3QL', 'XGI7FM0VBJ', 'S0E37H52ON', 'XN9NGL5C0B', '50KUU3PQUF', 'EWE3U0DZIV', 'GMRBOMI0O1', 'YOTSVPRBQ7', '5EFAFD0JLI', 'PNRMPSYR1J', 'RQRB7RMTAD', '3518UD5CE8', '7ZNO5EBALT', 'T4WBZSW0XI']
        condition_1 = user_data['country'].isin(strange_entries)
        condition_2 = user_data['first_name'] == "NULL"
        user_data = user_data.drop(user_data[condition_1 | condition_2].index) 

        user_data['address'] = user_data['address'].str.replace('\n', ', ')

        user_data['country_code'] = user_data['country_code'].str.replace('GGB', 'GB')

        user_data['phone_number'] = user_data['phone_number'].str.replace('-', ' ') 
        user_data['phone_number'] = user_data['phone_number'].str.replace('.', ' ')


        user_data['date_of_birth'] = pd.to_datetime(user_data['date_of_birth'], format='mixed')
        user_data['join_date'] = pd.to_datetime(user_data['join_date'], format='mixed')

        return user_data

    def clean_card_data(self):
        '''This method is used to clean the card data.

        Here, we are using the method `retrieve_pdf_data` from the `data_extractor` module, where the argument is a link to the pdf we are extracting data from. Next, we make a list called `strange_entries`, where we store all the corrupted data from the `card_provider` column We get this list again by using the fact there is only a small amount of entries in this column. We then find the `'NULL'` values in the `card_number` column. We then use both of these to drop all the rows with the corrupted data as they are consistent across all columns. After this, we remove all `?` from all the rows which include them in the `card_number` column. Next, we format the dates in the`expiry_date` and `date_payment_confirmed` columns.

        Returns:
            store_data (`dataframe`): This is the cleaned dataframe.
        
        '''

        card_data = self.de.retrieve_pdf_data('https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf')

        card_data.reset_index(drop=True)

        strange_entries = ['NB71VBAHJE','WJVMUO4QX6', 'JRPRLPIBZ2', 'TS8A81WFXV', 'JCQMU8FN85', '5CJH7ABGDR', 'DE488ORDXY', 'OGJTXI6X1H', '1M38DYQTZV', 'DLWF2HANZF', 'XGZBYBYGUW', 'UA07L7EILH', 'BU9U947ZGV', '5MFWFBZRM9']
        condition_1 = card_data['card_provider'].isin(strange_entries)
        condition_2 = card_data['card_number'] == 'NULL'
        card_data = card_data.drop(card_data[condition_1 | condition_2].index)

        card_data['card_number'] = card_data['card_number'].astype('string')
        card_data['card_number'] = card_data['card_number'].str.replace('?', '')
        card_data['card_number'] = card_data['card_number'].str.replace('???', '')
        card_data['card_number'] = card_data['card_number'].str.replace('????', '')

        card_data['expiry_date'] = pd.to_datetime(card_data['expiry_date'], format='%m/%y').dt.strftime('%y-%m')

        card_data['date_payment_confirmed'] = pd.to_datetime(card_data['date_payment_confirmed'], format='mixed')

        return card_data

    def clean_store_data(self):
        ''' This method is used to clean store data.

        Firstly, we used the method `retrieve_stores_data` from the module `data_extractor` to obtain the data to be cleaned. Next, we then find the `'NULL'` values in the `opening_date` column. Then, we make a list called `strange_entries`, where we store all the corrupted data from the `country_code` column We get this list by using the fact there is only a small amount of entries in this column. We then use both of these to drop all the rows with the corrupted data as they are consistent across all columns. Now, in the address column, we replaced the `\n` with `, ` just to make it easier to read. We then dropped the `lat` column as all the data here was `'NULL'`. After this, in the `staff_numbers` column, we removed all the alphabetical charecters from the numbers where neccessary. Next, we formatted the dates in the `opening_date` column correctly, Finally, we replaced all `N/A` entries with `NaN`, just so it is easier to work with.

        Returns:
            store_data (`dataframe`): This is the cleaned dataframe.
        
        '''

        store_data = self.de.retrieve_stores_data()

        strange_entries = ['YELVM536YT','FP8DLXQVGH','HMHIFNLOBN','F3AO8V2LHU','OH20I92LX3','OYVW925ZL8','B3EH2ZGQAV']
        condition_1 = store_data['country_code'].isin(strange_entries)
        condition_2 = store_data['opening_date'] == 'NULL'
        store_data = store_data.drop(store_data[condition_1 | condition_2].index)

        store_data = store_data.drop('lat', axis=1)

        store_data['address'] = store_data['address'].str.replace('\n', ', ')

        store_data['staff_numbers'] = store_data['staff_numbers'].str.replace(r'\D', '', regex=True)

        store_data['opening_date'] = pd.to_datetime(store_data['opening_date'], format='mixed', errors='ignore')

        store_data['continent'] = store_data['continent'].str.replace('ee', '')

        store_data.replace('N/A', pd.NA, inplace=True)

        store_data = store_data.reset_index(drop=True)

        return store_data
    
    def convert_product_weights(self, product_data):
        ''' This method converts the products weights into kilograms.

        Firstly, we make a list called `strange_entries`, where we store all the corrupted data from the `category` column. We get this list by using the fact there is only a small amount of entries in this column. Then, we removed all the rows with `'NULL'` values in. To find these rows, we simply found the `'NULL'` values in the `weight` column and dropped these rows as they contain `'NULL'` values in every column. We then use this to drop all the rows with the corrupted data as they are consistent across all columns. Finally, we iterate through all the data in the `weight` column and convert them into the correct units, that being kilograms.

        Args: 
            product_data (`dataframe`): the dataframe we want to convert weights for.

        Returns:
            product_data (`dataframe`): This is a dataframe where the product weights are adjusted. Some cleaning has been done too.
        
        '''

        strange_entries = ['S1YB74MLMJ', 'C3NCA2CL35', 'WVPMHZP59U']
        condition_1 = product_data['category'].isin(strange_entries)
        condition_2 = pd.isna(product_data['weight'])
        product_data = product_data.drop(product_data[condition_1 | condition_2].index)

        for _ in product_data['weight']:

            weight_to_convert = str(_)

            if 'x' in weight_to_convert:
                stripped_weight = re.findall(r'\d+', weight_to_convert)
                adjusted_weight = (float(stripped_weight[0]) * float(stripped_weight[1])) / 1000

            elif 'kg' in weight_to_convert:
                adjusted_weight = weight_to_convert.replace('kg', '')

            else:
               stripped_weight = re.findall(r'\d+', weight_to_convert)
               adjusted_weight = int(stripped_weight[-1]) / 1000

            product_data['weight'] = product_data['weight'].replace(_ , adjusted_weight) 

        return product_data   

    def clean_products_data(self):
        ''' This method cleans the product data. 

        Firstly, we are using the method `extract_from_s3` from the `data_extractor` module to get the data we need to clean. Now, we then drop the column `Unnamed: 0` as we don't need it. We then pass the dataframe we have extracted to the `convert_product_weights` method as we want to convert the weights into kilograms. Next, we converted all the data in the `date_added` column to datetime. After this, we corrected a typographical error in the `removed` column. Then, in the `product_price` column, we dropped the `£` from all values.

        Returns:
            product_data (`dataframe`): This is the cleaned dataframe.
       
        '''

        product_data = self.de.extract_from_s3('s3://data-handling-public/products.csv')

        product_data = product_data.drop('Unnamed: 0', axis=1 )

        product_data = self.convert_product_weights(product_data)

        product_data['removed'] = product_data['removed'].replace('Still_avaliable', 'Still_available')

        product_data['product_price'] = product_data['product_price'].str.replace('£', '').astype('string')

        product_data['date_added'] = pd.to_datetime(product_data['date_added'], format='mixed')

        return product_data

    def clean_orders_data(self):
        ''' This method is used to clean the orders data.

        Firstly, we extract the `orders_table` using the `read_rds_table` method from the moudule `data_extractor`. After this, we simply drop the columns `level_0`, `first_name`, `last_name` and `1` as these are not needed. 

        Returns:
            orders_data (`dataframe`): This is the cleaned dataframe.
        
        '''

        orders_data = self.de.read_rds_table('orders_table')

        orders_data = orders_data.drop('level_0', axis=1)
        orders_data = orders_data.drop('first_name', axis=1)
        orders_data = orders_data.drop('last_name', axis=1)
        orders_data = orders_data.drop('1', axis=1)

        return orders_data
    
    def clean_date_time_data(self):
        ''' This method is used to clean the data time data.

        Firstly, we supplied a url to the method `extract_from_s3` from the `data_extractor` module to obtain the data we need to clean. Then, we make a list called `strange_entries`, where we store all the corrupted data from the `month` column. We get this list by using the fact there is only a small amount of entries in this column. Next, we then find the `'NULL'` values in the `month` column and then dropped the corresponding rows, again as they are consistent across all rows. We then use both of these conditions to drop the rows with the corrupted data.

        Returns:
            date_time_data (`dataframe`): This is the cleaned dataframe.

        '''

        url = 'https://data-handling-public.s3.eu-west-1.amazonaws.com/date_details.json'

        date_time_data = self.de.extract_from_s3(url)
        
        strange_entries = ['1YMRDJNU2T', '9GN4VIO5A8', 'NF46JOZMTA', 'LZLLPZ0ZUA', 'YULO5U0ZAM', 'SAT4V9O2DL', '3ZZ5UCZR5D', 'DGQAH7M1HQ', '4FHLELF101', '22JSMNGJCU', 'EB8VJHYZLE', '2VZEREEIKB', 'K9ZN06ZS1X', '9P3C0WBWTU', 'W6FT760O2B', 'DOIR43VTCM', 'FA8KD82QH3', '03T414PVFI', 'FNPZFYI489', '67RMH5U2R6', 'J9VQLERJQO', 'ZRH2YT3FR8', 'GYSATSCN88']
        condition_1 = date_time_data['month'].isin(strange_entries)
        condition_2 = date_time_data['month'] == 'NULL'
        date_time_data = date_time_data.drop(date_time_data[condition_1 | condition_2].index)

        return date_time_data