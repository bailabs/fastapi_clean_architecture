"""
ABSTRACT CLASSES HERE
"""
from domain.entities.user import ChangePasswordModel, UserAuthModel, UserCreateModel, VerificationModel, VerifyModel, \
    UpdateNameModel
from fastapi import Request
from abc import ABC, abstractmethod


class AuthenticationRepo(ABC):
    @abstractmethod
    def auth(self, params: UserAuthModel) -> object:
        """
        Used to login user
        @parameters:
        identifer: str
        password: str
        """
        pass

    @abstractmethod
    def register(self, request: Request, params: UserCreateModel, templates: any) -> object:
        """
        Used to register user
        @parameters:
        identifer: str
        password: str
        email: str
        """
        pass

    @abstractmethod
    def logout(self, request: Request) -> object:
        """
        Used to logout user [needs access_token]
        """
        pass

    @abstractmethod
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

    @abstractmethod
    def get_user(self, request: Request) -> object:
        """
        Used to get user information
        """
        pass

    @abstractmethod
    def update_name(self, request: Request, params: UpdateNameModel) -> object:
        """
        Used to change user firstname and lastname
        @parameters
        firstname: str
        lastname: str
        """
        pass

    @abstractmethod
    def send_verification(self, request: Request, user_id: str, code: any, params: VerificationModel) -> object:
        """
        Used to send email verification to user's email
        @parameters
        callback_url: str -> Url to display after button click
        """
        pass

    @abstractmethod
    def verify(self, request: Request, params: VerifyModel) -> object:
        """
        Used to verify user
        @parameters
        code: str -> code from the email sent to user from using send_verification
        """
        pass
