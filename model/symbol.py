from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

class Symbol:
    __tablename__ = 'symbols'

    id =            Column(Integer, primary_key=True)
    libc_binary_id =Column(Integer, ForeignKey('libc_binary.id'))
    libc_binary =   relationship("LibcBinary", backref=backref('symbol', order_by=id))

    name =          Column(String)
    nsym =          Column(Integer)
    version_filename = Column(String)
    version_index = Column(String)
    version_hidden =Column(String)
    version_name =  Column(String)
    st_value =      Column(Boolean)
    st_size =       Column(Integer)
    st_info_type =  Column(String)
    st_info_bind =  Column(String)
    st_other_visibility = Column(String)
    st_shndx =      Column(Integer)
