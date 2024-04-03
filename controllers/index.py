from app import app
from flask import render_template, request, session

from utils import get_db_connection
from models.index_model import get_store, get_combo_box, set_delivery, get_new_store, new_order

@app.route('/', methods=['get'])
def index():
    conn = get_db_connection()

    #нажата кнопка Найти
    if request.values.get('store'):
        store_id = int(request.values.get('store'))
        session['store_id'] = store_id

    elif request.values.get('return'):
        order_id = int(request.values.get('return'))
        set_delivery(conn, order_id)

    # нажата кнопка Добавить со страницы Новый читатель
    elif request.values.get('new_store'):
        new_store = request.values.get('new_store')
        session['store_id'] = get_new_store(conn, new_store)

    # # нажата кнопка Добавить со страницы Поиск
    elif request.values.get('product'):
        product_quantity = int(request.values.get('product_num'))
        product_id = int(request.values.get('product'))
        new_order(conn, product_id, product_quantity, session['store_id'])

    # нажата кнопка Назад книгу со страницы Поиск
    elif request.values.get('noselect'):
        pass
    # вошли первый раз
    else:
        session['store_id'] = 1

    df_store = get_store(conn)
    df_combo_box = get_combo_box(conn, session['store_id'])

    html = render_template(
        'index.html',
        store_id=session['store_id'],
        store=df_store,
        combo_box=df_combo_box,
        len=len,
    )
    return html


if __name__ == '__main__':
    app.run(debug=True)
