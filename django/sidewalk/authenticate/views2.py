from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from authform import *
from models import *
# from django.views.generic.base import TemplateView

# Create your views here.
    #return render(request, 'home.html', {
    #    'login_form': login_form,
    #    'reg_form': reg_form
    #})
    #if request.method == 'POST':
    #    form = LoginForm(request.POST)
    # login_form = LoginForm(prefix = 'login')
    # registration_form = RegistrationForm(prefix = 'registration')
    # return render(request, 'home.html', {
    #     'login_form': login_form,
    #     'registration_form': registration_form
    # })

def index(request):
    html = "<html><body>hi</body></html>"
    return HttpResponse(html)

def home(request):
    def displayHomeWithContext(request, incorrect=False, expired_acc='', 
            invalid_uname='', invalid_email=''):
        login_form = LoginForm(prefix = 'login')
        reg_form = RegistrationForm(prefix = 'registration')
        
        context_dict = {
                'login_form': login_form,
                'reg_form': reg_form
        }
        if incorrect:
            context_dict['incorrect'] = True
        if (expired_acc != ''):
            context_dict['expired_acc'] = expired_acc
        if (invalid_uname != ''):
            context_dict['invalid_uname'] = invalid_uname
        if (invalid_email != ''):
            invalid_email['invalid_email'] = invalid_email
        context = Context(context_dict)
        return render(request, 'home.html', context)

    #html = "<html><body><h1>Whatup</h1></body></html>"
    if request.method == 'POST':
       if 'login' in request.POST:
           login_form = LoginForm(request.POST, prefix='login')
           if login_form.is_valid():
               #...Handle login
               username = login_form.cleaned_data['username']
               password = login_form.cleaned_data['password']
               user = authenticate(username=username, password=password)
               if user is not None:
                   if user.is_active:
                       login(request, user)
                       return HttpResponseRedirect('../dash/')
                   else:
                       return displayHomeWithContext(request, expired_acc=username)
                       # return HttpResponseRedirect('../home/expired')
                       
               else:
                   return displayHomeWithContext(request, incorrect=True)
       elif 'registration' in request.POST:     
           reg_form = RegistrationForm(request.POST, prefix = 'registration')
           if reg_form.is_valid():
               #...Handle registration
               first_name = reg_form.cleaned_data['first_name']
               last_name = reg_form.cleaned_data['last_name']
               username = reg_form.cleaned_data['username']
               password = reg_form.cleaned_data['password']
               email = reg_form.cleaned_data['email']
               ver_email = reg_form.cleaned_data['ver_email']
               location = reg_form.cleaned_data['location']
               existing_users = User.objects.filter(username__exact=username)
               if (len(existing_users) > 0):
                   #return HttpResponseRedirect('../home/existing_user-' + username)
                   return displayHomeWithContext(request, invalid_uname=username)
               existing_email = User.objects.filter(email__exact=email)
               if (len(existing_email) > 0):
                   #return HttpResponseRedirect('../home/existing_email-' + email)
                   return displayHomeWithContext(request, invalid_email=email)
               user = User.objects.create_user(username=username, first_name=first_name,
                       last_name=last_name, email=email, password = password)
               #quser = QUser(user=user, location=location, stats=new_stats)
               user.save()
               user = authenticate(username=username, password=password)
               login(request, user)
               return HttpResponseRedirect('../dash/')
    else:
       return displayHomeWithContext(request)
#def existing_user(request, username):
    
#def existing_email(request, 

def dash(request):
    html = "<html><body> Dash </body></html>"
    return HttpResponse(html)
    #return render(request, 'dash.html', {})
    # Get current quests
    # Get trending quests

def profile(request, username):
    #html = "<html><body> goodwife </body></html>"
    #return HttpResponse(html)
    try:
        User.objects.get(username = username)
    except (KeyError, User.DoesNotExist):
        return render(request, 'profile.html', {
            'error_message': 'This user does not exist',
            })
    else:
        quser = user.quser
        return render_to_response('profile.html', {'quser': quser})

    #return render_to_response('authenticate/profile.html', 
        #{'user': current_user})
        

# t = get_template('hello.html')
# html = t.render(Context({'name': name}))
# return HttpResponse(html)

# render_to_response('hello.html', {'name': name})

# class HelloTemplate(TemplateView):
# template_name = 'hello_class.html'
#
# def get_context_data(self, **kwargs):
#    context = super(HelloTemplate, self).get_context_data(**kwargs)
#    context['name'] = 'Mike'
#    return context
