# 🛠️ BankWise API Usage Examples

This document provides detailed examples for each of the BankWise API endpoints.

## 👤 Account Services

### Get Account Balance

```bash
curl -X POST "http://localhost:8000/api/account/balance" \
     -H "Content-Type: application/json" \
     -d '{
       "account_number": "123456789012"
     }'
```

**Response:**

```json
{
  "account_number": "******9012",
  "balance": 15430.55,
  "currency": "INR",
  "as_of": "2025-09-21T09:00:00+05:30",
  "status": "success"
}
```

### Get Transaction History

```bash
curl -X POST "http://localhost:8000/api/account/transactions" \
     -H "Content-Type: application/json" \
     -d '{
       "account_number": "123456789012",
       "limit": 5
     }'
```

**Response:**

```json
{
  "account_number": "******9012",
  "transactions": [
    {
      "id": "TXN1234567",
      "date": "2025-09-20T10:30:00+05:30",
      "description": "Purchase at Amazon",
      "amount": 1250.0,
      "type": "PURCHASE",
      "balance_after": 14180.55
    }
  ],
  "total_count": 5,
  "status": "success"
}
```

### Get Transaction Details

```bash
curl -X POST "http://localhost:8000/api/account/transaction" \
     -H "Content-Type: application/json" \
     -d '{
       "transaction_id": "TXN1234567"
     }'
```

**Response:**

```json
{
  "transaction_id": "TXN1234567",
  "account_number": "******9012",
  "transaction_date": "2025-09-20T10:30:00+05:30",
  "description": "Purchase at Amazon",
  "amount": 1250.0,
  "type": "PURCHASE",
  "balance_after": 14180.55,
  "status": "COMPLETED",
  "reference_id": "REF12345",
  "merchant_id": "Amazon",
  "location": "Mumbai",
  "status_response": "success"
}
```

## 💳 Card Services

### Block a Card

```bash
curl -X POST "http://localhost:8000/api/card/block" \
     -H "Content-Type: application/json" \
     -d '{
       "last4": "9012",
       "reason": "Lost card"
     }'
```

**Response:**

```json
{
  "card_number": "****9012",
  "status": "BLOCKED",
  "blocked_at": "2025-09-21T09:00:00+05:30",
  "ticket_id": "BLOCK12345",
  "status": "success"
}
```

## 🧾 Cheque Services

### Get Cheque Status

```bash
curl -X POST "http://localhost:8000/api/cheque/status" \
     -H "Content-Type: application/json" \
     -d '{
       "cheque_number": "123456"
     }'
```

**Response:**

```json
{
  "cheque_number": "123456",
  "content": "Cleared",
  "amount": 25000.0,
  "date": "2025-09-15T10:00:00+05:30",
  "clearing_date": "2025-09-18T15:00:00+05:30",
  "status": "success"
}```

## 🗣️ Dispute & Complaint Services

### Raise a Dispute

```bash
curl -X POST "http://localhost:8000/api/dispute/raise" \
     -H "Content-Type: application/json" \
     -d '{
       "amount": 1250.0,
       "transaction_date": "2025-09-20",
       "reason": "Incorrect amount charged",
       "description": "I was charged 1250.0 instead of 125.0"
     }'
```

**Response:**

```json
{
  "ticket_id": "DISPUTE12345",
  "content": "UNDER_REVIEW",
  "amount": 1250.0,
  "estimated_resolution_days": 15,
  "status": "success"
}
```

### Create a New Complaint

```bash
curl -X POST "http://localhost:8000/api/complaint/new" \
     -H "Content-Type: application/json" \
     -d '{
       "account_number": "123456789012",
       "subject": "Unauthorized Transaction",
       "description": "I have noticed an unauthorized transaction on my account.",
       "category": "TRANSACTION"
     }'
```

**Response:**

```json
{
  "complaint": {
    "ticket_id": "COMPLAINT12345",
    "account_number": "123456789012",
    "subject": "Unauthorized Transaction",
    "description": "I have noticed an unauthorized transaction on my account.",
    "category": "TRANSACTION",
    "status": "OPEN",
    "priority": "HIGH",
    "created_at": "2025-09-28T12:00:00Z",
    "resolved_at": null,
    "estimated_resolution_days": 2,
    "assigned_agent": null,
    "resolution_notes": null,
    "customer_satisfaction": null
  },
  "status": "success"
}
```

### Check Complaint Status

```bash
curl -X POST "http://localhost:8000/api/complaint/status" \
     -H "Content-Type: application/json" \
     -d '{
       "ticket_id": "COMPLAINT12345"
     }'
```

