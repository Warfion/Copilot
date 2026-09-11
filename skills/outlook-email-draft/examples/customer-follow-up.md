# Customer follow-up

Fictional input supplied in the current conversation: "We reviewed the draft
architecture with the customer. Network requirements are still open. Ask the
customer to share them. No deadline or recipient address has been confirmed."

Email preview

Integration: Microsoft 365 Mail MCP
Target: Signed-in user's mailbox (account address unverified)
To: (empty)
CC: (empty)
BCC: (empty)
Subject: Follow-up: network requirements for the draft architecture
Body type: Text

Body:

Hello,

Thank you for reviewing the draft architecture with us.

The network requirements remain open. Please share the relevant requirements
so we can assess their implications for the architecture.

Kind regards,
[Your name]

Context sources used:

- Current conversation

Assumptions:

- A professional customer-facing tone is appropriate.

Missing information:

- Recipient address; the user agreed to leave recipient fields empty.
- Sender name; the closing contains a visible placeholder.
- No deadline has been agreed or included.

Would you like me to create this message in Outlook Drafts?

Use `contentType: Text` for this English email. Stop and wait for the user's response.
If approved, invoke the verified draft tool with normal VS Code tool confirmation.
Only after the result confirms draft state and no sending:
"The email was saved as a draft and was not sent."
