from aiogram import Dispatcher
from aiogram.types import CallbackQuery, InlineKeyboardButton

from tgbot.keyboards.inline import referral_kb, back_cb, ref_value_kb


async def user_profile_return(cb: CallbackQuery):
    await cb.answer()
    await cb.message.edit_caption(caption=f"<b>👤 Профиль</b>\n\n"
                                          f"<b>🆔 ID:</b>\n<code>{cb.from_user.id}</code>\n"
                                          f"<b>👤 Username:</b>\n<code>{cb.from_user.username}</code>\n"
                                          f"<b>⏱ Дата регистрации:</b>\nНужно сделать БД",
                                  reply_markup=referral_kb)


async def ref_system(cb: CallbackQuery):
    await cb.answer()

    back_btn = InlineKeyboardButton(text="🔙 Назад",
                                    callback_data=back_cb.new(action="to_profile"))
    ref_value_kb.insert(back_btn)

    await cb.message.edit_caption("<b>👥 Реферальная система</b>\n\n"
                                  "👤 Кол-во рефералов: <b>0</b>\n"
                                  "💰 Заработано: <b>0.0 ₽</b>\n\n"
                                  "— За каждую победу Вашего реферала - Вы будете получать 0.5%\n"
                                  "— Вывод заработанных денег возможен от 300 ₽\n\n"
                                  "🔗 <b>Ваша реферальная ссылка</b>\n"
                                  f"https://t.me/Shu23_Test_bot?start={cb.from_user.id}",
                                  reply_markup=ref_value_kb
                                  )
    ref_value_kb.inline_keyboard.pop()


async def ref_reward_cb(cb: CallbackQuery):
    await cb.answer("⚠️ У вас нулевой счет", show_alert=True)
    # тут надо работать с БД


def register_referral_sys(dp: Dispatcher):
    dp.register_callback_query_handler(ref_system, lambda cb: cb.data == "ref_sys")
    dp.register_callback_query_handler(user_profile_return, back_cb.filter(action="to_profile"))
    dp.register_callback_query_handler(ref_reward_cb, lambda cb: cb.data == "bonus_funds")