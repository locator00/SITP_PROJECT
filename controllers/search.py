from app import app
from flask import render_template, request, session

from utils import get_db_connection
from models.search_model import get_count_type, get_count_manufacturer, get_count_country, get_product, get_filter_product


@app.route('/search', methods=['get', 'post'])
def search():
    conn = get_db_connection()
    df_type = get_count_type(conn)
    df_manufacturer = get_count_manufacturer(conn)
    df_country = get_count_country(conn)
    checked_list_type = []
    checked_list_manufacturer = []
    checked_list_country = []
    df_filter_product = get_product(conn)

    if request.values.get('types') or request.values.get('manufacturers') or request.values.get('countrys'):
        checked_list_type = request.form.getlist('types')
        checked_list_manufacturer = request.form.getlist('manufacturers')
        checked_list_country = request.form.getlist('countrys')
        df_filter_product = get_filter_product(
            conn,
            checked_list_type,
            checked_list_manufacturer,
            checked_list_country
        )

    if request.values.get('reset'):
        df_filter_product = get_product(conn)
        checked_list_type = []
        checked_list_manufacturer = []
        checked_list_country = []

    html = render_template(
        'search.html',
        type_box=df_type,
        manufacturer_box=df_manufacturer,
        country_box=df_country,
        filter_box=df_filter_product,
        checked_list_type=checked_list_type,
        checked_list_manufacturer=checked_list_manufacturer,
        checked_list_country=checked_list_country,
        len=len
    )
    return html


if __name__ == '__main__':
    app.run(debug=True)