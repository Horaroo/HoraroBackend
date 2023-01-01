from django.contrib.auth.tokens import default_token_generator
from djoser import utils
from djoser.conf import settings
from templated_mail.mail import BaseEmailMessage


class CustomPasswordResetEmail(BaseEmailMessage):
    template_name = "api/password_reset.html"

    def get_context_data(self):
        context = super().get_context_data()
        user = context.get("user")
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.PASSWORD_RESET_CONFIRM_URL.format(**context)
        return context


class CustomActivationEmail(BaseEmailMessage):
    template_name = "api/activation.html"

    def get_context_data(self):
        context = super().get_context_data()

        user = context.get("user")
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.ACTIVATION_URL.format(**context)
        return context


def copy_week(queryset, username, from_week, week):
    for data in queryset.filter(group__username=username, week_id=from_week).all():
        queryset.create(
            number_pair=data.number_pair,
            subject=data.subject,
            teacher=data.teacher,
            audience=data.audience,
            week=week,
            group=data.group,
            type_pair=data.type_pair,
            day=data.day,
            start_time=data.start_time,
            end_time=data.end_time,
        )
