# AetherOps_Inya_Final

## Inya.ai Buildathon 2025 - Final Submission

### Inbound Banking Support Agent by BankWise AI

---

**Team Name:** AetherOps  
**Team Member:** Mohana Krishna (23BAI10630)  
**Contact Email:** codexmohan@gmail.com  
**Submission Date:** September 30, 2025

---

## 1. Executive Summary

### Project Overview

BankWise AI presents "Aria", an advanced AI-powered inbound banking support agent designed to handle real-world banking scenarios across both Voice and Chat channels. Our solution addresses the critical challenges faced by inbound banking teams including heavy call volumes, repeated queries, strict compliance requirements, and seamless human escalation.

### Key Achievements

- ✅ **Complete Scenario Coverage**: Implemented all 10+ required banking scenarios
- ✅ **Multi-Channel Support**: Voice and Chat ready with adaptive persona
- ✅ **Robust Architecture**: FastAPI backend with PostgreSQL + fallback mock data
- ✅ **Security First**: Complete PII masking and data protection
- ✅ **Production Ready**: Deployed on Render.com with full CI/CD

### Unique Differentiators

1. **Adaptive Persona System**: Dynamic tone switching based on user emotional state
2. **Intelligent Fallback**: Seamless database-to-mock data failover
3. **Smart Validation**: Foreign key constraint handling with data integrity
4. **Proactive Assistance**: Context-aware next-step suggestions
5. **Zero Trust Security**: Complete data masking and authentication

## 2. Architecture Overview

### System Architecture

![API Backend Architecture](api_backend_architecture.md)

Our architecture follows a layered approach:

- **External Interfaces**: Inya.ai Platform integration
- **FastAPI Application**: 12+ specialized endpoints
- **Business Logic**: Service controllers with validation
- **Data Layer**: PostgreSQL primary + JSON fallback
- **External Services**: SMS, escalation, location services

### AI Agent Logic Flow

![AI Agent Logic Flow](ai_agent_logic_flow.md)

The AI agent "Aria" implements:

- **Decision-Making Framework**: 4-step logical process
- **Persona State Management**: Adaptive emotional intelligence
- **Error Recovery**: Silent retry with graceful escalation
- **Security Validation**: Risk assessment for sensitive operations

### Hybrid Data Retrieval Strategy

Our agent employs a hybrid data retrieval strategy to ensure both accuracy and efficiency:

- **Static Knowledge Base**: For general, non-user-specific information that does not change frequently, the agent relies on a static knowledge base. This includes details about banking products (e.g., FD rates, loan types), FAQs, branch hours, and general bank policies. This ensures fast, consistent answers for common queries.
- **Dynamic API Actions**: For user-specific, real-time data, the agent triggers secure API actions. These actions retrieve dynamic information such as account balances, transaction histories, KYC status, and complaint details from the backend database.

This dual approach allows "Aria" to provide comprehensive support by combining a stable repository of general knowledge with secure access to live, personal data.

## 3. Implemented Banking Scenarios

| #   | Scenario            | Intent             | API Endpoint                | Status       |
| --- | ------------------- | ------------------ | --------------------------- | ------------ |
| 1   | Account Balance     | `account_info`     | `/api/account/balance`      | ✅ Complete  |
| 2   | Transaction History | `tx_history`       | `/api/account/transactions` | ✅ Complete  |
| 3   | Card Block/Hotlist  | `card_block`       | `/api/card/block`           | ✅ Complete  |
| 4   | Dispute Initiation  | `raise_dispute`    | `/api/dispute/raise`        | ✅ Complete  |
| 5   | New Complaint       | `complaint_new`    | `/api/complaint/new`        | ✅ Complete  |
| 6   | Complaint Status    | `complaint_status` | `/api/complaint/status`     | ✅ Complete  |
| 7   | Branch Locator      | `locate_branch`    | `/api/branch/locate`        | ✅ Complete  |
| 8   | ATM Locator         | `locate_atm`       | `/api/atm/locate`           | ✅ Complete  |
| 9   | KYC Status          | `kyc_status`       | `/api/kyc/status`           | ✅ Complete  |
| 10  | Cheque Status       | `cheque_status`    | `/api/cheque/status`        | ✅ Complete  |
| 11  | FD Rate Information | `fd_rate_info`     | `/api/fd/rates`             | ✅ Complete  |
| 12  | Loan Status         | `loan_status`      | `/api/loan/status`          | ✅ Complete  |
| 13  | Human Escalation    | `speak_to_agent`   | `/api/escalate`             | ⚠️ Prototype |

