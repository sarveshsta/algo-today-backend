import inspect

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.deprecation import MiddlewareMixin

import jwt
from asgiref.sync import async_to_sync

from core.tokens import SessionTokenObtainPairSerializer
from user.models import UserSession

SECRET_KEY = settings.SECRET_KEY


class JWTMiddleware(MiddlewareMixin):
    """
    Custom JWT authentication middleware.

    This middleware handles JWT authentication logic, including decoding and verification
    of JWT tokens, handling expired tokens, and managing user sessions.

    Attributes:
    - `user_model`: The user model for the Django project.
    - `refresh_token_lookup`: The header key used to look up the refresh token.
    - `access_token_lookup`: The header key used to look up the access token.
    - `claim_id`: The claim ID used in the JWT payload to identify the user.
    - `algorithms`: The list of algorithms used for JWT verification.

    Example:
    ```python
    class MyView(APIView):
        authentication_classes = [JWTMiddleware]
        ...
    ```
    """

    user_model = get_user_model()
    refresh_token_lookup = "x-refresh"
    access_token_lookup = "x-access"
    claim_id = settings.SIMPLE_JWT.get("USER_ID_CLAIM", "user_id")
    algorithms = settings.SIMPLE_JWT.get(
        "ALGORITHM",
        [
            "HS256",
        ],
    )

    def get_access_token_for_user(self, user, session_id):
        refresh = SessionTokenObtainPairSerializer.get_token(user=user, session_id=session_id)
        return str(refresh.access_token)

    async def async_function(self, response_data):
        return await response_data

    @classmethod
    def decode_token(cls, token):
        """
        Decode a JWT token.

        Args:
        - `token`: The JWT token to decode.

        Returns:
        - dict: The decoded payload of the JWT token.
        """
        payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=cls.algorithms)
        return payload

    def get_session(self, payload):
        """
        Get the user session associated with the JWT payload.

        Args:
        - `payload`: The decoded payload of the JWT token.

        Returns:
        - UserSession or None: The user session or None if not found.
        """
        try:
            session_id = payload[self.claim_id]
            session = UserSession.objects.get(id=session_id)
            return session
        except UserSession.DoesNotExist:
            return None

    def handle_verified_user(self, response, access_token):
        """
        Handle the response for a verified user.

        Args:
        - `response`: The HTTP response.
        - `access_token`: The valid access token.

        Returns:
        - HTTPResponse: The modified HTTP response.
        """
        return response

    def handle_unverified_user(self, response, access_token, user):
        """
        Handle the response for an unverified user.

        Args:
        - `response`: The HTTP response.
        - `access_token`: The valid access token.
        - `user`: The unverified user.

        Returns:
        - HTTPResponse: The modified HTTP response.
        """
        response.status_code = 401
        res = '{"message": "Email is not verified", "email":"' + user.email + '"}'
        response.headers.setdefault(self.access_token_lookup, access_token)
        response.content = bytes(res, encoding="UTF8")
        return response

    def handle_expired_access_token(self, request, response):
        """
        Handle the case of an expired access token.

        Args:
        - `request`: The HTTP request.
        - `response`: The HTTP response.

        Returns:
        - HTTPResponse: The modified HTTP response.
        """
        try:
            refresh_token = request.headers.get(self.refresh_token_lookup)
            if refresh_token:
                refresh_token_payload = self.decode_token(refresh_token)
                session = self.get_session(refresh_token_payload)
                if session:
                    new_access_token = self.get_access_token_for_user(session.user, session.id)
                    request.META["HTTP_AUTHORIZATION"] = f"Bearer {new_access_token}"
                    request.META[self.access_token_lookup] = new_access_token
                    response = self.get_response(request)
                    if inspect.iscoroutine(response):
                        response = async_to_sync(self.async_function)(response)
                    if session.user.is_active:
                        response.headers.setdefault(self.access_token_lookup, new_access_token)
                    else:
                        return self.handle_unverified_user(response, new_access_token, session.user)
                return response
            response.status_code = 403
            return response
        except UserSession.DoesNotExist:
            response.status_code = 403
            return response
        except jwt.ExpiredSignatureError:
            response.status_code = 403
            return response

    def handle_invalid_token(self, request, response):
        """
        Handle the case of an invalid token.

        Args:
        - `request`: The HTTP request.
        - `response`: The HTTP response.

        Returns:
        - HTTPResponse: The modified HTTP response.
        """
        response.status_code = 403
        return response

    def process_response(self, request, response):
        """
        Process the HTTP response.

        Args:
        - `request`: The HTTP request.
        - `response`: The HTTP response.

        Returns:
        - HTTPResponse: The modified HTTP response.
        """
        if "Authorization" in request.headers:
            access_token = request.headers.get("Authorization").replace("Bearer ", "")
            try:
                access_token_payload = self.decode_token(access_token)
                get_session = self.get_session(access_token_payload)

                if get_session.user.is_active:
                    return self.handle_verified_user(response, access_token)
                else:
                    return self.handle_unverified_user(response, access_token, get_session.user)

            except jwt.ExpiredSignatureError:
                return self.handle_expired_access_token(request, response)

            except jwt.InvalidTokenError:
                return self.handle_invalid_token(request, response)
        else:
            return response
