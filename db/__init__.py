from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask import Flask, g
import app
from sqlalchemy.orm import registry
mapper_registry = registry()
import config
#print("Using SQLAlchemy path: " + str(SQLALCHEMY_DATABASE_URI))
UNIQUE_EMAIL = True
UNIQUE_USER = False
UNIQUE_USEREMAIL = False
engine = create_engine(config.SQLALCHEMY_DATABASE_URI, echo = True)
Session = sessionmaker(bind = engine)
mainsession = Session() # Only valid in the main application thread!
Model = declarative_base()
main_table_list = {}

def AppSession():
    if g.db is not None:
        return g.db
#    print("Attempted to grab db.AppSession() without a database entry!!!")

@app.app.before_request
def before_request():
    print("Opening db connection")
    g.db = Session()


@app.app.after_request
def after_request(response):
    if g.db is not None:
        print("Closin db connection")
        g.db.close()
    return response


from models.group import Group
from models.user import User
from models.permission import Permission
def initialize_empty_database(db):
    db.mapper_registry.metadata.create_all(bind=db.engine)
    for tbl in reversed(db.mapper_registry.metadata.sorted_tables):
        try:
            tbl.drop(db.engine)
        except:
            pass
    db.mapper_registry.metadata.create_all(bind=db.engine)
    db.mainsession.commit()

def populate_sample_data(db):
    permission = Permission(api_permission="/*")
    try:
        db.mainsession.add(permission)
        db.mainsession.commit()
    except Exception as ex:
        print("unable to add permissions to DB")
        print(ex)
        db.mainsession.rollback()
        pass
    admingroup = Group(name="Admin",permissions=[permission])
    try:
        db.mainsession.add(admingroup)
        db.mainsession.commit()
    except Exception as ex:
        print("unable to add groups to DB")
        print(ex)
        db.mainsession.rollback()
        pass
    user = User(name="Mike",username="malcom2073",password="12345",email="malcom@mike.com",groups=[admingroup],validated=True)
    try:
        db.mainsession.add(user)
        db.mainsession.commit()
    except Exception as ex:
        print("unable to add user to DB")
        db.mainsession.rollback()
        print(ex)
        pass

