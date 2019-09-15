import logging
from flask_sqlalchemy import SQLAlchemy
import datetime

from app import db
from app.models import Contact, Email


# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
logger = logging.getLogger('REPO')


class ContactListRepo:
    """
    Repository for handling Contact list
    """
    def __init__(self):
        pass
    
    def get_contact_list(self):
        contact_list = Contact.query.all()
        return contact_list

    def create_contact(self, username, first_name, last_name, emails):
        contact = None
        try:
            created = datetime.datetime.now()
            contact = Contact(username, first_name, last_name, created)

            for email in emails:
                email_item = Email(address=email)
                contact.emails.append(email_item)
                db.session.add(email_item)
        
            db.session.add(contact)
            db.session.commit()
        except:
            db.session.rollback()

        return contact


class ContactRepo:
    """
    Repository for handling Contact item
    """
    def __init__(self):
        pass
    
    def get_contact(self, username):
        contact = Contact.query.filter_by(username=username).first()
        return contact

    def update_contact(self, username, new_username, first_name, last_name, emails):
        try:
            contact = Contact.query.filter_by(username=username).first()

            contact.username = new_username
            contact.first_name = first_name
            contact.last_name = last_name
            contact.created = datetime.datetime.now()

            logger.debug(f'REPO: AFTER CONTACTID {contact}!!!!!!!!!!!')
            db.session.add(contact)
            db.session.commit()

            contact_id = contact.id
            logger.debug(f'REPO: AFTER CONTACTID {contact}!!!!!!!!!!!')

            # First delete old emails if new ones are added
            emails_to_delete = Email.query.filter_by(contact_id=contact_id)
            for email in emails_to_delete:
                db.session.delete(email)
            for email in emails:
                email_item = Email(address=email)
                contact.emails.append(email_item)
                db.session.add(email_item)

            db.session.commit()
            result = contact
        except:
            db.session.rollback()
            result = None

        return result

    def delete_contact(self, username, older_than):
        try:
            # If delete api call made with path param (username)
            if username:
                contact = Contact.query.filter_by(username=username).first()
                db.session.delete(contact)
                db.session.commit()
            
            # If delete api call made with query param time filter
            if older_than:
                time_threshold_seconds = datetime.datetime.now() - datetime.timedelta(minutes=1)
                logger.debug(f'REPO DELETE: time_threshold_seconds {time_threshold_seconds}')
                contacts_to_delete = Contact.query.filter(Contact.created < time_threshold_seconds).all()
                logger.debug(f'REPO DELETE: AFTER NOW calc!!!!!!!!!! {contacts_to_delete}')
                contact_list_to_delete = [db.session.delete(contact) for contact in contacts_to_delete]
                db.session.commit()
    
            result = True
        except:
            db.session.rollback()
            result = False

        return result
