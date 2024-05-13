from sqlalchemy import Column, Integer, String, ForeignKey,Float,Boolean, DateTime
from sqlalchemy.orm import relationship,joinedload
from sqlalchemy.orm import Session
from Connections.connections import Base, engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy import Time
import random
class Sitter(Base):
    __tablename__ = 'sitter'
    
    id = Column(Integer, primary_key=True, index=True) 
    name = Column(String)
    location = Column(String)
    date_of_birth = Column(String)
    contact = Column(String)
    gender = Column(String)
    next_of_kin = Column(String)
    NIN = Column(String)
    recommended_by = Column(String)
    religion = Column(String, nullable=True)
    level_of_education = Column(String, nullable=True)
    status = Column(String, default='off_duty')

    # sitter_number: str 
    # baby = relationship('Baby', back_populates='sitter_assigned')
    # payment = relationship('Payment', back_populates='sitter_id')

    @staticmethod
    def create_sitter(db_session, sitter: dict):
        print("""Creating sitter""")
        # print(sitter)
        new_sitter = Sitter(name=sitter['name'], location=sitter['location'], date_of_birth=sitter['date_of_birth'], contact=sitter['contact'], gender = sitter['gender'], next_of_kin = sitter['next_of_kin'],
                            NIN = sitter['NIN'], recommended_by = sitter['recommended_by'], religion = sitter['religion'], level_of_education = sitter['level_of_education'])
        
        db_session.add(new_sitter)
        db_session.commit()
        # print(f"new sitter: {new_sitter}")
        return new_sitter

class Baby(Base):
    __tablename__ = 'baby'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    gender = Column(String)
    age = Column(Integer)
    location = Column(String)
    name_of_brought_person = Column(String)
    time_of_arrival = Column(Time)
    name_of_parent = Column(String)
    fee = Column(Float)
    duration = Column(String, default="half_day")
    is_monthly = Column(Boolean, default=False)
    payment_type = Column(String)
    baby_access = Column(String)
    date = Column(DateTime, default=datetime.now())
    sitter_assigned = Column(Integer, ForeignKey('sitter.id'))
    # payment = relationship('Payment', back_populates='baby_id')
    # procurement_item = relationship('ProcurementItem', back_populates='sold_to_babies')

    def get_baby_by_id(db_session, baby_id):
        baby = db_session.query(Baby).filter_by(id=baby_id).first()
        return baby
    
    def get_all_babies(db_session):
        babies = db_session.query(Baby).all()
        return babies
    
    def update_baby(db_session, baby_id, baby_data):
        baby = db_session.query(Baby).filter_by(id=baby_id).first()
        if baby:
            baby.name_of_brought_person = baby_data['name_of_brought_person']
            baby.time_of_arrival = baby_data['time_of_arrival']
            baby.fee = baby_data['fee']
        
            db_session.commit()
            return baby
        

class Admin(Base):
    __tablename__ = 'admin'
    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String)
    lastname = Column(String)
    password = Column(String)
    email = Column(String, unique=True)
    contact = Column(String)
    role = Column(String, default="admin")

class AdminSignUpToken(Base):
    __tablename__ = 'admin_sign_up_token'

    id = Column(Integer, primary_key=True, index=True)
    jti = Column(String, unique=True, nullable=False) 
    email = Column(String, nullable=False)
    time = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="False")
    added_by = Column(Integer, ForeignKey('admin.id'))

    @staticmethod
    def create_token(db_session, email, admin_id):
        print(f"Creating token for email {email} by admin {admin_id}")
        jti = str(random.randint(10000000, 99999999))
        existing_token = db_session.query(AdminSignUpToken).filter_by(email=email).first()
        if existing_token:
            existing_token.jti = jti
            existing_token.time = datetime.utcnow()
            existing_token.status = "False"
            existing_token.added_by = admin_id
            token_to_return = existing_token
        else:
            new_token_entry = AdminSignUpToken(jti=jti, email=email, added_by=admin_id)
            db_session.add(new_token_entry)
            db_session.flush()
            token_to_return = new_token_entry

        try:
            db_session.commit()
            return {
                "id": token_to_return.id,
                "token": token_to_return.jti,
                "email": token_to_return.email,
                "status": token_to_return.status,
                "time": token_to_return.time,
                "added_by": token_to_return.added_by
            }
        except Exception as e:
            db_session.rollback()
            print(f"Error in token creation or update: {e}")
            return None

    @staticmethod
    def validate_token(db_session, email, token):
        print(f"received token {token} for email {email}")
        try:
            token_record = db_session.query(AdminSignUpToken).filter(
                AdminSignUpToken.email == email,
                AdminSignUpToken.jti == token,
                AdminSignUpToken.status == "False"
            ).first()
            token_validity_period = timedelta(hours=24)

            if token_record:
                token_age = datetime.utcnow() - token_record.time
                if token_age <= token_validity_period:
                    token_record.status = "True"
                    db_session.commit()
                    return True
                else:
                    
                    print(f"Token {token} for email {email} has expired.")
                    return False
            else:
            
                print(f"No valid token found for email {email} with token {token}.")
                return False
        except Exception as e:
            print(f"Exception during token validation for email {email} with token {token}: {e}")
            return False

        
    @staticmethod
    def mark_token_as_used(db_session, jti):
        token_record = db_session.query(AdminSignUpToken).filter(AdminSignUpToken.jti == jti).first()
        if token_record:
            token_record.status = "True"
            db_session.commit()
            return True
        return False
    
    @staticmethod
    def get_token_by_admin(db_session, admin_id):
        return db_session.query(AdminSignUpToken).filter(AdminSignUpToken.added_by == admin_id).all()

    @staticmethod
    def delete_token(db_session, jti):
        token_record = db_session.query(AdminSignUpToken).filter(AdminSignUpToken.jti == jti).first()
        if token_record:
            db_session.delete(token_record)
            db_session.commit()
            return True
        return False
    
class DailyPayment(Base):
    __tablename__ = 'payment'
    id = Column(Integer, primary_key=True, index=True)
    sitter_id = Column(Integer, ForeignKey('sitter.id'))
    amount = Column(Float, default=3000)
    number_of_babies = Column(Integer, default= 0)
    total_amount = Column(Float, default=0.0)
    payment_date = Column(DateTime, nullable=True)
    is_paid = Column(Boolean, default=False)

class BabyRelease(Base):
    __tablename__ = 'baby_release'
    id = Column(Integer, primary_key=True, index=True)
    baby_id = Column(Integer, ForeignKey('baby.id'))
    sitter_id = Column(Integer, ForeignKey('sitter.id'))
    status = Column(String, default="released")
    date = Column(DateTime, default=datetime.now())

class PresentSitter(Base):
    __tablename__ = 'present_sitter'
    id = Column(Integer, primary_key=True, index=True)
    sitter_id = Column(Integer, ForeignKey('sitter.id'))
    date = Column(DateTime)

    sitter = relationship("Sitter", backref="present_sitters")

class PresentBaby(Base):
    __tablename__ = 'present_sitter'
    id = Column(Integer, primary_key=True, index=True)
    baby_id = Column(Integer, ForeignKey('baby.id'))
    date = Column(DateTime)

    babies = relationship("Sitter", backref="present_babies")

class ProcurementItem(Base):
    __tablename__ = 'procurement_item'
    id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String)
    price = Column(Float)
    is_resold_to_babies = Column(Boolean, default=False)
    sold_to_babies = Column(Integer, ForeignKey('baby.id'))

Base.metadata.create_all(engine)
# Base.metadata.drop_all(engine)

