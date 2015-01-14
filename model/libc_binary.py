from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

class LibcBinary(Base):
    __tablename__ = 'libc_binaries'

    id =        Column(Integer, primary_key=True)
    symbols =   relationship("Symbol", order_by="Symbol.id", backref="libc_binary")

    source =    Column(String)
    filename =  Column(String)
    distro =    Column(String)
    release =   Column(String)
    version =   Column(String)
    md5sum =    Column(String(32))

