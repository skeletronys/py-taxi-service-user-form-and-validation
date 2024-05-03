from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator, MinLengthValidator

from taxi.models import Driver, Car

MIN_LEN_LICENSE_NUMBER = 8
MAX_LEN_LICENSE_NUMBER = 8


def validate_license(value: str) -> None:
    if value[:3] != value[:3].upper() or not value[:3].isalpha():
        raise ValidationError(
            "License number must starts with 3 upper case letters"
        )

    if not value[-5:].isdigit():
        raise ValidationError(
            "License number must ends with 5 digits"
        )


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        validators=(
            MaxLengthValidator(MAX_LEN_LICENSE_NUMBER),
            MinLengthValidator(MIN_LEN_LICENSE_NUMBER),
            validate_license,
        )
    )

    class Meta:
        model = Driver
        fields = ["license_number", ]


class CreateDriverForm(forms.ModelForm):
    license_number = forms.CharField(
        validators=(
            MaxLengthValidator(MAX_LEN_LICENSE_NUMBER),
            MinLengthValidator(MIN_LEN_LICENSE_NUMBER),
            validate_license,
        )
    )

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name"
        )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
