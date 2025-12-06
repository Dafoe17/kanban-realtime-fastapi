from uuid import UUID

from fastapi import HTTPException

from src.redis import TokenStorage
from src.repositories import UsersRepository
from src.schemas import UserRead, UsersListResponse


class UsersService:

    ALLOWED_SORT_FIELDS = {"username", "email"}

    @staticmethod
    def get_user(db, id: UUID) -> UserRead:
        user = UsersRepository.get_by_id(db, id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserRead.model_validate(user)

    @staticmethod
    def get_users(
        db,
        skip: int | None,
        limit: int | None,
        search: str | None,
        sort_by: str,
        order: str,
    ) -> UsersListResponse:

        if sort_by not in UsersService.ALLOWED_SORT_FIELDS:
            raise HTTPException(
                status_code=400, detail=f"Invalid sort field: {sort_by}"
            )

        filters = []

        if search:
            filters.append(UsersRepository.search(search))

        query = UsersRepository.apply_filters(db, filters)
        query = UsersRepository.apply_sorting(query, sort_by, order)
        total = UsersRepository.count(query)
        users = UsersRepository.paginate(query, skip, limit)

        response = UsersListResponse(
            total=total,
            skip=skip,
            limit=limit,
            users=[UserRead.model_validate(user) for user in users],
        )
        return response

    @staticmethod
    def patch_user(db, current_user, data) -> UserRead:
        if (
            data.email
            and UsersRepository.get_by_email(db, data.email)
            and current_user.email != data.email
        ):
            raise HTTPException(status_code=409, detail="Email already in use")

        user_dict = data.model_dump()
        try:
            user = UsersRepository.patch_user(db, current_user, user_dict)
            return UserRead.model_validate(user)
        except Exception as e:
            UsersRepository.rollback(db)
            raise HTTPException(500, f"Failed to patch user: {str(e)}")

    @staticmethod
    async def delete_user(db, current_user) -> UserRead:
        try:
            user = UsersRepository.delete_user(db, current_user)
            await TokenStorage.delete_token(current_user.id)
            return UserRead.model_validate(user)
        except Exception as e:
            UsersRepository.rollback(db)
            raise HTTPException(500, f"Failed to delete user: {str(e)}")
