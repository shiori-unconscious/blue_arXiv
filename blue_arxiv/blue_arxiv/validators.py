from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
import re

class CustomValidator:
    def __init__(self, *args, **kwargs):
        pass

    def validate(self, password, user=None):
        if len(password) < 12:
            raise ValidationError(
                _("你的密码至少要包括12个字符"),
                code='password_too_short',
            )
        if bool(re.search(r'\d', password)) == False:
            raise ValidationError(
                _("你的密码至少要包括一个数字"),
                code='password_without_number',
            )
            

    def get_help_text(self):
        return _("你的密码至少要包括12个字符"
                 "你的密码至少要包括一个数字")
