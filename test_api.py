#!/usr/bin/env python3
"""
Test script for the Banking Support API
"""

import asyncio
import aiohttp
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

async def test_api_endpoints():
    """Test all API endpoints"""
    async with aiohttp.ClientSession() as session:
        print("🧪 Testing Banking Support API...")
        print("=" * 50)
        
        # Test health check
        await test_health_check(session)
        
        # Test account balance
        await test_account_balance(session)
        
        # Test transaction history
        await test_transaction_history(session)
        
        # Test card blocking
        await test_card_block(session)
        
        # Test complaint creation
        await test_complaint_creation(session)
        
        # Test branch locator
        await test_branch_locator(session)
        
        # Test ATM locator
        await test_atm_locator(session)
        
        # Test KYC status
        await test_kyc_status(session)
        
        # Test FD rates
        await test_fd_rates(session)
        
        # Test loan status
        await test_loan_status(session)
        
        # Test escalation
        await test_escalation(session)
        
        # Test intent processing
        await test_intent_processing(session)
        
        print("\n✅ All tests completed!")

async def test_health_check(session):
    """Test health check endpoint"""
    try:
        async with session.get(f"{BASE_URL}/health") as response:
            if response.status == 200:
                data = await response.json()
                print(f"✅ Health Check: {data['status']} | Sessions: {data['active_sessions']}")
            else:
                print(f"❌ Health Check Failed: {response.status}")
    except Exception as e:
        print(f"❌ Health Check Error: {e}")

async def test_account_balance(session):
    """Test account balance endpoint"""
    try:
        request_data = {
            "account_number": "123456789012"
        }
        async with session.post(f"{BASE_URL}/api/account/balance", json=request_data) as response:
            if response.status == 200:
                data = await response.json()
                print(f"✅ Account Balance: ₹{data['balance']:,} | Account: {data['account_number']}")
            else:
                print(f"❌ Account Balance Failed: {response.status}")
    except Exception as e:
        print(f"❌ Account Balance Error: {e}")

async def test_transaction_history(session):
    """Test transaction history endpoint"""
    try:
        request_data = {
            "account_number": "123456789012",
            "limit": 3
        }
        async with session.post(f"{BASE_URL}/api/account/transactions", json=request_data) as response:
            if response.status == 200:
                data = await response.json()
                print(f"✅ Transaction History: {data['total_count']} transactions")
                for tx in data['transactions'][:2]:  # Show first 2 transactions
                    print(f"   - {tx['date']}: ₹{tx['amount']:,} | {tx['description']}")
            else:
                print(f"❌ Transaction History Failed: {response.status}")
    except Exception as e:
        print(f"❌ Transaction History Error: {e}")

async def test_card_block(session):
    """Test card blocking endpoint"""
    try:
        request_data = {
            "last4": "9012",
            "reason": "Lost card"
        }
        async with session.post(f"{BASE_URL}/api/card/block", json=request_data) as response:
            if response.status == 200:
                data = await response.json()
                print(f"✅ Card Block: {data['content']} | Ticket: {data['ticket_id']}")
            else:
                print(f"❌ Card Block Failed: {response.status}")
    except Exception as e:
        print(f"❌ Card Block Error: {e}")

async def test_complaint_creation(session):
    """Test complaint creation endpoint"""
    try:
        request_data = {
            "subject": "ATM Not Working",
            "description": "ATM machine is not dispensing cash",
            "category": "ATM"
        }
        async with session.post(f"{BASE_URL}/api/complaint/new", json=request_data) as response:
            if response.status == 200:
                data = await response.json()
                print(f"✅ Complaint Created: {data['content']} | Ticket: {data['ticket_id']}")
            else:
                print(f"❌ Complaint Creation Failed: {response.status}")
    except Exception as e:
        print(f"❌ Complaint Creation Error: {e}")

async def test_branch_locator(session):
    """Test branch locator endpoint"""
    try:
        request_data = {
            "branch_city": "Mumbai",
            "limit": 2
        }
        async with session.post(f"{BASE_URL}/api/branch/locate", json=request_data) as response:
            if response.status == 200:
                data = await response.json()
                print(f"✅ Branch Locator: {data['total_count']} branches in Mumbai")
                for branch in data['branches'][:1]:  # Show first branch
                    print(f"   - {branch['name']} | {branch['address']}")
            else:
                print(f"❌ Branch Locator Failed: {response.status}")
    except Exception as e:
        print(f"❌ Branch Locator Error: {e}")

