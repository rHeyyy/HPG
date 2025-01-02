from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from .models import CustomUser, Owner, Appointment, Service, Pet, Groomer

# User registration form
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Enter a valid email address.")

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use. Please choose a different one.")
        return email


# User login form
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        required=True,
        max_length=150,
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
    )

    # Override the default method to customize the error message
    def confirm_login_allowed(self, user):
        # Check the username and password manually to customize the error message
        if not user.is_active:
            raise forms.ValidationError(
                "Please enter a correct username and password.",
                code='invalid_login'
            )
        if not user.check_password(self.cleaned_data['password']):
            raise forms.ValidationError(
                "Please enter a correct username and password.",
                code='invalid_login'
            )
        return super().confirm_login_allowed(user)  # Call the original method


# Owner form for pet owner details
class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ['phone', 'email']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        if len(phone) < 10 or len(phone) > 15:
            raise forms.ValidationError("Phone number must be between 10 and 15 digits.")
        return phone

class DelOwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ['phone', 'email']

        

# Appointment form for pet grooming appointments
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['pet', 'service', 'groomer', 'date', 'time', 'notes', 'is_confirmed']

    def clean(self):
        cleaned_data = super().clean()
        groomer = cleaned_data.get('groomer')
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')

        # Check groomer's availability
        if groomer and Appointment.objects.filter(groomer=groomer, date=date, time=time).exists():
            raise forms.ValidationError("This groomer already has an appointment at the selected time.")

        # Check for daily appointment limits (5 per day per groomer)
        if groomer:
            daily_appointments = Appointment.objects.filter(groomer=groomer, date=date).count()
            daily_limit = 5  # You can make this configurable
            if daily_appointments >= daily_limit:
                raise forms.ValidationError(
                    f"{groomer.name} cannot take more than {daily_limit} appointments on {date}."
                )

        return cleaned_data
    
class RescheduleAppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['date', 'time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }
    
class AppointmentApprovalForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['status']


# CustomUser form for updating user profile (including profile picture)
class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'profile_picture']  # Include the profile_picture field
        widgets = {
            'profile_picture': forms.ClearableFileInput(attrs={'multiple': False}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("This email is already in use. Please choose a different one.")
        return email

    def clean_profile_picture(self):
        profile_picture = self.cleaned_data.get('profile_picture')
        # Add validation if necessary (e.g., file size, type)
        if profile_picture:
            if not profile_picture.name.endswith(('.jpg', '.jpeg', '.png')):
                raise forms.ValidationError("Only image files (jpg, jpeg, png) are allowed.")
        return profile_picture
    
#ServieModels
class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'duration', 'picture', 'price']

class DelServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'duration', 'picture', 'price']

#PetModels
class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['owner', 'name', 'species', 'picture', 'breed', 'age_years', 'age_months']

class DelPetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['owner', 'name', 'species', 'picture', 'breed', 'age_years', 'age_months']

#GroomerModels
class GroomerForm(forms.ModelForm):
    class Meta:
        model = Groomer
        fields = ['picture', 'name', 'phone', 'email', 'experience_years']
