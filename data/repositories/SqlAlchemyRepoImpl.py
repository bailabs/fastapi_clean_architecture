import os
import hashlib
from app.boot.engine import SessionLocal
from data.utils.jwt_handler import sign_jwt
from sqlalchemy.exc import SQLAlchemyError
from fastapi import Request

# PARAMS MODELS
from domain.entities.user import (
    ChangePasswordModel,
    UserAuthModel,
    UserCreateModel,
    VerificationModel,
    VerifyModel,
    UpdateNameModel,
)

# DB MODELS
from app.boot.tables import User
from app.boot.tables import UserInfo

# Mailer
from data.utils.elasticemail import send_email
from data.utils.response_object import ResponseObject as Response
from domain.repositories.AuthenticationRepo import AuthenticationRepo


class SqlAlchemyRepoImpl(AuthenticationRepo):
    def __init__(self):
        self.session = SessionLocal()
        pass

    def auth(self, params: UserAuthModel):
        user = (
            self.session.query(User)
            .filter_by(identifier=params.identifier)
            .first()
        )
        if user:
            salt = user.salt
            key = user.key
            to_compare = hashlib.pbkdf2_hmac(
                "sha256",
                params.password.encode("utf-8"),
                salt,
                100000,
                dklen=128,
            )
            if to_compare == key:
                return Response.success(access_token=sign_jwt(user.id))

        return Response.failure(status_code=403, message="Invalid Login")

    def register(self, params: UserCreateModel):
        self.session = SessionLocal()
        try:
            salt = os.urandom(32)
            key = hashlib.pbkdf2_hmac(
                "sha256",
                params.password.encode("utf-8"),
                salt,
                100000,
                dklen=128,
            )

            new_user = User(
                identifier=params.identifier,
                email=params.email,
                salt=salt,
                key=key,
            )

            self.session.add(new_user)
            self.session.flush()

        except SQLAlchemyError as e:
            error = str(e.__dict__["orig"])
            if "UNIQUE" in error:
                return Response.failure(error="User already exists")
            return Response.failure(error=str(e))

        user_info = UserInfo(
            firstname=params.firstname,
            lastname=params.lastname,
            user_id=new_user.id,
            fullname=params.fullname,
        )
        self.session.add(user_info)
        self.session.commit()
        return Response.success()

    def logout(self, new_blacklist):
        self.session = SessionLocal()
        self.session.add(new_blacklist)
        self.session.commit()
        return Response.success()

    def change_password(self, params: ChangePasswordModel):
        self.session = SessionLocal()
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac(
            "sha256",
            params.newPassword.encode("utf-8"),
            salt,
            100000,
            dklen=128,
        )
        user = (
            self.session.query(User)
            .filter_by(identifier=params.identifier)
            .first()
        )
        if user:
            user.salt = salt
            user.key = key
            self.session.commit()
            return Response.success()
        else:
            return Response.failure(error="User not found")

    def get_user(self, user_id: str):
        self.session = SessionLocal()

        user = self.session.query(User).filter_by(id=user_id).first()
        userExtraInfo = (
            self.session.query(UserInfo).filter_by(user_id=user_id).first()
        )

        return Response.success(
            id=user.id,
            identifier=user.identifier,
            is_verified=user.is_verified,
            is_active=user.is_active,
            email=user.email,
            fullname=userExtraInfo.fullname,
            firstname=userExtraInfo.firstname,
            lastname=userExtraInfo.lastname,
            description=userExtraInfo.description,
        )

    def update_name(self, user_id: str, params: UpdateNameModel):
        self.session = SessionLocal()
        userInfo = self.session.query(UserInfo).filter_by(id=user_id).first()
        userInfo.firstname = params.firstname
        userInfo.lastname = params.lastname
        userInfo.fullname = params.fullname
        self.session.commit()
        return Response.success()

    # def send_verification(
    #     self, request, user_id: str, code: any, params: VerificationModel
    # ):
    #     self.session = SessionLocal()
    #     user = self.session.query(User).filter_by(id=user_id).first()
    #
    #     user.verification_code = code
    #     self.session.commit()
    #     callback = params.callback_url + "?code=" + code
    #
    #     if user.is_verified:
    #         return Response.failure(error="User already verified")
    #
    #     with open("../utils/verification_email.html", "r") as file:
    #         verification_email = file.read().replace("\n", "")
    #
    #     verification_email = verification_email.replace(
    #         "THECALLBACKURL", callback
    #     )
    #     if user.email:
    #         send_email(
    #             user.email,
    #             "Company Verification Email",
    #             verification_email,
    #             verification_email,
    #             "admin@email.test",
    #             "My Company",
    #             "admin@email.test",
    #             "Do not reply",
    #             "My Company",
    #         )
    #     else:
    #         return Response.failure(error="No email found")
    #     return Response.success()
    #
    # def verify(self, user_id: str, params: VerifyModel):
    #     self.session = SessionLocal()
    #     user = self.session.query(User).filter_by(id=user_id).first()
    #     if user.verification_code == params.code:
    #         user.is_verified = 1
    #         self.session.commit()
    #         return Response.success()
    #
    #     return Response.failure()
