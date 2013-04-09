import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid',
    'SQLAlchemy',
    'transaction',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'pyramid_beaker',
    'zope.sqlalchemy',
    'waitress',
    'bcryptor',
    'yamlog', # Bcryptor-1.2.2 needs this but doesn't decalare it.
    ]

setup(name='consensus',
      version='0.0',
      description='consensus',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='consensus',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = consensus:main
      [console_scripts]
      initialize_consensus_db = consensus.scripts.initializedb:main
      """,
      )