## 4. Data Schemas & API Documentation

### Core Data Models

#### Account Balance Request/Response

```json
// Request
{
  "account_number": "123456784157",
  "channel": "voice",
  "language_pref": "en"
}

// Response
{
  "status": "success",
  "data": {
    "account_number": "******4157",
    "balance": 15430.55,
    "currency": "INR",
    "account_type": "Savings",
    "as_of": "2025-09-29T10:00:00+05:30"
  }
}
```

#### Transaction History Response

```json
{
  "status": "success",
  "data": {
    "account_number": "******4157",
    "transactions": [
      {
        "date": "2025-09-28T14:30:00+05:30",
        "description": "UPI Transfer to John Doe",
        "amount": -2500.0,
        "type": "DEBIT",
        "balance_after": 15430.55
      }
    ],
    "total_count": 156
  }
}
```

#### Branch Locator Response

```json
{
  "status": "success",
  "data": {
    "branches": [
      {
        "name": "BOB Mumbai Fort",
        "address": "123 Fort Road, Mumbai",
        "city": "Mumbai",
        "pincode": "400001",
        "ifsc": "BARB0FORTXX",
        "phone": "022-12345678",
        "distance_km": 2.5
      }
    ]
  }
}
```

## 5. Technology Stack

### Backend Technologies

- **Framework**: FastAPI 0.100+ (Python 3.11+)
- **Database**: PostgreSQL (Neon.tech hosted)
- **Authentication**: API Token based
- **Validation**: Pydantic models
- **Logging**: Structured logging with file output
- **Deployment**: Render.com

### AI Integration

- **Platform**: Inya.ai for NLU and dialogue management
- **Intent Recognition**: 13 canonical intents
- **Entity Extraction**: 10+ canonical entities
- **Language Support**: English, Hindi, Code-mixing

### External Services

- **SMS**: Twilio integration
- **Location**: Geocoding for branch/ATM finder
- **Monitoring**: Health checks and performance metrics

## 6. Security & Compliance

### Data Protection

- **PII Masking**: All sensitive data masked in responses
- **No Real Data**: 100% mock data, no real customer information
- **Input Validation**: Comprehensive Pydantic validation
- **Error Handling**: Secure error messages without system exposure

### Authentication & Authorization

- **API Token**: Header-based authentication
- **Request Validation**: All endpoints protected
- **Session Management**: Secure session handling
- **Audit Trail**: Complete interaction logging

## 7. Setup & Deployment Instructions

### Local Development Setup

```bash
# Clone repository
git clone https://github.com/your-repo/BankWise.git
cd BankWise

# Install dependencies
pip install -r requirements.txt

# or Use UV to install the dependencies
uv sync

# Or Install

# Configure environment
cp .env.example .env
# Edit .env with your Neon DB connection string

# Run locally
# a) If using pip:
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# b) If using UV:
uv run unicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Production Deployment (Render.com)

1. **Connect Repository**: Link your Git repository to Render
2. **Configure Environment Variables**:
   - `DATABASE_URL`: Neon PostgreSQL connection string
   - `API_TOKEN`: Your secure API token
   - `TWILIO_*`: SMS service credentials
3. **Deploy**: Render auto-detects `render.yaml` configuration
4. **Verify**: Access health endpoint at `/health`

### Environment Variables (Example)

```env
DATABASE_URL=postgresql://user:pass@host:5432/db
API_TOKEN=your_secure_token_here
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_PHONE_NUMBER=+1234567890
ENVIRONMENT=production
```

## 8. API Documentation & Testing

### Interactive Documentation

- **Swagger UI**: Available at `/docs`
- **ReDoc**: Available at `/redoc`
- **Health Check**: Available at `/health`

### API Base URL

- **Production**: `https://bankwise-fekm.onrender.com`
- **Local**: `http://localhost:8000`

### Authentication

All API endpoints require authentication header:

```bash
curl -H "X-API-Token: your_token_here" \
     -H "Content-Type: application/json" \
     -X POST https://bankwise-fekm.onrender.com/api/account/balance \
     -d '{"account_number": "123456784157"}'
```

