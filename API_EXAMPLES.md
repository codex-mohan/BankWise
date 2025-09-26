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

### Escalate to Agent

```bash
curl -X POST "http://localhost:8000/api/escalate" \
     -H "Content-Type: application/json" \
     -d '{
       "reason": "Complex transaction issue",
       "urgency": "high"
     }'
```

**Response:**

```json
{
  "escalation_id": "ESCALATION12345",
  "agent_id": "AGENT789",
  "estimated_wait_time": 15,
  "status": "success"
}