from extensions import db
from sqlalchemy import Column, Integer, String, ForeignKey


class BenefitUser(db.Model):
    __tablename__ = 'benefit_user'
    benefit_id = Column(Integer, ForeignKey('benefit.id'), primary_key=True, nullable=False)
    user_rut = Column(String(12), ForeignKey('user.rut'), primary_key=True, nullable=False)

    def serialize(self):
        return {
            "benefit_id": self.benefit_id,
            "user_rut": self.user_rut,
        }
