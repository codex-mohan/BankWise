from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from enum import Enum


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