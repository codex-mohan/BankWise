# Request Payload Templates

This file contains templates for the request payloads for the BankWise API.

## Get Account Balance
This action retrieves the current balance for a specified bank account.

`POST /api/account/balance`

```json
{"account_number": "{{account_number}}"}
```
- `account_number`: The bank account number of the customer.

## Get Transaction History
This action retrieves a list of recent transactions for a specified bank account.

`POST /api/account/transactions`

```json
{"account_number": "{{account_number}}", "limit": "{{limit}}"}
```
- `account_number`: The bank account number of the customer.
- `limit`: The maximum number of transactions to retrieve.

## Block a Card
This action blocks a customer's credit or debit card.

`POST /api/card/block`

```json
{"last4": "{{last4}}", "reason": "{{reason}}"}
```
- `last4`: The last 4 digits of the card to be blocked.
- `reason`: The reason for blocking the card.

## Raise a Transaction Dispute
This action allows a customer to raise a dispute for a specific transaction.

`POST /api/dispute/raise`

```json
{"amount": "{{amount}}", "transaction_date": "{{transaction_date}}", "reason": "{{reason}}", "description": "{{description}}"}
```
- `amount`: The amount of the transaction to dispute.
- `transaction_date`: The date of the transaction in "YYYY-MM-DD" format.
- `reason`: The reason for the dispute.
- `description`: A detailed description of the dispute.

## Create a New Complaint
This action allows a customer to create a new complaint.

`POST /api/complaint/new`

```json
{"account_number": "{{account_number}}", "complaint_text": "{{complaint_text}}"}
```
- `account_number`: The bank account number of the customer.
- `complaint_text`: The text of the complaint.

## Check Complaint Status
This action allows a customer to check the status of an existing complaint.

`POST /api/complaint/status`

```json
{"complaint_id": "{{complaint_id}}"}```
- `complaint_id`: The ID of the complaint to check.

## Locate Bank Branches
This action helps customers find bank branches in a specific city.

`POST /api/branch/locate`

```json
{"branch_city": "{{branch_city}}", "limit": "{{limit}}"}
```
- `branch_city`: The city to search for branches in.
- `limit`: The maximum number of branches to retrieve.

## Find ATMs
This action helps customers find ATMs in a specific pincode.

`POST /api/atm/locate`

```json
{"pincode": "{{pincode}}"}
```
- `pincode`: The pincode to search for ATMs in.

## Check KYC Status
This action allows a customer to check their Know Your Customer (KYC) status.

`POST /api/kyc/status`

```json
{"account_number": "{{account_number}}"}
```
- `account_number`: The bank account number of the customer.

## Check Cheque Status
This action allows a customer to check the status of a cheque.

`POST /api/cheque/status`

```json
{"cheque_number": "{{cheque_number}}"}
```
- `cheque_number`: The number of the cheque to check.

## Get FD Rates
This action retrieves the current interest rates for fixed deposits.

`POST /api/fd/rates`

```json
{"tenure_in_months": "{{tenure_in_months}}"}
```- `tenure_in_months`: The tenure in months for the fixed deposit.

## Check Loan Status
This action allows a customer to check the status of their loan application.

`POST /api/loan/status`

```json
{"loan_id": "{{loan_id}}"}
```
- `loan_id`: The ID of the loan to check.

## Escalate to Human Agent
This action allows a customer to escalate their issue to a human agent.

`POST /api/escalate`

```json
{"reason": "{{reason}}", "urgency": "{{urgency}}"}
```
- `reason`: The reason for escalation.
- `urgency`: The urgency of the escalation (e.g., "high", "medium", "low").

## Process Natural Language Intent
This action processes natural language text to determine the user's intent.

`POST /api/chat/intent`

```json
{"text": "{{text}}"}
```
- `text`: The natural language text from the user.
