# Frequently Asked Questions (FAQ)

This document serves as a guideline for the AI agent to provide comprehensive support to customers, using plain language and a supportive tone. It outlines common customer questions and how the agent can facilitate or inform about actions within the defined scenarios.

**Important Note:** The responses below describe the _types of actions_ the AI agent can take or the _information it can access_. They do not use specific internal tool or API names, as these are subject to change in a production environment.

## 1. Account & Transaction Information (Scenario Type: `account_info`, `tx_history`)

### Q1: How can I check my account balance?

- **A:** I can retrieve your account balance. To proceed, please provide your account number.
  - **Example Action:** This requires the `account_info` tool. The agent must collect the `account_number` before calling the tool.

### Q2: How can I view my recent transactions?

- **A:** I can fetch your recent transaction history. Please provide your account number.
  - **Example Action:** This requires the `tx_history` tool. The agent must collect the `account_number`.

### Q3: What should I do if I see an unauthorized transaction?

- **A:** I can help you raise a dispute for an unauthorized transaction. Please provide the transaction amount and date.
  - **Example Action:** This requires the `raise_dispute` tool. The agent must collect `amount` and `transaction_date`.

## 2. Card Services (Scenario Type: `card_block`)

### Q4: How do I hotlist or block my lost/stolen debit or credit card?

- **A:** I can block your card immediately to prevent misuse. Please provide the last four digits of the card number.
  - **Example Action:** This requires the `card_block` tool. The agent must collect the `last4` digits.

### Q5: How can I request a replacement for my damaged or hotlisted card?

- **A:** While I can block your card for security, I cannot issue a replacement. A new card is typically dispatched automatically to your registered address after you report it lost or stolen.
  - **Example Action:** This is an unsupported action. No tool should be used. The agent should inform the user about the standard process.

### Q6: My debit/credit card is expiring soon. How do I get a new one?

- **A:** A new card will be automatically dispatched to your registered address approximately one month before your current card expires. If you don't receive it, please contact a human agent for assistance.
  - **Example Action:** This is an unsupported action. No tool should be used. The agent should provide information and offer to escalate.

## 3. Disputes & Complaints (Scenario Type: `raise_dispute`, `complaint_new`, `complaint_status`)

### Q7: How do I initiate a dispute or chargeback for a transaction?

- **A:** I can help you initiate a dispute for a transaction. Please provide the transaction amount and date.
  - **Example Action:** This requires the `raise_dispute` tool. The agent must collect `amount` and `transaction_date`.

### Q8: How can I register a new complaint?

- **A:** I can register a new complaint for you. Please describe the issue, and I will generate a ticket ID for you.
  - **Example Action:** This requires the `complaint_new` tool. The agent should collect a description of the issue.

### Q9: How can I check the status of my existing complaint?

- **A:** I can check your complaint's status. Please provide the ticket ID.
  - **Example Action:** This requires the `complaint_status` tool. The agent must collect the `ticket_id`.

## 4. Locators (Branch & ATM) (Scenario Type: `locate_branch`, `locate_atm`)

### Q10: How can I find the nearest Mauryan Bank branch?

- **A:** I can find a nearby branch for you. Please provide the city you are in.
  - **Example Action:** This requires the `locate_branch` tool. The agent must collect the `branch_city`.

### Q11: How can I find the nearest Mauryan Bank ATM?

- **A:** I can find a nearby ATM. Please provide the pincode.
  - **Example Action:** This requires the `locate_atm` tool. The agent must collect the `pincode`.

## 5. KYC & Document Status (Scenario Type: `kyc_status`)

### Q12: How can I check my KYC (Know Your Customer) status?

- **A:** I can check your KYC status. Please provide your account number.
  - **Example Action:** This requires the `kyc_status` tool. The agent must collect the `account_number`.

### Q13: What documents are required for KYC update?

- **A:** For KYC updates, you typically need a valid proof of identity (like an Aadhaar card or Passport) and proof of address (like a recent utility bill). For the complete process, please visit a branch.
  - **Example Action:** This is an informational query. No tool is used. The agent should provide the information from its knowledge base.

## 6. Cheque Services (Scenario Type: `cheque_status`)

### Q14: How can I check the status of a cheque I issued or deposited?

- **A:** I can check the status of a cheque for you. Please provide the cheque number.
  - **Example Action:** This requires the `cheque_status` tool. The agent must collect the `cheque_number`.

### Q15: Can I stop payment for a cheque?

- **A:** To stop a cheque payment, you need to visit a branch or use our net banking portal. I cannot perform that action for you.
  - **Example Action:** This is an unsupported action. No tool should be used. The agent should inform the user about the correct procedure.

## 7. Fixed Deposit (FD) Information (Scenario Type: `fd_rate_info`)

### Q16: What are the current interest rates for Fixed Deposits?

- **A:** I can provide you with the current Fixed Deposit interest rates. If you have a specific tenure in mind, let me know. Otherwise, I can provide all available rates.
  - **Example Action:** For general inquiries, use `GetAllFDRatesAction`. If the user specifies a tenure, use `GetFDRatesByTenureAction`. Do not ask for `tenure` or `amount` if the user wants general rates.

### Q17: Can I prematurely withdraw my Fixed Deposit?

- **A:** Yes, premature withdrawal of Fixed Deposits is generally allowed but may be subject to a penalty. For details specific to your account, please refer to your FD advice or contact a branch.
  - **Example Action:** This is an informational query. No tool is used. The agent should provide the general policy from its knowledge base.

## 8. Loan Status & Payment Options (Scenario Type: `loan_status`)

### Q18: How can I check the status of my loan application?

- **A:** I can check your loan application status. Please provide your loan ID or reference number.
  - **Example Action:** This requires the `loan_status` tool. The agent must collect the `loan_id`.

### Q19: What are the available payment options for my loan EMIs?

- **A:** Information on EMI payment options is available on our website and mobile app. I can also help you find a nearby branch if you'd like to discuss it in person.
  - **Example Action:** This is an informational query. No tool is used. The agent should provide information and offer a supported action (`locate_branch`).

### Q20: How can I get a No Objection Certificate (NOC) for my closed loan?

- **A:** You can request an NOC for a closed loan through our net banking portal or by visiting your nearest branch.
  - **Example Action:** This is an unsupported action. No tool should be used. The agent should inform the user about the correct procedure.
