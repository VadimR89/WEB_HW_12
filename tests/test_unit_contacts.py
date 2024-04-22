import unittest
from unittest.mock import MagicMock, AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession
from src.entity.models import Contact, User
from src.schemas.contact import ContactSchema, ContactUpdateSchema
from src.repository.contacts import (
    create_contact,
    get_contacts,
    get_contact,
    update_contact,
    delete_contact,
    get_contact_by_params,
)


class TestAsyncContact(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.user = User(id=1, username="test_user", passwor="blabla", confirmed=True)
        self.session = AsyncMock(spec=AsyncSession)

    async def test_get_contacts(self):
    """    
    The test_get_contacts function tests the get_contacts function.
    It does this by mocking a session object and then calling the get_contacts function with that mocked session object.
    The test asserts that the result of calling get_contacts is equal to a list of two Contact objects.
    
    :param self: Access the attributes and methods of the class in python
    :return: A list of contacts
    :doc-author: Trelent
    """
        limit = 10
        offset = 0
        contacts = [
            Contact(
                id=1,
                title="test_title_1",
                description="test_description_1",
                user=self.user,
            ),
            Contact(
                id=2,
                title="test_title_2",
                description="test_description_2",
                user=self.user,
            ),
        ]
        mocked_contacts = MagicMock()
        mocked_contacts.scalars.return_value.all.return_value = contacts
        self.session.execute.return_value = mocked_contacts
        result = await get_contacts(limit, offset, self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact(self):
        """    
    The test_get_contact function tests the get_contact function.
    It does this by mocking a session object and a user object, then calling the get_contact function with these mocked objects as arguments.
    The test asserts that the result of calling get_contact is equal to an expected list of contacts.
    
    :param self: Access the instance of the class
    :return: A list of two objects
    :doc-author: Trelent
    """
        limit = 10
        offset = 0
        contacts = [
            Contact(
                id=1,
                title="test_title_1",
                description="test_description_1",
                user=self.user,
            ),
            Contact(
                id=2,
                title="test_title_2",
                description="test_description_2",
                user=self.user,
            ),
        ]
        mocked_contacts = MagicMock()
        mocked_contacts.scalars.return_value.all.return_value = contacts
        self.session.execute.return_value = mocked_contacts
        result = await get_contact(limit, offset, self.session, self.user)
        self.assertEqual(result, contacts)

    async def test_create_contact(self):
    """    
    The test_create_contact function tests the create_contact function.
    It does this by creating a ContactSchema object, which is then passed to the create_contact function.
    The result of that call is then checked to see if it's an instance of Contact and if its title and description are equal to those in the body.
    
    :param self: Represent the instance of the class
    :return: An instance of the contact class
    :doc-author: Trelent
    """
        body = ContactSchema(title="test_title", description="test_description")
        result = await create_contact(body, self.session, self.user)
        self.assertIsInstance(result, Contact)
        self.assertEqual(result.title, body.title)
        self.assertEqual(result.description, body.description)

    async def test_update_contact(self):
    """
    The test_update_contact function tests the update_contact function.
    It does this by creating a ContactUpdateSchema object, which is used to create a mocked contact object.
    The mocked contact's scalar_one_or_none method returns a Contact object with an id of 1, title of test_title, 
    description of test_description and user equal to self.user (which is set in the setup function).
    The session's execute method then returns the mocked contact and result becomes equal to await update-contact(...). 
    The assertIsInstance statement checks that result is an instance of Contact and asserts that it has been updated correctly.
    
    :param self: Represent the instance of the class
    :return: A contact object
    :doc-author: Trelent
    """
        body = ContactUpdateSchema(
            title="test_title", description="test_description", completed=True
        )
        mocked_contact = MagicMock()
        mocked_contact.scalar_one_or_none.return_value = Contact(
            id=1, title="test_title", description="test_description", user=self.user
        )
        self.session.execute.return_value = mocked_contact
        result = await update_contact(1, body, self.session, self.user)
        self.assertIsInstance(result, Contact)
        self.assertEqual(result.title, body.title)
        self.assertEqual(result.description, body.description)

    async def test_delete_contact(self):
    """
    The test_delete_contact function tests the delete_contact function in the contacts.py file.
    It does this by mocking a contact object and returning it when scalar_one_or_none is called on it,
    and then calling execute on self.session with that mocked contact as an argument, which returns 
    the mocked contact again (this is done to simulate what happens in the actual delete function). 
    Then we call delete and commit on self.session to simulate deleting a row from our database table, 
    and finally assert that result is an instance of Contact.
    
    :param self: Access the variables in the class
    :return: A contact object
    :doc-author: Trelent
    """
        mocked_contact = MagicMock
        mocked_contact.scalar_one_or_none.return_value = Contact(
            id=1, title="test_title", description="test_description", user=self.user
        )
        self.session.execute.return_value = mocked_contact
        result = await delete_contact(1, self.session, self.user)
        self.session.delete.assert_called_once()
        self.session.commit.assert_called_once()
        self.assertIsInstance(result, Contact)
