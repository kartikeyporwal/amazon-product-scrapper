# Amazon Web Scrapper

## Features  
- Opens `amazon.com`  
- Search a specified product  
- Extract  
    `Product Id / ASIN`  
    `Product Name`  
    `Price`  
    `Sponsored`  
    `Review Count`  
    `Average Ratings`  
- save csv and ingest mysql database  

## Consideration  
- Create a SQL table `create table amazon (asin varchar(255), product_name varchar(255), price varchar(255), sponsored varchar(255), review_count varchar(255), ratings varchar(255));`  
- table name `amazon` with columns `asin`, `product_name`, `price`, `sponsored`, `review_count`, `ratings` should be created  

## To run code  
1. Install necessary packages like selenium, beautifulsoup, pymysql, pandas, lxml
2. Download geckodriver binary and specify its path
3. Specify product to search in scrap_amazon.py
4. Run `python scrap_amazon.py`

## Result
- a csv file with product name will be created in the project directory.
- a mysql table amazon will be ingested with the retrieved data.
