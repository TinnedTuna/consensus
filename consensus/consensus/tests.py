import unittest
import transaction
import uuid

from pyramid import testing

from .models import DBSession


class TestUser(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        from sqlalchemy import create_engine
        engine = create_engine('sqlite://')
        from .models import (
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

    def test_it(self):
        from .views import login 
        request = testing.DummyRequest()
        info = login(request)
        #self.assertEqual(info['one'].name, 'one')
        #self.assertEqual(info['project'], 'consensus')
