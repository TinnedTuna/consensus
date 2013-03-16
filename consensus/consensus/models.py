from sqlalchemy import (
    Column,
    Integer,
    Text,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from sqlalchemy.types import (
  Binary,
  TypeDecorator
  )

from zope.sqlalchemy import ZopeTransactionExtension

import uuid

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    value = Column(Integer)

    def __init__(self, name, value):
        self.name = name
        self.value = value

class UUID(TypeDecorator):
  impl = Binary
  def __init__(self):
    self.impl.length = 16
    TypeDecorator.__init__(self,length=self.impl.length)

  def process_bind_param(self,value,dialect=None):
    if value and isinstance(value,uuid.UUID):
      return value.bytes
    elif value and not isinstance(value.uuid.UUID):
      raise ValueError,'value %s is not a valid uuid.UUID' % value
    else:
      return None

  def process_result_value(self,value,dialect=None):
    if value:
      return uuid.UUID(bytes=value)
    else:
      return None

class User(Base):
  __tablename__ = "users"
  id = Column(UUID, primary_key = True, default=uuid.uuid4)
  username = Column(Text, unique=True)
  password = Column(Text)
  salt = Column(Text)
  
  def __init__(self, id, username, password, salt):
    self.id = id
    self.username = username
    self.password = password
    self.salt = salt
  

