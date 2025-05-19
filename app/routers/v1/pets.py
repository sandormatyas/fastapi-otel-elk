import logging

from fastapi import APIRouter
from app.models.pets import Pet

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
    pets = [
        Pet(id=1, name="Bruno", age=5, type="Dog"),
        Pet(
            id=2,
            name="Giacomino, guardiano delle galassie e dell'iperspazio",
            age=3,
            type="Cat",
        ),
        Pet(id=3, name="Nemo", age=2, type="Fish"),
    ]
    logger.info("User fetched all pets")
    logger.info("Fetching all pets from the database")
    logger.info(f"Got {len(pets)} records from the database")
    return {"pets": pets}


@router.post("")
async def add_pet(pet: Pet):
    """
    Add a new pet
    """
    # There is an intentional runtime error here
    logger.info("User added a new pet")
    logger.info(f"Adding {pet} to the database")
    logger.info(f"Pet vaccination status: {pet.vaccinated}")

    return {"message": "Pet added successfully", "pet": pet}
