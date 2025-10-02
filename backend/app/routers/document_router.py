import logging
import os

import aiofiles
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/docs", tags=["Docs"])
logger = logging.getLogger(__name__)


@router.get("/rules/{game_type}")
async def get_rules(game_type: str):
    """
    Get the rules for a specific game.
    """
    rules_directory = "backend/app/rules"
    file_path = os.path.join(rules_directory, f"{game_type}.md")

    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404, detail="Rules not found for this game type."
        )

    try:
        async with aiofiles.open(file_path) as f:
            content = await f.read()
        return {"game_type": game_type, "rules": content}
    except Exception as e:
        logger.error(f"An unexpected error occurred in get_rules: {e}")
        raise HTTPException(
            status_code=500, detail="An internal error occurred."
        ) from e
