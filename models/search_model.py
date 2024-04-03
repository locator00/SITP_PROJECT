import pandas as pd
import sqlite3

def get_count_type(conn):
    return pd.read_sql('''
        SELECT type_id, type_name as Тип, COUNT(product_id) AS Товары_типов
        FROM type
        LEFT JOIN product USING(type_id)
        GROUP BY type.type_id;
    ''', conn)

def get_count_manufacturer(conn):
    return pd.read_sql('''
        SELECT manufacturer_id, manufacturer_name as Производитель, COUNT(product_id) AS Товары_производителя
        FROM manufacturer
        LEFT JOIN product USING(manufacturer_id)
        GROUP BY manufacturer.manufacturer_id;
    ''', conn)

def get_count_country(conn):
    return pd.read_sql('''
        SELECT country_id, country_name as Страна, COUNT(product_id) AS Товары_страны
        FROM country
        LEFT JOIN product USING(country_id)
        GROUP BY country.country_id;
    ''', conn)

def get_product(conn):
    return pd.read_sql('''
        SELECT product_name AS Название, type_name AS Тип_продукта, 
            manufacturer_name AS Производитель, country_name AS Страна_Производитель, 
            price AS Цена, storage_quantity AS Количество, product_id AS ID_продукта
        FROM product
            JOIN type USING(type_id)
            JOIN manufacturer USING(manufacturer_id)
            JOIN country USING(country_id)
        GROUP BY product_id;
    ''', conn)

def get_filter_product(conn, type, manufacturer, country):
    if type == []:
        type = [1, 2, 3]
   
    if manufacturer == []:
        manufacturer = [1, 2, 3]
   
    if country == []:
        country = [1, 2, 3]

    query = '''
        SELECT product_name AS Название, type_name AS Тип_продукта, 
            manufacturer_name AS Производитель, country_name AS Страна_Производитель, 
            price AS Цена, storage_quantity AS Количество, product_id AS ID_продукта
        FROM product p
            JOIN type USING(type_id)
            JOIN manufacturer USING(manufacturer_id)
            JOIN country USING(country_id)
        WHERE type_id IN ({})
          AND manufacturer_id IN ({})
          AND country_id IN ({})
        GROUP BY product_id;
    '''.format(','.join('?' * len(type)), ','.join('?' * len(manufacturer)), ','.join('?' * len(country)))

    params = tuple(type + manufacturer + country)
    return pd.read_sql(query, conn, params=params)