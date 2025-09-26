"""
Database engine and session management.
Based on FastAPI full-stack template with PostgreSQL configuration.
"""

from sqlmodel import Session, create_engine, select

from app.core.config import settings

# Create the database engine
engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def get_session():
    """Get database session generator for dependency injection."""
    with Session(engine) as session:
        yield session


def init_db(session: Session) -> None:
    """
    Initialize the database with initial data.
    Tables should be created with Alembic migrations.
    """
    # Import here to avoid circular imports
    from app import crud
    from app.models import User, UserCreate
    
    # Create first superuser if it doesn't exist
    user = session.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            full_name="Super User",
            is_superuser=True,
        )
        # Note: This requires implementing crud.create_user function
        # For now, we'll create the user directly
        from app.core.security import get_password_hash
        
        user = User(
            email=user_in.email,
            hashed_password=get_password_hash(user_in.password),
            full_name=user_in.full_name,
            is_superuser=user_in.is_superuser,
        )
        session.add(user)
        session.commit()
        session.refresh(user)