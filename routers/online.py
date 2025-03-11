import logging
from fastapi import APIRouter, Depends, Request
from deps import verify_credentials

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.options("/online")
async def read_online(request: Request):
    print("Headers:", request.headers)
    print("Query Params:", request.query_params)
    print("Body:", await request.body())
    return {"status": "success", "message": "Online endpoint hit"}