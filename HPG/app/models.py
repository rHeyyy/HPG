from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta


class CustomUser(AbstractUser):
    USER_ROLES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    role = models.CharField(
        max_length=10,
        choices=USER_ROLES,
        default='user',
    )

    profile_picture = models.ImageField(
        upload_to='images/profile_pics',
        null=True,
        blank=True,
    )

    def is_admin(self):
        """Returns True if the user is an admin."""
        return self.role == 'admin'

    def is_user(self):
        """Returns True if the user is a regular user."""
        return self.role == 'user'

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class Owner(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='owner_profile'
    )
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)

    # Temporarily add a default value for 'name'
    name = models.CharField(max_length=100, editable=False, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Automatically set the owner's name to the user's full name
        if self.user:
            self.name = self.user.get_full_name()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name



# Signal to create Owner profile automatically
@receiver(post_save, sender=CustomUser)
def create_owner_profile(sender, instance, created, **kwargs):
    if created and instance.is_user():  # Only for 'user' role
        Owner.objects.create(user=instance, email=instance.email)

class Pet(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='pets')
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=50, choices=[('dog', 'Dog'), ('cat', 'Cat')])
    picture = models.ImageField(upload_to='images/pet_picture', blank=True, null=True)
    breed = models.CharField(max_length=100, blank=True)
    age_years = models.PositiveIntegerField(default=0, verbose_name="Age (Years)")
    age_months = models.PositiveIntegerField(default=0, verbose_name="Age (Months)")

    def __str__(self):
        return f"{self.name} ({self.species})"

    def get_absolute_url(self):
        return reverse("admin_main")

    def get_age_display(self):
        """
        Returns a string representation of the pet's age in years and months.
        """
        parts = []
        if self.age_years:
            parts.append(f"{self.age_years} year{'s' if self.age_years > 1 else ''}")
        if self.age_months:
            parts.append(f"{self.age_months} month{'s' if self.age_months > 1 else ''}")
        return ", ".join(parts) if parts else "Unknown"


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    duration = models.DurationField(help_text="Duration of the service in hours and minutes")
    picture = models.ImageField(upload_to='images/service_pictures', blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.duration_in_hours_and_minutes})"

    def get_absolute_url(self):
        return reverse("admin_main")

    @property
    def duration_in_hours_and_minutes(self):
        total_seconds = self.duration.total_seconds()
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        return f"{hours} hours {minutes} minutes"

    @duration_in_hours_and_minutes.setter
    def duration_in_hours_and_minutes(self, value):
        hours, minutes = map(int, value.split(':'))
        self.duration = timedelta(hours=hours, minutes=minutes)


class Groomer(models.Model):
    picture = models.ImageField(upload_to='images/groomer_pictures', blank=True, null=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    experience_years = models.PositiveIntegerField(help_text="Years of grooming experience")

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("admin_main")

from django.utils.translation import gettext_lazy as _

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('reschedule', _('Reschedule')),
        ('confirmed', _('Confirmed')),
        ('completed', _('Completed')),
        ('canceled', _('Canceled')),
    ]

    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='appointments')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='appointments')
    groomer = models.ForeignKey(Groomer, on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments')
    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True)
    is_confirmed = models.BooleanField(default=False)  # Consider removing this if `status` supersedes it.
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
    )

    class Meta:
        unique_together = ('pet', 'date', 'time')

    def get_absolute_url(self):
        return reverse("admin_main")

    def __str__(self):
        return f"{self.pet.name} - {self.service.name} on {self.date} at {self.time} ({self.get_status_display()})"

    def clean(self):
        if self.groomer:
            appointments_on_same_day = Appointment.objects.filter(
                groomer=self.groomer,
                date=self.date
            ).count()
            if appointments_on_same_day >= 5:
                raise ValidationError(f"{self.groomer.name} is not available for more appointments on {self.date}.")
        overlapping_appointment = Appointment.objects.filter(
            groomer=self.groomer,
            date=self.date,
            time=self.time
        ).exclude(id=self.id).exists()
        if overlapping_appointment:
            raise ValidationError("This groomer already has an appointment at the selected time.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def reschedule(self, new_date, new_time):
        self.date = new_date
        self.time = new_time
        self.status = 'reschedule'
        self.save()
