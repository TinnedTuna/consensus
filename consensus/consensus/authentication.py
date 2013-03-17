from consensus.models import (
    Role,
    DBSession,
    User,
    )

"""Error to represent the condition that authentication failed.
"""
class AuthenticationError():
    pass

"""Represents a logged in user.
"""
class Authentication():
    roles = set()
    user = None
  
    def __init__(self, user, roles):
        self.user = user
        if (len(self.roles) == 0):
            self.roles.add(Role('ROLE_ANON'))
        else:
            self.roles = roles

    def is_authenticated(self):
        if (not (self.user is None or self.roles is None or len(self.roles) < 1)):
            return self.roles != list().append(Role('ROLE_ANON'))
        else:
            return False
            

"""Exceptionally basic local user authentication
"""
class AuthenticationStrategy():

    def __init__(self):
        pass

    def authenticate(self, request):
        try:
            supplied_username = request.POST.getone('username')
            password = request.POST.getone('password')
        except KeyError:
            raise AuthenticationError()

        user = DBSession.query(User).filter_by(username=supplied_username).first()        
        if (user.password == password):
          return Authentication(user,user.roles)  
        else:
          raise AuthenticationError()
