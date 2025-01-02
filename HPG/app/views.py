from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm, CustomUserForm, ServiceForm, DelServiceForm, PetForm, DelPetForm, OwnerForm, DelOwnerForm, GroomerForm, AppointmentForm
from .models import CustomUser, Service, Pet, Owner, Groomer, Appointment
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError

# Registration Form
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('user_home')  # Redirect to user's dashboard
        else:
            # Pass errors and indicate to show the register modal
            context = {
                'login_form': UserLoginForm(),
                'register_form': form,
                'show_register_modal': True,
            }
            return render(request, 'app/FrontPage.html', context)
    return redirect('FrontPage')  # Redirect if not POST


# Login Form
def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                if user.role == 'admin':  # Use the 'role' field directly
                    return redirect('admin_main')  # Redirect to admin dashboard
                return redirect('user_home')  # Redirect to user dashboard
            else:
                form.add_error(None, "Invalid username or password.")
        # Pass errors and indicate to show the login modal
        context = {
            'login_form': form,
            'register_form': UserRegisterForm(),
            'show_login_modal': True,
        }
        return render(request, 'app/FrontPage.html', context)
    return redirect('FrontPage')  # Redirect if not POST


# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')


# Set user as admin
@login_required
def set_user_as_admin(request, user_id):
    if request.user.role != 'admin':  # Check if the logged-in user is admin
        return redirect('user_home')  # Redirect to user dashboard if not an admin

    user = get_object_or_404(CustomUser, id=user_id)

    if user.role == 'admin':  # Check if the user is already an admin
        messages.warning(request, f"{user.username} is already an admin.")
    else:
        user.role = 'admin'  # Set the role to 'admin'
        user.save()
        messages.success(request, f"{user.username} has been promoted to admin.")

    return redirect('admin_main')  # Redirect back to admin dashboard after updating


# Remove user as admin
@login_required
def remove_user_as_admin(request, user_id):
    if request.user.role != 'admin':  # Check if the logged-in user is admin
        return redirect('user_home')  # Redirect to user dashboard if not an admin

    user = get_object_or_404(CustomUser, id=user_id)

    if user.role == 'user':  # If the user is already a regular user, no action is needed
        messages.warning(request, f"{user.username} is already a regular user.")
    else:
        user.role = 'user'  # Set the role to 'user'
        user.save()
        messages.success(request, f"{user.username} has been removed from admin status.")

    return redirect('admin_main')  # Redirect back to admin dashboard after updating

# Delete user
@login_required
def delete_user(request, user_id):
    if request.user.role != 'admin':  # Only admins can delete users
        return redirect('user_home')  # Redirect to user dashboard if not an admin

    user = get_object_or_404(CustomUser, id=user_id)

    # Show confirmation form before deletion
    if request.method == 'GET':
        return render(request, 'app/admin/delete_user.html', {'user': user})

    # Handle deletion after form submission
    if request.method == 'POST':
        if user == request.user:
            messages.error(request, "You cannot delete your own account.")
        else:
            user.delete()
            messages.success(request, f"{user.username}'s account has been deleted.")
        
        # Redirect after deletion
        return redirect('admin_main')  # Redirect to admin dashboard or another page


# Update user profile (including photo)
@login_required
def update_user_profile(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.user.role != 'admin' and request.user != user:
        return redirect('user_home')  # Ensure that only the user or admin can update the profile

    if request.method == 'POST':
        form = CustomUserForm(request.POST, request.FILES, instance=user)  # Ensure to handle image upload
        if form.is_valid():
            form.save()
            messages.success(request, f"{user.username}'s profile has been updated.")
            return redirect('admin_main' if request.user.role == 'admin' else 'user_home')
    else:
        form = CustomUserForm(instance=user)

    return render(request, 'app/admin/update_user_profile.html', {'form': form, 'user': user})

# FrontPageView (for login and register modals)
class FrontPageView(TemplateView):
    template_name = 'app/FrontPage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_form'] = UserLoginForm()
        context['register_form'] = UserRegisterForm()
        return context


# This is For Admin HTML
@login_required
def admin_main(request):
    if request.user.role != 'admin':  # Check role directly
        return redirect('user_home')

    users = CustomUser.objects.all()
    services = Service.objects.all()
    pets = Pet.objects.all()
    owners = Owner.objects.all()
    groomers = Groomer.objects.all()
    appointments = Appointment.objects.all()
    dogs = pets.filter(species='dog') 
    cats = pets.filter(species='cat') 
    form = CustomUserForm()  
    return render(request, 'app/admin/admin_main.html', {'users': users, 'services': services, 'form': form, 'pets': pets, 'owners': owners, 'groomers': groomers, 'appointments': appointments, 'dogs_count': dogs.count(), 'cats_count': cats.count()})

@login_required
def admin_service(request):
    if request.user.role != 'admin':  # Restrict to admin users only
        return redirect('user_home')

    services = Service.objects.all()
    owners = Owner.objects.all()
    return render(request, 'app/admin/service/admin_service.html', {'services': services, 'owners': owners})


