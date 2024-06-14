from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout,update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from account.forms import LoginUserForm, NewUserForm, UserPasswordChangeForm
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm

def user_login(request):
    if request.user.is_authenticated and "next" in request.GET:
        return render(request, "account/login.html", {"error": "Yetkiniz yok."})

    if request.method == "POST":
        form = LoginUserForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.add_message(request, messages.SUCCESS, "Giriş başarılı")
                next_url = request.GET.get("next", None)
                if next_url is None:
                    return redirect("index")
                else:
                    return redirect(next_url)
            else:
                messages.add_message(request, messages.ERROR, "Geçersiz kullanıcı adı veya şifre.")
        else:
            messages.add_message(request, messages.ERROR, "Form geçersiz.")
        return render(request, "account/login.html", {"form": form})
    else:
        form = LoginUserForm()
        return render(request, "account/login.html", {"form": form})

def user_register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            
            # Hata ayıklama: Kullanıcı adı ve parola yazdır
            print(f"DEBUG: username={username}, password={password}")

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("index")
            else:
                # Hata ayıklama: Kullanıcı doğrulaması başarısız
                print("DEBUG: Kullanıcı doğrulaması başarısız")
                messages.add_message(request, messages.ERROR, "Kullanıcı doğrulaması başarısız.")
                return render(request, "account/register.html", {"form": form})
        else:
            # Hata ayıklama: Form hatalarını yazdır
            print(f"DEBUG: form errors={form.errors}")
            return render(request, "account/register.html", {"form": form})

    else:
        form = NewUserForm()
        return render(request, "account/register.html", {"form": form})

def change_password(request):
    if request.method == "POST":
        form=UserPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request,user)
            messages.success(request,"parola güncellendi.")
            return redirect("change_password")
        else:
            return render(request, "account/change-password.html",{"form":form})

    form = UserPasswordChangeForm(request.user)
    return render(request, "account/change-password.html",{"form":form})


def user_logout(request):
    messages.add_message(request, messages.SUCCESS, "Çıkış başarılı")
    logout(request)
    return redirect("index")
