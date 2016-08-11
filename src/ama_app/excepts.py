class LoginExcept(Exception):
    error_code = 0x0001
    error_msg = "login failed"


class CaptchaExcept(Exception):
    error_code = 0x0002
    error_msg = "captcha validate failed"


class UserHasExist(Exception):
    error_code = 0x0003
    error_code = "user has existed"
