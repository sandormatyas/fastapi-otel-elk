import logging

from fastapi import APIRouter

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/pets",
    tags=["pets"],
)


@router.get("")
async def get_pets():
    """
    Get all pets
    """
    logger.info("User fetched all pets")
    pets = [
        {"id": 1, "name": "Dog"},
        {"id": 2, "name": "Cat"},
        {"id": 3, "name": "Fish"},
    ]
    return {"pets": pets}
