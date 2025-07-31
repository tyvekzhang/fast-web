from datetime import datetime
from enum import Enum
from functools import wraps
from typing import Optional

from fastapi import HTTPException, Request
from pydantic import BaseModel

from src.main.app.core.context.contextvars import current_user_id
from src.main.app.core.service.permission_service import ss


def pre_authorize(permission: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user_id = current_user_id.get()

            if not await ss.check_operation_permission(user_id, permission):
                raise HTTPException(status_code=403, detail="No operation permission")

            return await func(*args, **kwargs)

        return wrapper

    return decorator


# 业务类型枚举 (对应Java的BusinessType)
class BusinessType(str, Enum):
    INSERT = "INSERT"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    GRANT = "GRANT"
    EXPORT = "EXPORT"
    IMPORT = "IMPORT"


# 操作日志模型
class OperLog(BaseModel):
    title: str  # 操作模块
    business_type: BusinessType  # 业务类型
    operator: str  # 操作人员（从token获取）
    oper_ip: str  # 操作IP
    oper_time: datetime  # 操作时间
    status: bool  # 操作状态
    params: Optional[dict] = None  # 请求参数
    result: Optional[str] = None  # 返回结果


def log(title: str, business_type: BusinessType):
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            # 1. 获取操作人信息（需根据实际token解析逻辑调整）
            current_user = None

            # 2. 记录请求参数（过滤敏感信息）
            params = {
                "path_params": request.path_params,
                "query_params": dict(request.query_params),
                # 如果是POST/PUT可以记录body（需根据实际需求调整）
            }

            # 3. 执行被装饰的方法
            try:
                result = await func(*args, **kwargs)
                status = True
            except Exception as e:
                status = False
                raise e
            finally:
                # 4. 异步记录日志（实际存储到数据库）
                log_data = OperLog(
                    title=title,
                    business_type=business_type,
                    operator=current_user.username,
                    oper_ip=request.client.host,
                    oper_time=datetime.utcnow(),
                    status=status,
                    params=params,
                    result=str(result) if status else None,
                )
                # 异步写入数据库（使用celery/background tasks）
                print(log_data)

            return result

        return wrapper

    return decorator
