from flask import Flask

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

import controllers.index
import controllers.new_store
import controllers.search