## 9. Detailed Test Cases & Scenarios

As per the buildathon requirements, we have prepared over 20 detailed test scripts covering both happy paths and critical edge cases. These tests are designed to be executable and reproducible.

| SR.             | User Utterance / Scenario                                                                                               | Expected Intent                | Required Entities                                     | Mock API Endpoint           | Expected Bot Response                                                                             | Escalation |
| --------------- | ----------------------------------------------------------------------------------------------------------------------- | ------------------------------ | ----------------------------------------------------- | --------------------------- | ------------------------------------------------------------------------------------------------- | ---------- |
| **Happy Paths** |                                                                                                                         |                                |                                                       |                             |                                                                                                   |            |
| 1               | "What is my account balance?"                                                                                           | `account_info`                 | `account_number="898370214157"`                       | `/api/account/balance`      | "Your savings account balance is ₹864,722.25 as of today."                                        | No         |
| 2               | "Show me my last 5 transactions."                                                                                       | `tx_history`                   | `account_number="898370214157"`                       | `/api/account/transactions` | "Here is your latest transaction: A failed DEPOSIT of ₹18369.92 on 2024-07-16 for Salary Credit." | No         |
| 3               | "I lost my card, please block it."                                                                                      | `card_block`                   | `account_number="898370214157"`, `last4` (prompted)   | `/api/card/block`           | "I've blocked the card ending in 4157. A replacement will be sent."                               | No         |
| 4               | "Block my card ending in 4157."                                                                                         | `card_block`                   | `account_number="898370214157"`, `last4=4157`         | `/api/card/block`           | "Confirmation: Your card ending in 4157 has been successfully blocked."                           | No         |
| 5               | "I want to dispute a transaction of 500 rupees from yesterday."                                                         | `raise_dispute`                | `account_number="898370214157"`, `amount=500`, `date` | `/api/dispute/raise`        | "Your dispute has been registered. Your ticket ID is D-98765."                                    | No         |
| 6               | "I need to register a complaint."                                                                                       | `complaint_new`                | `account_number="898370214157"` (prompted)            | `/api/complaint/new`        | "Certainly. Please describe your issue so I can raise a ticket for you."                          | No         |
| 7               | "What's the status of my ticket COMPLAINT69541?"                                                                        | `complaint_status`             | `ticket_id=COMPLAINT69541`                            | `/api/complaint/status`     | "The complaint 'COMPLAINT69541' regarding CARD is currently CLOSED."                              | No         |
| 8               | "Find the nearest branch in Address: 456, 5th Block, Koramangala, Bengaluru, Karnataka 560095 - IFSC Code: MAUR0000003" | `locate_branch`                | `branch_city=Bangalore`                               | `/api/branch/locate`        | "I found 3 branches in Koramangala. The nearest one is at [Address], 1.5km away."                 | No         |
| 9               | "Where is an ATM near pincode 560001?"                                                                                  | `locate_atm`                   | `pincode=560001`                                      | `/api/atm/locate`           | "Here are the top 3 ATMs near 560001: [Lists ATMs with addresses]."                               | No         |
| 10              | "Can you check my KYC status?"                                                                                          | `kyc_status`                   | `account_number="898370214157"`                       | `/api/kyc/status`           | "Your KYC is verified and up-to-date. No further action is needed."                               | No         |
| 11              | "What is the status of cheque number 123456?"                                                                           | `cheque_status`                | `cheque_number=123456`                                | `/api/cheque/status`        | "Cheque number 123456 was cleared on September 28, 2025."                                         | No         |
| 12              | "Tell me about the current fixed deposit interest rates."                                                               | `fd_rate_info`                 | None                                                  | `/api/fd/rates`             | "For a normal customer, the rate for 7 days is 5.22%, and for a senior citizen, it is 4.26%."     | No         |
| 13              | "I want to know my loan status, ID is LN77584."                                                                         | `loan_status`                  | `loan_id=LN77584`                                     | `/api/loan/status`          | "The GOLD_LOAN with ID LN77584 is COMPLETED. The principal was ₹4,590,791.35."                    | No         |
| **Edge Cases**  |                                                                                                                         |                                |                                                       |                             |                                                                                                   |            |
| 14              | "I want to speak to a human agent."                                                                                     | `speak_to_agent`               | None                                                  | `/api/escalate`             | "(Prototype) Of course. Connecting you to a live agent now. Please wait a moment."                | Yes (Mock) |
| 15              | "I have a card issue." (Ambiguous)                                                                                      | `card_block` / `raise_dispute` | `account_number="898370214157"`                       | -                           | "I can help with that. Are you looking to block your card or raise a dispute?"                    | No         |
| 16              | "Mera balance batao." (Language Switch)                                                                                 | `account_info`                 | `account_number="898370214157"`, `language_pref=hi`   | `/api/account/balance`      | "Aapke khaate ka balance ₹864,722.25 hai." (Replies in Hindi)                                     | No         |
| 17              | "Branch in Mumbai" (Disambiguation)                                                                                     | `locate_branch`                | `branch_city=Mumbai`                                  | `/api/branch/locate`        | "Mumbai is a big city! Could you please specify an area or pincode?"                              | No         |
| 18              | "Dispute for a transaction that doesn't exist."                                                                         | `raise_dispute`                | `account_number="898370214157"`, `amount`, `date`     | `/api/dispute/raise`        | "I could not find a transaction matching those details. Please double-check."                     | No         |
| 19              | (API timeout during balance check)                                                                                      | `account_info`                 | `account_number="898370214157"`                       | `/api/account/balance`      | "I'm having trouble fetching your balance right now. Please try again in a moment."               | No         |
| 20              | "This is useless, get me a person." (Frustration)                                                                       | `speak_to_agent`               | None                                                  | `/api/escalate`             | "(Prototype) I understand your frustration. I'm transferring you to a specialist."                | Yes (Mock) |
| 21              | "Check balance for account ABCDE." (Invalid Input)                                                                      | `account_info`                 | `account_number=ABCDE`                                | -                           | "That doesn't seem to be a valid account number. It should be a 12-digit number."                 | No         |

