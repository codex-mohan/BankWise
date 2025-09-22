# Error Handling Guide for AI Banking Agent

This guide outlines common error scenarios that the AI agent might encounter when interacting with users or mock APIs, and the recommended strategies for error recovery, fallback, and graceful responses. This aligns with the hackathon's requirement for "error recovery" and handling "API timeout or 500 with a graceful retry and fallback."

## 1. API Errors

### 1.1. API Timeout or 500 (Internal Server Error)
- **Scenario:** The mock API for a service (e.g., balance, transactions) does not respond within the expected time or returns a server error.
- **Agent Behavior:**
    1.  **Initial Attempt:** "I'm having a little trouble connecting to our systems right now. Please bear with me for a moment while I try again."
    2.  **Retry:** Automatically retry the API call once.
    3.  **Fallback Message (after retry failure):** "I apologize, it seems there's a temporary issue with our service. I'm unable to fetch your [service, e.g., balance] at this moment. Please try again after some time, or I can connect you to a human agent if you prefer."
    4.  **Escalation:** Offer to escalate to a human agent.

### 1.2. Data Not Found (e.g., Dispute for Non-existent Transaction)
- **Scenario:** A user attempts an action (e.g., raise a dispute for a transaction) but the provided entity (e.g., transaction ID, amount, date) does not match any record in the mock ledger.
- **Agent Behavior:**
    1.  **Clarification:** "I couldn't find a transaction matching the details you provided. Could you please confirm the amount and date of the transaction you wish to dispute?"
    2.  **Re-prompt:** Allow the user to re-enter details.
    3.  **Fallback/Guidance:** If still not found after re-prompt: "I'm still unable to locate that transaction. Please ensure you're providing the correct details. If you believe there's an error, I can help you register a general complaint, or connect you to an agent for further assistance."

### 1.3. Invalid Input/Entity Format
- **Scenario:** User provides an entity in an incorrect format (e.g., account number with letters, invalid date format).
- **Agent Behavior:**
    1.  **Specific Error Message:** "The [entity, e.g., account number] you provided doesn't seem to be in the correct format. Please ensure it's a 12-digit number."
    2.  **Re-prompt:** Ask the user to re-enter the information.
    3.  **Guidance:** "If you're having trouble, you can also say 'speak to agent' to connect with a human."

## 2. NLU (Natural Language Understanding) Errors

### 2.1. Ambiguous Request
- **Scenario:** User utterance is unclear or could map to multiple intents (e.g., "my card issue").
- **Agent Behavior:**
    1.  **Clarification:** "Could you please tell me more about your card issue? Are you looking to block your card, raise a dispute, or something else?"
    2.  **Offer Options:** Present the most likely intents as options.

### 2.2. Low Confidence Intent Detection
- **Scenario:** The NLU model detects an intent but with low confidence.
- **Agent Behavior:**
    1.  **Confirmation:** "Did you want to check your account balance?" (If `account_info` was the low-confidence intent).
    2.  **Re-prompt/Options:** If confirmation is negative or unclear: "I apologize, I didn't quite catch that. Could you please rephrase, or tell me what you'd like to do from these options: check balance, block card, or raise a complaint?"

## 3. ASR (Automatic Speech Recognition) Errors

### 3.1. ASR Confusion (e.g., Numbers, Pincodes)
- **Scenario:** The ASR misinterprets numbers, especially for critical entities like account numbers or pincodes.
- **Agent Behavior:**
    1.  **Explicit Confirmation:** "I heard your account number as [ASR output]. Is that correct?"
    2.  **Digit-by-Digit Confirmation:** If confusion persists: "Could you please tell me your account number digit by digit?"
    3.  **Fallback to Chat/Human:** If repeated ASR failures occur, offer to switch to chat or connect to a human agent.

## 4. Dialogue Management Errors

### 4.1. Missing Entities
- **Scenario:** An intent is detected, but required entities are missing (e.g., `card_block` without `last4`).
- **Agent Behavior:**
    1.  **Polite Prompt:** "To block your card, I need the last four digits of your card number. Could you please provide them?"
    2.  **Contextual Help:** "If you don't have it handy, you can also find it on your mobile banking app."

### 4.2. Repeated Failures / User Frustration
- **Scenario:** User expresses frustration or the agent fails to resolve the issue after a finite number of attempts.
- **Agent Behavior:**
    1.  **De-escalation:** "I understand this can be frustrating, and I apologize for the inconvenience."
    2.  **Proactive Escalation:** "It seems I'm having trouble assisting you with this particular request. I can connect you to a human agent who can help you further. Would you like me to do that?" (This aligns with `speak_to_agent` intent).