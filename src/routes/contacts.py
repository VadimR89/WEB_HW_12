from fastapi import APIRouter, HTTPException, Depends, status, Path, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.entity.models import User, Role
from src.repository import contacts as repositories_contacts
from src.schemas.contact import ContactSchema, ContactUpdateSchema, ContactResponse
from src.services.auth import auth_service
from src.services.roles import RoleAccess

router = APIRouter(prefix='/contacts', tags=['contacts'])

access_to_route_all = RoleAccess([Role.admin, Role.moderator])


@router.get("/", response_model=list[ContactResponse])
async def get_contacts(limit: int = Query(10, ge=10, le=500), offset: int = Query(0, ge=0),
                       db: AsyncSession = Depends(get_db), user: User = Depends(auth_service.get_current_user)):
        """
The get_contacts function returns a list of contacts.

:param limit: int: Limit the number of contacts returned
:param ge: Set a minimum value for the limit parameter
:param le: Limit the number of contacts returned
:param offset: int: Specify the number of records to skip
:param ge: Specify that the limit must be greater than or equal to 10
:param db: AsyncSession: Get the database session
:param user: User: Get the current user from the auth_service
:return: A list of contacts
:doc-author: Trelent
"""
    contacts = await repositories_contacts.get_contacts(limit, offset, db, user)
    return contacts


@router.get("/", response_model=ContactResponse)
async def get_contact(
        contact_id: int = Query(None),
        first_name: str = Query(None),
        last_name: str = Query(None),
        email: str = Query(None),
        db: AsyncSession = Depends(get_db)
):
      """
The get_contact function is used to retrieve a contact from the database.
    The function can be called with either a contact_id or first_name, last_name, and email.
    If all three of those parameters are provided then the function will return the first matching result.

:param contact_id: int: Specify the contact_id of the contact to be deleted
:param first_name: str: Get the first name of a contact
:param last_name: str: Filter the contacts by last name
:param email: str: Get the contact by email
:param db: AsyncSession: Pass the database connection to the function
:return: A contact object
:doc-author: Trelent
"""
    if first_name or last_name or email:
        contact = await repositories_contacts.get_contact_by_params(
            first_name=first_name,
            last_name=last_name,
            email=email,
            db=db,
        )
    else:
        contact = await repositories_contacts.get_contacts(contact_id, db)

    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")

    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactSchema, db: AsyncSession = Depends(get_db),
                         user: User = Depends(auth_service.get_current_user)):
        """
The create_contact function creates a new contact in the database.

:param body: ContactSchema: Validate the request body
:param db: AsyncSession: Pass the database session to the repository
:param user: User: Get the current user from the request
:return: A contactschema object
:doc-author: Trelent
"""
    contact = await repositories_contacts.create_contact(body, db, user)
    return contact


@router.put("/{contact_id}")
async def update_contact(body: ContactUpdateSchema, contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db),
                         user: User = Depends(auth_service.get_current_user)):
        """
The update_contact function updates a contact in the database.

:param body: ContactUpdateSchema: Get the contact information from the request body
:param contact_id: int: Specify the id of the contact to be deleted
:param db: AsyncSession: Get the database session
:param user: User: Get the current user
:return: A contact object
:doc-author: Trelent
"""
    contact = await repositories_contacts.update_contact(contact_id, body, db, user)
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db),
                         user: User = Depends(auth_service.get_current_user)):
        """
The delete_contact function deletes a contact from the database.

:param contact_id: int: Get the contact id from the path
:param db: AsyncSession: Pass the database session to the function
:param user: User: Get the current user from the auth_service
:return: A dict with the deleted contact
:doc-author: Trelent
"""
    contact = await repositories_contacts.delete_contact(contact_id, db, user)
    return contact
