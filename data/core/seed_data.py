from database import get_connection


def seed_data():
    conn = get_connection()

    # ---------------------------------------------------------
    # Account
    # ---------------------------------------------------------
    conn.execute(
        """
        INSERT OR IGNORE INTO Account
        (account_id, account_name, platform, status)
        VALUES (1, 'CultPass', 'Internal CRM', 'active')
        """
    )

    # ---------------------------------------------------------
    # Users
    # ---------------------------------------------------------
    users = [
        (1, "CULT-001", "Rahul", "rahul@example.com"),
        (1, "CULT-002", "Priya", "priya@example.com"),
        (1, "CULT-003", "Arun", "arun@example.com"),
    ]

    for account_id, external_id, name, email in users:
        conn.execute(
            """
            INSERT OR IGNORE INTO User
            (account_id, external_user_id, name, email)
            VALUES (?, ?, ?, ?)
            """,
            (account_id, external_id, name, email),
        )

    # ---------------------------------------------------------
    # Tickets
    # ---------------------------------------------------------
    tickets = [
        (
            1,
            "Unable to login",
            "I cannot login to my CultPass account.",
            "chat",
        ),
        (
            2,
            "Payment failed",
            "My payment failed while renewing my subscription.",
            "email",
        ),
        (
            3,
            "Refund status",
            "I requested a refund and want to know its status.",
            "web",
        ),
    ]

    for user_id, subject, description, channel in tickets:
        conn.execute(
            """
            INSERT INTO Ticket
            (user_id, subject, description, channel)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, subject, description, channel),
        )

    # ---------------------------------------------------------
    # Knowledge Base
    # ---------------------------------------------------------
    articles = [
        (
            "Account Creation",
            "account",
            "Customers can create a CultPass account using their registered email address.",
        ),
        (
            "Password Reset",
            "account",
            "Customers who forget their password can use the password reset option on the login page. A reset link is sent to the registered email address.",
        ),
        (
            "Login Problems",
            "technical",
            "If login fails, verify the registered email, reset the password, and retry. Repeated failures may require support escalation.",
        ),
        (
            "Subscription Plans",
            "subscription",
            "CultPass provides multiple subscription plans. Customers can view available plans from the subscription section of the application.",
        ),
        (
            "Subscription Cancellation",
            "subscription",
            "Customers can cancel an active subscription from subscription settings. Cancellation prevents future renewal according to the applicable plan terms.",
        ),
        (
            "Subscription Renewal",
            "subscription",
            "Subscriptions can renew automatically when auto-renewal is enabled. Customers can manage renewal settings from their subscription page.",
        ),
        (
            "Refund Policy",
            "billing",
            "Refund eligibility depends on the applicable CultPass refund policy and transaction status. Eligible refund requests are processed through the support process.",
        ),
        (
            "Refund Status",
            "billing",
            "Customers can contact support to check the status of an existing refund request. Support can verify the associated transaction.",
        ),
        (
            "Payment Failure",
            "billing",
            "If a payment fails, verify payment details and retry the transaction. If the issue continues, support should verify the transaction status.",
        ),
        (
            "Duplicate Payment",
            "billing",
            "If a customer believes they were charged twice, support should verify the transaction history before initiating any refund process.",
        ),
        (
            "Booking Problems",
            "booking",
            "If a booking fails, verify availability, booking details, and payment status. Persistent booking failures should be escalated to support.",
        ),
        (
            "Application Technical Issues",
            "technical",
            "For application issues, customers should restart the application, verify connectivity, and retry. Persistent technical failures should be escalated.",
        ),
        (
            "Profile Update",
            "account",
            "Customers can update supported profile information from their account settings.",
        ),
        (
            "Account Closure",
            "account",
            "Customers can request account closure through support. The request must be validated before processing.",
        ),
        (
            "Membership Pause",
            "subscription",
            "Customers may request a membership pause where the applicable subscription plan supports this feature.",
        ),
        (
            "Coupon and Promotional Codes",
            "billing",
            "Promotional codes must be valid and applicable to the selected subscription or transaction. Invalid or expired codes cannot be applied.",
        ),
        (
            "Invoice and Billing Details",
            "billing",
            "Customers can request billing and invoice information for completed transactions. Support can verify transaction details before providing information.",
        ),
        (
            "Escalation Policy",
            "support",
            "Issues without sufficient knowledge-base coverage, unresolved technical failures, or low-confidence cases should be escalated to a human support team.",
        ),
    ]

    for title, category, content in articles:
        conn.execute(
            """
            INSERT INTO Knowledge
            (title, category, content, source)
            VALUES (?, ?, ?, ?)
            """,
            (title, category, content, "CultPass Support KB"),
        )

    conn.commit()
    conn.close()

    print("CultPass sample data seeded successfully.")
    print(f"Knowledge articles added: {len(articles)}")


if __name__ == "__main__":
    seed_data()