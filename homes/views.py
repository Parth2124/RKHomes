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
                f'Submitted At (IST): {inquiry.created_at.astimezone(inquiry.created_at.tzinfo).strftime("%Y-%m-%d %H:%M:%S %Z%z")}\n\n'
                f'View Admin Panel: {admin_full_url}'
            )

            html_message = f'''
                <div style="font-family: Arial, sans-serif; background: #f9f9f9; padding: 32px;">
                  <div style="max-width: 500px; margin: auto; background: #fff; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.07); padding: 32px;">
                    <h2 style="color: #2d3748; margin-bottom: 16px;">New Inquiry Received</h2>
                    <p style="color: #4a5568; margin-bottom: 24px;">You have a new inquiry with the following details:</p>
                    <table style="width: 100%; border-collapse: collapse;">
                      <tr><td style="font-weight: bold; padding: 8px 0; color: #2d3748;">Name:</td><td style="padding: 8px 0; color: #4a5568;">{inquiry.name}</td></tr>
                      <tr><td style="font-weight: bold; padding: 8px 0; color: #2d3748;">Phone:</td><td style="padding: 8px 0; color: #4a5568;">{inquiry.phone}</td></tr>
                      <tr><td style="font-weight: bold; padding: 8px 0; color: #2d3748;">Email:</td><td style="padding: 8px 0; color: #4a5568;">{inquiry.email}</td></tr>
                      <tr><td style="font-weight: bold; padding: 8px 0; color: #2d3748;">Message:</td><td style="padding: 8px 0; color: #4a5568;">{inquiry.message}</td></tr>
                      <tr><td style="font-weight: bold; padding: 8px 0; color: #2d3748;">Status:</td><td style="padding: 8px 0; color: #4a5568;">{inquiry.status}</td></tr>
                      <tr><td style="font-weight: bold; padding: 8px 0; color: #2d3748;">Submitted At (IST):</td><td style="padding: 8px 0; color: #4a5568;">{inquiry.created_at.astimezone(inquiry.created_at.tzinfo).strftime('%Y-%m-%d %H:%M:%S %Z%z')}</td></tr>
                    </table>
                    <div style="margin-top: 32px; text-align: center;">
                      <a href="{admin_full_url}" style="display: inline-block; background: #3182ce; color: #fff; text-decoration: none; padding: 12px 28px; border-radius: 6px; font-weight: bold;">View in Admin Panel</a>
                    </div>
                  </div>
                </div>
            '''
            from_email = 'rkpropertiesandconstruction11@gmail.com'
            recipient_list = ['rkpropertiesandconstruction11@gmail.com']

            try:
                send_mail(subject, message, from_email, recipient_list, fail_silently=False, html_message=html_message)
                messages.success(request, 'Your inquiry has been submitted and we will get back to you shortly!')
            except Exception as e:
                messages.error(request, f'There was an error sending the email. Please try again later. Error: {e}')

            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    return redirect('home')