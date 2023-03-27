from aiogram.dispatcher.filters.state import StatesGroup, State


class Withdrawal(StatesGroup):
    Amount = State()
    Requisites = State()


class Present(StatesGroup):
    Enter_id = State()
    Enter_amount = State()


class Promo(StatesGroup):
    Activate_promo = State()
    Name = State()
    Count = State()
    Price = State()
    Buy = State()


class Slots(StatesGroup):
    Bet = State()


class Play(StatesGroup):
    Bet = State()
