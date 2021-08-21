"""
ENTITY MODELS HERE
"""


from pydantic import BaseModel
from fastapi import Request


class UserCreateModel(BaseModel):
    identifier: str
    password: str
    email: str
    firstname: str
    lastname: str
    fullname: str


class UserAuthModel(BaseModel):
    identifier: str
    password: str


class ChangePasswordModel(BaseModel):
    identifier: str
    password: str
    confirmPassword: str
    newPassword: str


class VerificationModel(BaseModel):
    callback_url: str


class UpdateNameModel(BaseModel):
    firstname: str
    lastname: str
    fullname: str = ""


class VerifyModel(BaseModel):
    code: str


class TokenModel(BaseModel):
    token: str
