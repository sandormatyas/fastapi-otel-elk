import logging

from fastapi import APIRouter, HTTPException

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/equipment",
    tags=["equipment"],
)


@router.get("")
async def get_equipment():
    """
    Get all equipment
    """
    logger.info("User fetched all equipment")
    # TODO: Implement this when the database is ready
    raise HTTPException(status_code=501, detail="Not implemented")
