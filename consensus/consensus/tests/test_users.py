import unittest
import transaction
import uuid

from pyramid import testing

from webob.multidict import MultiDict

from consensus.models import (
    DBSession,
    Role,
    User,
    )

from consensus.views import signup 

class TestUsers(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        from sqlalchemy import create_engine
        engine = create_engine('sqlite://')
        from consensus.models import (
            Base,
            User,
            )
        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)
        with transaction.manager:
            role = Role('ROLE_USER', 'The default role for all users.')
            DBSession.add(role)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_user_signup(self):
        request = testing.DummyRequest() 
        request.POST = MultiDict()
        request.POST['username'] = 'TestUser'
        request.POST['password'] = 'TestPass'
        response = signup(request)
        self.assertEqual(response.status_int, 200)
        
    def test_duplicate_user_signup(self):
        request = testing.DummyRequest() 
        request.POST = MultiDict()
        request.POST['username'] = 'TestUser'
        request.POST['password'] = 'TestPass'
        response = signup(request)
        self.assertEqual(response.status_int, 200)
        request = testing.DummyRequest() 
        request.POST = MultiDict()
        request.POST['username'] = 'TestUser'
        request.POST['password'] = 'TestPass'
        response = signup(request)
        self.assertEqual(response.status_int, 400)
 
 