## 10. Mock Data & Compliance

### Data Sources

- **Accounts**: 100 realistic mock accounts
- **Cards**: 182 associated cards with various states
- **Transactions**: 13,374+ transaction records
- **Branches**: 50+ branch locations across India
- **ATMs**: 200+ ATM locations
- **Complaints**: 200 mock complaint records
- **All data is completely synthetic with no real PII**

### Compliance Features

- **Data Masking**: Account numbers displayed as `******4157`
- **No Real Data**: 100% synthetic dataset. Generated using Faker Python Package
- **Privacy Protection**: No personal information exposed
- **Secure Logging**: Structured logs without sensitive data

## 11. Innovation & Technical Excellence

### Innovative Features

1. **Adaptive Persona**: AI that adjusts tone based on user emotional state
2. **Smart Fallback Architecture**: Seamless database failover
3. **Foreign Key Validation**: Intelligent data integrity handling
4. **Proactive Assistance**: Context-aware suggestions
5. **Multi-Channel Ready**: Voice and chat optimized

### Technical Achievements

- **Zero Downtime Deployment**: Blue-green deployment ready
- **Horizontal Scalability**: Stateless design for scaling
- **Comprehensive Monitoring**: Health checks and metrics
- **Error Recovery**: Graceful failure handling
- **Performance Optimized**: Async operations throughout

## 12. Future Enhancements

### Phase 2 Features

- **Multi-Language Support**: Extended language coverage
- **Voice Optimization**: Speech-specific response formatting
- **Analytics Dashboard**: Usage metrics and insights
- **Machine Learning**: Predictive assistance based on user patterns
- **Integration Framework**: Easy bank-specific customization

### Scalability Roadmap

- **Microservices**: Service decomposition for scale
- **Caching Layer**: Redis for improved performance
- **Load Balancing**: Multi-region deployment
- **Real-time Analytics**: Live dashboard for operations

---

---

### 13\. Scenario Demo Videos

To demonstrate the functionality of each scenario, we have prepared short video recordings.

