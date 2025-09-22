from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import logging
import json
import uuid
from datetime import datetime, timedelta
import random
from enum import Enum
import math

from mock_data_storage import mock_storage
from database import db_manager

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


# Base models
class BaseEntity(BaseModel):
    intent: Intent
    channel: Channel
    language_pref: Language = Language.EN
    session_id: Optional[str] = None


class AccountNumber(BaseModel):
    account_number: str


class Last4Digits(BaseModel):
    last4: str


class TransactionDate(BaseModel):
    transaction_date: str


class Amount(BaseModel):
    amount: float


class BranchCity(BaseModel):
    branch_city: str


class Pincode(BaseModel):
    pincode: str


class IFSC(BaseModel):
    ifsc: str


class TicketID(BaseModel):
    ticket_id: str


# Request models
class AccountInfoRequest(BaseModel):
    account_number: str
    last4: Optional[str] = None


class TransactionHistoryRequest(BaseModel):
    account_number: str
    limit: int = 5


class CardBlockRequest(BaseModel):
    last4: str
    reason: Optional[str] = None


class DisputeRequest(BaseModel):
    amount: float
    transaction_date: str
    reason: str
    description: Optional[str] = None


class ComplaintRequest(BaseModel):
    subject: str
    description: str
    category: str


class ComplaintStatusRequest(BaseModel):
    ticket_id: str


class BranchLocatorRequest(BaseModel):
    branch_city: str
    limit: int = 3


class ATMLocatorRequest(BaseModel):
    pincode: str
    limit: int = 3


class KYCStatusRequest(BaseModel):
    account_number: str


class ChequeStatusRequest(BaseModel):
    cheque_number: str


class FDRateInfoRequest(BaseModel):
    tenure: Optional[int] = None
    amount: Optional[float] = None


class LoanStatusRequest(BaseModel):
    loan_id: str


class SpeakToAgentRequest(BaseModel):
    reason: Optional[str] = None
    urgency: str = "medium"


# Response models
class BalanceResponse(BaseModel):
    account_number: str
    balance: float
    currency: str
    as_of: str
    status: Status


class Transaction(BaseModel):
    id: str
    date: str
    description: str
    amount: float
    type: str
    balance_after: float


class TransactionHistoryResponse(BaseModel):
    account_number: str
    transactions: List[Transaction]
    total_count: int
    status: Status


class CardBlockResponse(BaseModel):
    card_number: str
    content: str
    blocked_at: str
    ticket_id: Optional[str] = None
    status: Status


class DisputeResponse(BaseModel):
    ticket_id: str
    content: str
    amount: float
    estimated_resolution_days: int
    status: Status


class ComplaintResponse(BaseModel):
    ticket_id: str
    content: str
    created_at: str
    estimated_resolution_days: int
    status: Status


class Branch(BaseModel):
    name: str
    address: str
    city: str
    pincode: str
    ifsc: str
    latitude: float
    longitude: float
    distance: Optional[float] = None


class BranchLocatorResponse(BaseModel):
    branches: List[Branch]
    total_count: int
    status: Status


class ATM(BaseModel):
    id: str
    address: str
    city: str
    pincode: str
    bank_name: str
    latitude: float
    longitude: float
    distance: Optional[float] = None


class ATMLocatorResponse(BaseModel):
    atms: List[ATM]
    total_count: int
    status: Status


class KYCStatusResponse(BaseModel):
    account_number: str
    kyc_status: str
    verification_level: str
    last_updated: str
    documents_required: List[str]
    status: Status


class ChequeStatusResponse(BaseModel):
    cheque_number: str
    content: str
    amount: Optional[float] = None
    date: Optional[str] = None
    clearing_date: Optional[str] = None
    status: Status


class FDRate(BaseModel):
    tenure: int
    rate: float
    min_amount: float
    max_amount: float
    currency: str


class FDRateInfoResponse(BaseModel):
    rates: List[FDRate]
    currency: str
    last_updated: str
    status: Status


