from sqlalchemy import create_engine

engine = create_engine('mysql+mysqlconnector://root@localhost/libc_db', echo=True)

