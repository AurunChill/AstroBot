from sqladmin import ModelView

from database.predictions.models import Prediction, PredictionType


class PredictionAdmin(ModelView, model=Prediction):
    column_list = [
        "id",
        "profile_id",
        "prediction_type",
        "recognition_str",
    ]

    column_searchable_list = [
        "id",
        "profile_id",
        "prediction_type",
        "recognition_str",
    ]

    column_filters = [
        "id",
        "profile_id",
        "prediction_type",
        "recognition_str",
    ]

    form_excluded_columns = [
        "id",
    ]

    column_sortable_list = [
        "id",
        "profile_id",
        "prediction_type",
        "recognition_str",
    ]

    column_labels = {
        "id": "ID",
        "profile_id": "ID профиля",
        "prediction_type": "Тип предсказания",
        "recognition_str": "Строка распознавания",
    }

    form_widget_args = {
        "prediction_type": {
            "choices": [
                (PredictionType.HOROSCOPE, PredictionType.HOROSCOPE.value),
            ]
        }
    }
