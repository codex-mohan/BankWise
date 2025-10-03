# Request Payload Templates

## Purpose of this Document

This document serves as a comprehensive guide for a Large Language Model (LLM) on how to interact with the BankWise API. It provides clear and detailed templates for request payloads, along with concrete examples of both requests and corresponding responses. The examples are derived from mock data to ensure a realistic representation of API interactions. This guide is intended to be used as a reference for the LLM to understand the API's functionality and to construct valid API requests.

## Security and Data Privacy

**Confidentiality:** This document contains information about the BankWise API that is for internal use only. The LLM must not, under any circumstances, disclose any information about the backend, API keys, or any other sensitive data to any user.

**Mock Data:** All data used in the examples, including account numbers, names, and transaction details, is entirely fictional and generated for testing and demonstration purposes. No real customer data is used in this document or in the associated mock data files.

---

## Get Account Balance

This action retrieves the current balance for a specified bank account.

`POST /api/account/balance`

```json
{ "account_number": "{{account_number}}" }
```

- `account_number`: The bank account number of the customer.

### Request Example

```json
{ "account_number": "619297175888" }
```

### Response Example

```json
{
  "account_number": "619297175888",
  "balance": 864722.25,
  "currency": "INR"
}
```

---

## Get Transaction History

This action retrieves a list of recent transactions for a specified bank account.

`POST /api/account/transactions`

```json
{ "account_number": "{{account_number}}", "limit": "{{limit}}" }
```

- `account_number`: The bank account number of the customer.
- `limit`: The maximum number of transactions to retrieve.

### Request Example

```json
{ "account_number": "619297175888", "limit": "2" }
```

### Response Example

```json
[
  {
    "id": "TXN1464871",
    "transaction_date": "2024-05-17T00:39:33.558955",
    "description": "Transfer to Wridesh Khatri",
    "amount": 18458.67,
    "type": "TRANSFER",
    "status": "FAILED"
  },
  {
    "id": "TXN9504954",
    "transaction_date": "2024-01-13T00:39:33.558980",
    "description": "Transfer to Vedant Hora",
    "amount": 7974.65,
    "type": "TRANSFER",
    "status": "COMPLETED"
  }
]
```

---

## Block a Card

This action blocks a customer's credit or debit card.

`POST /api/card/block`

```json
{ "last4": "{{last4}}", "reason": "{{reason}}" }
```

- `last4`: The last 4 digits of the card to be blocked.
- `reason`: The reason for blocking the card.

### Request Example

```json
{ "last4": "1567", "reason": "Lost Card" }
```

### Response Example

```json
{
  "message": "Card ending in 1567 has been successfully blocked.",
  "card_number": "****1567",
  "status": "BLOCKED"
}
```

---

## Raise a Transaction Dispute

This action allows a customer to raise a dispute for a specific transaction.

`POST /api/dispute/raise`

```json
{
  "amount": "{{amount}}",
  "transaction_date": "{{transaction_date}}",
  "reason": "{{reason}}",
  "description": "{{description}}"
}
```

- `amount`: The amount of the transaction to dispute.
- `transaction_date`: The date of the transaction in "YYYY-MM-DD" format.
- `reason`: The reason for the dispute.
- `description`: A detailed description of the dispute.

### Request Example

```json
{
  "amount": "32609.71",
  "transaction_date": "2025-09-20",
  "reason": "Unauthorized Transaction",
  "description": "I did not make this transaction. Please investigate."
}
```

### Response Example

```json
{
  "message": "Dispute raised successfully.",
  "ticket_id": "DISPUTE34424",
  "status": "OPEN"
}
```

---

## Create a New Complaint

This action allows a customer to create a new complaint.

`POST /api/complaint/new`

```json
{
  "account_number": "{{account_number}}",
  "subject": "{{subject}}",
  "description": "{{description}}",
  "category": "{{category}}"
}
```

- `account_number`: The bank account number of the customer.
- `subject`: The subject of the complaint.
- `description`: A detailed description of the complaint.
- `category`: The category of the complaint. Possible values are "ACCOUNT", "CARD", "TRANSACTION", "ATM", "BRANCH", "LOAN", "FD", "NET_BANKING", "MOBILE_BANKING", "OTHER".

### Request Example

```json
{
  "account_number": "265096191009",
  "subject": "Issue with Net Banking",
  "description": "I am unable to login to my net banking account.",
  "category": "NET_BANKING"
}
```

### Response Example

```json
{
  "message": "Complaint created successfully.",
  "ticket_id": "COMPLAINT18829",
  "status": "OPEN"
}
```

