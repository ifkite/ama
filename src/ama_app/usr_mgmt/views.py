from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from ama_app.excepts import LoginExcept, CaptchaExcept, UserHasExist
from ama_app.usr_mgmt.utils import LOGIN_ERR
import logging

log = logging.getLogger(__file__)


def create_user(username, password):
    user = User.objects.create_user(username=username, password=password)
    user.save()
    return user


def chk_usr_exist(username):
    return User.objects.filter(username=username).exists()


def register_handler(params, *args, **kwargs):
    username = params.get('username')
    password = params.get('password')
    captcha_hash = params.get('captcha_hash')
    code = params.get('code')
    request = kwargs.get('request')

    if not chk_captcha(captcha_hash, code):
        raise CaptchaExcept

    if request.user.is_authenticated():
        return redirect(reverse('home'))

    if chk_usr_exist(username):
        log.warning("register failed: username {0} has existed".format(username))
        raise UserHasExist

    create_user(username, password)
    # login
    user = authenticate(username=username, password=password)
    auth_login(request, user)
    request.session.set_expiry(0)

    return redirect(reverse('home'))


def register_page(request):
    context = {"action": "register"}
    captcha_hash = CaptchaStore.generate_key()
    captcha_image = captcha_image_url(captcha_hash)
    context.update({
            "captcha_hash": captcha_hash,
            "captcha_image": captcha_image
    })

    return render(request, "login.html", context=context)


@require_http_methods(["GET", "POST"])
def register(request):
    # in fact, verification and user profile are required
    if request.method == "POST":
        params = {
                "username": request.POST.get('username'),
                "password": request.POST.get('password'),
                "captcha_hash": request.POST.get('captcha_hash'),
                "code": request.POST.get('code'),
        }
        try:
            return register_handler(params, request=request)
        except (CaptchaExcept, UserHasExist):
            return register_page(request)
    else:
        return register_page(request)


def chk_captcha(hashkey, response):
    return CaptchaStore.objects.filter(hashkey=hashkey, response=response)


def chk_login_err(request):
    return request.session.get('login_err') > LOGIN_ERR


def login_handler(params, *args, **kwargs):
    username = params.get('username')
    password = params.get('password')
    captcha_hash = params.get('captcha_hash')
    code = params.get('code')
    next = params.get('next')
    request = kwargs.get('request')

    if chk_login_err(request) and not chk_captcha(captcha_hash, code):
        raise CaptchaExcept

    user = authenticate(username=username, password=password)
    # ignore if user is_active or not
    try:
        auth_login(request, user)
    except AttributeError:
        request.session['login_err'] = request.session.get('login_err', 0) + 1
        log.warning('login failed: username {0}'.format(username))
        raise LoginExcept

    request.session['login_err'] = 0
    request.session.set_expiry(0)

    # TODO: check next, next shuold in our domain
    try:
        return redirect(next)
    except:
        return redirect(reverse('home'))


def login_page(request):
    # TODO: make sure that next should in domain
    context = {"action": "login", "next": request.GET.get('next', '')}
    if chk_login_err(request):
        captcha_hash = CaptchaStore.generate_key()
        captcha_image = captcha_image_url(captcha_hash)
        context.update({
                "captcha_hash": captcha_hash,
                "captcha_image": captcha_image
        })
    return render(request, "login.html", context=context)


@require_http_methods(["GET", "POST"])
def login(request):
    if request.method == "POST":
        params = {
                "username": request.POST.get('username'),
                "password": request.POST.get('password'),
                "captcha_hash": request.POST.get('captcha_hash'),
                "code": request.POST.get('code'),
                "next": request.POST.get('next', '')
        }
        try:
            return login_handler(params, request=request)
        except (LoginExcept, CaptchaExcept):
            return login_page(request)
    else:
        return login_page(request)


@require_http_methods(["GET", "POST"])
def logout(request):
    auth_logout(request)
    return redirect(reverse('home'))
