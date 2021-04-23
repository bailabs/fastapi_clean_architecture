"""
ABSTRACT CLASSES HERE
"""
from domain.entities.user import ChangePasswordModel, UserAuthModel, UserCreateModel, VerificationModel, VerifyModel, \
    UpdateNameModel
from fastapi import Request


class AuthenticationRepo:
    def auth(self, params: UserAuthModel) -> object:
        """
        Used to login user
        @parameters:
        identifer: str
        password: str
        """
        pass

    def register(self, request: Request, params: UserCreateModel, templates) -> object:
        """
        Used to register user
        @parameters:
        identifer: str
        password: str
        email: str
        """
        pass

    def logout(self, request: Request) -> object:
        """
        Used to logout user [needs access_token]
        """
        pass

    def change_password(self, params: ChangePasswordModel) -> object:
        """
        Used to change user password
        @parameters:
        identifier: str
        password: str
        confirmPassword: str
        newPassword: str
        """
        pass

    def get_user(self, request: Request) -> object:
        """
        Used to get user information
        """
        pass

    def update_name(self, request: Request, params: UpdateNameModel) -> object:
        """
        Used to change user firstname and lastname
        @parameters
        firstname: str
        lastname: str
        """
        pass

    def send_verification(self, request: Request, params: VerificationModel) -> object:
        """
        Used to send email verification to user's email
        @parameters
        callback_url: str -> Url to display after button click
        """
        pass

    def verify(self, request: Request, params: VerifyModel) -> object:
        """
        Used to verify user
        @parameters
        code: str -> code from the email sent to user from using send_verification
        """
        pass
