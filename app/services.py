import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
logger = logging.getLogger('REPO')


class ContactListService:
    """
    Service class responsible for handling contact list
    """
    def __init__(self, repo):
        self.repo = repo

    def get_contact_list(self):
        return self.repo.get_contact_list()

    def create_contact(self, username, first_name, last_name, emails):
        contact = self.repo.create_contact(username, first_name, last_name, emails)
        return contact


class ContactService:
    """
    Service class responsible for handling contact items
    """
    def __init__(self, repo):
        self.repo = repo

    def get_contact(self, username):
        return self.repo.get_contact(username)

    def update_contact(self, username, new_username, first_name, last_name, emails):
        updated_item = self.repo.update_contact(username, new_username, first_name, last_name, emails)
        return updated_item

    def delete_contact(self, username, older_than):
        is_item_deleted = self.repo.delete_contact(username, older_than)
        return is_item_deleted