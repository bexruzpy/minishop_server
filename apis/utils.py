import json, base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

def create_license(data: dict):
    # Private keyni yuklash
    with open("private_key.pem", "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)

    # JSON ma’lumot
    license_json = json.dumps(data).encode()

    # RSA bilan imzolash
    signature = private_key.sign(
        license_json,
        padding.PKCS1v15(),
        hashes.SHA256()
    )

    # Litsenziya fayl
    license_file = {
        "data": base64.b64encode(license_json).decode(),
        "signature": base64.b64encode(signature).decode()
    }
    return license_file

if __name__ == "__main__":
    # Misol uchun litsenziya
    data = {
        "user": "Bexruz",
        "product": "minishop",
        "expire": "2026-01-01"
    }
    create_license(data)
