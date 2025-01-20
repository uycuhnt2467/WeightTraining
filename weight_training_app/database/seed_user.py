from sqlalchemy.orm import Session
from ..models.user import User, UserType
from ..utils.security import get_password_hash

def seed_initial_data(db: Session):
    # Create admin user
    admin_user = User(
        email="admin@example.com",
        username="admin",
        hashed_password=get_password_hash("admin123"),
        user_type=UserType.ADMIN
    )

    # Create test trainer
    trainer_user = User(
        email="trainer@example.com",
        username="trainer",
        hashed_password=get_password_hash("trainer123"),
        user_type=UserType.TRAINER
    )

    # Create test customer
    customer_user = User(
        email="customer@example.com",
        username="customer",
        hashed_password=get_password_hash("customer123"),
        user_type=UserType.CUSTOMER
    )

    db.add_all([admin_user, trainer_user, customer_user])
    try:
        db.commit()
        print("Initial data seeded successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error seeding initial data: {e}")