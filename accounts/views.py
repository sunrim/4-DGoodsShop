from django.shortcuts import render

from accounts.forms import RegisterForm


def register(request):
  if request.method == 'POST':
    #회원가입 데이터 입력하고 버튼 눌렀을 때
    user_form = RegisterForm(request.POST)
    if user_form.is_valid():
      new_user = user_form.save(commit=False)
      new_user.set_password(user_form.cleaned_data['password'])
      new_user.save()

    return render(request, 'accounts/register_done.html', {'new_user': new_user})
  else: #회원가입 폼 나오게
    user_form = RegisterForm()

  return render(request, 'accounts/register.html', {'form': user_form})