async def test_atm_locator(session):
    """Test ATM locator endpoint"""
    try:
        request_data = {
            "pincode": "400001",
            "limit": 2
        }
        async with session.post(f"{BASE_URL}/api/atm/locate", json=request_data) as response:
            if response.status == 200:
                data = await response.json()
                print(f"✅ ATM Locator: {data['total_count']} ATMs in 400001")
                for atm in data['atms'][:1]:  # Show first ATM
                    print(f"   - {atm['bank_name']} | {atm['address']}")
            else:
                print(f"❌ ATM Locator Failed: {response.status}")
    except Exception as e:
        print(f"❌ ATM Locator Error: {e}")

async def test_kyc_status(session):
    """Test KYC status endpoint"""
    try:
        request_data = {
            "account_number": "123456789012"
        }
        async with session.post(f"{BASE_URL}/api/kyc/status", json=request_data) as response:
            if response.status == 200:
                data = await response.json()
                print(f"✅ KYC Status: {data['kyc_status']} | Level: {data['verification_level']}")
            else:
                print(f"❌ KYC Status Failed: {response.status}")
    except Exception as e:
        print(f"❌ KYC Status Error: {e}")

async def test_fd_rates(session):
    """Test FD rates endpoint"""
    try:
        request_data = {}
        async with session.post(f"{BASE_URL}/api/fd/rates", json=request_data) as response:
            if response.status == 200:
                data = await response.json()
                print(f"✅ FD Rates: {len(data['rates'])} rate tiers available")
                # Show first few rates
                for rate in data['rates'][:3]:
                    print(f"   - {rate['tenure']} days: {rate['rate']}%")
            else:
                print(f"❌ FD Rates Failed: {response.status}")
    except Exception as e:
        print(f"❌ FD Rates Error: {e}")

async def test_loan_status(session):
    """Test loan status endpoint"""
    try:
        request_data = {
            "loan_id": "LN12345"
        }
        async with session.post(f"{BASE_URL}/api/loan/status", json=request_data) as response:
            if response.status == 200:
                data = await response.json()
                loan = data['loan_info']
                print(f"✅ Loan Status: {loan['status']} | EMI: ₹{loan['emi_amount']:,}")
            else:
                print(f"❌ Loan Status Failed: {response.status}")
    except Exception as e:
        print(f"❌ Loan Status Error: {e}")

async def test_escalation(session):
    """Test escalation endpoint"""
    try:
        request_data = {
            "reason": "Need human assistance for complex issue",
            "urgency": "high"
        }
        async with session.post(f"{BASE_URL}/api/escalate", json=request_data) as response:
            if response.status == 200:
                data = await response.json()
                print(f"✅ Escalation: Agent {data['agent_id']} | Wait: {data['estimated_wait_time']} min")
            else:
                print(f"❌ Escalation Failed: {response.status}")
    except Exception as e:
        print(f"❌ Escalation Error: {e}")

async def test_intent_processing(session):
    """Test intent processing endpoint"""
    try:
        request_data = {
            "text": "What is my account balance?",
            "session_id": "test_session_123"
        }
        async with session.post(f"{BASE_URL}/api/chat/intent", json=request_data) as response:
            if response.status == 200:
                data = await response.json()
                print(f"✅ Intent Processing: {data['intent']} | Confidence: {data['confidence']:.2f}")
            else:
                print(f"❌ Intent Processing Failed: {response.status}")
    except Exception as e:
        print(f"❌ Intent Processing Error: {e}")

if __name__ == "__main__":
    print("🚀 Starting API Tests...")
    print(f"⏰ Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Run tests
    asyncio.run(test_api_endpoints())
    
    print("\n🎉 API Testing Complete!")
    print("\n💡 To run the API server:")
    print("   python main.py")
    print("\n💡 To run tests with server running:")
    print("   python test_api.py")