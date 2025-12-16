from fastapi import APIRouter, Depends, HTTPException
from app.database.db import get_session
from sqlalchemy.ext.asyncio import AsyncSession

sessionDep: AsyncSession = Depends(get_session)
