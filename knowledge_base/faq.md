# Frequently Asked Questions (FAQ)

This document serves as a guideline for the AI agent to provide comprehensive support to customers, using plain language and a supportive tone. It outlines common customer questions and how the agent can facilitate or inform about actions within the defined scenarios.

**Important Note:** The responses below describe the *types of actions* the AI agent can take or the *information it can access*. They do not use specific internal tool or API names, as these are subject to change in a production environment.

## 1. Account & Transaction Information (Scenario Type: `account_info`, `tx_history`)

### Q1: How can I check my account balance?
- **A:** I can access your account information to provide your balance. Please provide your account number or the last four digits of your card.
  - **Example Action:** The agent would conceptually perform an 'account_info' action to retrieve the balance.

### Q2: How can I view my recent transactions?
- **A:** I can retrieve your recent transaction history. Please provide your account number or the last four digits of your card.
  - **Example Action:** The agent would conceptually perform a 'tx_history' action to fetch transactions.

### Q3: What should I do if I see an unauthorized transaction?
- **A:** If you notice any unauthorized transaction, I can assist you in initiating a dispute. Please provide the transaction details (amount, date, merchant) so I can proceed.
  - **Example Action:** The agent would conceptually perform a 'raise_dispute' action.

## 2. Card Services (Scenario Type: `card_block`)

### Q4: How do I hotlist or block my lost/stolen debit or credit card?
- **A:** I can process a request to block your card immediately to prevent any unauthorized use. Please confirm the last four digits of your card number.
  - **Example Action:** The agent would conceptually perform a 'card_block' action.

### Q5: How can I request a replacement for my damaged or hotlisted card?
- **A:** After a card is blocked, I can arrange for a replacement card to be dispatched to your registered address.
  - **Example Action:** The agent would conceptually perform a 'card_replacement' action (if supported by the mock API).

### Q6: My debit/credit card is expiring soon. How do I get a new one?
- **A:** A new card will be automatically dispatched to your registered address approximately one month before your current card expires. If you don't receive it, I can assist you in checking its status.
  - **Example Action:** The agent would conceptually perform a 'card_status_check' action.

## 3. Disputes & Complaints (Scenario Type: `raise_dispute`, `complaint_new`, `complaint_status`)

### Q7: How do I initiate a dispute or chargeback for a transaction?
- **A:** I can initiate a dispute for a transaction. Please provide the transaction details (amount, date, merchant) so I can proceed.
  - **Example Action:** The agent would conceptually perform a 'raise_dispute' action.

### Q8: How can I register a new complaint?
- **A:** I can register a new complaint for you. Please describe your issue, and I will provide you with a ticket ID for tracking.
  - **Example Action:** The agent would conceptually perform a 'complaint_new' action.

### Q9: How can I check the status of my existing complaint?
- **A:** I can check the status of your complaint. Please provide your ticket ID.
  - **Example Action:** The agent would conceptually perform a 'complaint_status' action.

## 4. Locators (Branch & ATM) (Scenario Type: `locate_branch`, `locate_atm`)

### Q10: How can I find the nearest Mauryan Bank branch?
- **A:** I can help you find the nearest Mauryan Bank branch by accessing location data. Please provide the city or pincode you are interested in.
  - **Example Action:** The agent would conceptually perform a 'locate_branch' action.

### Q11: How can I find the nearest Mauryan Bank ATM?
- **A:** I can help you find the nearest Mauryan Bank ATM by accessing location data. Please provide the city or pincode you are interested in.
  - **Example Action:** The agent would conceptually perform a 'locate_atm' action.

## 5. KYC & Document Status (Scenario Type: `kyc_status`)

### Q12: How can I check my KYC (Know Your Customer) status?
- **A:** I can check your KYC status by accessing your account information. Please provide your account number.
  - **Example Action:** The agent would conceptually perform a 'kyc_status' action.

### Q13: What documents are required for KYC update?
- **A:** For KYC updates, you typically need a valid proof of identity (e.g., Aadhaar, PAN, Passport) and proof of address (e.g., Aadhaar, utility bill). I can provide information on the required documents and the process.
  - **Example Action:** The agent would conceptually access 'kyc_document_info' (information retrieval).

## 6. Cheque Services (Scenario Type: `cheque_status`)

### Q14: How can I check the status of a cheque I issued or deposited?
- **A:** I can check the status of any cheque by accessing cheque processing information. Please provide the cheque number.
  - **Example Action:** The agent would conceptually perform a 'cheque_status' action.

### Q15: Can I stop payment for a cheque?
- **A:** Yes, I can initiate a stop payment for an uncashed cheque by processing your request. Please provide the cheque number and account details. Applicable charges may apply.
  - **Example Action:** The agent would conceptually perform a 'stop_cheque_payment' action.

## 7. Fixed Deposit (FD) Information (Scenario Type: `fd_rate_info`)

### Q16: What are the current interest rates for Fixed Deposits?
- **A:** I can provide you with the current Fixed Deposit interest rates by accessing our product information. Please specify the tenure you are interested in, or I can provide a general overview.
  - **Example Action:** The agent would conceptually perform an 'fd_rate_info' action.

### Q17: Can I prematurely withdraw my Fixed Deposit?
- **A:** Yes, premature withdrawal of Fixed Deposits is allowed, but it may be subject to a penalty as per bank policy. I can provide more details if you wish.
  - **Example Action:** The agent would conceptually access 'fd_withdrawal_policy' (information retrieval).

## 8. Loan Status & Payment Options (Scenario Type: `loan_status`)

### Q18: How can I check the status of my loan application?
- **A:** I can track your loan application status by accessing loan records. Please provide your loan application reference number.
  - **Example Action:** The agent would conceptually perform a 'loan_status' action.

### Q19: What are the available payment options for my loan EMIs?
- **A:** I can provide information on available payment options for your loan EMIs by accessing loan product details. Please specify your loan type.
  - **Example Action:** The agent would conceptually access 'loan_payment_options' (information retrieval).

### Q20: How can I get a No Objection Certificate (NOC) for my closed loan?
- **A:** I can assist you in requesting a No Objection Certificate (NOC) for your closed loan by processing your request. Please provide your loan account details.
  - **Example Action:** The agent would conceptually perform a 'request_loan_noc' action.