---

## Check Complaint Status

This action allows a customer to check the status of an existing complaint.

`POST /api/complaint/status`

```json
{ "ticket_id": "{{ticket_id}}" }
```

- `ticket_id`: The ID of the complaint to check.

### Request Example

```json
{ "ticket_id": "COMPLAINT18829" }
```

### Response Example

```json
{
  "ticket_id": "COMPLAINT18829",
  "status": "CLOSED",
  "resolution_notes": "The issue has been resolved. Please try logging in again."
}
```

---

## Locate Bank Branches

This action helps customers find bank branches in a specific city.

`POST /api/branch/locate`

```json
{ "branch_city": "{{branch_city}}", "limit": "{{limit}}" }
```

- `branch_city`: The city to search for branches in.
- `limit`: The maximum number of branches to retrieve.

### Request Example```json

{ "branch_city": "Mumbai", "limit": "1" }

````

### Response Example```json
[
  {
    "name": "BOB Mumbai Main",
    "address": "H.No. 79, Ahuja Zila",
    "city": "Mumbai",
    "pincode": "226421"
  }
]
````

---

## Find ATMs

This action helps customers find ATMs in a specific pincode.

`POST /api/atm/locate`

```json
{ "pincode": "{{pincode}}", "limit": "{{limit}}" }
```

- `pincode`: The pincode to search for ATMs in.
- `limit`: The maximum number of ATMs to retrieve.

### Request Example

````json
{ "pincode": "153328", "limit": "1" }```

### Response Example
```json
[
  {
    "address": "74, Khurana Circle",
    "city": "Mumbai",
    "pincode": "153328",
    "bank_name": "Mauryan Bank"
  }
]
````

---

## Check KYC Status

This action allows a customer to check their Know Your Customer (KYC) status.

`POST /api/kyc/status`

```json
{ "account_number": "{{account_number}}" }
```

- `account_number`: The bank account number of the customer.

### Request Example

```json
{ "account_number": "619297175888" }
```

### Response Example

```json
{
  "account_number": "619297175888",
  "kyc_status": "PENDING"
}
```

---

## Check Cheque Status

This action allows a customer to check the status of a cheque.

`POST /api/cheque/status`

```json
{ "cheque_number": "{{cheque_number}}" }
```

- `cheque_number`: The number of the cheque to check.

### Request Example

```json
{ "cheque_number": "825691" }
```

### Response Example

```json
{
  "cheque_number": "825691",
  "status": "Pending"
}
```

---

## Get FD Rates

This action retrieves the current interest rates for fixed deposits. You can retrieve all available rates or filter them by a specific tenure.

`POST /api/fd/rates`

### Use Case 1: Get All FD Rates

To retrieve all available FD rates, send an empty request body.

#### Request Example

```json
{}
```

### Use Case 2: Get FD Rates by Tenure

To retrieve FD rates for a specific tenure.

#### Request Payload Template

```json
{ "tenure": "{{tenure}}", "amount": "{{amount}}" }
```

- `tenure` (optional): The tenure in months for the fixed deposit.
- `amount` (optional): The amount for the fixed deposit.

#### Request Example

```json
{ "tenure": "7" }
```

### Response Example

The response format is the same for all `Get FD Rates` requests. The example below shows a possible response.

```json
[
  {
    "tenure": 7,
    "rate": 7.31,
    "customer_type": "NORMAL"
  },
  {
    "tenure": 7,
    "rate": 5.94,
    "customer_type": "SENIOR_CITIZEN"
  }
]
```

---

## Check Loan Status

This action allows a customer to check the status of their loan application.

`POST /api/loan/status`

```json
{ "loan_id": "{{loan_id}}" }
```

- `loan_id`: The ID of the loan to check.

### Request Example

```json
{ "loan_id": "LN41782" }
```

### Response Example

```json
{
  "loan_id": "LN41782",
  "status": "DEFAULT"
}
```

---

## Escalate to Human Agent (Enhanced with Intelligent Matching)

This action allows a customer to escalate their issue to a human agent with intelligent agent selection based on specialization and availability.

`POST /api/escalate`

```json
{ "reason": "{{reason}}", "urgency": "{{urgency}}" }
```

- `reason`: The reason for escalation. The system intelligently determines the best agent specialization based on keywords in the reason.
- `urgency`: The urgency of the escalation (e.g., "high", "medium", "low").

### Request Example

```json
{
  "reason": "I need to block my lost credit card immediately",
  "urgency": "high"
}
```

