
# core/views.py
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.core.mail import EmailMessage
from .forms import ContactForm



def index(request):
    return render(request, 'core/index.html')



def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            # build email body
            body = (
                f"Name: {form.cleaned_data['name']}\n"
                f"Company: {form.cleaned_data.get('company','-')}\n"
                f"Email: {form.cleaned_data['email']}\n"
                f"Phone: {form.cleaned_data.get('phone','-')}\n\n"
                f"Process: {form.cleaned_data.get('process','-')}\n"
                f"Quantity: {form.cleaned_data.get('quantity','-')}\n"
                f"Turnaround: {form.cleaned_data.get('turnaround','-')}\n\n"
                f"Message:\n{form.cleaned_data.get('message','-')}\n"
            )
            email = EmailMessage(
                subject="Website contact",
                body=body,
                to=['james@trutonemetal.com', 'admin@trutonemetal.com'],
                reply_to=[form.cleaned_data['email']],
            )
            attachment = form.cleaned_data.get('attachment')
            if attachment:
                email.attach(attachment.name, attachment.read(), attachment.content_type)
            try:
                email.send(fail_silently=False)
                messages.success(request, "Thanks — your request has been sent.")
            except Exception:
                messages.error(request, "There was an error sending your message. Please try again or call us.")
            return redirect(reverse('contact'))
    else:
        form = ContactForm()
    return render(request, 'core/contact.html', {'form': form})
