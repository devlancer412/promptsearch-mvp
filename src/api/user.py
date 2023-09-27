from __future__ import annotations
from typing import Callable, List, Annotated
from app.__internal import Function
from fastapi import (
    FastAPI,
    APIRouter,
    status,
    HTTPException,
    Depends,
    Query,
    Path
)
from sqlalchemy.orm import Session
from operator import and_


from src.schemas.user import UserBase, UserRegister
from src.models import User
from src.deps.database import get_db_session

from src.ml.user import upset_user


class UserAPI(Function):
    def __init__(self, error: Callable):
        self.log.info("This is where the initialization code go")

    def Bootstrap(self, app: FastAPI):
        router = APIRouter(
            prefix="/user",
            tags=["user"],
            responses={404: {"description": "Not found"}},
        )

        # @router.get("/", summary="get current user's users")
        # async def get_user_user(
        #     offset: int = Query(
        #         default=0, description="offset for pagination"),
        #     limit: int = Query(
        #         default=10, description="limit for pagination"),
        #     payload: TokenPayload = Depends(
        #         get_current_user_from_oauth),
        #     session: Session = Depends(get_db_session),
        # ):
        #     users: List[User] = (
        #         session.query(User)
        #         .filter(User.user_id == int(payload.sub)).offset(offset).limit(limit)
        #         .all()
        #     )

        #     return users

        @router.get("/list", summary="get all users")
        async def get_all_user(
            offset: int = Query(
                default=0, description="offset for pagination"),
            limit: int = Query(
                default=10, description="limit for pagination"),
            session: Session = Depends(get_db_session),
        ):
            users: List[User] = (
                session.query(User).offset(offset).limit(limit).all()
            )

            return users

        @router.get("/{id}", summary="get a user")
        async def get_user(
            id: int = Annotated[int, Path(title="The ID of the user to get", ge=1)],
            session: Session = Depends(get_db_session),
        ):
            user: User = (
                session.query(User).filter(User.id == id).first()
            )

            if user is None:
                raise HTTPException(status.HTTP_404_NOT_FOUND,
                                    detail="Can't find such user")

            return user

        @router.post("/", summary="create a user")
        async def create_user(
            data: UserBase,
            session: Session = Depends(get_db_session),
        ):
            user = User()
            user.name = data.name
            user.email = data.email
            user.skills = data.skills.replace(",", " ")

            session.add(user)
            session.flush()
            session.commit()
            session.refresh(user, attribute_names=["id", "name", "email", "skills"])

            upset_user(user)

            return user

        @router.put("/{id}", summary="update a user")
        async def update_user(
            data: UserBase,
            id: int = Annotated[int, Path(title="The ID of the user to update", ge=1)],
            session: Session = Depends(get_db_session),
        ):
            user: User = session.query(User).filter(User.id == id).first()

            if user is None:
                raise HTTPException(status.HTTP_404_NOT_FOUND,
                                    detail="Can't find such user")

            if data.name != None:
                user.name = data.name
            if data.email != None:
                user.email = data.email
            if data.skills != None:
                user.skills = data.skills

            session.commit()
            session.refresh(user, attribute_names=["id", "name", "email", "skills"])

            upset_user(user)

            return user

        @router.delete("/{id}", summary="delete user")
        async def delete(
            id: int = Annotated[int, Path(title="The ID of the user to delete", ge=1)],
            session: Session = Depends(get_db_session),
        ):
            user: user = (
                session.query(User)
                .filter(User.id == int(id))
                .first()
            )

            if user is None:
                raise HTTPException(status.HTTP_404_NOT_FOUND,
                                    detail="Can't find such user")

            session.delete(user)
            session.flush()
            session.commit()

            return {
                "success": True
            }

        app.include_router(router)