from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .models import AlcoholIntake, CigaretteIntake


class CustomUserCreationForm(UserCreationForm):
    name = forms.CharField(max_length=255, required=True)
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female')], required=True, widget=forms.RadioSelect)
    feet = forms.IntegerField(label='Height (Feet)', min_value=0, required=True)
    inches = forms.IntegerField(label='Height (Inches)', min_value=0, max_value=11, required=True)
    weight = forms.IntegerField(required=True, min_value=0)
    phone_number = forms.CharField(max_length=15, required=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'name', 'gender', 'feet', 'inches', 'weight', 'phone_number', 'password1', 'password2')

    def clean(self):
        cleaned_data = super().clean()
        feet = cleaned_data.get("feet")
        inches = cleaned_data.get("inches")

        # Convert feet and inches to total inches
        total_inches = feet * 12 + inches
        cleaned_data["height"] = total_inches
        return cleaned_data

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)

        # Calculate height in inches
        total_inches = self.cleaned_data['feet'] * 12 + self.cleaned_data['inches']

        user.height = total_inches

        if commit:
            user.save()

        return user




class AlcoholForm(forms.ModelForm):
    amount = forms.IntegerField(min_value=0)
    alcohol_type = forms.ChoiceField(choices=AlcoholIntake.ALCOHOL_TYPES)
    class Meta:
        model = AlcoholIntake
        fields = ['alcohol_type', 'amount']


class CigaretteForm(forms.ModelForm):
    units = forms.IntegerField(min_value=0)
    class Meta:
        model = CigaretteIntake
        fields = ['units']
