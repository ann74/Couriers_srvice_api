from fastapi import APIRouter, Depends
from starlette import status

from app.database.database import Paginator, get_async_session
from app.order.schemas import CreateOrderRequest

router = APIRouter(
    prefix="/orders",
    tags=["order-controller"],
    # dependencies=[Depends(get_token_header)],
    responses={400: {"description": "bad request"}},
)


@router.get('', status_code=status.HTTP_200_OK)
async def get_orders(pagination_params: Paginator = Depends()):
    pass


@router.post('')
async def create_orders(orders: CreateOrderRequest):
    pass
