from Models.models import Admin, AdminSignUpToken, AdminResetToken
from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from Connections.connections import session
from Connections.tokens_and_keys import (
    EMAIL,
    EMAIL_PASSWORD
)
from datetime import datetime, timedelta
from hashing import Harsher
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib

async def generate_signup_token(email,adminid,role):
    try: 
        token_info = AdminSignUpToken.create_token(session, email, adminid) 
        if token_info:
            token = token_info['token'] 
            send_signup_token_email(email, token, role) 
            return token_info 
        else:

            raise Exception("Token not created")
    except Exception as e:
        session.rollback()
        print(f"Error occurred: {e}")
        return False
    
def send_signup_token_email(email, token, role):
    sender_email = EMAIL
    sender_password = EMAIL_PASSWORD

    base_url = "https://agrogetaway.vercel.app/signup"
    role_paths = {
        "Admin": "admin",
        "Agent": "agent",
        "ModelFarmer": "modelfarmer"
    }
    role_path = role_paths.get(role, "admin") 
    signup_url = f"{base_url}/{role_path}?token={token}"

    msg = MIMEMultipart('related')
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = f"{role} Signup Email!"

    html_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; color: #333;">
                <p>Dear {role},</p>
                <br />
                Welcome to DayStar Daycare! Please use the button below to complete your signup process:
                <br /><br />
                <!- <a href="{signup_url}" style="background-color: #4CAF50; color: white; padding: 14px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px;">Complete Signup</a> ->
                <b> Sigup Token </b> : {token}
                <br /><br />
                <p>If you have any questions or require assistance, our support team is always here to help.</p>
                <p>Thank you for stepping into this vital role within DayStar Daycare. Together, we'll drive the future of our babies.</p>
                <p>Warm regards,</p>
                <p>The DayStar Team</p>
                <p><i>Note: This is an automated message, please do not reply to this email.</i></p>
            </body>
        </html>
                """

    msg.attach(MIMEText(html_body, 'html'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    try:
        server.login(sender_email, sender_password)
    except smtplib.SMTPAuthenticationError:
        print("SMTP Authentication Error: The username or password you entered is not correct.")
        return

    server.send_message(msg)
    server.quit()
    
async def create_admin_controller(db_session: Session, admin: dict):
    print("""Validating token""")
    email = admin["email"]
    signup_token = admin["token"]

    try:
        if not AdminSignUpToken.validate_token(db_session, email, signup_token):
            raise HTTPException(status_code=400, detail="Invalid token")
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error occurred during token validation: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    
    admin.pop("token", None)
    
    print("""Creating admin""")
    new_admin = Admin(**admin)
    new_admin.password = Harsher.get_hash_password(new_admin.password)
    db_session.add(new_admin)
    db_session.commit()
    db_session.refresh(new_admin)
    
    return {
        "message": "Admin created successfully",
        "status_code": 200,
        "data": {
            "admin_id": new_admin.id,
            "fastname": new_admin.firstname,
            "email": new_admin.email
        }
    }


async def login_admin(db_session: Session, admin_credentials):
    email = admin_credentials["email"]
    password = admin_credentials["password"]
    admin = db_session.query(Admin).filter(Admin.email == email).first()
    if admin is None:
        raise HTTPException(status_code=404, detail="Admin not found")
    
    else: 
        if Harsher.verify_password(password, admin.password):
            return {
                "message": "Admin logged in successfully",
                "status_code": 200,
                "data": {
                    "admin_id": admin.id,
                    "name": admin.firstname,
                    "email": admin.email,
                    "role": admin.role
                }
            }
        else:
            raise HTTPException(status_code=401, detail="Invalid password")
        
async def generate_reset_token(db: Session, email: str):
    try:
        admin = db.query(Admin).filter(Admin.email == email).first()
        if not admin:
            raise Exception("Email not found")

        token = AdminResetToken.create_or_update_token(db, email, admin.id)
        if token:
            send_reset_email(email, token)
            return True
        else:
            raise Exception("Token not created")
    except Exception as e:
        db.rollback()
        print(f"Error occurred: {e}")
        return False

def send_reset_email(email: str, token: str):
    msg = MIMEMultipart()
    msg['From'] = EMAIL
    msg['To'] = email
    msg['Subject'] = "Password Reset Request"
    
    body = f"""
    <html>
        <body style="font-family: Arial, sans-serif; color: #333;">
            <p>Dear User,</p>
            <p>Click on the button below to reset your password:</p>
            <a href="https://daycare-management.vercel.app/html/changePassword.html?token={token}" style="display: inline-block; padding: 10px 20px; font-size: 16px; color: white; background-color: #4CAF50; text-align: center; text-decoration: none; border-radius: 5px;">Reset Password</a>
            <p>If you have any questions or require assistance, our support team is always here to help.</p>
            <p>Thank you for stepping into this vital role within DayStar Daycare. Together, we'll drive the future of our babies.</p>
            <p>Warm regards,</p>
            <p>The DayStar Team</p>
            <p><i>Note: This is an automated message, please do not reply to this email.</i></p>
        </body>
    </html>
    """
    
    msg.attach(MIMEText(body, 'html'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(EMAIL, EMAIL_PASSWORD)
    text = msg.as_string()
    server.sendmail(EMAIL, email, text)
    server.quit()

    
def reset_password(db: Session, token: str, new_password: str):
    try:
        valid_token = validate_reset_token(db, token)
        if not valid_token:
            raise HTTPException(status_code=400, detail="Invalid or expired token")

        admin = db.query(Admin).filter_by(email=valid_token.email).first()
        if not admin:
            raise HTTPException(status_code=404, detail="User not found")

        admin.password = Harsher.get_hash_password(new_password)
        valid_token.status = "True"  # Mark token as used
        db.commit()
        return {"message": "Password reset successfully", "status_code": 200}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

def validate_reset_token(db: Session, token: str):
    try:
        token_record = db.query(AdminResetToken).filter(
            AdminResetToken.token == token,
            AdminResetToken.status == "False"
        ).first()

        if token_record:
            token_validity_period = timedelta(hours=24)
            token_age = datetime.now() - token_record.created_at

            if token_age <= token_validity_period:
                return token_record
            else:
                print(f"Token {token} has expired.")
                return None
        else:
            print(f"No valid token found for token {token}.")
            return None
    except Exception as e:
        print(f"Exception during token validation for token {token}: {e}")
        return None
