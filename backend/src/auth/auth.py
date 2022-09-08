import json
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen
import os

# Read values for environemnt variables

AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN', 'dev--0iw-l86.us.auth0.com')
ALGORITHMS = os.getenv('ALGORITHMS', ['RS256'])
API_AUDIENCE = os.getenv('API_AUDIENCE', 'http://localhost:4200/')

# AuthError Exception


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header

def get_token_auth_header():
    auth_header = request.headers.get('Authorization', None)
    if not auth_header:
        raise AuthError({
            'code': 'missing_header',
            'description': 'Authorization header  is not found.'
        }, 401)

    header_parts = auth_header.split()
    if header_parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_token',
            'description': 'Authorization header is invalid. it  must start with "Bearer".'
        }, 401)

    elif len(header_parts) == 1:
        raise AuthError({
            'code': 'invalid_token',
            'description': 'Token not found in authorization header.'
        }, 401)

    elif len(header_parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header does not contain a valid token'
        }, 401)

    token = header_parts[1]
    return token


# This will check is the user has permissions like get:drinks-detail,
# post:drinks, delete:drinks and patch:drinks

def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'User doesnot have a permission to access this resource'
        }, 400)
    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'User doesnot have a permission to access this resource'
        }, 401)
    return True


# Decode and veryfy JWT token
def verify_decode_jwt(token):
    auth0_json_url = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(auth0_json_url.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for secret_key in jwks['keys']:
        if secret_key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': secret_key['kty'],
                'kid': secret_key['kid'],
                'use': secret_key['use'],
                'n': secret_key['n'],
                'e': secret_key['e']
            }
    if rsa_key:
        try:
            # Decode JWT
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token has been expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. it may related to incorrect issuer or identity'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Something went wrong. Unable to parse authentication token.'
            }, 400)
    raise AuthError({
        'code': 'invalid_header',
                'description': 'JWT cannot be decoded. Unable to find the appropriate key.'
    }, 400)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            has_permission = check_permissions(permission, payload)
            if not has_permission:
                return "user has no permission"
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
