from django import forms
    
supported_locs = (
    ('Boston, MA', 'Boston, MA'),
    ('Houston, TX', 'Houston, TX'),
    ('San Fransisco, CA', 'San Fransisco, CA'),
    ('New York, NY', 'New York, NY'),
    ('Seattle, WA', 'Seattle, WA'),
    ('Atlanta, GA', 'Atlanta, GA'),
    ('Orlando, FL', 'Orlando, FL')
)

class LoginForm(forms.Form):
    username = forms.CharField(max_length = 60, widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}))
    password = forms.CharField(max_length = 60, widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))

class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length = 60, widget=forms.TextInput(attrs={'placeholder': 'First Name', 'id': 'first-name', 'class': 'form-control'}))
    last_name = forms.CharField(max_length = 60, widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'id': 'last-name', 'class': 'form-control'}))
    username = forms.CharField(max_length = 30, widget=forms.TextInput(attrs={'placeholder': 'Username (max 30 characters 0-9 A-z)', 'id': 'username', 'class': 'form-control'}))
    password = forms.CharField(max_length = 60, widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'id': 'password', 'class': 'form-control'}))
    verify_password = forms.CharField(max_length = 60, widget=forms.PasswordInput(attrs={'placeholder': 'Verify Password', 'id': 'verify-password', 'class': 'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email', 'id': 'email', 'class': 'form-control'}))
    verify_email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Verify Email', 'id': 'verify-email', 'class': 'form-control'}))
    location = forms.ChoiceField(supported_locs, widget=forms.Select(attrs={'id': 'location', 'class': 'form-control'}))

# class AccountSettingsForm(forms.Form):
#     first_name = forms.CharField(max_length = 60)
#     last_name = forms.CharField(max_length = 60)
#     email = forms.EmailField()
#     cur_password = forms.CharField(max_length = 30)
#     new_password = forms.CharField(max_length = 30)
#     ver_new_password = forms.CharField(max_length = 30)
#     location = forms.ChoiceField(supported_locs)

    
