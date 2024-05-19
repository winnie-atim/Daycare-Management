from Models.models import Admin, AdminSignUpToken
from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from Connections.connections import session
from Connections.tokens_and_keys import (
    EMAIL,
    EMAIL_PASSWORD
)
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

    # firebase_url = 'https://firebasestorage.googleapis.com/v0/b/bfamproject-80d95.appspot.com/o/prod%2Fproducts%2F1705940735027_gen_visual.jpeg?alt=media&token=de7a990b-2238-455f-a6d2-1f0ba71f55d2'

    # response = requests.get(firebase_url)
    # if response.status_code == 200:
    #     img_data = response.content
    #     img = MIMEImage(img_data)
    #     img.add_header('Content-ID', '<company_logo>')
    #     msg.attach(img)
    # else:
    #     print("Failed to retrieve image from Firebase")

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
    # print("""Validating token""")
    # email = admin["email"]
    # signup_token = admin["token"]

    # try:
    #     if not AdminSignUpToken.validate_token(db_session, email, signup_token):
    #         raise Exception("Invalid token")
    # except Exception as e:
    #     print(f"Error occurred during token validation: {e}")
    #     return {"message": str(e), "status": 400}  
    
    # admin.pop("token", None)
    
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