class LoanInfo(BaseModel):
    loan_id: str
    loan_type: str
    principal: float
    emi_amount: float
    due_date: str
    remaining_tenure: int
    interest_rate: float
    status: str


class LoanStatusResponse(BaseModel):
    loan_info: LoanInfo
    next_payment_date: str
    status: Status


class EscalationResponse(BaseModel):
    escalation_id: str
    agent_id: str
    estimated_wait_time: int
    status: Status


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


@app.post("/api/account/balance", response_model=BalanceResponse)
async def get_account_balance(request: AccountInfoRequest):
    """Get account balance information"""
    try:
        logger.info(f"Account balance request for account: {request.account_number}")

        # Try to get from database first
        async with db_manager.get_connection() as conn:
            if conn:
                account = await conn.fetchrow(
                    "SELECT * FROM accounts WHERE account_number = $1",
                    request.account_number,
                )
                if account:
                    # Mask account number for security
                    masked_account = f"******{request.account_number[-4:]}"

                    response = BalanceResponse(
                        account_number=masked_account,
                        balance=float(account["balance"]),
                        currency=account["currency"],
                        as_of=datetime.now().isoformat(),
                        status=Status.SUCCESS,
                    )

                    logger.info(
                        f"Balance retrieved from database for account: {request.account_number}"
                    )
                    return response

        # Fallback to mock data
        account = mock_storage.get_account_by_number(request.account_number)
        if not account:
            logger.warning(f"Account not found: {request.account_number}")
            raise HTTPException(status_code=404, detail="Account not found")

        # Mask account number for security
        masked_account = f"******{request.account_number[-4:]}"

        response = BalanceResponse(
            account_number=masked_account,
            balance=account["balance"],
            currency=account["currency"],
            as_of=datetime.now().isoformat(),
            status=Status.SUCCESS,
        )

        logger.info(
            f"Balance retrieved from mock data for account: {request.account_number}"
        )
        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Error getting balance for account {request.account_number}: {str(e)}"
        )
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/api/account/transactions", response_model=TransactionHistoryResponse)
async def get_transaction_history(request: TransactionHistoryRequest):
    """Get recent transaction history"""
    try:
        logger.info(
            f"Transaction history request for account: {request.account_number}, limit: {request.limit}"
        )

        # Try to get from database first
        async with db_manager.get_connection() as conn:
            if conn:
                tx_records = await conn.fetch(
                    "SELECT * FROM transactions WHERE account_number = $1 ORDER BY transaction_date DESC LIMIT $2",
                    request.account_number,
                    request.limit,
                )

                if tx_records:
                    transaction_list = []
                    for tx in tx_records:
                        transaction_list.append(
                            Transaction(
                                id=tx["transaction_id"],
                                date=tx["transaction_date"].isoformat(),
                                description=tx["description"],
                                amount=float(tx["amount"]),
                                type=tx["type"],
                                balance_after=float(tx["balance_after"]),
                            )
                        )

                    response = TransactionHistoryResponse(
                        account_number=f"******{request.account_number[-4:]}",
                        transactions=transaction_list,
                        total_count=len(transaction_list),
                        status=Status.SUCCESS,
                    )

                    logger.info(
                        f"Transaction history retrieved from database for account: {request.account_number}"
                    )
                    return response

        # Fallback to mock data
        account = mock_storage.get_account_by_number(request.account_number)
        if not account:
            logger.warning(f"Account not found: {request.account_number}")
            raise HTTPException(status_code=404, detail="Account not found")

        transactions = mock_storage.get_transactions_by_account(
            request.account_number, request.limit
        )

        transaction_list = []
        for tx in transactions:
            transaction_list.append(
                Transaction(
                    id=tx["id"],
                    date=tx["transaction_date"],
                    description=tx["description"],
                    amount=tx["amount"],
                    type=tx["type"],
                    balance_after=tx["balance_after"],
                )
            )

        response = TransactionHistoryResponse(
            account_number=f"******{request.account_number[-4:]}",
            transactions=transaction_list,
            total_count=len(transaction_list),
            status=Status.SUCCESS,
        )

        logger.info(
            f"Transaction history retrieved from mock data for account: {request.account_number}"
        )
        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Error getting transaction history for account {request.account_number}: {str(e)}"
        )
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/api/card/block", response_model=CardBlockResponse)
async def block_card(request: CardBlockRequest):
    """Block a card"""
    try:
        logger.info(f"Card block request for card ending with: {request.last4}")

        # Try to get from database first
        async with db_manager.get_connection() as conn:
            if conn:
                card = await conn.fetchrow(
                    "SELECT * FROM cards WHERE card_number LIKE $1", f"%{request.last4}"
                )
                if card:
                    # Simulate card blocking process
                    blocked_at = datetime.now()
                    ticket_id = f"BLOCK{random.randint(10000, 99999)}"

                    # Update card status in database
                    await conn.execute(
                        "UPDATE cards SET card_status = $1 WHERE card_number LIKE $2",
                        "BLOCKED",
                        f"%{request.last4}",
                    )

                    response = CardBlockResponse(
                        card_number=f"****{request.last4}",
                        content="BLOCKED",
                        blocked_at=blocked_at.isoformat(),
                        ticket_id=ticket_id,
                        status=Status.SUCCESS,
                    )

                    logger.info(
                        f"Card blocked in database for card ending with: {request.last4}"
                    )
                    return response

        # Fallback to mock data
        card = mock_storage.get_card_by_last4(request.last4)
        if not card:
            logger.warning(f"Card not found ending with: {request.last4}")
            raise HTTPException(status_code=404, detail="Card not found")

        # Simulate card blocking process
        blocked_at = datetime.now()
        ticket_id = f"BLOCK{random.randint(10000, 99999)}"

        response = CardBlockResponse(
            card_number=f"****{request.last4}",
            content="BLOCKED",
            blocked_at=blocked_at.isoformat(),
            ticket_id=ticket_id,
            status=Status.SUCCESS,
        )

        logger.info(f"Card blocked in mock data for card ending with: {request.last4}")
        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error blocking card ending with {request.last4}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/api/dispute/raise", response_model=DisputeResponse)
