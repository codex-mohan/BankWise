from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
import json
import os
import logging
from typing import Dict, Any, List

from mock_data_storage import mock_storage
from database import db_manager

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/dashboard", tags=["dashboard"])
templates = Jinja2Templates(directory="templates")


def get_mock_data(data_type: str, limit: int = 100) -> List[Dict[str, Any]]:
    """Get mock data with a limit on records"""
    data = []
    file_path = f"mock_data/{data_type}.json"
    
    if not os.path.exists(file_path):
        logger.warning(f"Mock data file not found: {file_path}")
        return []
    
    try:
        with open(file_path, "r") as f:
            content = f.read()
            # Parse the full JSON array
            full_data = json.loads(content)
            # Limit the results
            data = full_data[:limit] if isinstance(full_data, list) else []
            logger.info(f"Loaded {len(data)} {data_type} records from mock data")
            return data
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing JSON from {file_path}: {str(e)}")
        return []
    except Exception as e:
        logger.error(f"Error reading mock data: {str(e)}")
        return []


async def get_db_data(data_type: str, limit: int = 100) -> List[Dict[str, Any]]:
    """Get database data with a limit on records"""
    try:
        async with db_manager.get_connection() as conn:
            if conn:
                table_name = data_type
                # Check if table exists first
                table_exists = await conn.fetchval(
                    """
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables
                        WHERE table_schema = 'public'
                        AND table_name = $1
                    )
                """,
                    table_name
                )
                
                if not table_exists:
                    logger.warning(f"Table {table_name} does not exist in database")
                    return []
                
                query = f"SELECT * FROM {table_name} LIMIT {limit}"
                records = await conn.fetch(query)
                data = [dict(record) for record in records]
                logger.info(f"Loaded {len(data)} {data_type} records from database")
                return data
        return []
    except Exception as e:
        logger.error(f"Error fetching data from database: {str(e)}")
        return []


@router.get("/api", response_class=JSONResponse)
async def dashboard_api(
    source: str = "mock", data_type: str = "accounts"
):
    """API endpoint for dashboard data"""
    try:
        logger.info(f"Dashboard API request: source={source}, data_type={data_type}")
        
        # Get data based on source
        if source == "mock":
            data = get_mock_data(data_type)
        else:
            data = await get_db_data(data_type)

        if not data:
            logger.warning(f"No data found for {data_type} from {source}")
            # Return empty data instead of error
            data = []

        logger.info(f"Returning {len(data)} records for {data_type}")
        return {
            "data": data,
            "data_type": data_type,
            "source": source,
            "timestamp": datetime.now().isoformat(),
            "count": len(data)
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in dashboard API: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/", response_class=HTMLResponse)
async def dashboard(
    request: Request, source: str = "mock", data_type: str = "accounts"
):
    """Endpoint for viewing data in a sophisticated table"""
    try:
        logger.info(f"Dashboard request: source={source}, data_type={data_type}")
        
        # Get data based on source
        if source == "mock":
            data = get_mock_data(data_type)
        else:
            data = await get_db_data(data_type)

        if not data:
            logger.warning(f"No data found for {data_type} from {source}")
            # Return empty data instead of error
            data = []

        logger.info(f"Returning {len(data)} records for {data_type}")
        return templates.TemplateResponse(
            "dashboard.html",
            {
                "request": request,
                "data": data,
                "data_type": data_type,
                "source": source,
                "timestamp": datetime.now().isoformat(),
            },
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in dashboard: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
