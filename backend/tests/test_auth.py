from auth import normalize_email, password_hash


def test_normalize_email_strips_whitespace_and_lowercases():
    assert normalize_email("  User@Example.COM ") == "user@example.com"


def test_password_is_hashed_and_can_be_verified():
    hashed = password_hash.hash("strong-password")

    assert hashed != "strong-password"
    assert password_hash.verify("strong-password", hashed)
    assert not password_hash.verify("wrong-password", hashed)
