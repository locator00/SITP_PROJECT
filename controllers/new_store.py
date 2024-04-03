from app import app
from flask import render_template, request, session

# from utils import get_db_connection
# from models.index_model import get_reader, get_book_reader, get_new_reader 



@app.route('/new_store', methods=['get'])
def new_store():
    html = render_template(
        'new_store.html',
        len=len
    )
    return html


if __name__ == '__main__':
    app.run(debug=True)
