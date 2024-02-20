from fastapi import APIRouter, Depends

from app import dependencies
from app.dependencies import UserDep

def tocken_dep(token: UserDep):
    pass

router =  APIRouter(
    dependencies=[Depends(tocken_dep)]
)

# create faction
# delete faction
# update faction
# get facion list
