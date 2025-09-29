# Knowledge Base: Mauryan Bank

This document provides a comprehensive knowledge base for the LLM about Mauryan Bank.

## 1. General Information

- **Bank Name:** Mauryan Bank
- **Headquarters:** Mumbai, Maharashtra, India
- **Tagline:** "Your Financial Fortress"
- **Timings:** 9:30 AM to 5:30 PM
- **Open Hours:** 10:00 AM to 4:00 PM (for customer transactions)
- **Closing Hours:** 5:30 PM
- **Number of Employees:** Approximately 1,200
- **Physical Receptionist:** Available at all branches during open hours.

## 2. History

Mauryan Bank was established in 2023 with a vision to merge traditional Indian values of trust and security with modern financial technology. The name "Mauryan" is inspired by the ancient Mauryan Empire, known for its economic prosperity and robust administrative systems. The bank aims to build a financial fortress for its customers, ensuring their wealth is protected and grows.

## 3. Branch & ATM Locations

Mauryan Bank has a strong presence in major metropolitan areas. All branches are equipped with 24/7 ATM facilities.

- **Mumbai - Fort Branch (Head Office)**
  - **Address:** 123, Mauryan Towers, Fort, Mumbai, Maharashtra 400001
  - **IFSC Code:** MAUR0000001
  - **Services:** Full-service branch, Wealth Management specialists available.
- **Delhi - Connaught Place Branch**
  - **Address:** A-1, Inner Circle, Connaught Place, New Delhi, Delhi 110001
  - **IFSC Code:** MAUR0000002
  - **Services:** Full-service branch, SME & Corporate Banking desk.
- **Bengaluru - Koramangala Branch**
  - **Address:** 456, 5th Block, Koramangala, Bengaluru, Karnataka 560095
  - **IFSC Code:** MAUR0000003
  - **Services:** Full-service branch, Tech hub with digital banking support.
- **Chennai - T. Nagar Branch**
  - **Address:** 789, Usman Road, T. Nagar, Chennai, Tamil Nadu 600017
  - **IFSC Code:** MAUR0000004
  - **Services:** Full-service branch, Gold loan services available.

## 4. Services & Products

### Personal Banking

- **Savings Accounts:** Including high-yield and zero-balance options.
- **Current Accounts:** For individuals and businesses.
- **Fixed and Recurring Deposits:** Competitive interest rates.
- **Loans:** Personal, Home, and Car Loans.
- **Wealth Management:** Financial advisory and portfolio management services.

### Digital Banking

- **Net Banking:** State-of-the-art online portal.
- **"Mauryan Money" Mobile App:** Includes UPI, bill payments, and investment tracking.
- **AI Chatbot "Chanakya":** 24/7 AI-powered assistant for customer support.

### Cards

- **Debit and Credit Cards:** A wide range of cards with tailored benefits and offers.
- **Mauryan Sapphire Credit Card:** 5% cashback on travel/dining, unlimited lounge access.
- **Mauryan Gold Credit Card:** 2% cashback on all online purchases.
- **Debit Card Offers:** Up to 20% discount at over 10,000 partner merchants, complimentary insurance cover.

## 5. Customer Procedures

### Account Opening

1.  **e-KYC:** Instant account opening via the mobile app using Aadhaar.
2.  **In-Branch:** Visit any branch with your PAN card, Aadhaar card, and a recent photograph.
3.  **Welcome Kit:** Delivered to your address within 7 working days.

### Loan Application

1.  **Online Portal:** Apply and track your application on our website or mobile app.
2.  **Loan Advisors:** Get expert guidance at any branch.
3.  **Quick Disbursal:** Streamlined process for fast loan disbursal.

## 6. AI Banking Assistant: Chanakya (LLM Technical Details)

This section provides technical details for the LLM to understand the underlying structure of Chanakya's dialogue system.

### Supported Scenarios

1.  **Account Information:** Balance and recent transactions.
2.  **Card Services:** Hotlist a lost/stolen card and request a replacement.
3.  **Dispute Management:** Initiate a dispute or chargeback.
4.  **Complaints:** Register a new complaint or check the status of an existing one.
5.  **Locators:** Find the nearest branch or ATM.
6.  **KYC Status:** Check the status of KYC documents.
7.  **Cheque Services:** Inquire about the status of a cheque.
8.  **Deposit Information:** Get details on fixed deposit interest rates.
9.  **Loan Services:** Check loan application status and payment options.
10. **Human Escalation:** Seamlessly transfer to a live agent.

### Canonical Intents

- `AccountBalanceAction`: For balance and transaction history.
- `GetTransactionHistoryAction`: For recent transactions.
- `BlockCard`: To block a debit or credit card.
- `RaiseTransactionDisputeAction`: To raise a dispute for a transaction.
- `NewComplaintAction`: To register a new complaint.
- `ComplaintStatusAction`: To check the status of an existing complaint.
- `LocateBranchAction`: To find a branch.
- `LocateATMAction`: To find an ATM.
- `CheckKYCStatusAction`: To check KYC status.
- `CheckChequeStatusAction`: To check the status of a cheque.
- `GetAllFDRatesAction`: To get information on fixed deposit rates.
- `GetFDRatesByTenureAction`: To get information on fixed deposit rates for a specific tenure.
- `GetLoanStatusAction`: To check the status of a loan.
- `escalate_to_agent`: To request a transfer to a human agent.

### Canonical Entities

- `account_number`: The customer's bank account number.
- `last4`: The last four digits of a debit or credit card.
- `transaction_date`: The date of a transaction.
- `amount`: The transaction amount.
- `branch_city`: The city where a branch is located.
- `pincode`: The pincode for locating branches or ATMs.
- `ifsc`: The IFSC code of a branch.
- `ticket_id`: The ID for a complaint or service request.
- `language_pref`: The customer's preferred language (e.g., English, Hindi).
- `channel`: The communication channel (e.g., voice, chat).

### Knowledge Base Correlation and Refinement

This section maps the detailed information from `banking_details.md` to the specific, actionable intents supported by the backend API.

- **`AccountBalanceAction` & `GetTransactionHistoryAction`:** When providing balance, reference the account types in `banking_details.md`. After providing history, mention related features like the "Mauryan Money" app.
- **`GetLoanStatusAction`:** Handle specific loan queries conversationally using knowledge from `banking_details.md` before calling the API for the status.
- **`BlockCard`:** After blocking a card, proactively inform the user that a new card will be issued and that they can use the mobile app for digital payments in the meantime.
- **General Queries & Unhandled Intents:** For topics in `banking_details.md` without a direct API intent (e.g., wealth management), provide a conversational answer and then guide the user to a supported action, like finding a branch (`LocateBranchAction`) or escalate to a human.
