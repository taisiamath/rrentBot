import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import (
    ReplyKeyboardBuilder,
    KeyboardButton,
    InlineKeyboardBuilder,
)

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Конфигурация бота
API_TOKEN = "7757068839:AAHlYJl3cDpG9HOiqRiLJRgjvdMyouYxDt4"
MANAGER_CHAT_ID = 1097537387
OWNER_CHAT_ID = 1097537387  # ID арендодателя

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


# ========== КЛАВИАТУРЫ ==========
def get_main_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(
        KeyboardButton(text="📷 Фото квартиры"),
        KeyboardButton(text="📝 Описание квартиры"),
        KeyboardButton(text="📅 Календарь бронирования"),
        KeyboardButton(text="🖥 Самостоятельное бронирование"),
        KeyboardButton(text="✅ Забронировать"),
        KeyboardButton(text="💬 Чат с арендодателем"),
    )
    builder.adjust(2, 2, 2)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=False)


# ========== ОБРАБОТЧИК КНОПКИ ЧАТА ==========
@dp.message(lambda message: message.text == "💬 Чат с арендодателем")
async def start_owner_chat(message: types.Message):
    try:
        client_builder = InlineKeyboardBuilder()
        client_builder.add(
            types.InlineKeyboardButton(
                text="💬 Написать арендодателю", url=f"tg://user?id={OWNER_CHAT_ID}"
            )
        )
        await message.answer(
            "Нажмите кнопку ниже, чтобы перейти в чат с арендодателем:",
            reply_markup=client_builder.as_markup(),
        )

        # Создаем инлайн-кнопку для админа (ссылка на клиента)
        admin_builder = InlineKeyboardBuilder()
        admin_builder.add(
            types.InlineKeyboardButton(
                text=f"👤 Клиент {message.from_user.full_name}",
                url=f"tg://user?id={message.from_user.id}",
            )
        )

        # Отправляем уведомление админу
        await bot.send_message(
            chat_id=MANAGER_CHAT_ID,
            text=f"🔔 Пользователь @{message.from_user.username} хочет связаться с арендодателем",
            reply_markup=admin_builder.as_markup(),
        )

    except Exception as e:
        logger.error(f"Ошибка при обработке запроса чата: {e}")
        await message.answer(
            "⚠️ Не удалось открыть чат. Пожалуйста, попробуйте позже.",
            reply_markup=get_main_keyboard(),
        )


# ========== СОСТОЯНИЯ ==========
class BookingStates(StatesGroup):
    name = State()
    dates = State()
    adults = State()
    children = State()
    pets = State()


# ========== ОБРАБОТЧИКИ КОМАНД ==========
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "🏠 Добро пожаловать в бота аренды квартиры!\nВыберите действие:",
        reply_markup=get_main_keyboard(),
    )


# ========== ОБРАБОТЧИКИ КНОПОК ==========
@dp.message(lambda message: message.text == "📷 Фото квартиры")
async def show_photos(message: types.Message):
    try:
        # Список путей к фотографиям
        photo_paths = [
            "photos/photo1.jpg",
            "photos/photo2.jpg",
            "photos/photo3.jpg",
            "photos/photo4.jpg",
            "photos/photo5.jpg",
            "photos/photo6.jpg",
            "photos/photo7.jpg",
            "photos/photo8.jpg",
            "photos/photo9.jpg",
            "photos/photo10.jpg",
        ]

        # Отправляем первое фото с подписью
        with open(photo_paths[0], "rb") as photo:
            await message.answer_photo(
                photo,
                caption="🏠 Фото квартиры (1/10)",
                reply_markup=get_main_keyboard(),
            )

        # Отправляем остальные фото
        for path in photo_paths[1:]:
            with open(path, "rb") as photo:
                await message.answer_photo(photo)

    except FileNotFoundError as e:
        logger.error(f"Файл не найден: {e}")
        await message.answer("⚠️ Фотографии временно недоступны. Попробуйте позже.")
    except Exception as e:
        logger.error(f"Ошибка при отправке фото: {e}")
        await message.answer(
            "⚠️ Произошла ошибка при загрузке фотографий. Попробуйте позже."
        )


