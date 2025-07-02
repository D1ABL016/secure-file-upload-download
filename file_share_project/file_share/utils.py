from django.core import signing
from django.conf import settings

def generate_signed_token(data, max_age=None):
    return signing.dumps(data, salt=settings.SECRET_KEY)

def verify_signed_token(token, max_age=None):
    try:
        data = signing.loads(token, salt=settings.SECRET_KEY, max_age=max_age)
        return data
    except signing.BadSignature:
        return None
    except signing.SignatureExpired:
        return None
