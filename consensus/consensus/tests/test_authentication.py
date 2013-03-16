import unittest
import transaction
import uuid

from pyramid import testing

from webob.multidict import MultiDict

from consensus.models import DBSession

from consensus.views import auth

class TestAuthentication(unittest.TestCase):
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
            model = User(uuid.uuid4(), 'TestUser','TestPass','TestSalt')
            DBSession.add(model)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_no_auth(self):
        request = testing.DummyRequest()
        request.POST = MultiDict()
        info = auth(request)
        self.assertEqual(info['authentication'], False)

    def test_auth_actual(self):
        request = testing.DummyRequest()
        request.POST = MultiDict()
        request.POST['username'] = 'TestUser'
        request.POST['password'] = 'TestPass'
        response = auth(request)
        self.assertEqual(response['username'], 'TestUser')
        self.assertEqual(response['password'], 'TestPass')
        self.assertEqual(response['authentication'], True)