async def raise_dispute(request: DisputeRequest):
    """Raise a transaction dispute"""
    try:
        logger.info(
            f"Dispute request for amount: {request.amount}, date: {request.transaction_date}"
        )

        # Generate dispute ticket
        ticket_id = f"DISPUTE{random.randint(10000, 99999)}"
        estimated_days = random.randint(5, 30)

        response = DisputeResponse(
            ticket_id=ticket_id,
            content="UNDER_REVIEW",
            amount=request.amount,
            estimated_resolution_days=estimated_days,
            status=Status.SUCCESS,
        )

        logger.info(f"Dispute raised successfully with ticket ID: {ticket_id}")
        return response

    except Exception as e:
        logger.error(f"Error raising dispute: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/api/complaint/new", response_model=ComplaintResponse)
async def create_complaint(request: ComplaintRequest):
    """Create a new complaint"""
    try:
        logger.info(f"Complaint creation request for category: {request.category}")

        # Generate complaint ticket
        ticket_id = f"COMPLAINT{random.randint(10000, 99999)}"
        created_at = datetime.now()
        estimated_days = random.randint(3, 15)

        response = ComplaintResponse(
            ticket_id=ticket_id,
            content="OPEN",
            created_at=created_at.isoformat(),
            estimated_resolution_days=estimated_days,
            status=Status.SUCCESS,
        )

        logger.info(f"Complaint created successfully with ticket ID: {ticket_id}")
        return response

    except Exception as e:
        logger.error(f"Error creating complaint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/api/complaint/status", response_model=ComplaintResponse)
