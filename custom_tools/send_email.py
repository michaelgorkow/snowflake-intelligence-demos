from snowflake.snowpark import Session

def send_email(session: Session, recipient: str, subject: str, text: str) -> str:
    """
    Sends an email using Snowflake's email functionality.
    
    Args:
        session (Session): Active Snowflake Snowpark session
        recipient (str): Email address of the recipient
        subject (str): Subject line of the email
        text (str): Body content of the email (will be sent as HTML)
    
    Returns:
        str: Confirmation message indicating email was sent
    """
    session.call(
        'SYSTEM$SEND_EMAIL',
        'ai_email_int',
        recipient,
        subject,
        text,
        'text/html'
    )
    
    # Return a confirmation message
    return f'Email was sent to {recipient} with subject: "{subject}".'