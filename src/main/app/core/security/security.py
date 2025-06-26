# Copyright (c) 2025 Fast web and/or its affiliates. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Authentication utilities for FastAPI application."""

from functools import wraps
from datetime import datetime, timedelta
from typing import Any, Optional, Callable, Union

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext

from src.main.app.core.config.config_manager import load_config
from src.main.app.core.schema import CurrentUser

# Configuration
config = load_config()
security_config = config.security
server_config = config.server

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def decode_jwt_token(token: str) -> dict[str, Any]:
    """Decode and validate JWT token.

    Args:
        token: JWT token string

    Returns:
        Decoded token payload

    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        return jwt.decode(
            token,
            security_config.secret_key,
            algorithms=[security_config.algorithm],
        )
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token has expired. Please log in again.",
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials.",
        )


def get_oauth2_scheme() -> OAuth2PasswordBearer:
    oauth2_scheme = OAuth2PasswordBearer(
        tokenUrl=f"{server_config.api_version}/user/login"
    )
    return oauth2_scheme


def get_current_user() -> Callable[[], CurrentUser]:
    """
    Acquire current info through access_token

    Returns:
        CurrentUser instance
    """

    def current_user(
        access_token: str = Depends(get_oauth2_scheme()),
    ) -> CurrentUser:
        security = load_config().security
        if not security.enable:
            user_id = 1
            return CurrentUser(user_id=user_id)
        try:
            user_id = get_user_id(access_token)
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Your token has expired. Please log in again.",
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Error when decoding the token. Please check your request.",
            )

        return CurrentUser(user_id=user_id)

    return current_user


def create_token(
    subject: Optional[Union[str, int]] = None,
    expires_delta: Optional[timedelta] = None,
    token_type: Optional[str] = None,
) -> str:
    """Create new JWT token.

    Args:
        subject: Token subject (usually user ID)
        expires_delta: Optional timedelta for token expiration
        token_type: Token type identifier

    Returns:
        Encoded JWT string
    """
    expire = datetime.now() + (
        expires_delta
        or timedelta(minutes=security_config.refresh_token_expire_minutes)
    )
    to_encode = {"exp": expire, "sub": str(subject), "type": token_type}
    return jwt.encode(
        to_encode,
        security_config.secret_key,
        algorithm=security_config.algorithm,
    )


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hashed version.

    Args:
        plain_password: Input password
        hashed_password: Stored hashed password

    Returns:
        True if passwords match
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate password hash.

    Args:
        password: Plain text password

    Returns:
        Hashed password string
    """
    return pwd_context.hash(password)


def validate_token(token: str) -> bool:
    """Check if token is valid and not expired.

    Args:
        token: JWT token to validate

    Returns:
        True if token is valid

    Raises:
        HTTPException: If token is invalid
    """
    try:
        payload = decode_jwt_token(token)
        if datetime.fromtimestamp(payload["exp"]) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
            )
        return True
    except JWTError:
        return False


def get_user_id(token: str) -> int:
    """Extract user ID from JWT token.

    Args:
        token: JWT token string

    Returns:
        User ID extracted from the token

    Raises:
        HTTPException: If token is invalid or expired
    """
    payload = decode_jwt_token(token)
    return int(payload["sub"])


def role_required(required_role: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(current_user: CurrentUser, *args, **kwargs):
            # Get the current user
            user_id = current_user.user_id

            # Get user role info or permission info
            # if user.get("role") != required_role:
            #     raise HTTPException(
            #         status_code=status.HTTP_403_FORBIDDEN,
            #         detail=f"Requires {required_role} role"
            #     )
            # return await func(request, *args, **kwargs)

        return wrapper

    return decorator
