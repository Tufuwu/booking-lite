import app.db.models as models
from sqlalchemy.orm import Session


class AdminRepository:
    async def get_by_user_name(self, db: Session, username: str):
        return db.query(models.Admin).filter(models.Admin.name == username).first()

    async def get_by_job_number(self, db: Session, job_number: str):
        return db.query(models.Admin).filter(models.Admin.job_number == job_number).first()

    async def create_admin(self, db: Session, admin: models.Admin):
        db.add(admin)
        db.commit()
        db.refresh(admin)
        return admin

    async def get_all_admins(self, db: Session):
        return db.query(models.Admin).all()
    
    async def update_admin(self, db: Session, admin: models.Admin):
        db.commit()
        db.refresh(admin)
        return admin

    async def delete_admin(self, db: Session, admin: models.Admin) -> None:
        db.delete(admin)
        db.commit()


admins = AdminRepository()
