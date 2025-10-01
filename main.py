from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
from datetime import datetime, timedelta


from mock_data_storage import mock_storage
from database import db_manager
from models import *

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("banking_api.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="BankWise AI Banking Support API",
    description="API backend for Inbound Banking Support Agent by BankWise AI",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# API Token Authentication
def verify_api_token(x_api_token: str = Header(...)):
    """Verify the API token from the request header"""
    expected_token = os.getenv("API_TOKEN")
    if not expected_token:
        raise HTTPException(status_code=500, detail="API token not configured")
    if x_api_token != expected_token:
        raise HTTPException(status_code=401, detail="Invalid or missing API token")
    return True


# Enums for standardization
class Intent(str, Enum):
    ACCOUNT_INFO = "account_info"
    TX_HISTORY = "tx_history"
    CARD_BLOCK = "card_block"
    RAISE_DISPUTE = "raise_dispute"
    COMPLAINT_NEW = "complaint_new"
    COMPLAINT_STATUS = "complaint_status"
    LOCATE_BRANCH = "locate_branch"
    LOCATE_ATM = "locate_atm"
    KYC_STATUS = "kyc_status"
    CHEQUE_STATUS = "cheque_status"
    FD_RATE_INFO = "fd_rate_info"
    LOAN_STATUS = "loan_status"
    SPEAK_TO_AGENT = "speak_to_agent"


class Language(str, Enum):
    EN = "en"
    HI = "hi"


class Channel(str, Enum):
    VOICE = "voice"
    CHAT = "chat"


class Status(str, Enum):
    SUCCESS = "success"
    PENDING = "pending"
    FAILED = "failed"
    NOT_FOUND = "not_found"


class ErrorResponse(BaseModel):
    error: str
    code: str
    details: Optional[Dict[str, Any]] = None


# Global session store (in production, use proper database)
sessions = {}


def get_session_data(session_id: str):
    """Get session data or create new one"""
    if session_id not in sessions:
        sessions[session_id] = {
            "created_at": datetime.now().isoformat(),
            "intent_history": [],
            "entities": {},
            "escalation_requested": False,
        }
    return sessions[session_id]


@app.on_event("startup")
async def startup_event():
    """Initialize database and mock data on startup"""
    logger.info("Starting BankWise AI Banking Support API")

    # Initialize database
    db_success = await db_manager.initialize()
    if db_success:
        logger.info("Database initialized successfully")
    else:
        logger.warning("Database initialization failed, using mock data only")
        logger.info(
            f"Initialized mock data with {len(mock_storage.accounts)} accounts, {len(mock_storage.cards)} cards, {len(mock_storage.transactions)} transactions"
        )


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "BankWise AI Banking Support API is running", "version": "1.0.0"}


@app.head("/")
async def head_root():
    return {"message": "service is up and running"}


@app.get("/health")
async def health_check():
    """Detailed health check"""
    db_status = "connected" if db_manager.initialized else "disconnected"
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "active_sessions": len(sessions),
        "database": db_status,
        "version": "1.0.0",
        "service": "BankWise AI",
    }


# Include all route modules
from routes import (
    account,
    card,
    dispute,
    complaint,
    branch,
    atm,
    kyc,
    cheque,
    fd,
    loan,
    escalation,
    chat,
    sms,
    dashboard,
)

app.include_router(account.router)
app.include_router(card.router)
app.include_router(dispute.router)
app.include_router(complaint.router)
app.include_router(branch.router)
app.include_router(atm.router)
app.include_router(kyc.router)
app.include_router(cheque.router)
app.include_router(fd.router)
app.include_router(loan.router)
app.include_router(escalation.router)
app.include_router(chat.router)
app.include_router(sms.router)
app.include_router(dashboard.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
