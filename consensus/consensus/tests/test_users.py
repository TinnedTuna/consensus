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

from consensus.views.user import (
    signup,
    auth,
    )

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

    def _get_request(self):
        self.config.include('consensus.routes_setup')
        request = testing.DummyRequest()
        request.POST = MultiDict()
        return request

    def test_user_signup(self):
        request = self._get_request()
        request.POST['username'] = 'TestUser'
        request.POST['password'] = 'TestPass'
        response = signup(request)
        self.assertEqual(response.status_int, 302)
        
    def test_duplicate_user_signup(self):
        request = self._get_request()
        request.POST['username'] = 'TestUser'
        request.POST['password'] = 'TestPass'
        response = signup(request)
        self.assertEqual(response.status_int, 302)
        request = self._get_request()
        request.POST['username'] = 'TestUser'
        request.POST['password'] = 'TestPass'
        response = signup(request)
        self.assertEqual(response.status_int, 400)
 
    def test_user_signup_and_auth(self):
        request = self._get_request()
        request.POST['username'] = 'TestUser'
        request.POST['password'] = 'TestPass'
        response = signup(request)
        self.assertEqual(response.status_int, 302)
        request = self._get_request()
        request.POST['username'] = 'TestUser'
        request.POST['password'] = 'TestPass'
        response = auth(request)
        self.assertEqual(response.status_int, 302)
        auth_token = request.session['authentication']
        self.assertTrue(auth_token.is_authenticated()) 
