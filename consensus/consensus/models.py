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

from sqlalchemy.schema import (
    UniqueConstraint,
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

    def __eq__(self, other):
        if (other is None):
            return False
        else:
            return (other.alias == self.alias)

"""An association table so that each user may have many roles.
"""
user_roles = Table('user_roles', Base.metadata,
    Column('user_id', UUID, ForeignKey('users.id')),
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
  
    def __eq__ (self, other):
        if (other is None):
            return False
        else:
            return (other.id == self.id)

"""Represents a method of holding an election, e.g. FPTP, STV, AV, etc.
"""
class Method(Base):
    __tablename__ = "methods"
    python_name = Column(Text, primary_key = True)
    name = Column(Text)
    description = Column(Text)

    def __init__(self, python_name, name, description):
        self.python_name = python_name
        self.name = name
        self.description = description

    def __eq__(self, other):
        if (other is None):
            return False 
        else:
            return (self.python_name == other.python_name)

"""Represents a ballot on an election.
"""
class Ballot(Base):
    __tablename__ = "ballots"
    id = Column(UUID, primary_key = True, default=uuid.uuid4)
    user_id = Column(UUID, ForeignKey('users.id'))
    user = relationship("User")
    election_id = Column(UUID, ForeignKey('elections.id'))
    election = relationship("Election")
    ballot = Column(Text)

    __table_args__ = (
        UniqueConstraint('user_id','election_id'),
    )

    def __init__(self, user, election, ballot):
        self.user = user
        self.election = election
        self.ballot = ballot

"""Represents an election in the system.
"""
class Election(Base):
    __tablename__ = "elections"
    id = Column(UUID, primary_key = True, default=uuid.uuid4)
    name = Column(Text, unique=True)
    body = Column(Text)
    method_id = Column(Text, ForeignKey('methods.python_name'))
    method = relationship("Method")

    def __init__(self, name, body, method):
      self.name = name
      self.body = body
      self.method = method

    def __eq__(self, other):
        if (other is None):
            return False
        else:
            return (other.id == self.id)
