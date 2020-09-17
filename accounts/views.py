from django.shortcuts import render

from accounts.forms import RegisterForm


def register(request):
    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            new_user:user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()

        return render(request, 'accounts/register')
    else:
        user_form=RegisterForm()


    return render(request, 'accounts/register.html', {'form':user_form})