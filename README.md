# Multinational Retail Data Centralisation

# Table of Contents
1. [Introduction](#1introduction)

2. [Technologies, Modules and Libraries](#2-technologies-modules-and-libraries)

    2.1 [Tecnologies](#21technologies)

    2.2 [Programming Language](#22programming-language)

    2.3 [Python Modules and Libraries](#23python-modules-and-libraries)
    
    2.4 [Database Documentation](#24database-documentation)

3. [Architecture and Database Design](#3-architecture-and-database-design)

    3.1 [Architechture Design](#31-architechture-design)

    3.2 [Database Design](#32-database-design)

4. [File Structure](#4-file-structure)

## 1. Introduction

This is my third project with AiCore, and I adored every part of it. Throughout this experience, I have honed my expertise in various areas, including `pandas`, data cleaning, AWS, APIs, SQL, and `SQLAlchemy`. Additionally, the project expanded my knowledge by introducing me to the Python module called `tabula`.

In this project: I extracted data from various sources, cleaned the data using pandas, and finally uploaded the cleaned data to a local PostgreSQL database. After the database was created, I altered tables so that the data types of each column were correct. Then in the `dim_products` table, I added a new column which catagorised the weights, and I also altered a column in this table to make it easier to understand. Then, I added the primary and foreign keys. Finally, I wrote queries which had 2 uses: to reinforce my SQL knowledge, and to check if I had cleaned the data correctly.

For more details on everything, including set up, please consult the [GitHub Wiki](https://github.com/kimiko-dev/Multinational-Retail-Data-Centralisation/wiki)

## 2. Technologies, Modules and Libraries

This project employs a combination of technologies, programming languages, and Python modules and libraries to achieve its goals. Here is a list of the what I used:

### 2.1 Technologies:

__AWS__: Used for cloud-based services and storage.

__PostgreSQL__: The chosen relational database management system.

__APIs__: Utilised for data retrieval and integration.

### 2.2 Programming Language:

__Python__

### 2.3 Python Modules and Libraries:

__`requests`__: Used for making HTTP requests and interacting with external APIs.

__`validators`__: Provides utilities for validating various data types, URLs, and email addresses.

__`pandas`__: A powerful data manipulation and analysis library, facilitating structured data handling.

__`sqlalchemy`__: A toolkit for SQL interaction and an Object-Relational Mapping (ORM) library for database operations.

__`tabula`__: Enables data extraction from PDF documents.

__`boto3`__: The AWS SDK for Python, used for AWS service integration.

__`yaml`__: A library for working with YAML files.

__`re`__: Python's regular expression library for pattern matching and data extraction.

### 2.4 Diagram Creation

__dbdocs__: Used for generating and documenting the database schema and structure.

## 3. Architecture and Database Design

### 3.1 Architechture Design

I succesfully implemented a fully functional ETL pipeline. The main structure can be seen in the diagram below. For more details on what happened at each stage, please consult the [GitHub Wiki](https://github.com/kimiko-dev/Multinational-Retail-Data-Centralisation/wiki/Architecture). 

![Diagrams/Pipeline_Architecture.png](https://github.com/kimiko-dev/Multinational-Retail-Data-Centralisation/blob/master/Diagrams/Pipeline_Architecture.png?raw=true)

### 3.2 Database Design

The __postgres__ database follows a star schema, as seen below in the diagram:

![Sales_Data_Database_Diagram.png](https://github.com/kimiko-dev/Multinational-Retail-Data-Centralisation/blob/master/Diagrams/Sales_Data_Database_Diagram.png?raw=true)

This star schema was defined using __primary keys__, which can be seen in the [`database_schema.sql`](https://github.com/kimiko-dev/Multinational-Retail-Data-Centralisation/blob/master/SQL%20Scripts/database_schema.sql) script.

For details about the data used, please consult the [GitHub Wiki](https://github.com/kimiko-dev/Multinational-Retail-Data-Centralisation/wiki/sales_data)

## 4. File Structure

```
├── Diagrams
│   ├── Pipeline_Architecture.png
│   └── Sales_Data_Database_Diagram.png
├── ETL Scripts
│   ├── data_cleaning.py # Transforms the data
│   ├── data_extractor.py # Extracts the data
│   ├── database_utils.py # Used to connect to databases, read files and uploads tables
│   └── upload_to_database.py # Loads the data into the postgres database
├── SQL Scripts
│   ├── database_schema.sql # Used to create the star schema
│   └── querying_the_data.sql # Holds all the queries. 
├── README.md
```
