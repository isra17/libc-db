from model import symbol, libc_binary
from sqlalchemy.ext.declarative import declarative_base
import config

Base = declarative_base()

Base.metadata.create_all(config.engine)
