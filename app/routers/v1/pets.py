import logging
from typing import Optional

from fastapi import APIRouter, Query

from app.models.pets import Pet

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/pets",
    tags=["pets"],
)


@router.get("")
async def get_pets(
    age: Optional[int] = Query(
        default=None,
        title="Pet age",
        description="Age of the pet to filter by",
    ),
    type: Optional[str] = Query(
        default=None,
        title="Pet type",
        description="Type of the pet to filter by",
    ),
):
    """
    Get all pets
    """
    logger.info("User fetched pets")
    logger.info("Fetching all pets from the database")
    pets = [
        Pet(id=1, name="Bruno", age=5, type="Dog"),
        Pet(
            id=2,
            name="Giacomino, guardiano delle galassie e dell'iperspazio",
            age=3,
            type="Cat",
        ),
        Pet(id=3, name="Nemo", age=2, type="Fish"),
        Pet(id=4, name="Brave, the cowardly dog", age=3, type="Dog"),
        Pet(id=5, name="Scoobert Doobert", age=2, type="Dog"),
    ]
    logger.info(f"Got {len(pets)} records from the database")
    logger.info("Filtering pets.")
    if type:
        pets = [pet for pet in pets if pet.type == type]
        logger.info(f"Filtered by type: {type}")
    elif age:
        pets = [pet for pet in pets if pet.age == age]
        logger.info(f"Filtered by age: {age}")
    return {"pets": pets}


@router.post("")
async def add_pet(pet: Pet):
    """
    Add a new pet
    """
    # There is an intentional runtime error here
    logger.info("User added a new pet")
    logger.info(f"Adding {pet} to the database")
    pet_dict = pet.model_dump()
    logger.info(f"Pet vaccination status: {pet_dict['vaccinated']}")

    return {"message": "Pet added successfully", "pet": pet}
