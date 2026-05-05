def get_credentials(kind: str = "valid"):
    credentials = {
        "valid": ("test.user@example.com", "Password123!"),
        "invalid": ("wrong.user@example.com", "WrongPass"),
    }
    return credentials.get(kind, credentials["invalid"])
