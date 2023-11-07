-- task 1 

SELECT country_code,
       COUNT(country_code) AS total_no_stores
FROM
    dim_store_details
WHERE store_code NOT LIKE 'WEB%'
GROUP BY 
    country_code
ORDER BY total_no_stores DESC;

-- task 2

SELECT locality,
       COUNT(locality) AS total_no_stores
FROM 
    dim_store_details
WHERE country_code = 'GB'
GROUP BY locality
ORDER BY total_no_stores DESC;

-- task 3

SELECT ROUND(CAST(SUM( dim_products.product_price * orders_table.product_quantity) AS NUMERIC), 2 ) AS total_sales,       
       dim_date_times.month AS month
FROM 
    dim_products
INNER JOIN 
    orders_table ON orders_table.product_code = dim_products.product_code
INNER JOIN 
    dim_date_times ON dim_date_times.date_uuid = orders_table.date_uuid
GROUP BY month
ORDER BY total_sales DESC;

-- task 4

SELECT SUM(orders_table.product_quantity) AS product_quantity_count, 
       COUNT(orders_table.date_uuid) AS number_of_sales,
       CASE
           WHEN dim_store_details.store_code LIKE 'WEB%' THEN 'Online'
           ELSE 'Offline'
        END AS location
       
FROM dim_store_details
INNER JOIN
    orders_table ON orders_table.store_code = dim_store_details.store_code
GROUP BY location;

-- task 5

WITH TotalSales AS (
    SELECT COUNT(date_uuid) AS total_num_sales
    FROM orders_table
)
SELECT dim_store_details.store_type,
       ROUND(CAST(SUM(dim_products.product_price * orders_table.product_quantity) AS NUMERIC), 2) AS total_sales,
       ROUND((CAST(COUNT(orders_table.date_uuid) AS NUMERIC) * 100 ) / (
        SELECT total_num_sales
        FROM TotalSales
       ), 2)  AS percentage_total
FROM orders_table
INNER JOIN
    dim_store_details ON orders_table.store_code = dim_store_details.store_code
INNER JOIN
    dim_products ON orders_table.product_code = dim_products.product_code
GROUP BY dim_store_details.store_type
ORDER BY total_sales DESC;

-- task 6

SELECT ROUND(CAST(SUM(orders_table.product_quantity * dim_products.product_price) AS NUMERIC), 2) AS total_sales,
       dim_date_times.year AS year,
       dim_date_times.month AS month
FROM dim_date_times
INNER JOIN
    orders_table ON orders_table.date_uuid = dim_date_times.date_uuid
INNER JOIN
    dim_products ON dim_products.product_code = orders_table.product_code
GROUP BY year, month
ORDER BY total_sales DESC

-- task 7

SELECT SUM(staff_numbers) AS total_staff_numbers,
    country_code
FROM dim_store_details
GROUP BY country_code
ORDER BY total_staff_numbers DESC

-- task 8

SELECT ROUND(CAST(SUM(orders_table.product_quantity * dim_products.product_price) AS NUMERIC), 2),
       store_type,
       country_code
FROM dim_store_details
INNER JOIN
    orders_table ON orders_table.store_code = dim_store_details.store_code
INNER JOIN
    dim_products ON orders_table.product_code = dim_products.product_code
WHERE country_code = 'DE'
GROUP BY store_type, country_code;

-- task 9

WITH cte_time_difference AS (
  SELECT
    formatted_date_time - LAG(formatted_date_time, 1, (day || '-' || month || '-' || year || ' ' || '00:00:00')::TIMESTAMP) OVER (PARTITION BY year ORDER BY formatted_date_time) AS time_diff,
    year
  FROM
    (
        SELECT (day || '-' || month || '-' || year || ' ' || timestamp)::TIMESTAMP AS formatted_date_time,
               day,
               month,
               year
        FROM 
        dim_date_times
    )
)
SELECT year,
       AVG(time_diff) AS actual_time_taken
FROM cte_time_difference
GROUP BY year
ORDER BY actual_time_taken DESC;