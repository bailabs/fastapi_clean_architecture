from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from domain.usecases.AuthenticationUsecase import AuthenticationUsecase
from data.utils.bearer import JWTBearer
from domain.entities.user import (
    UserCreateModel,
    UserAuthModel,
    ChangePasswordModel,
    UpdateNameModel,
    VerificationModel,
    VerifyModel,
)

# Models

public = APIRouter()
protected = APIRouter(dependencies=[Depends(JWTBearer())])
auth = AuthenticationUsecase()

templates = Jinja2Templates(directory="public/templates")


@public.post("/register")
def create_user(request: Request, params: UserCreateModel):
    return auth.register(request, params, templates)


@public.post("/login")
def login(params: UserAuthModel):
    return auth.auth(params)


@protected.post("/logout")
def logout(request: Request):
    return auth.logout(request)


@protected.post("/change_password")
def change_password(params: ChangePasswordModel):
    return auth.change_password(params)


@protected.post("/get_user_info")
def get_user_info(request: Request):
    return auth.get_user(request)


@protected.post("/update_name")
def update_name(request: Request, params: UpdateNameModel):
    return auth.update_name(request, params)


# @protected.post("/send_verification")
# def send_verification(request: Request, params: VerificationModel):
#     return auth.send_verification(request, params)
#
#
# @protected.post("/verify")
# def verify(request: Request, params: VerifyModel):
#     return auth.verify(request, params)
