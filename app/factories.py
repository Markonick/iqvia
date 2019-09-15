from app.services import ContactListService, ContactService
from app.repositories import ContactListRepo, ContactRepo

def create_contact_list_repo():
    return ContactListRepo()

def create_contact_repo():
    return ContactRepo()

def create_contact_list_service():
    return ContactListService(create_contact_list_repo())

def create_contact_service():
    return ContactService(create_contact_repo())