async def get_complaint_status(request: ComplaintStatusRequest):
    """Get complaint status"""
    try:
        logger.info(f"Complaint status request for ticket ID: {request.ticket_id}")

        # Try to get from database first
        async with db_manager.get_connection() as conn:
            if conn:
                complaint = await conn.fetchrow(
                    "SELECT * FROM complaints WHERE ticket_id = $1", request.ticket_id
                )
                if complaint:
                    response = ComplaintResponse(
                        ticket_id=complaint["ticket_id"],
                        content=complaint["status"],
                        created_at=complaint["created_at"].isoformat(),
                        estimated_resolution_days=complaint[
                            "estimated_resolution_days"
                        ],
                        status=Status.SUCCESS,
                    )

                    logger.info(
                        f"Complaint status retrieved from database for ticket ID: {request.ticket_id}"
                    )
                    return response

        # Fallback to mock data
        complaint = mock_storage.get_complaint_by_id(request.ticket_id)
        if not complaint:
            logger.warning(f"Complaint not found with ticket ID: {request.ticket_id}")
            raise HTTPException(status_code=404, detail="Complaint not found")

        response = ComplaintResponse(
            ticket_id=complaint["ticket_id"],
            content=complaint["status"],
            created_at=complaint["created_at"],
            estimated_resolution_days=complaint["estimated_resolution_days"],
            status=Status.SUCCESS,
        )

        logger.info(
            f"Complaint status retrieved from mock data for ticket ID: {request.ticket_id}"
        )
        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Error getting complaint status for ticket ID {request.ticket_id}: {str(e)}"
        )
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/api/branch/locate", response_model=BranchLocatorResponse)
async def locate_branch(request: BranchLocatorRequest):
    """Locate branches in a city"""
    try:
        logger.info(
            f"Branch locator request for city: {request.branch_city}, limit: {request.limit}"
        )

        # Try to get from database first
        async with db_manager.get_connection() as conn:
            if conn:
                branch_records = await conn.fetch(
                    "SELECT * FROM branches WHERE city ILIKE $1 ORDER BY name LIMIT $2",
                    f"%{request.branch_city}%",
                    request.limit,
                )

                if branch_records:
                    branch_list = []
                    for branch in branch_records:
                        # Calculate distance from city center (mock calculation)
                        distance = round(random.uniform(0.5, 15.0), 1)
                        branch_list.append(
                            Branch(
                                name=branch["name"],
                                address=branch["address"],
                                city=branch["city"],
                                pincode=branch["pincode"],
                                ifsc=branch["ifsc"],
                                latitude=branch["latitude"],
                                longitude=branch["longitude"],
                                distance=distance,
                            )
                        )

                    response = BranchLocatorResponse(
                        branches=branch_list,
                        total_count=len(branch_list),
                        status=Status.SUCCESS,
                    )

                    logger.info(
                        f"Branches located from database in city: {request.branch_city}"
                    )
                    return response

        # Fallback to mock data
        branches = mock_storage.get_branches_by_city(request.branch_city, request.limit)

        if not branches:
            logger.warning(f"No branches found in city: {request.branch_city}")
            raise HTTPException(
                status_code=404, detail="No branches found in the specified city"
            )

        branch_list = []
        for branch in branches:
            # Calculate distance from city center (mock calculation)
            distance = round(random.uniform(0.5, 15.0), 1)
            branch_list.append(
                Branch(
                    name=branch["name"],
                    address=branch["address"],
                    city=branch["city"],
                    pincode=branch["pincode"],
                    ifsc=branch["ifsc"],
                    latitude=branch["latitude"],
                    longitude=branch["longitude"],
                    distance=distance,
                )
            )

        response = BranchLocatorResponse(
            branches=branch_list, total_count=len(branch_list), status=Status.SUCCESS
        )

        logger.info(f"Branches located from mock data in city: {request.branch_city}")
        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error locating branches in city {request.branch_city}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/api/atm/locate", response_model=ATMLocatorResponse)
