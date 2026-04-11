import app.db.models as models
from sqlalchemy.orm import Session


class AdminRepository:

    async def get_by_user_id(self, admin_id: str, db: Session):
        return db.query(models.Admin).filter(models.Admin.id == admin_id).first()

    
    async def get_by_user_id(self, admin_id: str, db: Session):
        return db.query(models.Admin).filter(models.Admin.id == admin_id).first()



admin = AdminRepository()