**Response:**

```json
{
  "complaint": {
    "ticket_id": "COMPLAINT12345",
    "account_number": "123456789012",
    "subject": "Unauthorized Transaction",
    "description": "I have noticed an unauthorized transaction on my account.",
    "category": "TRANSACTION",
    "status": "IN_PROGRESS",
    "priority": "HIGH",
    "created_at": "2025-09-28T12:00:00Z",
    "resolved_at": null,
    "estimated_resolution_days": 2,
    "assigned_agent": "AGENT123",
    "resolution_notes": null,
    "customer_satisfaction": null
  },
  "status": "success"
}
```

## 📍 Location Services

### Locate Branches

```bash
curl -X POST "http://localhost:8000/api/branch/locate" \
     -H "Content-Type: application/json" \
     -d '{
       "branch_city": "Mumbai",
       "limit": 3
     }'
```

**Response:**

```json
{
  "branches": [
    {
      "name": "BOB Mumbai Main",
      "address": "123, MG Road",
      "city": "Mumbai",
      "pincode": "400001",
      "ifsc": "BARB0MUMBAI",
      "latitude": 19.076,
      "longitude": 72.8777,
      "distance": 2.5
    }
  ],
  "total_count": 3,
  "status": "success"
}```

## 🧑‍💼 Support Services

### Escalate to Agent (Enhanced with Intelligent Matching)

```bash
curl -X POST "http://localhost:8000/api/escalate" \
     -H "Content-Type: application/json" \
     -d '{
       "reason": "I need to block my lost credit card immediately",
       "urgency": "high"
     }'
```

**Response:**

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

### Get Available Agents

```bash
curl -X GET "http://localhost:8000/api/agents/available?specialization=Card Issues&limit=5" \
     -H "Content-Type: application/json"
```

**Response:**

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

### Get Agent Statistics

```bash
curl -X GET "http://localhost:8000/api/agents/statistics" \
     -H "Content-Type: application/json"
```

**Response:**

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

### Get Agent Details

```bash
curl -X GET "http://localhost:8000/api/agents/AGENT7818" \
     -H "Content-Type: application/json"
```

**Response:**

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

### Update Agent Status

```bash
curl -X PUT "http://localhost:8000/api/agents/AGENT7818/status" \
     -H "Content-Type: application/json" \
     -d '{
       "status": "Busy"
     }'
```

**Response:**

```json
{
  "message": "Agent status updated to Busy"
}

## 👨‍⚖️ Judge Dashboard

### Access the Dashboard

```bash
# Open in browser
http://localhost:8000/dashboard/
```

### Dashboard API Endpoint

```bash
# Get dashboard data (JSON format)
curl "http://localhost:8000/dashboard/api?source=mock&data_type=accounts"
```

**Response:**

```json
{
  "data": [
    {
      "account_number": "810224329338",
      "account_type": "Savings",
      "balance": 85985.32,
      "currency": "INR",
      "customer_name": "Rayaan Kata",
      "customer_id": "CUST52914",
      "branch_code": "BRANCH124",
      "ifsc_code": "BARB9462",
      "kyc_status": "PENDING",
      "kyc_level": "LEVEL_3",
      "last_updated": "2025-05-02T20:46:59.184297",
      "account_status": "ACTIVE",
      "linked_cards": ["****5030", "****8159"],
      "mobile_numbers": ["+918441918127", "+918326653923"]
    }
  ],
  "data_type": "accounts",
  "source": "mock",
  "timestamp": "2025-09-29T18:20:00.123456",
  "count": 1
}
```

### Available Data Types

- **accounts**: Customer account information
- **transactions**: Transaction history
- **branches**: Bank branch details
- **atms**: ATM locations and status
- **complaints**: Customer complaints
- **disputes**: Transaction disputes
- **loans**: Loan information
- **fd_rates**: Fixed deposit rates
- **cards**: Credit/debit card details
- **cheques**: Cheque status information

### Available Data Sources

- **mock**: JSON files in `mock_data/` directory
- **db**: PostgreSQL database (if configured)

### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `source` | string | `mock` | Data source (mock or db) |
| `data_type` | string | `accounts` | Type of data to retrieve |

### Features

- **Interactive Web Interface**: Professional dashboard with sortable tables
- **Dual Data Sources**: Switch between mock data and database
- **Multiple Views**: Table view and JSON view
- **Responsive Design**: Works on desktop and mobile
- **Auto-refresh**: Data updates every 5 minutes
- **Error Handling**: Graceful handling of missing data