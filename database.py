import asyncio
import asyncpg
from typing import List, Optional, Dict, Any
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
import logging

from datetime import datetime


def parse_datetime(date_str):
    """Parse a datetime string into a datetime object, handling various formats."""
    if not date_str:
        return None
    try:
        # First, try the format with microseconds
        return datetime.fromisoformat(date_str)
    except ValueError:
        # If that fails, try without microseconds
        return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")


# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Database manager for Neon DB integration"""

    def __init__(self):
        self.db_url = os.getenv("DATABASE_URL")
        self.pool = None
        self.initialized = False

    async def initialize(self):
        """Initialize database connection and create tables if needed"""
        try:
            if not self.db_url:
                logger.warning(
                    "DATABASE_URL not set, using mock data only - BankWise AI Banking Support API"
                )
                return False

            # Create connection pool
            self.pool = await asyncpg.create_pool(
                self.db_url, min_size=5, max_size=20, command_timeout=60
            )

            # Check if tables exist
            async with self.pool.acquire() as conn:
                tables_exist = await conn.fetchval(
                    """
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_schema = 'public' 
                        AND table_name = 'accounts'
                    )
                """
                )

                if not tables_exist:
                    logger.info("Creating database tables...")
                    await self._create_tables(conn)
                    await self._populate_initial_data(conn)
                    self.initialized = True
                    logger.info(
                        "BankWise AI Banking Support API - Database initialized successfully"
                    )
                else:
                    self.initialized = True
                    logger.info(
                        "BankWise AI Banking Support API - Database tables already exist"
                    )

            return True

        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            return False

    async def _create_tables(self, conn):
        """Create all necessary tables"""

        # Accounts table
        await conn.execute(
            """
            CREATE TABLE accounts (
                id SERIAL PRIMARY KEY,
                account_number VARCHAR(20) UNIQUE NOT NULL,
                account_type VARCHAR(20) NOT NULL,
                balance DECIMAL(15,2) NOT NULL,
                currency VARCHAR(3) NOT NULL,
                customer_name VARCHAR(100) NOT NULL,
                customer_id VARCHAR(20) NOT NULL,
                branch_code VARCHAR(20) NOT NULL,
                ifsc_code VARCHAR(20) NOT NULL,
                kyc_status VARCHAR(20) NOT NULL,
                kyc_level VARCHAR(20) NOT NULL,
                last_updated TIMESTAMP NOT NULL,
                account_status VARCHAR(20) NOT NULL
            )
        """
        )

        # Cards table
        await conn.execute(
            """
            CREATE TABLE cards (
                id SERIAL PRIMARY KEY,
                card_number VARCHAR(20) NOT NULL,
                account_number VARCHAR(20) NOT NULL REFERENCES accounts(account_number),
                card_type VARCHAR(20) NOT NULL,
                card_network VARCHAR(20) NOT NULL,
                expiry_date VARCHAR(7) NOT NULL,
                cvv VARCHAR(3) NOT NULL,
                card_status VARCHAR(20) NOT NULL,
                daily_limit DECIMAL(15,2) NOT NULL,
                monthly_limit DECIMAL(15,2) NOT NULL,
                international_usage VARCHAR(20) NOT NULL,
                contactless VARCHAR(3) NOT NULL,
                issue_date TIMESTAMP NOT NULL,
                customer_name VARCHAR(100) NOT NULL
            )
        """
        )

        # Transactions table
        await conn.execute(
            """
            CREATE TABLE transactions (
                id SERIAL PRIMARY KEY,
                transaction_id VARCHAR(20) UNIQUE NOT NULL,
                account_number VARCHAR(20) NOT NULL REFERENCES accounts(account_number),
                transaction_date TIMESTAMP NOT NULL,
                description VARCHAR(200) NOT NULL,
                amount DECIMAL(15,2) NOT NULL,
                type VARCHAR(20) NOT NULL,
                balance_after DECIMAL(15,2) NOT NULL,
                status VARCHAR(20) NOT NULL,
                reference_id VARCHAR(20),
                merchant_id VARCHAR(100),
                location VARCHAR(100)
            )
        """
        )

        # Branches table
        await conn.execute(
            """
            CREATE TABLE branches (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                address TEXT NOT NULL,
                city VARCHAR(50) NOT NULL,
                pincode VARCHAR(10) NOT NULL,
                ifsc VARCHAR(20) UNIQUE NOT NULL,
                latitude DECIMAL(10,6) NOT NULL,
                longitude DECIMAL(10,6) NOT NULL,
                phone VARCHAR(20) NOT NULL,
                email VARCHAR(100) NOT NULL,
                working_hours VARCHAR(50) NOT NULL,
                branch_type VARCHAR(20) NOT NULL,
                facilities TEXT[],
                manager_name VARCHAR(100) NOT NULL,
                established_date TIMESTAMP NOT NULL
            )
        """
        )

        # ATMs table
        await conn.execute(
            """
            CREATE TABLE atms (
                id SERIAL PRIMARY KEY,
                atm_id VARCHAR(20) UNIQUE NOT NULL,
                address TEXT NOT NULL,
                city VARCHAR(50) NOT NULL,
                pincode VARCHAR(10) NOT NULL,
                bank_name VARCHAR(50) NOT NULL,
                latitude DECIMAL(10,6) NOT NULL,
                longitude DECIMAL(10,6) NOT NULL,
                type VARCHAR(20) NOT NULL,
                "24x7" VARCHAR(3) NOT NULL,
                facilities TEXT[],
                last_maintenance TIMESTAMP NOT NULL,
                status VARCHAR(20) NOT NULL
            )
        """
        )

        # Complaints table
        await conn.execute(
            """
            CREATE TABLE complaints (
                id SERIAL PRIMARY KEY,
                ticket_id VARCHAR(20) UNIQUE NOT NULL,
                account_number VARCHAR(20) REFERENCES accounts(account_number),
                subject VARCHAR(200) NOT NULL,
                description TEXT NOT NULL,
                category VARCHAR(50) NOT NULL,
                status VARCHAR(20) NOT NULL,
                priority VARCHAR(20) NOT NULL,
                created_at TIMESTAMP NOT NULL,
                resolved_at TIMESTAMP,
                estimated_resolution_days INTEGER NOT NULL,
                assigned_agent VARCHAR(20),
                resolution_notes TEXT,
                customer_satisfaction INTEGER,
                CONSTRAINT cs_rating CHECK (customer_satisfaction IS NULL OR (customer_satisfaction >= 1 AND customer_satisfaction <= 5))
            )
        """
        )

        # Disputes table
        await conn.execute(
            """
            CREATE TABLE disputes (
                id SERIAL PRIMARY KEY,
                ticket_id VARCHAR(20) UNIQUE NOT NULL,
                account_number VARCHAR(20) REFERENCES accounts(account_number),
                transaction_id VARCHAR(20) NOT NULL,
                amount DECIMAL(15,2) NOT NULL,
                transaction_date TIMESTAMP NOT NULL,
                dispute_type VARCHAR(50) NOT NULL,
                reason TEXT NOT NULL,
                description TEXT,
                status VARCHAR(20) NOT NULL,
                created_at TIMESTAMP NOT NULL,
                resolved_at TIMESTAMP,
                estimated_resolution_days INTEGER NOT NULL,
                assigned_officer VARCHAR(20),
                resolution_notes TEXT,
                evidence_submitted VARCHAR(3) NOT NULL,
                customer_contacted VARCHAR(3) NOT NULL
            )
        """
        )

        # Loans table
        await conn.execute(
            """
            CREATE TABLE loans (
                id SERIAL PRIMARY KEY,
                loan_id VARCHAR(20) UNIQUE NOT NULL,
                account_number VARCHAR(20) REFERENCES accounts(account_number),
                loan_type VARCHAR(50) NOT NULL,
                principal DECIMAL(15,2) NOT NULL,
                interest_rate DECIMAL(5,2) NOT NULL,
                tenure_months INTEGER NOT NULL,
                emi_amount DECIMAL(15,2) NOT NULL,
                disbursement_date TIMESTAMP NOT NULL,
                emi_start_date TIMESTAMP NOT NULL,
                next_emi_date TIMESTAMP NOT NULL,
                total_emis INTEGER NOT NULL,
                paid_emis INTEGER NOT NULL,
                remaining_tenure INTEGER NOT NULL,
                status VARCHAR(20) NOT NULL,
                collateral_details TEXT,
                processing_fee DECIMAL(15,2) NOT NULL,
                insurance_details TEXT
            )
        """
        )

        # FD Rates table
        await conn.execute(
            """
            CREATE TABLE fd_rates (
                id SERIAL PRIMARY KEY,
                tenure INTEGER NOT NULL,
                rate DECIMAL(5,2) NOT NULL,
                customer_type VARCHAR(20) NOT NULL,
                min_amount DECIMAL(15,2) NOT NULL,
                max_amount DECIMAL(15,2) NOT NULL,
                currency VARCHAR(3) NOT NULL,
                last_updated TIMESTAMP NOT NULL,
                special_features VARCHAR(50)
            )
        """
        )

        logger.info("BankWise AI Banking Support API - All tables created successfully")

    async def _populate_initial_data(self, conn):
        """Populate tables with initial mock data"""
        from mock_data import mock_data

        logger.info(
            "BankWise AI Banking Support API - Populating database with initial data..."
        )

        # Insert accounts
        for account in mock_data.accounts:
            await conn.execute(
                """
                INSERT INTO accounts (
                    account_number, account_type, balance, currency, customer_name,
                    customer_id, branch_code, ifsc_code, kyc_status, kyc_level,
                    last_updated, account_status
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
            """,
                account["account_number"],
                account["account_type"],
                account["balance"],
                account["currency"],
                account["customer_name"],
                account["customer_id"],
                account["branch_code"],
                account["ifsc_code"],
                account["kyc_status"],
                account["kyc_level"],
                parse_datetime(account["last_updated"]),
                account["account_status"],
            )

        # Insert cards
        for card in mock_data.cards:
            await conn.execute(
                """
                INSERT INTO cards (
                    card_number, account_number, card_type, card_network,
                    expiry_date, cvv, card_status, daily_limit, monthly_limit,
                    international_usage, contactless, issue_date, customer_name
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)
            """,
                card["card_number"],
                card["account_number"],
                card["card_type"],
                card["card_network"],
                card["expiry_date"],
                card["cvv"],
                card["card_status"],
                card["daily_limit"],
                card["monthly_limit"],
                card["international_usage"],
                card["contactless"],
                parse_datetime(card["issue_date"]),
                card["customer_name"],
            )

        # Insert transactions (sample to avoid too much data)
        sample_transactions = mock_data.transactions[
            :1000
        ]  # Limit to 1000 for initial load
        for tx in sample_transactions:
            await conn.execute(
                """
                INSERT INTO transactions (
                    transaction_id, account_number, transaction_date, description,
                    amount, type, balance_after, status, reference_id,
                    merchant_id, location
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
            """,
                tx["id"],
                tx["account_number"],
                parse_datetime(tx["transaction_date"]),
                tx["description"],
                tx["amount"],
                tx["type"],
                tx["balance_after"],
                tx["status"],
                tx["reference_id"],
                tx["merchant_id"],
                tx["location"],
            )

        # Insert branches
        for branch in mock_data.branches:
            await conn.execute(
                """
                INSERT INTO branches (
                    name, address, city, pincode, ifsc, latitude, longitude,
                    phone, email, working_hours, branch_type, facilities,
                    manager_name, established_date
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14)
            """,
                branch["name"],
                branch["address"],
                branch["city"],
                branch["pincode"],
                branch["ifsc"],
                branch["latitude"],
                branch["longitude"],
                branch["phone"],
                branch["email"],
                branch["working_hours"],
                branch["branch_type"],
                branch["facilities"],
                branch["manager_name"],
                parse_datetime(branch["established_date"]),
            )

        # Insert ATMs (sample)
        sample_atms = mock_data.atms[:100]  # Limit to 100 for initial load
        for atm in sample_atms:
            await conn.execute(
                """
                INSERT INTO atms (
                    atm_id, address, city, pincode, bank_name, latitude, longitude,
                    type, "24x7", facilities, last_maintenance, status
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
            """,
                atm["id"],
                atm["address"],
                atm["city"],
                atm["pincode"],
                atm["bank_name"],
                atm["latitude"],
                atm["longitude"],
                atm["type"],
                atm["24x7"],
                atm["facilities"],
                parse_datetime(atm["last_maintenance"]),
                atm["status"],
            )

        # Insert complaints (sample)
        sample_complaints = mock_data.complaints[:50]  # Limit to 50 for initial load
        for complaint in sample_complaints:
            await conn.execute(
                """
                INSERT INTO complaints (
                    ticket_id, account_number, subject, description, category,
                    status, priority, created_at, resolved_at, estimated_resolution_days,
                    assigned_agent, resolution_notes, customer_satisfaction
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)
            """,
                complaint["ticket_id"],
                complaint["account_number"],
                complaint["subject"],
                complaint["description"],
                complaint["category"],
                complaint["status"],
                complaint["priority"],
                parse_datetime(complaint["created_at"]),
                parse_datetime(complaint["resolved_at"]),
                complaint["estimated_resolution_days"],
                complaint["assigned_agent"],
                complaint["resolution_notes"],
                complaint["customer_satisfaction"],
            )

        # Insert disputes (sample)
        sample_disputes = mock_data.disputes[:30]  # Limit to 30 for initial load
        for dispute in sample_disputes:
            await conn.execute(
                """
                INSERT INTO disputes (
                    ticket_id, account_number, transaction_id, amount, transaction_date,
                    dispute_type, reason, description, status, created_at, resolved_at,
                    estimated_resolution_days, assigned_officer, resolution_notes,
                    evidence_submitted, customer_contacted
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16)
            """,
                dispute["ticket_id"],
                dispute["account_number"],
                dispute["transaction_id"],
                dispute["amount"],
                parse_datetime(dispute["transaction_date"]),
                dispute["dispute_type"],
                dispute["reason"],
                dispute["description"],
                dispute["status"],
                parse_datetime(dispute["created_at"]),
                parse_datetime(dispute["resolved_at"]),
                dispute["estimated_resolution_days"],
                dispute["assigned_officer"],
                dispute["resolution_notes"],
                dispute["evidence_submitted"],
                dispute["customer_contacted"],
            )

        # Insert loans (sample)
        sample_loans = mock_data.loans[:50]  # Limit to 50 for initial load
        for loan in sample_loans:
            await conn.execute(
                """
                INSERT INTO loans (
                    loan_id, account_number, loan_type, principal, interest_rate,
                    tenure_months, emi_amount, disbursement_date, emi_start_date,
                    next_emi_date, total_emis, paid_emis, remaining_tenure, status,
                    collateral_details, processing_fee, insurance_details
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17)
            """,
                loan["loan_id"],
                loan["account_number"],
                loan["loan_type"],
                loan["principal"],
                loan["interest_rate"],
                loan["tenure_months"],
                loan["emi_amount"],
                parse_datetime(loan["disbursement_date"]),
                parse_datetime(loan["emi_start_date"]),
                parse_datetime(loan["next_emi_date"]),
                loan["total_emis"],
                loan["paid_emis"],
                loan["remaining_tenure"],
                loan["status"],
                loan["collateral_details"],
                loan["processing_fee"],
                loan["insurance_details"],
            )

        # Insert FD rates
        for rate in mock_data.fd_rates:
            await conn.execute(
                """
                INSERT INTO fd_rates (
                    tenure, rate, customer_type, min_amount, max_amount,
                    currency, last_updated, special_features
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            """,
                rate["tenure"],
                rate["rate"],
                rate["customer_type"],
                rate["min_amount"],
                rate["max_amount"],
                rate["currency"],
                parse_datetime(rate["last_updated"]),
                rate["special_features"],
            )

        logger.info(
            f"BankWise AI Banking Support API - Database populated with {len(mock_data.accounts)} accounts, {len(mock_data.cards)} cards, and other data"
        )

    @asynccontextmanager
    async def get_connection(self):
        """Get database connection from pool"""
        if not self.pool:
            yield None
            return

        try:
            async with self.pool.acquire() as conn:
                yield conn
        except Exception as e:
            logger.error(f"Database connection error: {e}")
            yield None

    async def close(self):
        """Close database connection pool"""
        if self.pool:
            await self.pool.close()
            self.pool = None


# Global database instance
db_manager = DatabaseManager()


async def get_db_connection():
    """Get database connection"""
    return await db_manager.get_connection()
