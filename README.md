# multinational-retail-data-centralisation

# Table of Contents
1. [Introduction](#introduction)
1. [Technologies, Modules and Libraries](#technologies-utilised-and-python-moduleslibraries)
    - [Tecnologies](#technologies)
    - [Programming Language](#programming-language)
    - [Python Modules and Libraries](#python-modules-and-libraries)
    - [Database Documentation](#database-documentation)
1. [Modules for Extraction, Cleaning and Uploading](#modules-for-extraction-cleaning-and-uploading)
    - [database_utils.py](#database_utilspy)
        - [DatabaseConnector Methods](#databaseconnector-methods)
    - [data_extractor.py](#data_extractorpy)
        - [DataExtractor Methods](#dataextractor-methods)
    - [data_cleaning.py](#data_cleaningpy)
        - [DataCleaning Methods](#datacleaning-methods)
1. [SQL Files](#sql-files)
    - [database_schema.sql](#database_schemasql)
    - [querying_the_data.sql](#querying_the_datasql)
1. [Database Diagram](#database-diagram)

## Introduction

This is my third project with The AiCore, and I adored every part of it. Throughout this experience, I have honed my expertise in various areas, including `pandas`, data cleaning, AWS, APIs, SQL, and `SQLAlchemy`. Additionally, the project expanded my knowledge by introducing me to the Python module called `tabula`.

Driven by a desire to exceed expectations, I've equipped myself with indispensable tools like dbdocs and Python modules such as `re` and `validators`. All of which have enhanced my project.

In this project: I extracted data from various sources, cleaned the data using pandas, and finally uploaded the cleaned data to a local PostgreSQL database. After the database was created, I altered tables so that the data types of each column were correct. Then in the `dim_products` table, I added a new column which catagorised the weights, and I also altered a column in this table to make it easier to understand. Then, I added the primary and foreign keys. Finally, I wrote queries which had 2 uses: to reinforce my SQL knowledge, and to check if I had cleaned the data correctly.

## Technologies Utilised and Python Modules/Libraries
This project employs a combination of technologies, programming languages, and Python modules and libraries to achieve its goals. Here is a list of the what I used:
### Technologies:

__AWS__: Used for cloud-based services and storage.

__PostgreSQL__: The chosen relational database management system.

__APIs__: Utilised for data retrieval and integration.

### Programming Language:

__Python__

### Python Modules and Libraries:

__`requests`__: Used for making HTTP requests and interacting with external APIs.

__`validators`__: Provides utilities for validating various data types, URLs, and email addresses.

__`pandas`__: A powerful data manipulation and analysis library, facilitating structured data handling.

__`sqlalchemy`__: A toolkit for SQL interaction and an Object-Relational Mapping (ORM) library for database operations.

__`tabula`__: Enables data extraction from PDF documents.

__`boto3`__: The AWS SDK for Python, used for AWS service integration.

__`yaml`__: A library for working with YAML files.

__`re`__: Python's regular expression library for pattern matching and data extraction.

### Database Documentation

__`dbdocs`__: Used for generating and documenting the database schema and structure.

## Getting Started

First of all, please download `database_utils.py`, `data_extractor.py`, `data_cleaning.py` and `database_schema`.

It is important that you have the following python packages installed in your current environment: `yaml`, `SQLAlchemy`, `requests`, `validators`, `pandas`, `tabula`, `boto3` and `re`.

Also, please make sure you have a credentials file, which should be a YAML file.

Now, go into the `database_utils.py` file and change the credentials in the method `upload_to_db` to the database you wish to upload the files into. Here is what I am talking about:

![Alt text](image.png)

In a seperate file, please use the following to upload the tables to the database, like this: 

```
import data_cleaning 
import database_utils


dc = data_cleaning.DataCleaning()
du = database_utils.DatabaseConnector(<credentials YAML file>)

df = dc.<cleaning function here>()

du.upload_to_db(df, <table name>)
```

Where you replace `<credentials YAML file>`, `<cleaning function here>`, and `<table name>`. 

When you have used the correct methods to clean the data and uploaded it to your database, you may run the `database_schema.sql` file to apply the correct schema to the database. 

You will now be able to successfully query the data in your database.

## Modules for Extraction, Cleaning and Uploading

I created three modules which streamlines the process for extracting data from various sources, cleaning the data and uploading the data to a local database. 

### database_utils.py

Here, we introduce the `DatabaseConnector` class. The main purpose of this class is introduce 3 methods that reads credentials, initialises an engine to connect to an RDS database, and to upload cleaned data to a local PostgreSQL database. We will discuss each method below.

#### `DatabaseConnector` Methods

1. `read_db_creds`: Here, we verify the credentials to check if they are in the correct format, correct file type and if the filepath is correct. We then extract the credential from this file and place them into a dictionary.

1. `init_db_engine`: We use the dictionary of credentials from `read_db_creds` to initialise an engine that will be used to connect to the RDS database.

1. `upload_cleaned_data(cleaned_dataframe, table_name)`: We supply this method with the cleaned dataframe and the desired table name. It connnects to a local PostgreSQL server and uploads the table to the correct database.

### data_extractor.py

We introduce the `DataExtractor` class, which introduces methods that serve to extract data that needs to be cleaned from various sources. We initialise this class with an engine using `init_db_engine` from the `DatabaseConnector` class as we will using this to connect to the RDS database. We also initialise it with the headers used to connect to the API we will extract data from.

#### `DataExtractor` Methods

1. `list_db_tables`: This method employs the SQLAlchemy inspector to inspect the RDS database (using the engine from before). It then retrieves the database table names,

1. `read_rds_table(table)`: This method is used to fetch the data from the RDS database table. We use the `read_sql_table` from the `pandas` module, which takes in the `table` name and the connection to the `engine` from the `DatabaseConnector`. It returns a `dataframe` which is used in cleaning.

1. `retrieve_pdf_data(link)`: This method retrieves tabular data from a URL we have provided as an argument. We validate the URL, if it is valid, a `dataframe` is returned with the correct data. If the URL is not valid, an error is thrown and `None` is returned.

1. `list_number_of_stores`: This method simply sends a GET request to the API to obtain the number of stores. The request is returned as a dictionary, so we return the value from the key `number_stores`, which is an integer.

1. `retrieve_stores_data`: This method uses the `list_number_of_stores` method from before as we need to iterate through each store number and perform a GET request. We then insert each of the stores data into a `dataframe` which is returned after we have obtained all the stores information.

1. `extract_from_s3(link)`: This method uses the `boto3` module to initialise an S3 client. By breaking up the link into each necessary part, we use the parts in `download_file` to download the file we need. Then we find the file type and insert the data into a dataframe according to the file type. `.csv` and `.json` are supported

### data_cleaning.py

We introduce the `DataCleaning` class, which introduces methods to clean the data we have extracted from the various sources. We initilaise the `DataExtractor` class from before since we will be using this a lot.

#### `DataCleaning` Methods

1. `clean_user_data`, `clean_card_data`, `clean_store_data`, `clean_products_data`, `clean_orders_data`, `clean_date_time_data`: I have clumped all these together since they all serve the same purpose. That is to clean the extracted data for corrupted data and erronous inputs. For the specific documentation for each method, please consult the docstrings in the `data_cleaning.py` file.

1. `convert_product_weights(product_data)`: This method takes in the `product_data` `dataframe` and converts all values in the `weight` column to kilograms. Some cleaning is done to remove the corrupted data. A `dataframe` is returned with the correct format for the `weights`.

## SQL Files

These were made in accordance to the tasks set. I will discuss below what each file is used for.

### database_schema.sql

Here, we are adjusting the data types in each table to the correct type. This is crucial to do as we need the correct data types when performing queries. For example, using aggregation functions.

We then added a new column to the `dim_products` table called `weight_class`. This is used to classify each weight into respective catagories. For example:
- If "weight" is less than 2kg, it's categorised as 'Light.'
- If "weight" is between 2kg (inclusive) and 40kg (exclusive), it's categorised as 'Mid_Sized.'
- If "weight" is between 40kg (inclusive) and 140kg (exclusive), it's categorised as 'Heavy.'
- If "weight" is 140kg or greater, it's categorised as 'Truck_Required.'

Next in the `dim_products` table, we renamed the `removed` column to `still_available`. We then updated the values in the `still_available` column to boolean values. If the product is assigned `Still_available` we change it to `True`. And if the product is assigned `Removed`, we change it to `False`.

In the appropriate tables, we assigned primary keys to columns that appear in the `orders_table`. Conversely, we assigned foreign keys to columns in the `orders_table` which correspond to the primary keys. 

### querying_the_data.sql

This is a SQL file that contains the queries we were asked to perform. 

- __Task 1__: How many stores does the business have and in which countries?

- __Task 2__: Which locations currently have the most stores?

- __Task 3__: Which months produce the average highest cost of sales typically?

- __Task 4__: How many sales are coming from online?

- __Task 5__: What percentage of sales come through each type of store?

- __Task 6__: Which month in each year produced the highest cost of sales?

- __Task 7__: What is our staff headcount?

- __Task 8__: Which German store type is selling the most?

- __Task 9__: How quickly is the company making sales?

## Database Diagram

I created a database diagram, which is located at `sales_data.png`. We can use this to easily see the relations with our database. It shows the primary keys as well as how the are related to the main table, `orders_table`. This makes it easier to navigate the tables when querying the data.