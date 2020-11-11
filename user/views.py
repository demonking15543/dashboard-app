

from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.contrib import messages
from . forms import UserSignupForm, UserLoginForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
# Create your views here.


class SignupView(FormView):
    """sign up user view"""
    form_class = UserSignupForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        """ process user signup"""
        user = form.save(commit=False)
        user.save()
        login(self.request, user)
        

        if user is not None:
            return HttpResponseRedirect(self.success_url)

        return super().form_valid(form)


def Logout(request):
    """logout logged in user"""
    logout(request)
    return redirect(reverse_lazy('login'))


class LoginView(FormView):
    """login view"""

    form_class = UserLoginForm
    success_url = reverse_lazy('dashboard')
    template_name = 'registration/login.html'

    def form_valid(self, form):
        """ process user login"""
        credentials = form.cleaned_data

        user = authenticate(username=credentials['email'],
                            password=credentials['password'])

        if user is not None:
            login(self.request, user)
            
            return HttpResponseRedirect(self.success_url)

        else:
            messages.info(request, "please try again")

            return HttpResponseRedirect(reverse_lazy('login'))

    








def user_detail_view(request):
    if request.user.is_authenticated:
        # if  user is logged in do following task
        try:
            # get requested user details that we have taken from user  at the time of signup.
            user  = get_user_model().objects.get(email=request.user.email)
        except get_user_model().DoesNotExist:
            messages.info(request, 'Invalid Details')
            return redirect('login')
    else:
        return redirect(reverse_lazy('login'))
    context = {'user_details': user}    
    return render(request, 'registration/user_details.html', context)         



