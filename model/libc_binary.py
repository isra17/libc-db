from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

class LibcBinary(Base):
    __tablename__ = 'libc_binaries'

    id =        Column(Integer, primary_key=True)
    symbols =   relationship("Symbol",
                    order_by="Symbol.id",
                    backref="lib_binary")
    sources =   relationship("DownloadTarget",
                    order_by="DownloadTarget.downloaded_at",
                    backref="lib_binary")

    created_at =    DateTime()

    distro =    Column(String)
    distro_release =   Column(String)

    filename =  Column(String)
    md5sum =    Column(String(32))
    lib_version =   Column(String)

