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
        body = ContactSchema(title="test_title", description="test_description")
        result = await create_contact(body, self.session, self.user)
        self.assertIsInstance(result, Contact)
        self.assertEqual(result.title, body.title)
        self.assertEqual(result.description, body.description)

    async def test_update_contact(self):
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
        mocked_contact = MagicMock
        mocked_contact.scalar_one_or_none.return_value = Contact(
            id=1, title="test_title", description="test_description", user=self.user
        )
        self.session.execute.return_value = mocked_contact
        result = await delete_contact(1, self.session, self.user)
        self.session.delete.assert_called_once()
        self.session.commit.assert_called_once()
        self.assertIsInstance(result, Contact)
