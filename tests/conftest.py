import pytest
import datetime
from freezegun import freeze_time

from app import create_app
from app import db
from app.models import Contact, Email


@pytest.fixture(scope='function')
def client():
    app = create_app(config_class='config.TestingConfig')
    test_client = app.test_client()

    ctx = app.app_context()
    ctx.push()
    yield test_client
    ctx.pop()

@pytest.fixture(scope='function')
def init_database():
    # Create the database and the database table
    db.create_all()

    # Insert user data
    with freeze_time("2019-09-15 12:00:00"):
        contact1 = Contact(username='nicomark', first_name='Nicolas', last_name='Markos', created=datetime.datetime.now())
        contact2 = Contact(username='speedster', first_name='Efi', last_name='Pappa', created=datetime.datetime.now())
    db.session.add(contact1)
    db.session.add(contact2)
    email1_1 = Email(address='mark123@gmail.com')
    email1_2 = Email(address='nicomark66@hotmail.com')
    email2 = Email(address='fifi@gmail.com')
    contact1.emails.extend([email1_1, email1_2])
    contact2.emails.append(email2)

    # Commit the changes for the users
    db.session.commit()

    yield db  # this is where the testing happens!

    db.drop_all()