async def locate_atm(request: ATMLocatorRequest):
    """Locate ATMs by pincode"""
    try:
        logger.info(
            f"ATM locator request for pincode: {request.pincode}, limit: {request.limit}"
        )

        # Try to get from database first
        async with db_manager.get_connection() as conn:
            if conn:
                atm_records = await conn.fetch(
                    "SELECT * FROM atms WHERE pincode = $1 ORDER BY bank_name LIMIT $2",
                    request.pincode,
                    request.limit,
                )

                if atm_records:
                    atm_list = []
                    for atm in atm_records:
                        # Calculate distance from pincode center (mock calculation)
                        distance = round(random.uniform(0.2, 8.0), 1)
                        atm_list.append(
                            ATM(
                                id=atm["atm_id"],
                                address=atm["address"],
                                city=atm["city"],
                                pincode=atm["pincode"],
                                bank_name=atm["bank_name"],
                                latitude=atm["latitude"],
                                longitude=atm["longitude"],
                                distance=distance,
                            )
                        )

                    response = ATMLocatorResponse(
                        atms=atm_list, total_count=len(atm_list), status=Status.SUCCESS
                    )

                    logger.info(
                        f"ATMs located from database for pincode: {request.pincode}"
                    )
                    return response

        # Fallback to mock data
        atms = mock_storage.get_atms_by_pincode(request.pincode, request.limit)

        if not atms:
            logger.warning(f"No ATMs found for pincode: {request.pincode}")
            raise HTTPException(
                status_code=404, detail="No ATMs found for the specified pincode"
            )

        atm_list = []
        for atm in atms:
            # Calculate distance from pincode center (mock calculation)
            distance = round(random.uniform(0.2, 8.0), 1)
            atm_list.append(
                ATM(
                    id=atm["id"],
                    address=atm["address"],
                    city=atm["city"],
                    pincode=atm["pincode"],
                    bank_name=atm["bank_name"],
                    latitude=atm["latitude"],
                    longitude=atm["longitude"],
                    distance=distance,
                )
            )

        response = ATMLocatorResponse(
            atms=atm_list, total_count=len(atm_list), status=Status.SUCCESS
        )

        logger.info(f"ATMs located from mock data for pincode: {request.pincode}")
        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error locating ATMs for pincode {request.pincode}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/api/kyc/status", response_model=KYCStatusResponse)
