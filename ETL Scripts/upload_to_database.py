# %%
import data_cleaning 
import database_utils


dc = data_cleaning.DataCleaning()
du = database_utils.DatabaseConnector('db_cred.yaml')

df = dc.clean_date_time_data()
du.upload_to_db(df, 'dim_date_times')

df = dc.clean_card_data()
du.upload_to_db(df, 'dim_card_details')

df = dc.clean_store_data()
du.upload_to_db(df, 'dim_store_details')

df = dc.clean_orders_data()
du.upload_to_db(df, 'orders_table')

df = dc.clean_products_data()
du.upload_to_db(df, 'dim_products')

df = dc.clean_user_data()
du.upload_to_db(df, 'dim_users')

# %%
