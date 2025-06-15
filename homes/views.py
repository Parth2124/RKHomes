from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .forms import InquiryForm
from .models import Inquiry # Import the Inquiry model
from django.urls import reverse # Import reverse
from django.contrib.sites.shortcuts import get_current_site # Import get_current_site

def home(request):
    return render(request, 'index.html')

def submit_inquiry(request):
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save() # Save the inquiry to get the instance

            # Dynamically build the admin link to the main admin index
            admin_url_path = reverse('admin:index') # Changed to admin index
            admin_full_url = request.build_absolute_uri(admin_url_path)

            # Send email notification
            subject = f'New Inquiry from {inquiry.name}'
            message = (
                f'Hello, you have a new inquiry!\n\n'
                f'Name: {inquiry.name}\n'
                f'Phone: {inquiry.phone}\n'
                f'Email: {inquiry.email}\n'
                f'Message: {inquiry.message}\n\n'
                f'Status: {inquiry.status}\n'
                f'Submitted At (IST): {inquiry.created_at.astimezone(inquiry.created_at.tzinfo).strftime('%Y-%m-%d %H:%M:%S %Z%z')}\n\n'
                f'View Admin Panel: {admin_full_url}'
            )
            from_email = 'classickcode@gmail.com'
            recipient_list = ['classickcode@gmail.com']

            try:
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                messages.success(request, 'Your inquiry has been submitted and we will get back to you shortly!')
            except Exception as e:
                messages.error(request, f'There was an error sending the email. Please try again later. Error: {e}')

            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    return redirect('home')