### Response Example

```json
{
  "escalation_id": "ESCALATION53590",
  "agent_info": {
    "agent_id": "AGENT6661",
    "employee_id": "EMP94007",
    "full_name": "Savita Agarwal",
    "department": "Priority Banking",
    "specialization": "International Banking",
    "languages_spoken": ["English", "Hindi", "Urdu"],
    "years_experience": 1,
    "performance_rating": 4.1,
    "customer_satisfaction_rate": 90.3,
    "current_status": "On Break",
    "is_available": false,
    "next_available_time": "2025-10-02T16:09:57.722957",
    "average_response_time": 68,
    "resolution_rate": 91.7,
    "escalation_level": "L2"
  },
  "estimated_wait_time": 1,
  "queue_position": 2,
  "alternative_agents": [],
  "status": "success"
}
```

---

## Get Available Agents

This action retrieves a list of currently available human agents, optionally filtered by specialization.

`GET /api/agents/available`

### Query Parameters

- `specialization` (optional): Filter agents by specialization (e.g., "Card Issues", "Account Queries", "Loan Processing").
- `limit` (optional): Maximum number of agents to return (default: 10).

### Request Example

```bash
GET /api/agents/available?specialization=Card Issues&limit=5
```

### Response Example

```json
[
  {
    "agent_id": "AGENT7818",
    "employee_id": "EMP53374",
    "full_name": "Manish Joshi",
    "department": "Account Services",
    "specialization": "Account Queries",
    "languages_spoken": ["English", "Hindi", "Telugu"],
    "years_experience": 8,
    "performance_rating": 4.9,
    "customer_satisfaction_rate": 90.2,
    "current_status": "Available",
    "is_available": true,
    "next_available_time": null,
    "average_response_time": 36,
    "resolution_rate": 91.2,
    "escalation_level": "L2"
  }
]
```

---

## Get Agent Statistics

This action retrieves comprehensive statistics about agent availability and distribution.

`GET /api/agents/statistics`

### Request Example

```bash
GET /api/agents/statistics
```

### Response Example

```json
{
  "total_agents": 25,
  "available_agents": 7,
  "availability_rate": 28.0,
  "department_distribution": {
    "Account Services": 3,
    "Technical Support": 4,
    "Loan Department": 4,
    "Priority Banking": 5,
    "Dispute Resolution": 3,
    "Card Services": 1,
    "Wealth Management": 1,
    "NRI Services": 2,
    "Customer Service": 2
  },
  "specialization_distribution": {
    "Account Queries": 2,
    "Loan Processing": 2,
    "Technical Support": 2,
    "Transaction Disputes": 5,
    "Business Accounts": 3,
    "KYC Verification": 2,
    "Investment Services": 2,
    "International Banking": 6,
    "Card Issues": 1
  }
}
```

---

## Get Agent Details

This action retrieves detailed information about a specific agent.

`GET /api/agents/{agent_id}`

### Path Parameters

- `agent_id`: The unique identifier of the agent.

### Request Example

```bash
GET /api/agents/AGENT7818
```

### Response Example

```json
{
  "agent_id": "AGENT7818",
  "employee_id": "EMP53374",
  "full_name": "Manish Joshi",
  "department": "Account Services",
  "specialization": "Account Queries",
  "languages_spoken": ["English", "Hindi", "Telugu"],
  "years_experience": 8,
  "performance_rating": 4.9,
  "customer_satisfaction_rate": 90.2,
  "current_status": "Available",
  "is_available": true,
  "next_available_time": null,
  "average_response_time": 36,
  "resolution_rate": 91.2,
  "escalation_level": "L2"
}
```

---

## Update Agent Status

This action updates the availability status of a specific agent.

`PUT /api/agents/{agent_id}/status`

### Path Parameters

- `agent_id`: The unique identifier of the agent.

### Request Body

```json
{ "status": "{{status}}" }
```

- `status`: The new status of the agent. Valid values: "Available", "Busy", "On Break", "In Training", "Off Duty".

### Request Example

```json
{ "status": "Busy" }
```

### Response Example

```json
{
  "message": "Agent status updated to Busy"
}
```

---

## Process Natural Language Intent

This action processes natural language text to determine the user's intent.

`POST /api/chat/intent`

```json
{ "text": "{{text}}" }
```

- `text`: The natural language text from the user.

### Request Example

````json
{ "text": "I want to know my account balance" }```

### Response Example
```json
{
  "intent": "get_balance",
  "entities": {}
}
````
