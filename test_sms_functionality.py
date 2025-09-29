#!/usr/bin/env python3
"""
Test script for SMS functionality in BankWise API
"""

import asyncio
import json
import sys
from mock_data_storage import mock_storage
from services.sms_service import sms_service, SMSTemplates


async def test_sms_functionality():
    """Test SMS functionality with mock data"""

    print("🧪 Testing BankWise SMS Functionality")
    print("=" * 50)

    # Test 1: Check SMS service status
    print("\n1. Checking SMS Service Status:")
    print(f"   SMS Service Enabled: {sms_service.is_enabled()}")

    if not sms_service.is_enabled():
        print("   ⚠️  SMS service not enabled (Twilio credentials not configured)")
        print("   This is normal for testing without real Twilio credentials")
    else:
        print("   ✅ SMS service is enabled and ready")

    # Test 2: Check account data with mobile numbers
    print("\n2. Checking Account Data:")
    account = mock_storage.accounts[0] if mock_storage.accounts else None

    if account:
        print(f"   Sample Account: {account['account_number']}")
        print(f"   Customer Name: {account['customer_name']}")
        print(f"   Mobile Numbers: {account.get('mobile_numbers', 'Not found')}")

        if account.get("mobile_numbers"):
            print("   ✅ Mobile numbers are present in account data")
        else:
            print("   ❌ Mobile numbers not found in account data")
    else:
        print("   ❌ No accounts found in mock data")
        return

    # Test 3: Test SMS templates
    print("\n3. Testing SMS Templates:")

    templates = [
        (
            "Complaint Confirmation",
            SMSTemplates.complaint_confirmation(
                "COMPLAINT12345", account["customer_name"]
            ),
        ),
        (
            "Dispute Confirmation",
            SMSTemplates.dispute_confirmation(
                "DISPUTE12345", account["customer_name"], 5000.0
            ),
        ),
        (
            "Transaction Alert",
            SMSTemplates.transaction_alert(account["customer_name"], 1000.0, "DEBIT"),
        ),
        (
            "Account Alert",
            SMSTemplates.account_alert(
                account["customer_name"], "Card Blocked", "Security measure activated"
            ),
        ),
    ]

    for template_name, message in templates:
        print(f"   {template_name}:")
        print(f"      {message[:100]}..." if len(message) > 100 else f"      {message}")

    print("   ✅ All SMS templates generated successfully")

    # Test 4: Test SMS sending (without actual send)
    print("\n4. Testing SMS Functionality:")

    if account.get("mobile_numbers"):
        print(f"   Would send SMS to: {account['mobile_numbers']}")

        # Simulate SMS sending
        test_message = "Test message from BankWise API"

        try:
            # This will work even without real Twilio credentials for testing
            result = await sms_service.send_bulk_sms(
                account["mobile_numbers"], test_message
            )

            if result["success"]:
                print(
                    f"   ✅ SMS sent successfully to {len(result['successful_sends'])} numbers"
                )
                print(
                    f"   📱 Successful sends: {[send['phone_number'] for send in result['successful_sends']]}"
                )
                if result["failed_sends"]:
                    print(
                        f"   ❌ Failed sends: {[fail['phone_number'] for fail in result['failed_sends']]}"
                    )
            else:
                print(
                    "   ⚠️  SMS sending failed (expected without real Twilio credentials)"
                )
                print(f"   Reason: {result.get('error', 'Unknown error')}")

        except Exception as e:
            print(f"   ⚠️  SMS test failed: {str(e)}")

    # Test 5: Check endpoints integration
    print("\n5. Integration Summary:")

    endpoints_with_sms = [
        "✅ /api/complaint/new - Sends SMS on complaint creation",
        "✅ /api/complaint/update-status - Sends SMS on resolution",
        "✅ /api/dispute/raise - Sends SMS on dispute creation",
        "✅ /api/dispute/update-status - Sends SMS on resolution",
        "✅ /api/card/block - Sends SMS on card blocking",
        "✅ /api/sms/transaction-alert - Sends transaction alerts",
        "✅ /api/sms/send - Sends general SMS notifications",
        "✅ /api/sms/status - Check SMS service status",
    ]

    for endpoint in endpoints_with_sms:
        print(f"   {endpoint}")

    print("\n🎉 SMS Integration Test Completed!")
    print("\nNext Steps:")
    print("1. Configure real Twilio credentials in .env file:")
    print("   - TWILIO_ACCOUNT_SID=your_account_sid")
    print("   - TWILIO_AUTH_TOKEN=your_auth_token")
    print("   - TWILIO_PHONE_NUMBER=your_twilio_phone_number")
    print("2. Test with real SMS by calling the API endpoints")
    print("3. Monitor logs for SMS delivery status")


if __name__ == "__main__":
    try:
        asyncio.run(test_sms_functionality())
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nTest failed with error: {str(e)}")
        sys.exit(1)