| SR.             | Scenario Description                                                                   | YouTube Demo Link                        |
| --------------- | -------------------------------------------------------------------------------------- | ---------------------------------------- |
| **Happy Paths** |                                                                                        |                                          |
| 1               | "What is my account balance?"                                                          | [Link](https://youtu.be/5yVpCyzgQwE)     |
| 2               | "Show me my last 5 transactions."                                                      | [Link](https://youtu.be/0NjQa58Hv00)     |
| 3               | "I lost my card, please block it."                                                     | [Link](https://youtu.be/G4yhhR1tDPU)     |
| 4               | "Block my card ending in 8491."                                                        | [Link](https://youtu.be/G4yhhR1tDPU)     |
| 5               | "I want to dispute a transaction of 100 rupees to a fradulent online store yesterday." | [Link](https://youtu.be/fueIDX2gHnE)     |
| 6               | "I want to register a complaint regarding the mobile app's crashing issues."           | [Link](https://youtu.be/XBConQAAWxs)     |
| 7               | "What's the status of my ticket COMPLAINT69541?"                                       | [Link](https://www.google.com/search?q=) |
| 8               | "Find the nearest branch in bangalore"                                                 | [Link](https://youtu.be/_dW3W0RCBKs)     |
| 9               | "Where is an ATM near pincode 429096?"                                                 | [Link](https://youtu.be/qZmmcuvRSOo)     |
| 10              | "Can you check my KYC status?"                                                         | [Link](https://www.google.com/search?q=) |
| 11              | "What is the status of cheque number 393742?"                                          | [Link](https://youtu.be/zEQtHUGhMko)     |
| 12              | "Tell me about the current fixed deposit interest rates."                              | [Link](https://youtu.be/z9UwC3UarWU)     |
| 13              | "I want to know my loan status, ID is LN77584."                                        | [Link](https://youtu.be/wDvfWkXN-I4)     |
| **Edge Cases**  |                                                                                        |                                          |
| 14              | "I want to speak to a human agent."                                                    | [Link](https://www.google.com/search?q=) |
| 15              | "I have a card issue." (Ambiguous)                                                     | [Link](https://www.google.com/search?q=) |
| 16              | "Mera balance batao." (Language Switch)                                                | [Link](https://www.google.com/search?q=) |
| 17              | "Branch in Mumbai" (Disambiguation)                                                    | [Link](https://www.google.com/search?q=) |
| 18              | "Dispute for a transaction that doesn't exist."                                        | [Link](https://www.google.com/search?q=) |
| 19              | (API timeout during balance check)                                                     | [Link](https://www.google.com/search?q=) |
| 20              | "This is useless, get me a person." (Frustration)                                      | [Link](https://www.google.com/search?q=) |
| 21              | "Check balance for account ABCDE." (Invalid Input)                                     | [Link](https://www.google.com/search?q=) |

**For all the Test case Scenarios check this Playlist Link**: [Link](https://www.youtube.com/playlist?list=PLkEGhqyjM49mF9Zd2iA235UXegDtLUzgr)

---

## 14. Inya.ai Agent Link

- **Chat Version:** [Link](https://app.inya.ai/chat-demo/ed8bb8ea-ccd5-4321-861f-b33c0c9fa1d5)
- **Web Based Voice:** [Link](https://app.inya.ai/demo/25a3c6ca-388f-4e32-bb84-57da53b4a972)
- **Agent Call Version** [link](https://app.inya.ai/demo/25a3c6ca-388f-4e32-bb84-57da53b4a972)

#### Note: For the Bank Name give `Mauryan Bank` as the input value.

## 15. Social Media Interactions

- **LinkedIn Post:** [Link](https://www.linkedin.com/posts/codex-mohan_ai-banking-fintech-activity-7378826377535455232-K6yx)

---

## Conclusion

BankWise AI's "Aria" represents a comprehensive solution for inbound banking support that successfully addresses all required scenarios while maintaining the highest standards of security, performance, and user experience. Our adaptive persona system and robust architecture make it production-ready for real-world banking environments.

**Repository**: [https://github.com/codex-mohan/BankWise](https://bankwise-fekm.onrender.com/)
**Live Demo**: [https://bankwise-fekm.onrender.com/](https://bankwise-fekm.onrender.com/)
**Documentation**: [https://bankwise-fekm.onrender.com/docs](https://bankwise-fekm.onrender.com/docs)
**Architecture Diagram of Agent**: [Google Drive Link](https://drive.google.com/file/d/1IAaK96J0UAWVZAFaAqrF5pwE7Cw3ZoKX/view?usp=sharing)
\*\* \*\*: [Google Drive Link](https://drive.google.com/file/d/1og3MJLGJfv418kHd9q1fWbvKQl8cP7AQ/view?usp=sharing)

---

_This submission represents our commitment to innovation in banking technology and AI-powered customer service._
