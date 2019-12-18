from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from .piastrix import Piastrix

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
piastrix = Piastrix(shop_id=app.config['PIASTRIX_SHOP_ID'],
                    secret_key=app.config['PIASTRIX_SECRET_KEY'])

from . import routes