class AdminServiceDetail(LoginRequiredMixin, DetailView):
    model = Service
    template_name = 'app/admin/service/admin_servicedetail.html'
    context_object_name = 'service'


class CreateService(LoginRequiredMixin, CreateView):
    model = Service
    fields = ['name', 'description', 'duration', 'picture', 'price']
    template_name = 'app/admin/service/admin_CreateService.html'

    def form_valid(self, form):
        # Make sure the picture is saved when the form is valid
        if form.is_valid():
            return super().form_valid(form)
        return super().form_invalid(form)


class UpdateService(LoginRequiredMixin, UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'app/admin/service/admin_UpdateService.html'
    success_url = reverse_lazy('admin_main')
    

class DeleteService(LoginRequiredMixin, DeleteView):
    model = Service
    form_class = DelServiceForm
    template_name = 'app/admin/service/admin_DeleteService.html'
    success_url = reverse_lazy('admin_main')


# For Owner
@login_required
def admin_owner(request):
    if request.user.role != 'admin':
        return redirect('user_home')
    
    # Prefetch related pets to avoid multiple queries
    owners = Owner.objects.prefetch_related('pets').all()
    users = CustomUser.objects.all()

    return render(request, 'app/admin/owner/admin_owner.html', {'owners': owners, 'users': users})


class AdminOwnerDetail(LoginRequiredMixin, DetailView):
    model = Owner
    template_name = 'app/admin/owner/OwnerDetail.html'
    context_object_name = 'owner'


class CreateOwner(LoginRequiredMixin, CreateView):
    model = Owner
    fields = ['phone', 'email']
    template_name = 'app/admin/owner/CreateOwner.html'

class UpdateOwner(LoginRequiredMixin, UpdateView):
    model = Owner
    form_class = OwnerForm
    template_name = 'app/admin/owner/UpdateOwner.html'
    success_url = reverse_lazy('admin_main')


class DeleteOwner(LoginRequiredMixin, DeleteView):
    model = Owner
    form_class = DelOwnerForm
    template_name = 'app/admin/owner/DeleteOwner.html'
    success_url = reverse_lazy('admin_main')


#For Pet
@login_required
def admin_pet(request):
    if request.user.role != 'admin':
        return redirect('user_home')
    
    pets = Pet.objects.all()
    
    return render(request, 'app/admin/pet/admin_pet.html', {'pets': pets })


class AdminPetDetail(LoginRequiredMixin, DetailView):
    model = Pet
    template_name = 'app/admin/pet/admin_petDetail.html'
    context_object_name = 'pet'


class CreatePet(LoginRequiredMixin, CreateView):
    model = Pet
    fields = ['owner', 'name', 'species', 'picture', 'breed', 'age_years', 'age_months']
    template_name = 'app/admin/pet/admin_petCreate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the logged-in user as the default owner
        context['owners'] = Owner.objects.filter(user=self.request.user)
        return context

    def form_valid(self, form):
        # Automatically associate the logged-in user as the owner
        owner = Owner.objects.filter(user=self.request.user).first()
        if owner:
            form.instance.owner = owner
        else:
            return self.form_invalid(form)  # Handle the case where no owner exists
        return super().form_valid(form)



class UpdatePet(LoginRequiredMixin, UpdateView):
    model = Pet
    form_class = PetForm
    template_name = 'app/admin/pet/admin_petUpdate.html'
    success_url = reverse_lazy('admin_main')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['owners'] = Owner.objects.all()  # Pass owners if required
        return context

class DeletePet(LoginRequiredMixin, DeleteView):
    model = Pet
    form_class = DelPetForm
    template_name = 'app/admin/pet/admin_petDelete.html'
    success_url = reverse_lazy('admin_main')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['owners'] = Owner.objects.all()  # Pass owners if required
        return context
    

#For Groomer
@login_required
def admin_groomer(request):
    if request.user.role != 'admin':
        return redirect('user_home')
    
    groomers = Groomer.objects.all()
    
    return render(request, 'app/admin/groomer/admin_groomer.html', {'groomers': groomers })


class AdminGroomerDetail(LoginRequiredMixin, DetailView):
    model = Groomer
    template_name = 'app/admin/groomer/GroomerDetail.html'
    context_object_name = 'groomer'


class CreateGroomer(LoginRequiredMixin, CreateView):
    model = Groomer
    fields = ['picture', 'name', 'phone', 'email', 'experience_years']
    template_name = 'app/admin/groomer/CreateGroomer.html'

    def form_valid(self, form):
        # Make sure the picture is saved when the form is valid
        if form.is_valid():
            return super().form_valid(form)
        return super().form_invalid(form)


class UpdateGroomer(LoginRequiredMixin, UpdateView):
    model = Groomer
    form_class = GroomerForm
    template_name = 'app/admin/groomer/UpdateGroomer.html'
    success_url = reverse_lazy('admin_main')


class DeleteGroomer(LoginRequiredMixin, DeleteView):
    model = Groomer
    template_name = 'app/admin/groomer/DeleteGroomer.html'
    success_url = reverse_lazy('admin_main')
    

#For APPOINTMENT!!
@login_required
def admin_Appointment(request):
    if request.user.role != 'admin':
        return redirect('user_home')
    
    appointments = Appointment.objects.all()
    
    return render(request, 'app/admin/pet/admin_appointment.html', {'appointments': appointments })


class CreateAppointment(LoginRequiredMixin, CreateView):
    model = Appointment
    fields = ['pet', 'service', 'groomer', 'date', 'time', 'notes']
    template_name = 'app/admin/appointment/Createappointment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Filter pets belonging to the logged-in user
        owner = Owner.objects.filter(user=self.request.user).first()
        context['pets'] = Pet.objects.filter(owner=owner) if owner else Pet.objects.none()
        context['services'] = Service.objects.all()
        context['groomers'] = Groomer.objects.all()
        return context

    def form_valid(self, form):
        # Automatically associate the logged-in user as the owner of the appointment's pet
        owner = Owner.objects.filter(user=self.request.user).first()
        if owner:
            # Ensure the selected pet belongs to the logged-in owner
            pet = form.cleaned_data['pet']
            if pet.owner != owner:
                form.add_error('pet', 'You can only create appointments for your own pets.')
                return self.form_invalid(form)
        else:
            return self.form_invalid(form)  # Handle the case where no owner exists
        return super().form_valid(form)


class UpdateAppointment(LoginRequiredMixin, UpdateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'app/admin/appointment/Updateappointment.html'
    success_url = reverse_lazy('admin_main')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Filter pets belonging to the logged-in user
        owner = Owner.objects.filter(user=self.request.user).first()
        context['pets'] = Pet.objects.filter(owner=owner) if owner else Pet.objects.none()
        context['services'] = Service.objects.all()
        context['groomers'] = Groomer.objects.all()
        return context

    def form_valid(self, form):
        # Validate that the logged-in user owns the pet
        owner = Owner.objects.filter(user=self.request.user).first()
        if owner:
            pet = form.cleaned_data['pet']
            if pet.owner != owner:
                form.add_error('pet', 'You can only update appointments for your own pets.')
                return self.form_invalid(form)
        else:
            return self.form_invalid(form)  # Handle the case where no owner exists
        return super().form_valid(form)


class DeleteAppointment(LoginRequiredMixin, DeleteView):
    model = Appointment
    template_name = 'app/admin/appointment/Deleteappointment.html'
    success_url = reverse_lazy('admin_main')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pets'] = Pet.objects.all()
        context['services'] = Service.objects.all() 
        context['groomers'] = Groomer.objects.all() 
        return context

@login_required
def appointment_Status(request, pk):
    if request.user.role != 'admin':
        return redirect('user_home')
    
    appointment = get_object_or_404(Appointment, pk=pk)

    if request.method == 'POST':
        status = request.POST.get('status')
        if status in ['confirmed', 'completed', 'canceled']:
            appointment.status = status
            appointment.save()
            messages.success(request, f'Appointment has been {status}.')
        else:
            messages.error(request, 'Invalid status.')
        return redirect('admin_main')  # Redirect back to the admin dashboard
    
    return render(request, 'app/admin/appointment/appointmentStatus.html', {'appointment': appointment})

@login_required
def reschedule_appointment(request, pk):
    if request.user.role != 'admin':
        return redirect('user_home')

    # Get the appointment by ID
    appointment = get_object_or_404(Appointment, pk=pk)

    error_message = None  # Initialize error_message

    if request.method == 'POST':
        # Get new date and time from the form
        new_date = request.POST.get('date')
        new_time = request.POST.get('time')

        if new_date and new_time:
            try:
                # Reschedule using the model's `reschedule` method
                appointment.reschedule(new_date, new_time)
                messages.success(request, 'Appointment rescheduled successfully.')
                return redirect('admin_main')  # Redirect after success
            except ValidationError as e:
                error_message = str(e)  # Capture validation error
        else:
            error_message = 'Date and time are required.'
        return redirect('admin_main') 

    # Render the modal form with the appointment and error_message
    return render(request, 'app/admin/appointment/Rescheduleappointment.html', {
        'appointment': appointment,
        'error_message': error_message,  # Pass the error message to the template
    })



# This is For User HTML
@login_required
def user_home(request):
    if request.user.role != 'user':  # Check role directly
        return redirect('admin_main')

    services = Service.objects.all()

    # Pass services to the template
    return render(request, 'app/user/home.html', {'services': services})


class ServiceList(LoginRequiredMixin, ListView):
    model = Service
    template_name = 'app/user/service.html'
    context_object_name = 'service'


class ServiceDetail(LoginRequiredMixin, DetailView):
    model = Service
    template_name = 'app/user/detail.html'
    context_object_name = 'service'

@login_required
def user_profile(request):
    # Ensure the logged-in user has an associated Owner profile
    owner = get_object_or_404(Owner, user=request.user)
    
    # Retrieve all appointments for pets owned by the logged-in user's Owner profile
    appointments = Appointment.objects.filter(pet__owner=owner)
    
    return render(request, 'app/user/profile.html', {'appointments': appointments})