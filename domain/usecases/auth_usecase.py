"""
USE CASES HERE

"""
import os
import binascii
from fastapi import Request
from fastapi.security.utils import get_authorization_scheme_param
from data.repositories.auth_repository import SqlAlchemyRepoImpl
from domain.entities.user import ChangePasswordModel, UserAuthModel, UserCreateModel, VerificationModel, VerifyModel, \
    UpdateNameModel
from domain.repositories.auth_repositories import AuthenticationRepo
from app.boot.tables import BlackListedAuthToken
from data.utils.jwt_handler import decode_jwt


class AuthenticationUsecase(AuthenticationRepo):
    def __init__(self, auth=SqlAlchemyRepoImpl()):
        self.authentication_repository = auth
        pass

    def auth(self, params: UserAuthModel):
        return self.authentication_repository.auth(params)

    def register(self, request: Request, params: UserCreateModel, templates):
        if params.password and params.identifier:
            params.fullname = str(params.firstname) + " " + str(params.lastname)
            return self.authentication_repository.register(params)
        else:
            return templates.TemplateResponse("404.html", {"request": request})

    def logout(self, request: Request):
        _, credentials = get_authorization_scheme_param(request.headers.get("authorization"))
        new_blacklist = BlackListedAuthToken(auth_token=credentials)
        return self.authentication_repository.logout(new_blacklist)

    def change_password(self, params: ChangePasswordModel):
        if params.password == params.confirmPassword and params.newPassword and params.identifier:
            return self.authentication_repository.change_password(params)
        else:
            return {'success': False}

    def get_user(self, request: Request):
        _, credentials = get_authorization_scheme_param(request.headers.get("authorization"))
        decoded = decode_jwt(credentials)
        user_id = decoded['user_id']
        return self.authentication_repository.get_user(user_id)

    def update_name(self, request: Request, params: UpdateNameModel):
        if params.firstname and params.lastname:
            _, credentials = get_authorization_scheme_param(request.headers.get("authorization"))
            decoded = decode_jwt(credentials)
            user_id = decoded['user_id']
            params.firstname = params.firstname.title()
            params.lastname = params.lastname.title()
            params.fullname = params.firstname.title() + " " + params.lastname.title()
            return self.authentication_repository.update_name(user_id, params)

    def send_verification(self, request: Request, user_id: str, code: any, params: VerificationModel):
        _, credentials = get_authorization_scheme_param(request.headers.get("authorization"))
        decoded = decode_jwt(credentials)
        user_id = decoded['user_id']
        salt = os.urandom(32)
        code = binascii.hexlify(salt).decode()
        return self.authentication_repository.send_verification(request, user_id, code, params)

    def verify(self, request: Request, params: VerifyModel):
        _, credentials = get_authorization_scheme_param(request.headers.get("authorization"))
        decoded = decode_jwt(credentials)
        user_id = decoded['user_id']
        return self.authentication_repository.verify(user_id, params)
