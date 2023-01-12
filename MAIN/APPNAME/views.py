
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
import random
from django.core.mail import send_mail
from cryptography.fernet import Fernet
from mechanize import Browser
import favicon
from .models import Password
# from .forms import ContactForm
from django.template.loader import render_to_string

br = Browser()
br.set_handle_robots(False)
fernet = Fernet(settings.KEY)


def home(request):
    if request.method == "POST":
        if "signup-form" in request.POST:
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")
            password2 = request.POST.get("password2")
            # if password are not identical
            if password != password2:
                msg = "Please make sure you're using the same password!"
                messages.error(request, msg)
                return render(request, "password.html")
            # if username exists
            elif User.objects.filter(username=username).exists():
                msg = f"{username} already exists!"
                messages.error(request, msg)
                return render(request, "password.html")
            # if email exists
            elif User.objects.filter(email=email).exists():
                msg = f"{email} already exists!"
                messages.error(request, msg)
                return render(request, "password.html")
            else:
                User.objects.create_user(username, email, password)
                new_user = authenticate(
                    request, username=username, password=password2)
                if new_user is not None:
                    login(request, new_user)
                    msg = f"{username}. Thanks for subscribing."
                    messages.success(request, msg)
                    return render(request, "password.html")
        elif "logout" in request.POST:
            msg = f"{request.user}. You logged out."
            logout(request)
            messages.success(request, msg)
            return render(request, "password.html")

        elif 'login-form' in request.POST:
            username = request.POST.get("username")
            password = request.POST.get("password")
            new_login = authenticate(
                request, username=username, password=password)
            if new_login is None:
                msg = f"Login failed! Make sure you're using the right account."
                messages.error(request, msg)
                return render(request, "password.html")
            else:
                code = str(random.randint(100000, 999999))
                global global_code
                global_code = code
                send_mail(
                    "Django Password Manager: confirm email",
                    f"Your verification code is {code}.",
                    settings.EMAIL_HOST_USER,
                    [new_login.email],
                    fail_silently=False,
                )
                return render(request, "password.html", {
                    "code": code,
                    "user": new_login,
                })

        elif "confirm" in request.POST:
            input_code = request.POST.get("code")
            user = request.POST.get("user")
            if input_code != global_code:
                msg = f"{input_code} is wrong!"
                messages.error(request, msg)
                return render(request, "password.html")
            else:
                login(request, User.objects.get(username=user))
                msg = f"{request.user} welcome again."
                messages.success(request, msg)
                return render(request, "password.html")

        elif "add-password" in request.POST:
            url = request.POST.get("url")
            email = request.POST.get("email")
            password = request.POST.get("password")
            # ecrypt data
            encrypted_email = fernet.encrypt(email.encode())
            encrypted_password = fernet.encrypt(password.encode())
            # get title of the website
            try:
                br.open(url)
                title = br.title()
            except:
                title = url
            # get the logo's URL
            try:
                icon = favicon.get(url)[0].url
            except:
                icon = "https://cdn-icons-png.flaticon.com/128/1006/1006771.png"
            # Save data in database
            new_password = Password.objects.create(
                user=request.user,
                name=title,
                logo=icon,
                email=encrypted_email.decode(),
                password=encrypted_password.decode(),
            )
            msg = f"{title} added successfully."
            messages.success(request, msg)
            return render(request, "password.html")

        elif "delete" in request.POST:
            to_delete = request.POST.get("password-id")
            msg = f"{Password.objects.get(id=to_delete).name} deleted."
            Password.objects.get(id=to_delete).delete()
            messages.success(request, msg)
            return render(request, "password.html")

    context = {}
    if request.user.is_authenticated:
        passwords = Password.objects.all().filter(user=request.user)
        for password in passwords:
            password.email = fernet.decrypt(password.email.encode()).decode()
            password.password = fernet.decrypt(
                password.password.encode()).decode()
        context = {
            "passwords": passwords,
        }

    return render(request, "home.html")


