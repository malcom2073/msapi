
import os
username = os.environ['DB_USER']
password = os.environ['DB_PASS']
hostname = os.environ['DB_HOST']
databasename = os.environ['DB_DATABASE']
#SQLALCHEMY_DATABASE_URI = "sqlite://"
#SQLALCHEMY_DATABASE_URI = 
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_MAIN_URI = "postgresql+psycopg2://" + username + ":" + password + "@" + hostname
SECRET_KEY = "asfdsafdsadfsafdsadffdsa"