from sqladmin import ModelView
from database.profile.models import Profile

class ProfileAdmin(ModelView, model=Profile):
    # Use column names as strings
    column_list = (
        'id', 
        'user_id', 
        'creation_date', 
        'title', 
        'birth_date', 
        'birth_time', 
        'birth_location_name',
        # 'location_latitude', 
        # 'location_longitude', 
        # 'location_timezone', 
    )

    column_searchable_list = (
        'id', 
        'user_id', 
        'title', 
        'birth_date', 
        'birth_time', 
        'birth_location_name',
        # 'location_latitude', 
        # 'location_longitude', 
        # 'location_timezone', 
    )

    column_sortable_list = (
        'id', 
        'user_id', 
        'creation_date', 
        'title', 
        'birth_date', 
        'birth_time', 
        'birth_location_name',
        # 'location_latitude', 
        # 'location_longitude', 
        # 'location_timezone', 
    )

    column_filters = (
        'id', 
        'user_id', 
        'creation_date', 
        'title', 
        'birth_date', 
        'birth_time', 
        'birth_location_name',
        # 'location_latitude', 
        # 'location_longitude', 
        # 'location_timezone', 
    )

    form_columns = (
        'id',
        'user_id', 
        'title', 
        'birth_date', 
        'birth_time', 
        'birth_location_name',
        # 'location_latitude', 
        # 'location_longitude', 
        # 'location_timezone', 
    )

    column_labels = {
        'id': 'ID',
        'user_id': 'ID пользователя',
        'creation_date': 'Дата создания',
        'title': 'Название',
        'birth_date': 'Дата рождения',
        'birth_time': 'Время рождения',
        'birth_location_name': 'Название места рождения',
        # 'location_latitude': 'Текущая широта',
        # 'location_longitude': 'Текущая долгота',
        # 'location_timezone': 'Часовой пояс',
    }
