import logging
from pathlib import Path

import aiofiles
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/docs", tags=["Docs"])
logger = logging.getLogger(__name__)

# Base path for rules directory (relative to this file)
BASE_DIR = Path(__file__).resolve().parent.parent  # points to backend/app
RULES_DIR = BASE_DIR / "rules"


@router.get("/rules/{game_type}")
async def get_rules(game_type: str):
    """
    Get the rules for a specific game.
    """

    # Sanitize input (only allow alphanumeric and underscores)
    if not game_type.isidentifier():
        raise HTTPException(status_code=400, detail="Invalid game type")

    file_path = RULES_DIR / f"{game_type}.md"

    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(
            status_code=404, detail="Rules not found for this game type."
        )

    try:
        async with aiofiles.open(file_path, encoding="utf-8") as f:
            content = await f.read()
        return {"rules": content}
    except Exception as e:
        logger.error(f"An unexpected error occurred in get_rules: {e}")
        raise HTTPException(
            status_code=500, detail="An internal error occurred."
        ) from e
