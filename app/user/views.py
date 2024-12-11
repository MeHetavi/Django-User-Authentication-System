from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from .forms import SignUpForm,LoginForm, ChangePasswordForm,ForgotPasswordForm,ResetPasswordForm
from django.contrib.auth import authenticate,login as auth_login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.utils import timezone
from django.core.mail import send_mail
from .models import CustomUser
from django.contrib.auth.forms import SetPasswordForm
# Create your views here.
import hashlib
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

def hash_email(email):
    return hashlib.sha256(email.encode('utf-8')).hexdigest()

def sign_up(request):
    try:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                user = authenticate(username=username, password=password)
                auth_login(request,user)
                messages.success(request, 'Account registered successfully!!')
                return HttpResponseRedirect('/dashboard')
        else:
            form = SignUpForm() 
        return render(request,'user/signup.html',{'form':form})
    except:
        messages.error(request, 'An unexpected error occured.')
        return HttpResponseRedirect('/signup')


def login(request):
    try:
        if request.method == 'POST':
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    auth_login(request, user)
                    messages.success(request, 'Logged in successfully!!')
                    return HttpResponseRedirect('/dashboard')
        else:
            form = LoginForm()
        return render(request, 'user/login.html', {'form': form})
    except:
        messages.error(request, 'An unexpected error occured.')
        return HttpResponseRedirect('/login')



@login_required(login_url='/login')
def profile(request):
    return render(request,'user/profile.html')


@login_required(login_url='/login')
def changePassword(request):
    try:
        if request.method == 'POST':
            form = ChangePasswordForm(user=request.user, data=request.POST)
            print(request.user)
            if form.is_valid():
                user = request.user
                user.last_updated = timezone.now()
                form.save()

                update_session_auth_hash(request, user)

                messages.success(request, 'Password changed successfully!!')
                return HttpResponseRedirect('/dashboard') 
        else:
            form = ChangePasswordForm(user=request.user)
        return render(request,'user/changepassword.html',{'form':form})
    except:
        messages.error(request, 'An unexpected error occured.')
        return HttpResponseRedirect('/dashboard')
    

@login_required(login_url='/login')
def dashboard(request):
    return render(request,'user/dashboard.html',{'user' : request.user})

def forgotPassword(request):
    try:
        if request.method == 'POST':
            form = ForgotPasswordForm(data = request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                hashed_email = hash_email(email)
                message = f"""<p>Hi,</p>
                <p>Click the link below to reset your password:</p>
                <p><a href="http://localhost:8000/resetPassword/{hashed_email}">Reset Password</a></p>
                """
                try:
                    send_mail(
                        'Reset password',
                        message,
                        'yogaconnectplus@gmail.com',
                        [email],
                        fail_silently=False,
                        html_message=message  # Specify the HTML message
                    )
                except Exception:
                    messages.error(request, 'Failed to send mail.')
                    return HttpResponseRedirect('/login')

                messages.success(request, 'Link to set password was mailed successfully!!')
                return HttpResponseRedirect('/login')
        else:
            form = ForgotPasswordForm()
        return render(request,'user/forgotPassword.html',{'form':form})
    except:
        messages.error(request, 'An unexpected error occured.')
        return HttpResponseRedirect('/login')

@login_required(login_url='/login')
def logout_view(request):
    logout(request)
    messages.error(request, 'Logged out.')
    return HttpResponseRedirect('/login')


def get_user_by_hashed_email(request,hashed_email):
    try:
        users = CustomUser.objects.all()
        user = None
        for user in users:
            if hashed_email == hashlib.sha256(user.email.encode('utf-8')).hexdigest():
                username = user.username
                break
        user = CustomUser.objects.get(username = username)
    except CustomUser.DoesNotExist:
        messages.error(request,'An unexpected error occured!')
        return HttpResponseRedirect('/login')
    except Exception:
        messages.error(request,'An unexpected error occured!')
        return HttpResponseRedirect('/login')

def resetPassword(request,hashed_email):

    try:
    
        user = get_user_by_hashed_email(request,hashed_email)

        if request.method == 'POST':
            form = ResetPasswordForm(request,data=request.POST)
            if form.is_valid():
                # form.save()
                new_password = request.POST.get('new_password1')
                
                # Set password on the USER, not the request
                user.set_password(new_password)
                messages.success(request,'Password set successfully!')
                return HttpResponseRedirect('/login')
        else :  
            form = ResetPasswordForm(user = user)
        return render(request,'user/resetPassword.html',{'form': form})
    except:
        messages.error(request,'An unexpected error occured!')
        return HttpResponseRedirect('/login')