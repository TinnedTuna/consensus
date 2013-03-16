from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Text,
    Table,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    )

from sqlalchemy.types import (
  Binary,
  TypeDecorator
  )

from zope.sqlalchemy import ZopeTransactionExtension

import uuid

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


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

class Role(Base):
  __tablename__ = "roles"
  alias=Column(Text, primary_key=True)
  description=Column(Text)

  def __init__(self, alias, description=None):
    self.alias = alias
    self.description = description

user_roles = Table('user_roles', Base.metadata,
  Column('user_id', Binary, ForeignKey('users.id')),
  Column('role_alias', Text, ForeignKey('roles.alias')))

class User(Base):
  __tablename__ = "users"
  id = Column(UUID, primary_key = True, default=uuid.uuid4)
  username = Column(Text, unique=True)
  password = Column(Text)
  salt = Column(Text)
 
  # Many to Many relationship to roles. 
  roles = relationship('Role', secondary='user_roles',  backref='users')

  def __init__(self, id, username, password, salt):
    self.id = id
    self.username = username
    self.password = password
    self.salt = salt
  

