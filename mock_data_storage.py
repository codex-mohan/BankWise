import orjson
import os
import random
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import logging
from faker import Faker

fake = Faker('en_IN')

logger = logging.getLogger(__name__)


class MockDataStorage:
    """Handles persistent storage of mock data in JSON files"""

    def __init__(self, data_dir: str = "mock_data"):
        self.data_dir = data_dir
        self.data_files = {
            "accounts": "accounts.json",
            "cards": "cards.json",
            "transactions": "transactions.json",
            "branches": "branches.json",
            "atms": "atms.json",
            "complaints": "complaints.json",
            "disputes": "disputes.json",
            "loans": "loans.json",
            "fd_rates": "fd_rates.json",
            "cheques": "cheques.json",
        }
        self.ensure_data_directory()
        self.load_or_create_data()

    def ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            logger.info(f"Created mock data directory: {self.data_dir}")

    def load_or_create_data(self):
        """Load data from JSON files or create new data"""
        try:
            self.accounts = (
                self._load_json_file("accounts") or self._generate_accounts()
            )
            self.cards = self._load_json_file("cards") or self._generate_cards()
            self.transactions = (
                self._load_json_file("transactions") or self._generate_transactions()
            )
            self.branches = (
                self._load_json_file("branches") or self._generate_branches()
            )
            self.atms = self._load_json_file("atms") or self._generate_atms()
            self.complaints = (
                self._load_json_file("complaints") or self._generate_complaints()
            )
            self.disputes = (
                self._load_json_file("disputes") or self._generate_disputes()
            )
            self.loans = self._load_json_file("loans") or self._generate_loans()
            self.fd_rates = (
                self._load_json_file("fd_rates") or self._generate_fd_rates()
            )
            self.cheques = self._load_json_file("cheques") or self._generate_cheques()

            # Save all data to ensure we have files
            self.save_all_data()

            logger.info("Mock data loaded from JSON files or generated successfully")

        except Exception as e:
            logger.error(f"Error loading mock data: {e}")
            # Fallback to generating all data
            self.accounts = self._generate_accounts()
            self.cards = self._generate_cards()
            self.transactions = self._generate_transactions()
            self.branches = self._generate_branches()
            self.atms = self._generate_atms()
            self.complaints = self._generate_complaints()
            self.disputes = self._generate_disputes()
            self.loans = self._generate_loans()
            self.fd_rates = self._generate_fd_rates()
            self.cheques = self._generate_cheques()
            self.save_all_data()

    def _load_json_file(self, data_type: str) -> Optional[List[Dict]]:
        """Load data from JSON file using orjson for better performance"""
        file_path = os.path.join(self.data_dir, self.data_files[data_type])
        if os.path.exists(file_path):
            try:
                with open(file_path, "rb") as f:  # orjson requires binary mode
                    data = orjson.loads(f.read())
                    logger.info(f"Loaded {len(data)} {data_type} records from JSON")
                    return data
            except Exception as e:
                logger.error(f"Error loading {data_type} from JSON: {e}")
                return None
        return None

    def _save_json_file(self, data_type: str, data: List[Dict]):
        """Save data to JSON file using orjson for better performance"""
        file_path = os.path.join(self.data_dir, self.data_files[data_type])
        try:
            # orjson.dumps returns bytes, write in binary mode
            json_data = orjson.dumps(data, option=orjson.OPT_INDENT_2)
            with open(file_path, "wb") as f:
                f.write(json_data)
            logger.info(f"Saved {len(data)} {data_type} records to JSON")
        except Exception as e:
            logger.error(f"Error saving {data_type} to JSON: {e}")

    def save_all_data(self):
        """Save all data to JSON files"""
        self._save_json_file("accounts", self.accounts)
        self._save_json_file("cards", self.cards)
        self._save_json_file("transactions", self.transactions)
        self._save_json_file("branches", self.branches)
        self._save_json_file("atms", self.atms)
        self._save_json_file("complaints", self.complaints)
        self._save_json_file("disputes", self.disputes)
        self._save_json_file("loans", self.loans)
        self._save_json_file("fd_rates", self.fd_rates)
        self._save_json_file("cheques", self.cheques)

    def _generate_accounts(self) -> List[Dict]:
        """Generate mock account data"""
        accounts = []
        account_types = ["Savings", "Current", "Salary"]

        for i in range(20):
            account_number = (
                f"{random.randint(1000, 9999)}{random.randint(10000000, 99999999)}"
            )
            # Generate mobile numbers list (1-3 numbers per account)
            mobile_numbers = []
            for _ in range(random.randint(1, 3)):
                mobile_numbers.append(f"+91{random.randint(7000000000, 9999999999)}")
            
            account = {
                "account_number": account_number,
                "account_type": random.choice(account_types),
                "balance": round(random.uniform(1000, 1000000), 2),
                "currency": "INR",
                "customer_name": fake.name(),
                "customer_id": f"CUST{random.randint(10000, 99999)}",
                "branch_code": f"BRANCH{random.randint(100, 999)}",
                "ifsc_code": f"BARB{random.randint(1000, 9999)}",
                "kyc_status": random.choice(["VERIFIED", "PENDING", "UNDER_REVIEW"]),
                "kyc_level": random.choice(["LEVEL_1", "LEVEL_2", "LEVEL_3"]),
                "last_updated": (
                    datetime.now() - timedelta(days=random.randint(1, 365))
                ).isoformat(),
                "account_status": random.choice(["ACTIVE", "INACTIVE", "FROZEN"]),
                "linked_cards": [
                    f"****{random.randint(1000, 9999)}"
                    for _ in range(random.randint(1, 3))
                ],
                "mobile_numbers": mobile_numbers,
            }
            accounts.append(account)

        return accounts

    def _generate_cards(self) -> List[Dict]:
        """Generate mock card data"""
        cards = []
        card_types = ["VISA", "MASTERCARD", "RUPAY"]
        card_networks = ["CREDIT", "DEBIT"]

        for account in self.accounts:
            for _ in range(random.randint(1, 3)):
                card_number = f"****{random.randint(1000, 9999)}"
                card = {
                    "card_number": card_number,
                    "account_number": account["account_number"],
                    "card_type": random.choice(card_types),
                    "card_network": random.choice(card_networks),
                    "expiry_date": f"{random.randint(1, 12)}/{random.randint(25, 30)}",
                    "cvv": f"{random.randint(100, 999)}",
                    "card_status": random.choice(
                        ["ACTIVE", "BLOCKED", "EXPIRED", "LOST"]
                    ),
                    "daily_limit": round(random.uniform(50000, 500000), 2),
                    "monthly_limit": round(random.uniform(200000, 2000000), 2),
                    "international_usage": random.choice(["ALLOWED", "BLOCKED"]),
                    "contactless": random.choice(["YES", "NO"]),
                    "issue_date": (
                        datetime.now() - timedelta(days=random.randint(30, 1095))
                    ).isoformat(),
                    "customer_name": account["customer_name"],
                }
                cards.append(card)

        return cards

    def _generate_transactions(self) -> List[Dict]:
        """Generate mock transaction data"""
        transactions = []
        transaction_types = [
            "DEPOSIT",
            "WITHDRAWAL",
            "TRANSFER",
            "PURCHASE",
            "CASHBACK",
            "INTEREST",
        ]
        merchants = [
            "Amazon",
            "Flipkart",
            "Walmart",
            "Target",
            "Starbucks",
            "McDonalds",
            "Uber",
            "Swiggy",
        ]

        for account in self.accounts:
            # Generate 50-200 transactions per account
            num_transactions = random.randint(1, 3)
            for i in range(num_transactions):
                transaction_date = datetime.now() - timedelta(
                    days=random.randint(1, 730)
                )
                transaction_type = random.choice(transaction_types)

                if transaction_type == "TRANSFER":
                    description = f"Transfer to {fake.name()}"
                    amount = round(random.uniform(100, 50000), 2)
                elif transaction_type == "PURCHASE":
                    description = f"Purchase at {random.choice(merchants)}"
                    amount = round(random.uniform(50, 10000), 2)
                elif transaction_type == "DEPOSIT":
                    description = "Salary Credit"
                    amount = round(random.uniform(10000, 100000), 2)
                elif transaction_type == "WITHDRAWAL":
                    description = "ATM Withdrawal"
                    amount = round(random.uniform(100, 20000), 2)
                else:
                    description = f"{transaction_type} Credit"
                    amount = round(random.uniform(10, 1000), 2)

                # Calculate running balance
                balance_after = (
                    account["balance"] - amount
                    if transaction_type in ["WITHDRAWAL", "TRANSFER", "PURCHASE"]
                    else account["balance"] + amount
                )

                transaction = {
                    "id": f"TXN{random.randint(1000000, 9999999)}",
                    "account_number": account["account_number"],
                    "transaction_date": transaction_date.isoformat(),
                    "description": description,
                    "amount": amount,
                    "type": transaction_type,
                    "balance_after": balance_after,
                    "status": random.choice(["COMPLETED", "PENDING", "FAILED"]),
                    "reference_id": f"REF{random.randint(10000, 99999)}",
                    "merchant_id": (
                        random.choice(merchants)
                        if transaction_type == "PURCHASE"
                        else None
                    ),
                    "location": fake.city() if transaction_type == "PURCHASE" else None,
                }
                transactions.append(transaction)

        return transactions

    def _generate_branches(self) -> List[Dict]:
        """Generate mock branch data"""
        branches = []
        cities = [
            "Mumbai",
            "Delhi",
            "Bangalore",
            "Hyderabad",
            "Chennai",
            "Kolkata",
            "Pune",
            "Ahmedabad",
            "Jaipur",
            "Lucknow",
        ]

        for city in cities:
            for i in range(random.randint(2, 5)):
                branch = {
                    "name": f"BOB {city} {random.choice(['Main', 'Branch', 'Road', 'Center'])}",
                    "address": fake.street_address(),
                    "city": city,
                    "pincode": f"{random.randint(110000, 500000)}",
                    "ifsc": f"BARB{random.randint(1000, 9999)}",
                    "latitude": random.uniform(18, 28),
                    "longitude": random.uniform(72, 88),
                    "phone": f"{random.randint(2000, 9999)}{random.randint(100000, 999999)}",
                    "email": f"branch{random.randint(100, 999)}@bob.com",
                    "working_hours": "9:30 AM - 4:30 PM",
                    "branch_type": random.choice(
                        ["FULL_SERVICE", "ATM_ONLY", "BUSINESS_CENTER"]
                    ),
                    "facilities": random.choice(
                        ["ATM", "LOCKER", "FOREX", "NET_BANKING", "MOBILE_BANKING"]
                    ),
                    "manager_name": fake.name(),
                    "established_date": (
                        datetime.now() - timedelta(days=random.randint(3650, 18250))
                    ).isoformat(),
                }
                branches.append(branch)

        return branches

    def _generate_atms(self) -> List[Dict]:
        """Generate mock ATM data"""
        atms = []
        banks = [
            "Bank of Baroda",
            "State Bank of India",
            "HDFC Bank",
            "ICICI Bank",
            "Punjab National Bank",
        ]
        cities = [
            "Mumbai",
            "Delhi",
            "Bangalore",
            "Hyderabad",
            "Chennai",
            "Kolkata",
            "Pune",
            "Ahmedabad",
            "Jaipur",
            "Lucknow",
        ]

        for city in cities:
            for i in range(random.randint(5, 15)):
                atm = {
                    "id": f"ATM{random.randint(10000, 99999)}",
                    "address": fake.street_address(),
                    "city": city,
                    "pincode": f"{random.randint(110000, 500000)}",
                    "bank_name": random.choice(banks),
                    "latitude": random.uniform(18, 28),
                    "longitude": random.uniform(72, 88),
                    "type": random.choice(["ON_SITE", "OFF_SITE"]),
                    "24x7": random.choice(["YES", "NO"]),
                    "facilities": random.choice(
                        [
                            "CASH_DEPOSIT",
                            "CASH_WITHDRAWAL",
                            "BALANCE_ENQUIRY",
                            "MINI_STATEMENT",
                            "CARD_RENEWAL",
                        ]
                    ),
                    "last_maintenance": (
                        datetime.now() - timedelta(days=random.randint(1, 90))
                    ).isoformat(),
                    "status": random.choice(
                        ["ACTIVE", "OUT_OF_SERVICE", "MAINTENANCE"]
                    ),
                }
                atms.append(atm)

        return atms

    def _generate_complaints(self) -> List[Dict]:
        """Generate mock complaint data"""
        complaints = []
        categories = [
            "ACCOUNT",
            "CARD",
            "TRANSACTION",
            "ATM",
            "BRANCH",
            "LOAN",
            "FD",
            "NET_BANKING",
            "MOBILE_BANKING",
            "OTHER",
        ]
        statuses = ["OPEN", "IN_PROGRESS", "RESOLVED", "CLOSED", "ESCALATED"]

        for i in range(50):
            complaint_date = datetime.now() - timedelta(days=random.randint(1, 365))
            resolved_date = None
            if random.random() < 0.7:  # 70% resolved
                resolved_date = complaint_date + timedelta(days=random.randint(1, 30))

            complaint = {
                "ticket_id": f"COMPLAINT{random.randint(10000, 99999)}",
                "account_number": random.choice(self.accounts)["account_number"],
                "subject": f"Complaint regarding {random.choice(categories)}",
                "description": fake.text(max_nb_chars=200),
                "category": random.choice(categories),
                "status": random.choice(statuses),
                "priority": random.choice(["LOW", "MEDIUM", "HIGH", "URGENT"]),
                "created_at": complaint_date.isoformat(),
                "resolved_at": resolved_date.isoformat() if resolved_date else None,
                "estimated_resolution_days": random.randint(1, 15),
                "assigned_agent": (
                    f"AGENT{random.randint(100, 999)}"
                    if random.random() < 0.8
                    else None
                ),
                "resolution_notes": (
                    fake.text(max_nb_chars=100) if resolved_date else None
                ),
                "customer_satisfaction": (
                    random.randint(1, 5) if resolved_date else None
                ),
            }
            complaints.append(complaint)

        return complaints

    def _generate_disputes(self) -> List[Dict]:
        """Generate mock dispute data"""
        disputes = []
        dispute_types = [
            "FRAUD",
            "UNAUTHORIZED",
            "BILLING_ERROR",
            "SERVICE_CHARGE",
            "OTHER",
        ]
        statuses = ["OPEN", "UNDER_REVIEW", "APPROVED", "REJECTED", "RESOLVED"]

        for i in range(30):
            dispute_date = datetime.now() - timedelta(days=random.randint(1, 90))
            resolved_date = None
            if random.random() < 0.6:  # 60% resolved
                resolved_date = dispute_date + timedelta(days=random.randint(3, 45))

            dispute = {
                "ticket_id": f"DISPUTE{random.randint(10000, 99999)}",
                "account_number": random.choice(self.accounts)["account_number"],
                "transaction_id": f"TXN{random.randint(1000000, 9999999)}",
                "amount": round(random.uniform(100, 50000), 2),
                "transaction_date": (
                    datetime.now() - timedelta(days=random.randint(1, 30))
                ).isoformat(),
                "dispute_type": random.choice(dispute_types),
                "reason": fake.sentence(),
                "description": fake.text(max_nb_chars=150),
                "status": random.choice(statuses),
                "created_at": dispute_date.isoformat(),
                "resolved_at": resolved_date.isoformat() if resolved_date else None,
                "estimated_resolution_days": random.randint(5, 30),
                "assigned_officer": (
                    f"OFFICER{random.randint(100, 999)}"
                    if random.random() < 0.7
                    else None
                ),
                "resolution_notes": (
                    fake.text(max_nb_chars=100) if resolved_date else None
                ),
                "evidence_submitted": random.choice(["YES", "NO"]),
                "customer_contacted": random.choice(["YES", "NO"]),
            }
            disputes.append(dispute)

        return disputes

    def _generate_loans(self) -> List[Dict]:
        """Generate mock loan data"""
        loans = []
        loan_types = [
            "HOME_LOAN",
            "PERSONAL_LOAN",
            "CAR_LOAN",
            "EDUCATION_LOAN",
            "GOLD_LOAN",
            "BUSINESS_LOAN",
        ]
        statuses = ["DISBURSED", "ACTIVE", "COMPLETED", "DEFAULT", "CLOSED"]

        for i in range(40):
            disbursement_date = datetime.now() - timedelta(
                days=random.randint(30, 3650)
            )
            tenure_months = random.randint(12, 360)
            emi_start_date = disbursement_date + timedelta(days=30)

            loan = {
                "loan_id": f"LN{random.randint(10000, 99999)}",
                "account_number": random.choice(self.accounts)["account_number"],
                "loan_type": random.choice(loan_types),
                "principal": round(random.uniform(50000, 10000000), 2),
                "interest_rate": round(random.uniform(7.5, 15.5), 2),
                "tenure_months": tenure_months,
                "emi_amount": round(random.uniform(1000, 100000), 2),
                "disbursement_date": disbursement_date.isoformat(),
                "emi_start_date": emi_start_date.isoformat(),
                "next_emi_date": (emi_start_date + timedelta(days=30)).isoformat(),
                "total_emis": tenure_months,
                "paid_emis": random.randint(0, tenure_months - 1),
                "remaining_tenure": tenure_months
                - random.randint(0, tenure_months - 1),
                "status": random.choice(statuses),
                "collateral_details": (
                    fake.text(max_nb_chars=100) if random.random() < 0.7 else None
                ),
                "processing_fee": round(random.uniform(1000, 50000), 2),
                "insurance_details": (
                    fake.text(max_nb_chars=50) if random.random() < 0.6 else None
                ),
            }
            loans.append(loan)

        return loans

    def _generate_fd_rates(self) -> List[Dict]:
        """Generate mock fixed deposit rates"""
        fd_rates = []
        tenures = [7, 14, 30, 45, 60, 90, 120, 180, 365, 730, 1095, 1825, 3650]
        customer_types = ["NORMAL", "SENIOR_CITIZEN"]

        for tenure in tenures:
            for customer_type in customer_types:
                rate = round(random.uniform(3.5, 8.5), 2)
                if customer_type == "SENIOR_CITIZEN":
                    rate += 0.5  # Senior citizens get 0.5% extra

                fd_rate = {
                    "tenure": tenure,
                    "rate": rate,
                    "customer_type": customer_type,
                    "min_amount": 10000,
                    "max_amount": 10000000,
                    "currency": "INR",
                    "last_updated": datetime.now().isoformat(),
                    "special_features": random.choice(
                        [
                            "TAX_SAVING",
                            "MONTHLY_PAYOUT",
                            "QUARTERLY_PAYOUT",
                            "CUMULATIVE",
                        ]
                    ),
                }
                fd_rates.append(fd_rate)

        return fd_rates

    def _generate_cheques(self) -> List[Dict]:
        """Generate mock cheque data"""
        cheques = []
        statuses = ["Cleared", "Pending", "Bounced", "Under Process"]

        for account in self.accounts:
            for _ in range(random.randint(1, 3)):
                status = random.choice(statuses)
                issue_date = datetime.now() - timedelta(days=random.randint(1, 365))
                clearing_date = None
                if status == "Cleared":
                    clearing_date = issue_date + timedelta(days=random.randint(1, 5))

                cheque = {
                    "cheque_number": f"{random.randint(100000, 999999)}",
                    "account_number": account["account_number"],
                    "amount": round(random.uniform(1000, 50000), 2),
                    "status": status,
                    "issue_date": issue_date.isoformat(),
                    "clearing_date": clearing_date.isoformat() if clearing_date else None,
                    "payee_name": fake.name(),
                }
                cheques.append(cheque)

        return cheques

    def get_account_by_number(self, account_number: str) -> Optional[Dict]:
        """Get account by account number"""
        for account in self.accounts:
            if account["account_number"] == account_number:
                return account
        return None

    def get_card_by_last4(self, last4: str) -> Optional[Dict]:
        """Get card by last 4 digits"""
        for card in self.cards:
            if card["card_number"].endswith(last4):
                return card
        return None

    def get_transactions_by_account(
        self, account_number: str, limit: int = 5
    ) -> List[Dict]:
        """Get transactions for an account"""
        account_transactions = [
            t for t in self.transactions if t["account_number"] == account_number
        ]
        # Sort by date (newest first)
        account_transactions.sort(key=lambda x: x["transaction_date"], reverse=True)
        return account_transactions[:limit]

    def get_branches_by_city(self, city: str, limit: int = 3) -> List[Dict]:
        """Get branches by city"""
        city_branches = [b for b in self.branches if b["city"].lower() == city.lower()]
        return city_branches[:limit]

    def get_atms_by_pincode(self, pincode: str, limit: int = 3) -> List[Dict]:
        """Get ATMs by pincode"""
        pincode_atms = [a for a in self.atms if a["pincode"] == pincode]
        return pincode_atms[:limit]

    def get_complaint_by_id(self, ticket_id: str) -> Optional[Dict]:
        """Get complaint by ticket ID"""
        for complaint in self.complaints:
            if complaint["ticket_id"] == ticket_id:
                return complaint
        return None

    def get_dispute_by_id(self, ticket_id: str) -> Optional[Dict]:
        """Get dispute by ticket ID"""
        for dispute in self.disputes:
            if dispute["ticket_id"] == ticket_id:
                return dispute
        return None

    def get_loan_by_id(self, loan_id: str) -> Optional[Dict]:
        """Get loan by loan ID"""
        for loan in self.loans:
            if loan["loan_id"] == loan_id:
                return loan
        return None

    def get_fd_rates(self, tenure: Optional[int] = None) -> List[Dict]:
        """Get FD rates, optionally filtered by tenure"""
        if tenure:
            return [r for r in self.fd_rates if r["tenure"] == tenure]
        return self.fd_rates

    def get_cheque_by_number(self, cheque_number: str) -> Optional[Dict]:
        """Get cheque by cheque number"""
        for cheque in self.cheques:
            if cheque["cheque_number"] == cheque_number:
                return cheque
        return None

    def add_complaint(self, complaint_data: Dict) -> Dict:
        """Add a new complaint"""
        complaint_data["ticket_id"] = f"COMPLAINT{random.randint(10000, 99999)}"
        complaint_data["created_at"] = datetime.now().isoformat()
        complaint_data["status"] = "OPEN"
        complaint_data["priority"] = "MEDIUM"
        self.complaints.append(complaint_data)
        self._save_json_file("complaints", self.complaints)
        return complaint_data

    def add_dispute(self, dispute_data: Dict) -> Dict:
        """Add a new dispute"""
        dispute_data["ticket_id"] = f"DISPUTE{random.randint(10000, 99999)}"
        dispute_data["created_at"] = datetime.now().isoformat()
        dispute_data["status"] = "OPEN"
        self.disputes.append(dispute_data)
        self._save_json_file("disputes", self.disputes)
        return dispute_data


# Initialize the storage
mock_storage = MockDataStorage()
