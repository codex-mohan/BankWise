from fastapi import APIRouter, HTTPException, Depends
from main import verify_api_token
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import logging

from mock_data_storage import mock_storage
from database import db_manager
from models import (
    AccountInfoRequest,
    TransactionHistoryRequest,
    BalanceResponse,
    Transaction,
    TransactionHistoryResponse,
    Status,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/account", tags=["account"])


@router.post("/balance", response_model=BalanceResponse)
async def get_account_balance(request: AccountInfoRequest, auth: bool = Depends(verify_api_token)):
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


@router.post("/transactions", response_model=TransactionHistoryResponse)
async def get_transaction_history(request: TransactionHistoryRequest, auth: bool = Depends(verify_api_token)):
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
