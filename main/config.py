import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    PIASTRIX_SHOP_ID = os.environ.get('PIASTRIX_SHOP_ID')
    PIASTRIX_SECRET_KEY = os.environ.get('PIASTRIX_SECRET_KEY')
