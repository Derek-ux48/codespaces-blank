import hashlib

def generate_secure_hash(amount, till_number, reference):
    """
    Simulates creating a cryptographic digital signature for the transaction.
    This prevents anyone from tampering with the bill amount mid-transit.
    """
    # Combine the data into a secret data string
    secret_salt = "SUPER_SECRET_RETAIL_KEY_2026"
    raw_data = f"{till_number}|{amount}|{reference}|{secret_salt}"
    
    # Generate a secure SHA-256 hash (One-way encryption)
    secure_signature = hashlib.sha256(raw_data.encode()).hexdigest()
    
    return secure_signature
