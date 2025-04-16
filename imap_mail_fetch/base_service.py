import hashlib
def hash_sha256(data: str) -> str:
    """Generate SHA256 hash of the given string."""
    return hashlib.sha256(data.encode()).hexdigest()