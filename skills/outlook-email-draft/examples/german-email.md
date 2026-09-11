# German Email Draft

Fictional context: Requirements have been discussed, but the interface list is
still missing. Ask the customer to provide it. No recipient address or delivery
date is known. The requested email language is German.

Email preview

Integration: Microsoft 365 Mail MCP
Target: Signed-in user's mailbox (account address unverified)
To: (empty)
CC: (empty)
BCC: (empty)
Subject: Nachbesprechung: Übersicht der Schnittstellen
Body type: Text

Body:

Guten Tag,

vielen Dank für das Gespräch zu den Anforderungen.

Für die weitere Abstimmung fehlt uns noch die Übersicht der Schnittstellen.
Bitte lassen Sie uns diese zukommen, damit wir die offenen Anforderungen
gemeinsam klären können.

Mit freundlichen Grüßen
[Ihr Name]

Context sources used:

- Current conversation

Assumptions:

- A formal customer-facing tone is appropriate.

Missing information:

- The recipient address is unknown; the user agreed to leave recipients empty.
- The sender's name is unknown and remains a visible placeholder in the body.
- No deadline has been confirmed, so none is included.

Would you like me to create this message in Outlook Drafts?

Use `contentType: Text`. Create the draft only after explicit approval in a
subsequent response and normal VS Code tool confirmation. Once the result
confirms draft state and no sending, report:
"The email was saved as a draft and was not sent."