@dp.message(lambda message: message.text == "📝 Описание квартиры")
async def show_description(message: types.Message):
    description = """
    🏢 Евродвушка от собственника в новом жк бизнес-класса Кватро:
    • Площадь: 36 м²
    • Спальня: двуспальная кровать, кресло-кровать, телевизор, места для хранения, стол
    • Гостинная: двуспальный диван, обеденный стол
    • Кухня: кухонный гарнитур, холодильник, посудомоечная машина, чайник, духовка, микроволновка
    • Удобства: Wi-Fi, кондиционер, стиральная машинка с сушкой, утюг и гладильная доска, фен, матрас (для моря), smart TV, вся необходимая посуда, в том числе для готовки

    <b>Всё необходимое — в шаговой доступности:</b>

• Сетевые магазины, аптека, пекарня
• Больница и автобусная остановка — рядом
• 15 минут неспешной прогулки — и вы на <b>пляже</b> или ж/д станции "Дагомыс"!

🚆 "Ласточка":
• До центра Сочи — 10 минут
• В любую точку побережья — быстро и комфортно

🚗 Удобство для гостей:
• Зона завершения всех сервисов каршеринга — арендуйте авто без проблем!

🌿 Природные достопримечательности рядом:
• Дагомысские корыта — освежающие купели в горной реке
• Парк "Солохоул" — захватывающие виды на ущелье реки Шахе
• Зиплайн — адреналин и полёт над каньоном! 

📍 ЖК с продуманной инфраструктурой — ваш комфорт на первом месте!

✨ Приезжайте — и почувствуйте гармонию моря, гор и городского удобства!

📍 <b>ВНИМАНИЕ!</b> При бронировании через этот бот, Вы получаете скидку 10% и трансфер от вокзала Сочи!  
"""
    await message.answer(description)


@dp.message(lambda message: message.text == "📅 Календарь бронирования")
async def show_calendar(message: types.Message):
    await message.answer(
        "Календарь доступен по ссылке:\nhttps://sutochno.ru/front/searchapp/detail/1856903?guests_adults=1&occupied=2025-07-18%3B2025-07-19"
    )


@dp.message(lambda message: message.text == "🖥 Самостоятельное бронирование")
async def self_booking(message: types.Message):
    await message.answer(
        "Для бронирования перейдите по ссылке:\nhttps://sutochno.ru/front/searchapp/detail/1856903?guests_adults=1&occupied=2025-07-18%3B2025-07-19"
    )


# ========== ПРОЦЕСС БРОНИРОВАНИЯ ==========
@dp.message(lambda message: message.text == "✅ Забронировать")
async def start_booking(message: types.Message, state: FSMContext):
    await state.set_state(BookingStates.name)
    await message.answer("Введите ваше имя:", reply_markup=types.ReplyKeyboardRemove())


@dp.message(BookingStates.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(BookingStates.dates)
    await message.answer("Укажите даты бронирования (например, 01.07.24-10.07.24):")


@dp.message(BookingStates.dates)
async def process_dates(message: types.Message, state: FSMContext):
    await state.update_data(dates=message.text)
    await state.set_state(BookingStates.adults)
    await message.answer("Количество взрослых:")


@dp.message(BookingStates.adults)
async def process_adults(message: types.Message, state: FSMContext):
    await state.update_data(adults=message.text)
    await state.set_state(BookingStates.children)
    await message.answer("Количество детей (если нет, введите 0):")


@dp.message(BookingStates.children)
async def process_children(message: types.Message, state: FSMContext):
    await state.update_data(children=message.text)
    await state.set_state(BookingStates.pets)
    await message.answer("Будут ли с вами животные? (да/нет)")


@dp.message(BookingStates.pets)
async def process_pets(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        booking_info = (
            "🔔 Новая заявка на бронирование:\n"
            f"👤 Имя: {data['name']}\n"
            f"📅 Даты: {data['dates']}\n"
            f"👥 Взрослых: {data['adults']}\n"
            f"🧒 Детей: {data['children']}\n"
            f"🐕 Животные: {'Да' if message.text.lower() in ['да', 'yes'] else 'Нет'}\n"
            f"🆔 ID пользователя: {message.from_user.id}\n"
            f"👤 Контакт: @{message.from_user.username or 'нет username'}"
        )

        # Создаем кнопку для связи с клиентом
        contact_builder = InlineKeyboardBuilder()
        contact_builder.add(
            types.InlineKeyboardButton(
                text=f"📩 Связаться с {data['name']}",
                url=f"tg://user?id={message.from_user.id}",
            )
        )

        await message.answer(
            "✅ Ваша заявка принята! Менеджер свяжется с вами в ближайшее время.",
            reply_markup=get_main_keyboard(),
        )

        await bot.send_message(
            chat_id=MANAGER_CHAT_ID,
            text=booking_info,
            reply_markup=contact_builder.as_markup(),
        )

    except Exception as e:
        logger.error(f"Ошибка при обработке заявки: {e}")
        await message.answer(
            "⚠️ Произошла ошибка. Пожалуйста, попробуйте позже.",
            reply_markup=get_main_keyboard(),
        )
    finally:
        await state.clear()


# Обработчик неизвестных сообщений
@dp.message()
async def unknown_message(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer(
            "Пожалуйста, используйте кнопки меню", reply_markup=get_main_keyboard()
        )


# Запуск бота
async def main():
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("🔄 Бот запускается...")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}")
    finally:
        await bot.session.close()
        logger.info("🛑 Бот остановлен")


if __name__ == "__main__":
    asyncio.run(main())
