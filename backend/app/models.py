"""
Database models for the finance application.
"""

import uuid
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class UserBase(SQLModel):
    """Base user model with shared fields."""
    email: str = Field(unique=True, index=True, max_length=255)
    full_name: str = Field(max_length=255)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)


class User(UserBase, table=True):
    """User model for database table."""
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
    
    # Relationships
    accounts: list["Account"] = Relationship(back_populates="user")
    transactions: list["Transaction"] = Relationship(back_populates="user")


class UserCreate(UserBase):
    """User creation model."""
    password: str = Field(min_length=8, max_length=100)


class UserUpdate(SQLModel):
    """User update model."""
    email: Optional[str] = Field(default=None, max_length=255)
    full_name: Optional[str] = Field(default=None, max_length=255)
    password: Optional[str] = Field(default=None, min_length=8, max_length=100)
    is_active: Optional[bool] = Field(default=None)
    is_superuser: Optional[bool] = Field(default=None)


class UserPublic(UserBase):
    """User public model for API responses."""
    id: uuid.UUID
    created_at: datetime


# Account Models
class AccountType(str, Enum):
    """Account type enumeration."""
    CHECKING = "checking"
    SAVINGS = "savings"  
    CREDIT_CARD = "credit_card"
    INVESTMENT = "investment"
    LOAN = "loan"


class AccountBase(SQLModel):
    """Base account model."""
    name: str = Field(max_length=255)
    account_type: str = Field(max_length=50)
    balance: Decimal = Field(default=Decimal("0.00"), decimal_places=2, max_digits=15)
    currency: str = Field(default="USD", max_length=3)
    is_active: bool = Field(default=True)


class Account(AccountBase, table=True):
    """Account model for database table."""
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
    
    # Relationships
    user: User = Relationship(back_populates="accounts")
    transactions: list["Transaction"] = Relationship(back_populates="account")


class AccountCreate(AccountBase):
    """Account creation model."""
    pass


class AccountUpdate(SQLModel):
    """Account update model."""
    name: Optional[str] = Field(default=None, max_length=255)
    account_type: Optional[str] = Field(default=None, max_length=50)
    balance: Optional[Decimal] = Field(default=None, decimal_places=2, max_digits=15)
    currency: Optional[str] = Field(default=None, max_length=3)
    is_active: Optional[bool] = Field(default=None)


class AccountPublic(AccountBase):
    """Account public model for API responses."""
    id: uuid.UUID
    created_at: datetime


# Transaction Models
class TransactionBase(SQLModel):
    """Base transaction model."""
    amount: Decimal = Field(decimal_places=2, max_digits=15)
    description: str = Field(max_length=500)
    category: Optional[str] = Field(default=None, max_length=100)
    transaction_date: datetime = Field(default_factory=datetime.utcnow)
    is_recurring: bool = Field(default=False)


class Transaction(TransactionBase, table=True):
    """Transaction model for database table."""
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    account_id: uuid.UUID = Field(foreign_key="account.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
    
    # Relationships
    user: User = Relationship(back_populates="transactions")
    account: Account = Relationship(back_populates="transactions")


class TransactionCreate(TransactionBase):
    """Transaction creation model."""
    account_id: uuid.UUID


class TransactionUpdate(SQLModel):
    """Transaction update model."""
    amount: Optional[Decimal] = Field(default=None, decimal_places=2, max_digits=15)
    description: Optional[str] = Field(default=None, max_length=500)
    category: Optional[str] = Field(default=None, max_length=100)
    transaction_date: Optional[datetime] = Field(default=None)
    account_id: Optional[uuid.UUID] = Field(default=None)
    is_recurring: Optional[bool] = Field(default=None)


class TransactionPublic(TransactionBase):
    """Transaction public model for API responses."""
    id: uuid.UUID
    account_id: uuid.UUID
    created_at: datetime