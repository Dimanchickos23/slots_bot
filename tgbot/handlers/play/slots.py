from asyncio import sleep

from aiogram import Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Regexp
from aiogram.types import CallbackQuery, Message
from aiogram.utils.exceptions import MessageNotModified

from tgbot.keyboards.inline import slots_kb, back_cb, back_kb
from tgbot.misc.states import Slots


async def start_slots(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    await state.finish()
    bot = Bot.get_current()
    slots_text = f"<b>🎰 SLOTS</b>\n\n<b>🎁 Рейты:</b>\n— При выбивании 2 одинаковых предмета на 1 и 2 позиции ваша " \
                 f"ставка умножается на <b>x2</b>\n— При выбивании 3 одинаковых предметов подряд ваша ставка " \
                 f"умножается на <b>x5</b>\n— При выбивании трех 7 ваша ставка умножается на <b>x7</b>\n\n<b>💰 Ваша " \
                 f"ставка - {bot['bet']} ₽</b> "

    if cb.message.animation:
        await cb.message.edit_caption(
            caption=slots_text,
            reply_markup=slots_kb
        )
    else:
        await cb.message.answer_animation(
            animation="CgACAgIAAxkBAAEBvb1kIHeXlluLI7wGSa8qUPGJndrHRQACJS0AAkJbyUhgfTtFSyXqfC8E",
            caption=slots_text,
            reply_markup=slots_kb
        )


async def set_new_bet(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    await Slots.Bet.set()
    await state.update_data(msg=cb.message)
    if cb.message.animation:
        await cb.message.edit_caption("<b>🎰 SLOTS</b>\n\n"
                                      "— Доступно: <b>0.0 ₽</b>\n"
                                      "— Минимум: <b>10 ₽</b>\n"
                                      "— Максимум: <b>100 ₽</b>\n\n"
                                      "<b>ℹ️ Введите новую ставку</b>",
                                      reply_markup=back_kb("to_slots"))
    else:
        await cb.message.edit_text("<b>🎰 SLOTS</b>\n\n"
                                   "— Доступно: <b>0.0 ₽</b>\n"
                                   "— Минимум: <b>10 ₽</b>\n"
                                   "— Максимум: <b>100 ₽</b>\n\n"
                                   "<b>ℹ️ Введите новую ставку</b>",
                                   reply_markup=back_kb("to_slots"))


async def wrong_bet(message: Message, state: FSMContext):
    await sleep(0.5)
    bot = Bot.get_current()
    await message.delete()
    data = await state.get_data()
    msg = data["msg"]
    try:

        if msg.animation:
            await bot.edit_message_caption(msg.chat.id, msg.message_id,
                                           caption="<b>⚠️ Неправильный ввод, нужно ввести число</b>\n\n"
                                                   "— Минимум: <b>10</b>\n"
                                                   "— Максимум: <b>100</b>\n\n"
                                                   "<b>ℹ️ Введите новую ставку</b>",
                                           reply_markup=back_kb("to_slots"))
        else:
            await bot.edit_message_text("<b>⚠️ Неправильный ввод, нужно ввести число</b>\n\n"
                                        "— Минимум: <b>10</b>\n"
                                        "— Максимум: <b>100</b>\n\n"
                                        "<b>ℹ️ Введите новую ставку</b>",
                                        msg.chat.id, msg.message_id,
                                        reply_markup=back_kb("to_slots"))
    except MessageNotModified:
        pass


async def approve_bet(message: Message, state: FSMContext):
    data = await state.get_data()
    msg = data["msg"]
    await state.finish()
    bot = Bot.get_current()
    bot['bet'] = int(message.text)
    await sleep(0.5)
    await message.delete()
    if msg.animation:
        await bot.edit_message_caption(msg.chat.id, msg.message_id,
                                       caption="<b>🎰 SLOTS</b>\n\n"
                                               "<b>🎁 Рейты:</b>\n"
                                               "— При выбивании 2 одинаковых предмета на 1 и 2 позиции ваша ставка "
                                               "умножается на <b>x2</b>\n "
                                               "— При выбивании 3 одинаковых предметов подряд ваша ставка умножается "
                                               "на "
                                               "<b>x5</b>\n "
                                               "— При выбивании трех 7 ваша ставка умножается на <b>x7</b>\n\n"
                                               f"<b>💰 Ваша ставка - {bot['bet']} ₽</b>",
                                       reply_markup=slots_kb)
    else:
        await bot.edit_message_text("<b>🎰 SLOTS</b>\n\n"
                                    "<b>🎁 Рейты:</b>\n"
                                    "— При выбивании 2 одинаковых предмета на 1 и 2 позиции ваша ставка "
                                    "умножается на <b>x2</b>\n "
                                    "— При выбивании 3 одинаковых предметов подряд ваша ставка умножается на "
                                    "<b>x5</b>\n "
                                    "— При выбивании трех 7 ваша ставка умножается на <b>x7</b>\n\n"
                                    f"<b>💰 Ваша ставка - {bot['bet']} ₽</b>",
                                    msg.chat.id, msg.message_id,
                                    reply_markup=slots_kb
                                    )


async def spin(cb: CallbackQuery):
    await cb.answer()
    bot = Bot.get_current()
    msg = await cb.message.answer_dice(emoji="🎰", disable_notification=False)
    value = msg.dice.value
    winning_slots = {
        6: {"values": ("grape", "grape", "bar"), "prize": 2},
        11: {"values": ("lemon", "lemon", "bar"), "prize": 2},
        16: {"values": ("seven", "seven", "bar"), "prize": 2},
        17: {"values": ("bar", "bar", "grape"), "prize": 2},
        27: {"values": ("lemon", "lemon", "grape"), "prize": 2},
        32: {"values": ("seven", "seven", "grape"), "prize": 2},
        33: {"values": ("bar", "bar", "lemon"), "prize": 2},
        38: {"values": ("grape", "grape", "lemon"), "prize": 2},
        48: {"values": ("seven", "seven", "lemon"), "prize": 2},
        49: {"values": ("bar", "bar", "seven"), "prize": 2},
        54: {"values": ("grape", "grape", "seven"), "prize": 2},
        59: {"values": ("lemon", "lemon", "seven"), "prize": 2},
        1: {"values": ("bar", "bar", "bar"), "prize": 5},
        22: {"values": ("grape", "grape", "grape"), "prize": 5},
        43: {"values": ("lemon", "lemon", "lemon"), "prize": 5},
        64: {"values": ("seven", "seven", "seven"), "prize": 7}
    }
    name = cb.from_user.get_mention(as_html=True)
    await sleep(2.35)
    if value not in winning_slots:
        await cb.message.answer(
            f"{name}, вы проиграли. 😢",
            reply_markup=slots_kb
        )
    else:
        prize = winning_slots[value]["prize"]
        await cb.message.answer(
            f"{name}, поздравляем с победой!\n"
            f"Ваш выйгрыш — <b>{bot['bet'] * prize} ₽</b>",
            reply_markup=slots_kb
        )


def register_slots(dp: Dispatcher):
    dp.register_callback_query_handler(start_slots, lambda cb: cb.data == "slots")
    dp.register_callback_query_handler(start_slots, back_cb.filter(action="to_slots"), state="*")
    dp.register_callback_query_handler(set_new_bet, lambda cb: cb.data == "bet")
    dp.register_message_handler(approve_bet, Regexp(r"^([1-9][0-9]|100)$"), state=Slots.Bet)
    dp.register_message_handler(wrong_bet, state=Slots.Bet)
    dp.register_callback_query_handler(spin, lambda cb: cb.data == "spin")
