from django.contrib.auth import get_user_model

from rest_framework import serializers


def _validate_email(email):
    user_model = get_user_model()

    if email != "":
        try:
            if user_model.objects.get(email__iexact=email):
                raise serializers.ValidationError("Email already in use.")
        except user_model.DoesNotExist:
            return email
    else:
        raise serializers.ValidationError("Email can not be blank")


def _validate_password(password, confirm_password):
    if password != confirm_password:
        raise serializers.ValidationError("Passwords do not match.")
    if len(password) > 68 or len(password) < 6:
        raise serializers.ValidationError("Check the length for password")
    if password.isdigit():
        raise serializers.ValidationError("Contain at least 1 Alphabet")
    if password.isupper() or password.islower():
        raise serializers.ValidationError("Must contain atleast 1 Uppercase and 1 Lowercase")
    for character in password:
        if character in [
            "~",
            "!",
            "@",
            "#",
            "$",
            "%",
            "^",
            "&",
            "*",
            "-",
            "+",
            "=",
        ]:
            return password
    raise serializers.ValidationError("Must contain atleast 1 Special Character (~,!,@,$,#,$,%,^,&,*,-,+,=)")


def _validate_mobile_number(mobile_number):
    user_model = get_user_model()
    if mobile_number != "":
        if mobile_number.isdigit():
            try:
                if user_model.objects.get(mobile_number=mobile_number):
                    return mobile_number
            except user_model.DoesNotExist:
                raise serializers.ValidationError("mobile_number not exist.", code="mobile_number")
        else:
            raise serializers.ValidationError("mobile_number must contain only numbers", code="mobile_number")
    else:
        raise serializers.ValidationError("mobile_number can not be blank", code="mobile_number")
