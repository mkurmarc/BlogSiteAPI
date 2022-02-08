from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time

# 
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:***REMOVED***@localhost/BlogSiteAPI'
#                         'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

"""
# temp solution to connect to DB. Later add production ready solution
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='BlogSiteAPI', user='postgres', 
                                password='***REMOVED***', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("DB connection was successful!")
        break
    except Exception as error:
        print("Connecting to DB failed!")
        print("Error: ", error)
        time.sleep(2)
"""
