# """User REST Controller"""
#
# from typing import Annotated, List
#
# from fastapi import APIRouter, Query, UploadFile, Form, Depends
# from fastapi.security import OAuth2PasswordRequestForm
# from starlette.responses import StreamingResponse
#
# from src.main.app.core.context.contextvars import current_user_id
# from src.main.app.core.schema import HttpResponse, Token, CurrentUser
# from src.main.app.core.schema import PageResult
# from src.main.app.core.security import get_current_user
# from src.main.app.core.utils import excel_util
# from src.main.app.core.utils.tree_util import list_to_tree
# from src.main.app.mapper.sys_menu_mapper import menuMapper
# from src.main.app.mapper.sys_user_mapper import userMapper
# from src.main.app.model.sys_user_model import UserModel
# from src.main.app.schema.sys_menu_schema import Menu
# from src.main.app.schema.sys_user_schema import (
#     UserQuery,
#     UserModify,
#     CreateUserRequest,
#     UserBatchModify,
#     UserDetail,
#     LoginForm,
#     UserPage,
#     UserInfo,
# )
# from src.main.app.service.impl.sys_menu_service_impl import MenuServiceImpl
# from src.main.app.service.impl.sys_user_service_impl import UserServiceImpl
# from src.main.app.service.sys_menu_service import MenuService
# from src.main.app.service.sys_user_service import UserService
#
# user_router = APIRouter()
# user_service: UserService = UserServiceImpl(mapper=userMapper)
# menu_service: MenuService = MenuServiceImpl(mapper=menuMapper)
#
#
# @user_router.post("")
# async def create_user(
#     req: CreateUserRequest,
# ) -> UserModel:
#     """
#     Create a new user
#
#     Args:
#         req: Request object containing user creation data
#
#     Returns:
#          UserModel: The newly created user object
#
#     Raises:
#         HttpException(409 Conflict): If the creation data already exists.
#         HttpException(403 Forbidden): If the current user don't have access rights.
#     """
#     user: UserModel = await user_service.create_user(
#         create_user=req,
#     )
#     result = user.copy()
#     result.password = None
#     return result
#
# @user_router.get("/menus")
# async def get_menus(current_user: CurrentUser = Depends(get_current_user())):
#     records, _ = await menu_service.retrieve_ordered_data_list(
#         current=1, page_size=1000
#     )
#     records = [Menu(**record.model_dump()) for record in records]
#     records = [record.model_dump() for record in records if record.visible == 1]
#     records.sort(key=lambda x: x["sort"])
#     result = list_to_tree(records)
#     return HttpResponse(data=result)
#
#
# @user_router.post("/login")
# async def login(
#     login_form_data: OAuth2PasswordRequestForm = Depends(),
# ) -> Token:
#     """
#     Authenticates user and provides an access token.
#
#     Args:
#         login_form_data: Login credentials.
#
#     Returns:
#         Token object with access token.
#     """
#     login_form = LoginForm(
#         username=login_form_data.username, password=login_form_data.password
#     )
#
#     return await user_service.login(login_form=login_form)
#
#
# @user_router.get("/me")
# async def get_me_info(
#     current_user: CurrentUser = Depends(get_current_user()),
# ) -> HttpResponse[UserInfo]:
#     """
#     Retrieves the profile of the current user.
#
#     Args:
#         current_user: Currently authenticated user.
#
#     Returns:
#         BaseResponse with current user's profile information.
#     """
#     user_id = current_user.user_id
#     user_page: UserPage = await user_service.find_by_id(id=user_id)
#     roles, role_models = await user_service.get_roles(id=user_id)
#     menus: list[Menu] = await user_service.get_menus(
#         id=user_id, role_models=role_models
#     )
#     if UserInfo.is_admin(user_id):
#         permissions = ["*.*.*"]
#     else:
#         permission_list = [menu.permission for menu in menus]
#         permissions = [
#             permission for permission in permission_list if permission
#         ]
#     user_info = UserInfo(
#         **user_page.model_dump(),
#         permissions=permissions,
#         roles=roles,
#         menus=menus,
#     )
#     return HttpResponse.success(user_info)
#
#
# @user_router.get("/page")
# async def get_user_by_page(
#     user_query: Annotated[UserQuery, Query()],
#     current_user: CurrentUser = Depends(get_current_user()),
# ) -> HttpResponse[PageResult]:
#     user_page_result: PageResult = await user_service.get_user_by_page(
#         user_query=user_query, current_user=current_user
#     )
#     return HttpResponse.success(user_page_result)
#
#
# @user_router.get("/detail/{id}")
# async def get_user_detail(
#     id: int, current_user: CurrentUser = Depends(get_current_user())
# ) -> HttpResponse[UserDetail]:
#     user_detail: UserDetail = await user_service.get_user_detail(
#         id=id, current_user=current_user
#     )
#     return HttpResponse.success(user_detail)
#
#
# @user_router.get("/export-template")
# async def export_template(
#     current_user: CurrentUser = Depends(get_current_user()),
# ) -> StreamingResponse:
#     return await excel_util.export_excel(
#         schema=CreateUserRequest, file_name="user_import_tpl"
#     )
#
#
# @user_router.get("/export")
# async def export_user_page(
#     current_user: CurrentUser = Depends(get_current_user()),
#     ids: list[int] = Query(...),
# ) -> StreamingResponse:
#     return await user_service.export_user_page(
#         ids=ids, current_user=current_user
#     )
#
#
#
# @user_router.post("/batch-create")
# async def batch_create_user(
#     user_create_list: list[CreateUserRequest],
#     current_user: CurrentUser = Depends(get_current_user()),
# ) -> HttpResponse[list[int]]:
#     ids: list[int] = await user_service.batch_create_user(
#         user_create_list=user_create_list, current_user=current_user
#     )
#     return HttpResponse.success(ids)
#
#
# @user_router.post("/import")
# async def import_user(
#     current_user: CurrentUser = Depends(get_current_user()),
#     file: UploadFile = Form(),
# ) -> HttpResponse[list[CreateUserRequest]]:
#     user_create_list: list[CreateUserRequest] = await user_service.import_user(
#         file=file, current_user=current_user
#     )
#     return HttpResponse.success(user_create_list)
#
#
# @user_router.delete("/remove/{id}")
# async def remove(
#     id: int, current_user: CurrentUser = Depends(get_current_user())
# ) -> HttpResponse:
#     await user_service.remove_by_id(id=id)
#     return HttpResponse.success()
#
#
# @user_router.delete("/batch-remove")
# async def batch_remove(
#     current_user: CurrentUser = Depends(get_current_user()),
#     ids: list[int] = Query(...),
# ) -> HttpResponse:
#     await user_service.batch_remove_by_ids(ids=ids)
#     return HttpResponse.success()
#
#
# @user_router.put("/modify")
# async def modify(
#     user_modify: UserModify,
#     current_user: CurrentUser = Depends(get_current_user()),
# ) -> HttpResponse:
#     await user_service.modify_by_id(
#         data=UserModel(**user_modify.model_dump(exclude_unset=True))
#     )
#     return HttpResponse.success()
#
#
# @user_router.put("/batch-modify")
# async def batch_modify(
#     user_batch_modify: UserBatchModify,
#     current_user: CurrentUser = Depends(get_current_user()),
# ) -> HttpResponse:
#     cleaned_data = {
#         k: v
#         for k, v in user_batch_modify.model_dump().items()
#         if v is not None and k != "ids"
#     }
#     await user_service.batch_modify_by_ids(
#         ids=user_batch_modify.ids, data=cleaned_data
#     )
#     return HttpResponse.success()
