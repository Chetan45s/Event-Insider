
# def successView(request):
#     messages.success(request,"Thank you for your message \n If you had any query then we will revert back to you as soon as possible")
#     return redirect(request.META.get('HTTP_REFERER')) 

from django.core.mail import EmailMessage
from django.shortcuts import redirect, render
from django.template.loader import get_template
from .forms import ContactForm
from django.contrib import messages


# our view
def contact(request):
    form_class = ContactForm

    # new logic!
    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            contact_name = request.POST.get(
                'contact_name'
            , '')
            contact_email = request.POST.get(
                'contact_email'
            , '')
            form_content = request.POST.get('content', '')

            # Email the profile with the
            # contact information
            template = get_template('sendemail/contact_template.txt')
            context = {
                'contact_name': contact_name,
                'contact_email': contact_email,
                'form_content': form_content,
            }
            content = template.render(context)

            email = EmailMessage(
                "New contact form submission",
                content,
                "Event Insider" +'',
                ['app.info.45@gmail.com'],
                headers = {'Reply-To': contact_email }
            )
            email.send()
            messages.success(request,"Thank you for your message \n If you had any query then we will revert back to you as soon as possible")   
            return redirect('home')

    return render(request, 'sendemail/email.html', {'form': form_class,})
