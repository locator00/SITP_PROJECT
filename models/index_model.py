import pandas


def get_store(conn):
    return pandas.read_sql('''SELECT * FROM store''', conn)


def get_combo_box(conn, store_id):
    return pandas.read_sql('''
        SELECT product_name AS Название, type_name AS Тип_продукта, order_id,
            quantity AS Количество, order_date AS дата_заказа,  delivery_date AS дата_доставки
        FROM order_
            JOIN store USING(store_id)
            JOIN product USING(product_id)
            JOIN type USING(type_id)
        WHERE store_id = :id            
            ORDER BY order_id
    ''', conn, params={"id": store_id})

def set_delivery(conn, order_id): 
    cur = conn.cursor() 
    cur.execute(''' 
        UPDATE order_
        SET delivery_date = DATE('now') 
        WHERE order_id = :order_id
    ''', {'order_id': order_id})
    conn.commit()

def get_new_store(conn, new_store):
    cur = conn.cursor()
    cur.execute(''' 
        INSERT INTO store (store_name) 
        VALUES (:new_store) 
    ''', {"new_store": new_store})
    conn.commit()
    return cur.lastrowid

def new_order(conn, product_id, product_quantity, store_id):
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO order_ (product_id, store_id, quantity, order_date, delivery_date)
        VALUES (:product_id, :store_id, :product_quantity, DATE('now'), NULL)
    ''', {"product_id": product_id, "product_quantity": product_quantity, "store_id": store_id})
    conn.commit()

    cur.execute(''' 
        UPDATE product
        SET storage_quantity = storage_quantity - :product_quantity
        WHERE product_id = :product_id
    ''', {'product_id': product_id, "product_quantity": product_quantity})
    conn.commit()
    return True