def password(request):
    if request.method == "POST":
        if "signup-form" in request.POST:
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")
            password2 = request.POST.get("password2")
            # if password are not identical
            if password != password2:
                msg = "Please make sure you're using the same password!"
                messages.error(request, msg)
                return render(request, "password.html")
            # if username exists
            elif User.objects.filter(username=username).exists():
                msg = f"{username} already exists!"
                messages.error(request, msg)
                return render(request, "password.html")
            # if email exists
            elif User.objects.filter(email=email).exists():
                msg = f"{email} already exists!"
                messages.error(request, msg)
                return render(request, "password.html")
            else:
                User.objects.create_user(username, email, password)
                new_user = authenticate(
                    request, username=username, password=password2)
                if new_user is not None:
                    login(request, new_user)
                    msg = f"{username}. Thanks for subscribing."
                    messages.success(request, msg)
                    return render(request, "password.html")
        elif "logout" in request.POST:
            msg = f"{request.user}. You logged out."
            logout(request)
            messages.success(request, msg)
            return render(request, "password.html")

        elif 'login-form' in request.POST:
            username = request.POST.get("username")
            password = request.POST.get("password")
            new_login = authenticate(
                request, username=username, password=password)
            if new_login is None:
                msg = f"Login failed! Make sure you're using the right account."
                messages.error(request, msg)
                return render(request, "password.html", context)
            else:
                code = '567321'
                global global_code
                global_code = code
                '''send_mail(
                    "Django Password Manager: confirm email",
                    f"Your verification code is {code}.",
                    settings.EMAIL_HOST_USER,
                    [new_login.email],
                    fail_silently=False,
                )'''
                return render(request, "password.html", {
                    "code": code,
                    "user": new_login,
                })

        elif "confirm" in request.POST:
            input_code = request.POST.get("code")
            user = request.POST.get("user")
            if input_code != global_code:
                msg = f"{input_code} is wrong!"
                messages.error(request, msg)
                return render(request, "password.html")
            else:
                login(request, User.objects.get(username=user))
                msg = f"{request.user} welcome again."
                messages.success(request, msg)
                return render(request, "password.html", context)

        elif "add-password" in request.POST:
            url = request.POST.get("url")
            email = request.POST.get("email")
            password = request.POST.get("password")
            # ecrypt data
            encrypted_email = fernet.encrypt(email.encode())
            encrypted_password = fernet.encrypt(password.encode())
            # get title of the website
            try:
                br.open(url)
                title = br.title()
            except:
                title = url
            # get the logo's URL
            try:
                icon = favicon.get(url)[0].url
            except:
                icon = "https://cdn-icons-png.flaticon.com/128/1006/1006771.png"
            # Save data in database
            new_password = Password.objects.create(
                user=request.user,
                name=title,
                logo=icon,
                email=encrypted_email.decode(),
                password=encrypted_password.decode(),
            )
            msg = f"{title} added successfully."
            messages.success(request, msg)
            return render(request, "password.html", context)

        elif "delete" in request.POST:
            to_delete = request.POST.get("password-id")
            msg = f"{Password.objects.get(id=to_delete).name} deleted."
            Password.objects.get(id=to_delete).delete()
            messages.success(request, msg)
            return render(request, "password.html", context)

    context = {}
    if request.user.is_authenticated:
        passwords = Password.objects.all().filter(user=request.user)
        for password in passwords:
            password.email = fernet.decrypt(password.email.encode()).decode()
            password.password = fernet.decrypt(
                password.password.encode()).decode()
        context = {
            "passwords": passwords,
        }

    return render(request, "password.html", context)


def base(request):
    return render(request, "base.html")


def pages(request):
    return render(request, "pages.html")


def about(request):
    return render(request, "about.html")


def service(request):
    return render(request, "service.html")



def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        website = request.POST.get('website')
        message = request.POST.get('message')
        form_data = {
            'name':name,
            'email':email,
            'phone':phone,
            'website':website,
            'message':message,
        }
        message = '''
        From:\n\t\t{}\n
        Message:\n\t\t{}\n
        Email:\n\t\t{}\n
        Phone:\n\t\t{}\n
        Website:\n\t\t{}\n
        '''.format(form_data['name'], form_data['message'], form_data['email'],form_data['phone'],form_data['website'])
        send_mail('You got a mail!', message, '',settings.EMAIL_HOST_USER, ['skfarzaan36@gmail.com'], fail_silently=False)
    return render(request, "contact.html")
    return render(request, "contact.html")

def index(request):
    return render(request, "index.html")


def index1(request):
    return render(request, "index1.html")


def qr(request):
    return render(request, "qr.html")


def cyber(request):
    return render(request, "cyber.html")


def cyber1(request):
    return render(request, "cyber1.html")


def cyber2(request):
    return render(request, "cyber2.html")


def cyber2b(request):
    return render(request, "cyber2b.html")


def cyber2c(request):
    return render(request, "cyber2c.html")


def cyber2d(request):
    return render(request, "cyber2d.html")


def privacy(request):
    return render(request, "privacy.html")


def privacy1(request):
    return render(request, "privacy1.html")


def privacy2(request):
    return render(request, "privacy2.html")


def privacy3(request):
    return render(request, "privacy3.html")


def privacy4(request):
    return render(request, "privacy4.html")


def privacy5(request):
    return render(request, "privacy5.html")


def privacy6(request):
    return render(request, "privacy6.html")


def privacy7(request):
    return render(request, "privacy7.html")


def privacy8(request):
    return render(request, "privacy8.html")


def privacy9(request):
    return render(request, "privacy9.html")


def message(request):
    return render(request, "message.php")
