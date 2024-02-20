from fastapi import APIRouter, Depends

from app.dependencies import UserDep


def tocken_dep(_: UserDep):
    pass


router = APIRouter(
    dependencies=[Depends(tocken_dep)]
)


# post player
# get players
# delete player
# update player

