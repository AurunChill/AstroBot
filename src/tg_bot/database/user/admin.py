from sqladmin import ModelView

from database.user.models import Subscription, User


class UserAdmin(ModelView, model=User):
    column_list = [
        User.id,
        User.name,
        User.locale,
        User.subscription,
        User.subscription_expiration_date,
        User.is_mail_subscribed,
    ]

    form_columns = [
        User.name,
        User.locale,
        User.subscription,
        User.subscription_expiration_date,
        User.is_mail_subscribed,
    ]

    column_filters = [
        User.id,
        User.name,
        User.locale,
        User.subscription,
        User.subscription_expiration_date,
        User.is_mail_subscribed,
    ]

    column_editable_list = [
        User.subscription,
        User.subscription_expiration_date,
        User.is_mail_subscribed,
    ]

    column_labels = {
        User.id: "ID",
        User.name: "Название",
        User.locale: "Язык",
        User.subscription: "Подписка",
        User.subscription_expiration_date: "Срок подписки",
        User.is_mail_subscribed: "Подписка на рассылку",
    }

    form_widget_args = {
        User.subscription: {"choices": (Subscription.FOREVER, Subscription.MONTHLY, Subscription.FREELY)},
    }
