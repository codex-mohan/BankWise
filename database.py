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
                    
                    # Check if we should populate data
                    await self._check_and_populate_data(conn)

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
                account_status VARCHAR(20) NOT NULL,
                linked_cards TEXT[],
                mobile_numbers TEXT[]
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
                facilities VARCHAR(100),
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
                facilities VARCHAR(100),
                last_maintenance TIMESTAMP NOT NULL,
                status VARCHAR(20) NOT NULL
            )
        """
        )

        # Cheques table
        await conn.execute(
            """
            CREATE TABLE cheques (
                id SERIAL PRIMARY KEY,
                cheque_number VARCHAR(20) UNIQUE NOT NULL,
                account_number VARCHAR(20) NOT NULL REFERENCES accounts(account_number),
                amount DECIMAL(15,2) NOT NULL,
                status VARCHAR(50) NOT NULL,
                issue_date TIMESTAMP NOT NULL,
                clearing_date TIMESTAMP,
                payee_name VARCHAR(100) NOT NULL
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

    async def _check_and_populate_data(self, conn):
        """Check if tables are empty and populate if needed or if override is set"""
        try:
            # Check environment variable for override
            force_populate = os.getenv("FORCE_POPULATE_DB", "false").lower() == "true"
            
            if force_populate:
                logger.info("FORCE_POPULATE_DB is enabled - clearing and repopulating database...")
                await self._clear_all_tables(conn)
                await self._populate_initial_data(conn)
                return

            # Check if tables are empty
            tables_to_check = [
                ("accounts", "SELECT COUNT(*) FROM accounts"),
                ("cards", "SELECT COUNT(*) FROM cards"),
                ("transactions", "SELECT COUNT(*) FROM transactions"),
                ("branches", "SELECT COUNT(*) FROM branches"),
                ("atms", "SELECT COUNT(*) FROM atms"),
                ("complaints", "SELECT COUNT(*) FROM complaints"),
                ("disputes", "SELECT COUNT(*) FROM disputes"),
                ("loans", "SELECT COUNT(*) FROM loans"),
                ("fd_rates", "SELECT COUNT(*) FROM fd_rates"),
                ("cheques", "SELECT COUNT(*) FROM cheques"),
            ]

            empty_tables = []
            for table_name, query in tables_to_check:
                try:
                    count = await conn.fetchval(query)
                    if count == 0:
                        empty_tables.append(table_name)
                except Exception as e:
                    # Table might not exist, add to empty list
                    logger.warning(f"Error checking {table_name} table: {e}")
                    empty_tables.append(table_name)

            if empty_tables:
                logger.info(f"Found empty tables: {empty_tables}. Populating with data...")
                await self._populate_initial_data(conn)
            else:
                logger.info("All tables contain data. Skipping population.")

        except Exception as e:
            logger.error(f"Error checking/populating data: {e}")

    async def _clear_all_tables(self, conn):
        """Clear all tables for fresh data population"""
        try:
            # Disable foreign key checks temporarily
            await conn.execute("SET session_replication_role = replica;")
            
            # Clear tables in reverse order to handle foreign key constraints
            tables = ["cheques", "fd_rates", "loans", "disputes", "complaints", "atms", "branches", "transactions", "cards", "accounts"]
            
            for table in tables:
                try:
                    await conn.execute(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE")
                    logger.info(f"Cleared table: {table}")
                except Exception as e:
                    logger.warning(f"Could not clear table {table}: {e}")
            
            # Re-enable foreign key checks
            await conn.execute("SET session_replication_role = DEFAULT;")
            logger.info("All tables cleared successfully")
            
        except Exception as e:
            logger.error(f"Error clearing tables: {e}")
            # Re-enable foreign key checks even if there was an error
            try:
                await conn.execute("SET session_replication_role = DEFAULT;")
            except:
                pass

    async def _populate_initial_data(self, conn):
        """Populate tables with initial mock data from JSON files"""
        from mock_data_storage import mock_storage

        logger.info(
            "BankWise AI Banking Support API - Populating database with initial data from JSON files..."
        )

        # Insert accounts with all fields first
        valid_account_numbers = set()
        for account in mock_storage.accounts:
            try:
                await conn.execute(
                    """
                    INSERT INTO accounts (
                        account_number, account_type, balance, currency, customer_name,
                        customer_id, branch_code, ifsc_code, kyc_status, kyc_level,
                        last_updated, account_status, linked_cards, mobile_numbers
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14)
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
                    account.get("linked_cards", []),
                    account.get("mobile_numbers", []),
                )
                valid_account_numbers.add(account["account_number"])
            except Exception as e:
                logger.warning(f"Failed to insert account {account['account_number']}: {e}")

        # Insert cards with validation
        cards_inserted = 0
        cards_skipped = 0
        for card in mock_storage.cards:
            if card["account_number"] in valid_account_numbers:
                try:
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
                    cards_inserted += 1
                except Exception as e:
                    logger.warning(f"Failed to insert card {card['card_number']}: {e}")
                    cards_skipped += 1
            else:
                cards_skipped += 1
                logger.debug(f"Skipped card {card['card_number']} - invalid account number {card['account_number']}")

        logger.info(f"Inserted {cards_inserted} cards, skipped {cards_skipped} cards with invalid references")

        # Insert transactions (limit to prevent excessive data) with validation
        sample_transactions = mock_storage.transactions[:5000]  # Limit to 5000 for initial load
        transactions_inserted = 0
        transactions_skipped = 0
        for tx in sample_transactions:
            if tx["account_number"] in valid_account_numbers:
                try:
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
                    transactions_inserted += 1
                except Exception as e:
                    logger.warning(f"Failed to insert transaction {tx['id']}: {e}")
                    transactions_skipped += 1
            else:
                transactions_skipped += 1
                logger.debug(f"Skipped transaction {tx['id']} - invalid account number {tx['account_number']}")

        logger.info(f"Inserted {transactions_inserted} transactions, skipped {transactions_skipped} transactions with invalid references")

        # Insert branches (single facilities field)
        for branch in mock_storage.branches:
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
                branch["facilities"],  # Single string, not array
                branch["manager_name"],
                parse_datetime(branch["established_date"]),
            )

        # Insert ATMs (single facilities field)
        for atm in mock_storage.atms:
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
                atm["facilities"],  # Single string, not array
                parse_datetime(atm["last_maintenance"]),
                atm["status"],
            )

        # Insert complaints with validation
        complaints_inserted = 0
        complaints_skipped = 0
        for complaint in mock_storage.complaints:
            if complaint["account_number"] and complaint["account_number"] in valid_account_numbers:
                try:
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
                    complaints_inserted += 1
                except Exception as e:
                    logger.warning(f"Failed to insert complaint {complaint['ticket_id']}: {e}")
                    complaints_skipped += 1
            else:
                complaints_skipped += 1
                logger.debug(f"Skipped complaint {complaint['ticket_id']} - invalid account number {complaint.get('account_number')}")

        logger.info(f"Inserted {complaints_inserted} complaints, skipped {complaints_skipped} complaints with invalid references")

        # Insert disputes with validation
        disputes_inserted = 0
        disputes_skipped = 0
        for dispute in mock_storage.disputes:
            if dispute["account_number"] and dispute["account_number"] in valid_account_numbers:
                try:
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
                    disputes_inserted += 1
                except Exception as e:
                    logger.warning(f"Failed to insert dispute {dispute['ticket_id']}: {e}")
                    disputes_skipped += 1
            else:
                disputes_skipped += 1
                logger.debug(f"Skipped dispute {dispute['ticket_id']} - invalid account number {dispute.get('account_number')}")

        logger.info(f"Inserted {disputes_inserted} disputes, skipped {disputes_skipped} disputes with invalid references")

        # Insert loans with validation
        loans_inserted = 0
        loans_skipped = 0
        for loan in mock_storage.loans:
            if loan["account_number"] and loan["account_number"] in valid_account_numbers:
                try:
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
                    loans_inserted += 1
                except Exception as e:
                    logger.warning(f"Failed to insert loan {loan['loan_id']}: {e}")
                    loans_skipped += 1
            else:
                loans_skipped += 1
                logger.debug(f"Skipped loan {loan['loan_id']} - invalid account number {loan.get('account_number')}")

        logger.info(f"Inserted {loans_inserted} loans, skipped {loans_skipped} loans with invalid references")

        # Insert FD rates
        for rate in mock_storage.fd_rates:
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

        # Insert cheques with validation
        cheques_inserted = 0
        cheques_skipped = 0
        for cheque in mock_storage.cheques:
            if cheque["account_number"] in valid_account_numbers:
                try:
                    await conn.execute(
                        """
                        INSERT INTO cheques (
                            cheque_number, account_number, amount, status, issue_date,
                            clearing_date, payee_name
                        ) VALUES ($1, $2, $3, $4, $5, $6, $7)
                    """,
                        cheque["cheque_number"],
                        cheque["account_number"],
                        cheque["amount"],
                        cheque["status"],
                        parse_datetime(cheque["issue_date"]),
                        parse_datetime(cheque["clearing_date"]),
                        cheque["payee_name"],
                    )
                    cheques_inserted += 1
                except Exception as e:
                    logger.warning(f"Failed to insert cheque {cheque['cheque_number']}: {e}")
                    cheques_skipped += 1
            else:
                cheques_skipped += 1
                logger.debug(f"Skipped cheque {cheque['cheque_number']} - invalid account number {cheque['account_number']}")

        logger.info(f"Inserted {cheques_inserted} cheques, skipped {cheques_skipped} cheques with invalid references")

        logger.info(
            f"BankWise AI Banking Support API - Database populated with {len(valid_account_numbers)} accounts, "
            f"{cards_inserted} cards, {transactions_inserted} transactions (limited), "
            f"{len(mock_storage.branches)} branches, {len(mock_storage.atms)} ATMs, "
            f"{complaints_inserted} complaints, {disputes_inserted} disputes, "
            f"{loans_inserted} loans, {len(mock_storage.fd_rates)} FD rates, "
            f"and {cheques_inserted} cheques"
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
