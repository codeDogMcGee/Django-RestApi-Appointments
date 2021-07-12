# from django.utils.crypto import get_random_string
# unique_id = get_random_string(length=32)

# https://docs.djangoproject.com/en/3.0/topics/auth/passwords/#module-django.contrib.auth.hashers
#  django.contrib.auth.hashers
# check_password(password, encoded)
# make_password(password, salt=None, hasher='default')
# is_password_usable(encoded_password)

from django.utils import timezone
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password, check_password

from api.models import EmailVerificationToken

def create_token() -> dict[str, str]:
    unique_id = get_random_string(length=32)
    return {'text': unique_id, 'hash': make_password(unique_id)}


def delete_tokens_if_expired() -> None:
    for token in EmailVerificationToken.objects.all():
        expiration_datetime = token.created + timezone.timedelta(seconds=token.keep_alive_seconds)
        if timezone.now() > expiration_datetime:
            token.delete()

def check_token(token_string: str, token_hash: str) -> bool:
    return check_password(token_string, token_hash)