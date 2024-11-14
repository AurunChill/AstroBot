from aiogram.fsm.state import StatesGroup, State

class RegistrationStates(StatesGroup):
    user_name = State()
    title = State()
    birth_date = State()
    birth_location = State()
    location = State()