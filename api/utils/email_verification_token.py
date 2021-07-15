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
    acceptable_chars = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    unique_id = get_random_string(length=6, allowed_chars=acceptable_chars)
    return {'text': unique_id, 'hash': make_password(unique_id)}


def delete_tokens_if_expired() -> None:
    for token in EmailVerificationToken.objects.all():
        expiration_datetime = token.created + timezone.timedelta(seconds=token.keep_alive_seconds)
        if timezone.now() > expiration_datetime:
            token.delete()

def check_token(token_string: str, token_hash: str) -> bool:
    return check_password(token_string, token_hash)


def create_unique_token() -> dict[str, str]:
    token_object = None
    while token_object is None:

        token_object = create_token()
        token_matched = False
        existing_tokens = EmailVerificationToken.objects.all()
        for token_to_try in existing_tokens:
            if token_matched is False:
                token_matched = check_token(token_object['text'], token_to_try.key)

        # If there's a match set token_object to None so it'll try again.
        if token_matched:
            token_object = None

    return token_object