async def get_kyc_status(request: KYCStatusRequest):
    """Get KYC status"""
    try:
        logger.info(f"KYC status request for account: {request.account_number}")

        # Try to get from database first
        async with db_manager.get_connection() as conn:
            if conn:
                account = await conn.fetchrow(
                    "SELECT * FROM accounts WHERE account_number = $1",
                    request.account_number,
                )
                if account:
                    response = KYCStatusResponse(
                        account_number=f"******{request.account_number[-4:]}",
                        kyc_status=account["kyc_status"],
                        verification_level=account["kyc_level"],
                        last_updated=account["last_updated"],
                        documents_required=[],
                        status=Status.SUCCESS,
                    )

                    logger.info(
                        f"KYC status retrieved from database for account: {request.account_number}"
                    )
                    return response

        # Fallback to mock data
        account = mock_storage.get_account_by_number(request.account_number)
        if not account:
            logger.warning(f"Account not found: {request.account_number}")
            raise HTTPException(status_code=404, detail="Account not found")

        response = KYCStatusResponse(
            account_number=f"******{request.account_number[-4:]}",
            kyc_status=account["kyc_status"],
            verification_level=account["kyc_level"],
            last_updated=account["last_updated"],
            documents_required=[],
            status=Status.SUCCESS,
        )

        logger.info(
            f"KYC status retrieved from mock data for account: {request.account_number}"
        )
        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Error getting KYC status for account {request.account_number}: {str(e)}"
        )
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/api/cheque/status", response_model=ChequeStatusResponse)
async def get_cheque_status(request: ChequeStatusRequest):
    """Get cheque status"""
    try:
        logger.info(f"Cheque status request for cheque number: {request.cheque_number}")

        # Mock cheque status - randomly assign status
        statuses = ["Cleared", "Pending", "Bounced", "Under Process"]
        status = random.choice(statuses)

        # Generate mock data based on status
        if status == "Cleared":
            amount = round(random.uniform(1000, 50000), 2)
            date = (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat()
            clearing_date = (
                datetime.now() - timedelta(days=random.randint(1, 5))
            ).isoformat()
        elif status == "Pending":
            amount = round(random.uniform(1000, 50000), 2)
            date = (datetime.now() - timedelta(days=random.randint(1, 10))).isoformat()
            clearing_date = None
        else:
            amount = round(random.uniform(1000, 50000), 2)
            date = (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat()
            clearing_date = None

        response = ChequeStatusResponse(
            cheque_number=request.cheque_number,
            content=status,
            amount=amount,
            date=date,
            clearing_date=clearing_date,
            status=Status.SUCCESS,
        )

        logger.info(
            f"Cheque status retrieved successfully for cheque number: {request.cheque_number}"
        )
        return response

    except Exception as e:
        logger.error(
            f"Error getting cheque status for cheque number {request.cheque_number}: {str(e)}"
        )
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/api/fd/rates", response_model=FDRateInfoResponse)
async def get_fd_rates(request: FDRateInfoRequest):
    """Get fixed deposit rates"""
    try:
        logger.info(f"FD rates request for tenure: {request.tenure}")

        # Try to get from database first
        async with db_manager.get_connection() as conn:
            if conn:
                if request.tenure:
                    rate_records = await conn.fetch(
                        "SELECT * FROM fd_rates WHERE tenure = $1 ORDER BY customer_type",
                        request.tenure,
                    )
                else:
                    rate_records = await conn.fetch(
                        "SELECT * FROM fd_rates ORDER BY tenure, customer_type"
                    )

                if rate_records:
                    rate_list = []
                    for rate in rate_records:
                        rate_list.append(
                            FDRate(
                                tenure=rate["tenure"],
                                rate=float(rate["rate"]),
                                min_amount=float(rate["min_amount"]),
                                max_amount=float(rate["max_amount"]),
                                currency=rate["currency"],
                            )
                        )

                    response = FDRateInfoResponse(
                        rates=rate_list,
                        currency="INR",
                        last_updated=datetime.now().isoformat(),
                        status=Status.SUCCESS,
                    )

                    logger.info(f"FD rates retrieved from database")
                    return response

        # Fallback to mock data
        rates = mock_storage.get_fd_rates(request.tenure)

        rate_list = []
        for rate in rates:
            rate_list.append(
                FDRate(
                    tenure=rate["tenure"],
                    rate=rate["rate"],
                    min_amount=rate["min_amount"],
                    max_amount=rate["max_amount"],
                    currency=rate["currency"],
                )
            )

        response = FDRateInfoResponse(
            rates=rate_list,
            currency="INR",
            last_updated=datetime.now().isoformat(),
            status=Status.SUCCESS,
        )

        logger.info(f"FD rates retrieved from mock data")
        return response

    except Exception as e:
        logger.error(f"Error getting FD rates: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/api/loan/status", response_model=LoanStatusResponse)
async def get_loan_status(request: LoanStatusRequest):
    """Get loan status"""
    try:
        logger.info(f"Loan status request for loan ID: {request.loan_id}")

        # Try to get from database first
        async with db_manager.get_connection() as conn:
            if conn:
                loan = await conn.fetchrow(
                    "SELECT * FROM loans WHERE loan_id = $1", request.loan_id
                )
                if loan:
                    loan_info = LoanInfo(
                        loan_id=loan["loan_id"],
                        loan_type=loan["loan_type"],
                        principal=float(loan["principal"]),
                        emi_amount=float(loan["emi_amount"]),
                        due_date=loan["next_emi_date"].isoformat(),
                        remaining_tenure=loan["remaining_tenure"],
                        interest_rate=float(loan["interest_rate"]),
                        status=loan["status"],
                    )

                    response = LoanStatusResponse(
                        loan_info=loan_info,
                        next_payment_date=loan["next_emi_date"].isoformat(),
                        status=Status.SUCCESS,
                    )

                    logger.info(
                        f"Loan status retrieved from database for loan ID: {request.loan_id}"
                    )
                    return response

        # Fallback to mock data
        loan = mock_storage.get_loan_by_id(request.loan_id)
        if not loan:
            logger.warning(f"Loan not found with ID: {request.loan_id}")
            raise HTTPException(status_code=404, detail="Loan not found")

        loan_info = LoanInfo(
            loan_id=loan["loan_id"],
            loan_type=loan["loan_type"],
            principal=loan["principal"],
            emi_amount=loan["emi_amount"],
            due_date=loan["next_emi_date"],
            remaining_tenure=loan["remaining_tenure"],
            interest_rate=loan["interest_rate"],
            status=loan["status"],
        )

        response = LoanStatusResponse(
            loan_info=loan_info,
            next_payment_date=loan["next_emi_date"],
            status=Status.SUCCESS,
        )

        logger.info(
            f"Loan status retrieved from mock data for loan ID: {request.loan_id}"
        )
        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Error getting loan status for loan ID {request.loan_id}: {str(e)}"
        )
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/api/escalate", response_model=EscalationResponse)
async def escalate_to_agent(request: SpeakToAgentRequest):
    """Escalate to human agent"""
    try:
        logger.info(f"Escalation request with urgency: {request.urgency}")

        escalation_id = f"ESCALATION{random.randint(10000, 99999)}"
        agent_id = f"AGENT{random.randint(100, 999)}"
        wait_time = random.randint(5, 30)

        response = EscalationResponse(
            escalation_id=escalation_id,
            agent_id=agent_id,
            estimated_wait_time=wait_time,
            status=Status.SUCCESS,
        )

        logger.info(f"Escalation created successfully with ID: {escalation_id}")
        return response

    except Exception as e:
        logger.error(f"Error processing escalation: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/api/chat/intent")
async def process_intent(request: Dict):
    """Process natural language intent (placeholder for NLU integration)"""
    try:
        logger.info(f"Intent processing request: {request}")

        # This is a placeholder for actual NLU processing
        # In a real implementation, this would integrate with a natural language understanding service

        # Mock intent detection based on keywords
        text = request.get("text", "").lower()

        if any(word in text for word in ["balance", "account balance"]):
            intent = Intent.ACCOUNT_INFO
        elif any(word in text for word in ["transaction", "history", "last 5"]):
            intent = Intent.TX_HISTORY
        elif any(word in text for word in ["block", "card block"]):
            intent = Intent.CARD_BLOCK
        elif any(word in text for word in ["dispute", "chargeback"]):
            intent = Intent.RAISE_DISPUTE
        elif any(word in text for word in ["complaint"]):
            intent = Intent.COMPLAINT_NEW
        elif any(word in text for word in ["branch", "find branch"]):
            intent = Intent.LOCATE_BRANCH
        elif any(word in text for word in ["atm", "atm near"]):
            intent = Intent.LOCATE_ATM
        elif any(word in text for word in ["kyc", "know your customer"]):
            intent = Intent.KYC_STATUS
        elif any(word in text for word in ["cheque", "check status"]):
            intent = Intent.CHEQUE_STATUS
        elif any(word in text for word in ["fd", "fixed deposit"]):
            intent = Intent.FD_RATE_INFO
        elif any(word in text for word in ["loan", "emi"]):
            intent = Intent.LOAN_STATUS
        elif any(word in text for word in ["agent", "human", "speak to"]):
            intent = Intent.SPEAK_TO_AGENT
        else:
            intent = Intent.SPEAK_TO_AGENT

        response = {
            "intent": intent.value,
            "confidence": random.uniform(0.7, 0.95),
            "entities": {},  # This would be populated by actual entity extraction
            "session_id": request.get("session_id", str(uuid.uuid4())),
        }

        logger.info(f"Intent detected: {intent.value}")
        return response

    except Exception as e:
        logger.error(f"Error processing intent: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
