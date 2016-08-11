from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url


def create_user(username, password):
    user = User.objects.create_user(username=username, password=password)
    user.save()
    return user


def chk_usr_exist(username):
    return User.objects.filter(username=username).exists()


def register_handler(params, *args, **kwargs):
    username = params.get('username')
    password = params.get('password')
    hashkey = params.get('hashkey')
    code = params.get('code')
    request = kwargs.get('request')

    check_captcha(hashkey, code)
    if request.user.is_authenticated():
        return redirect(reverse('home'))
    if chk_usr_exist(username):
        # TODO: eliminate const num and string
        return JsonResponse({"error_code": 400, "error_msg": "username :{0} existed".format(username)})

    create_user(username, password)
    # login
    user = authenticate(username=username, password=password)
    auth_login(request, user)
    request.session.set_expiry(0)

    return redirect(reverse('home'))


@require_http_methods(["GET", "POST"])
def register(request):
    # in fact, verification and user profile are required
    if request.method == "POST":
        params = {
                "username": request.POST.get('username'),
                "password": request.POST.get('password'),
                "hashkey": request.POST.get('hashkey'),
                "code": request.POST.get('code'),
        }
        return register_handler(params, request=request)
    else:
        captcha_hash = CaptchaStore.generate_key()
        captcha_image = captcha_image_url(captcha_hash)
        context = {
                "action": "register",
                "captcha_hash": captcha_hash,
                "captcha_image": captcha_image
        }
        return render(request, "login.html", context=context)


def check_captcha(hashkey, code):
    captcha = CaptchaStore.objects.filter(hashkey=hashkey, response=code)
    return captcha.exists()


def login_handler(params, *args, **kwargs):
    username = params.get('username')
    password = params.get('password')
    hashkey = params.get('hashkey')
    code = params.get('code')
    request = kwargs.get('request')

    check_captcha(hashkey, code)

    user = authenticate(username=username, password=password)
    # ignore if user is_active or not
    auth_login(request, user)
    request.session.set_expiry(0)

    # redirect
    return redirect(reverse('home'))


@require_http_methods(["GET", "POST"])
def login(request):
    if request.method == "POST":
        params = {
                "username": request.POST.get('username'),
                "password": request.POST.get('password'),
                "hashkey": request.POST.get('hashkey'),
                "code": request.POST.get('code'),
        }
        return login_handler(params, request=request)
    else:
        captcha_hash = CaptchaStore.generate_key()
        captcha_image = captcha_image_url(captcha_hash)
        context = {
                "action": "login",
                "captcha_hash": captcha_hash,
                "captcha_image": captcha_image
        }
        return render(request, "login.html", context=context)
