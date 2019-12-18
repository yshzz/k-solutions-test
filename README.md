# k-solutions-test
Test task

# To run locally
Install dependencies with [Poetry](https://python-poetry.org/docs/)
```python
poetry install
```

Configure environment variables:
+ SECRET_KEY
+ SQLALCHEMY_DATABASE_URI
+ PIASTRIX_SHOP_ID
+ PIASTRIX_SECRET_KEY

To create the initial database, just import the db object from an interactive Python shell and 
run the SQLAlchemy.create_all() method to create the tables and database:
```python
>>> from main import db
>>> db.create_all()
```

Now you are able to test application on your local machine
```python
python run.py
```
