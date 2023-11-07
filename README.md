# multinational-retail-data-centralisation

# Table of Contents
1. [Introduction](#introduction)
1. [Technologies, Modules and Libraries](#technologies-utilised-and-python-moduleslibraries)
    - [Tecnologies](#technologies)
    - [Programming Language](#programming-language)
    - [Python Modules and Libraries](#python-modules-and-libraries)
    - [Database Documentation](#database-documentation)
1. [Modules for Extraction, Cleaning and Uploading](#modules-for-extraction-cleaning-and-uploading)
    - [database_utils](#database_utils)
        - [DatabaseConnector Class Methods](#databaseconnector-class-methods)
    - [data_extractor](#data_extractor)
    - [data_cleaning](#data_cleaning)
    - [sales_data.png](#sales_datapng)

## Introduction

## Technologies Utilised and Python Modules/Libraries
This project employs a combination of technologies, programming languages, and Python modules and libraries to achieve its goals. Here is a list of the what I used:
### Technologies:

__AWS__: Used for cloud-based services and storage.

__PostgreSQL__: The chosen relational database management system.

__APIs__: Utilized for data retrieval and integration.

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

## Modules for Extraction, Cleaning and Uploading

I made 3 modules which streamlines the process for extracting data from various sources, cleaning the data and uploading the data to a database. 

### database_utils

Here, we introduce the `DatabaseConnector` class. The main purpose of this class is introduce 3 methods that reads credentials, initialises an engine to connect to an RDS database, and to upload cleaned data to a local PostgreSQL database. We will discuss each method below.

#### `DatabaseConnector` Class Methods

1. `read_db_creds`: Here, we verify the credentials to check if they are in the correct format, correct file type and if the filepath is correct. We then extract the credential from this file and place them into a dictionary.

1. `init_db_engine`: We use the dictionary of credentials from `read_db_creds` to initialise an engine that will be used to connect to the RDS database.

1. `upload_cleaned_data(cleaned_dataframe, table_name)`: We supply this method with the cleaned dataframe and the desired table name. It connnects to a local PostgreSQL server and uploads the table to the correct database.

### data_extractor

We introduce the `DataExtractor` class, which introduces methods that serve to extract data that needs to be cleaned from various sources. We initialise this class with an engine using `init_db_engine` from the `DatabaseConnector` class as we will using this to connect to the RDS database. We also initialise it with the headers used to connect to the API we will extract data from.

#### `DataExtractor` Class Methods

1. `list_db_tables`: This method employs the SQLAlchemy inspector to inspect the RDS database (using the engine from before). It then retrieves the database table names,

1. `read_rds_table(table)`: This method is used to fetch the data from the RDS database table 

1. `retrieve_pdf_data`:

1. `list_number_of_stores`:

1. `retrieve_stores_data`:

1. `extract_from_s3`:

### data_cleaning

### sales_data.png