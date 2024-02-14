from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from . config import settings
import psycopg2
from psycopg2.extras import RealDictCursor

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get session-creates a session in db to perform operation
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
 
 
# while True:
#     try:
#         conn = psycopg2.connect(host="localhost",database="fastapi",user='postgres',password="dbpass123",cursor_factory=RealDictCursor)
#         # The use of RealDictCursor is beneficial when mapping column values to keys in dictionaries. However, it's important to note that accessing columns is not limited to RealDictCursor. 
#         # Even without using it, default cursor types, such as the regular cursor, allow access to columns, albeit in the form of tuples where each element corresponds to a column in the result set.
#         cursor=conn.cursor()    #Execute database commands
#         print("Database connection was successfull!")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error :",error)
#         time.sleep(2)
#         # We have established connection and now we can perform SQL Codes.
        
# @app.get("/")
# async def root(): #Defining function//root is a function name
#     cursor.execute("""SELECT * FROM posts""") #Exceute commands where cursor is used to execute commands
#     posts=cursor.fetchall()
#     # print(posts)
#     return posts

