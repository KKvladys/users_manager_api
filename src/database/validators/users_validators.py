import email_validator


def validate_name(name: str):
    """
    Validate the user's name.
    """
    if not name.strip():
        raise ValueError("Name cannot be empty.")
    if len(name) > 255:
        raise ValueError("Name is too long (max 255 characters)")
    return name


def validate_email(user_email: str) -> str:
    """
    Function to validate the provided email using the
    'email_validator' library. It also normalizes the email if valid.
    """
    try:
        email_info = email_validator.validate_email(user_email, check_deliverability=False)
        email = email_info.normalized
    except email_validator.EmailNotValidError as error:
        raise ValueError(str(error))
    else:
        return email
