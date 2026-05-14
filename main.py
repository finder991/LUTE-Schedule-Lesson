from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
)

TOKEN = "TOKEN"
SEMESTER_START = datetime(2026, 2, 9)
ANCHOR_WEEK_TYPE = "Лекційний тиждень"

DAYS_UA = {
    "Monday": "Понеділок", "Tuesday": "Вівторок", "Wednesday": "Середа",
    "Thursday": "Четвер", "Friday": "П'ятниця",
    "Saturday": "Субота", "Sunday": "Неділя",
}


def get_week() -> str:
    anchor = SEMESTER_START.isocalendar()[1]
    now = datetime.now().isocalendar()[1]
    if (now % 2) == (anchor % 2):
        return ANCHOR_WEEK_TYPE
    return "Практичний тиждень"


def current_day() -> str:
    return datetime.now().strftime("%A")


BELLS = {
    "bach23": {
        "title": "Бакалавр, 2–3 курс",
        "pairs": [
            ("9:00", "10:20"),
            ("10:30", "11:50"),
            ("12:20", "13:40"),
            ("13:50", "15:10"),
            ("15:20", "16:40"),
            ("16:50", "18:10"),
        ],
    },
    "bach14": {
        "title": "Бакалавр, 1 та 4 курс",
        "pairs": [
            ("9:00", "10:20"),
            ("10:30", "11:50"),
            ("12:20", "13:40"),
            ("13:50", "15:10"),
        ],
    },
    "master": {
        "title": "Магістр",
        "pairs": [
            ("9:00", "10:20"),
            ("10:30", "11:50"),
            ("12:20", "13:40"),
            ("13:50", "15:10"),
        ],
    },
}



LECTURES = {
    "Global": {
        "Monday": [
            {"pair": 1, "time": "9:00–10:20", "subject": "Теорія прийняття рішень",
             "teacher": "доц. Р. Олійник", "room": "Т.Б. 121"},
            {"pair": 2, "time": "10:30–11:50", "subject": "Теорія прийняття рішень",
             "teacher": "доц. Р. Олійник", "room": "Т.Б. 121"},
        ],
        "Tuesday": [
            {"pair": 1, "time": "9:00–10:20",
             "subject": "Електроніка, комп'ютерна схемотехніка та архітектура комп'ютерів",
             "teacher": "доц. В. Пущак", "room": "С. 510"},
            {"pair": 2, "time": "10:30–11:50",
             "subject": "Електроніка, комп'ютерна схемотехніка та архітектура комп'ютерів",
             "teacher": "доц. В. Пущак", "room": "С. 510"},
        ],
        "Wednesday": [
            {"pair": 1, "time": "9:00–10:20", "subject": "Самоменеджмент",
             "teacher": "доц. І. Саврас", "room": "Т.Б. 106", "elective": True},
            {"pair": 2, "time": "10:30–11:50", "subject": "Самоменеджмент",
             "teacher": "доц. І. Саврас", "room": "Т.Б. 106", "elective": True},
            {"pair": 3, "time": "12:20–13:40", "subject": "Паралельні та розподілені обчислення",
             "teacher": "доц. О. Папка", "room": "Т.Б. 121"},
            {"pair": 4, "time": "13:50–15:10", "subject": "Паралельні та розподілені обчислення",
             "teacher": "доц. О. Папка", "room": "Т.Б. 121"},
        ],
        "Thursday": [
            {"pair": 1, "time": "9:00–10:20", "subject": "Проектування інформаційних систем",
             "teacher": "проф. Г. Аніловська", "room": "М. 502"},
            {"pair": 2, "time": "10:30–11:50", "subject": "Проектування інформаційних систем",
             "teacher": "проф. Г. Аніловська", "room": "М. 502"},
        ],
        "Friday": [
            {"pair": 1, "time": "9:00–10:20", "subject": "Основи SMM",
             "teacher": "проф. Ю. Полякова", "room": "Т.Б. 312", "elective": True},
            {"pair": 2, "time": "10:30–11:50", "subject": "Основи SMM",
             "teacher": "проф. Ю. Полякова", "room": "Т.Б. 312", "elective": True},
            {"pair": 5, "time": "15:20–16:40", "subject": "Іспанська мова",
             "teacher": "доц. А. Степанов", "room": "М. 509", "elective": True},
            {"pair": 6, "time": "16:50–18:10", "subject": "Іспанська мова",
             "teacher": "доц. А. Степанов", "room": "М. 509", "elective": True},
        ],
    }
}

PRACTICE = {
    "КН-351": {
        "Monday": [
            {"pair": 1, "time": "9:00–10:20", "subject": "Теорія прийняття рішень",
             "teacher": "доц. Р. Зацерковний, доц. Р. Олійник", "room": "Т.Б. 126, 127"},
            {"pair": 2, "time": "10:30–11:50", "subject": "Теорія прийняття рішень",
             "teacher": "доц. Р. Зацерковний, доц. Р. Олійник", "room": "Т.Б. 126, 127"},
        ],
        "Tuesday": [
            {"pair": 1, "time": "9:00–10:20",
             "subject": "Електроніка, комп'ютерна схемотехніка та архітектура комп'ютерів",
             "teacher": "доц. В. Пущак", "room": "С. 505"},
            {"pair": 2, "time": "10:30–11:50",
             "subject": "Електроніка, комп'ютерна схемотехніка та архітектура комп'ютерів",
             "teacher": "доц. В. Пущак", "room": "С. 505"},
            {"pair": 3, "time": "12:20–13:40",
             "subject": "Електроніка, комп'ютерна схемотехніка та архітектура комп'ютерів",
             "teacher": "доц. В. Пущак", "room": "С. 505"},
        ],
        "Wednesday": [
            {"pair": 1, "time": "9:00–10:20", "subject": "Паралельні та розподілені обчислення",
             "teacher": "доц. О. Чабан, доц. О. Папка", "room": "Т.Б. 126, 127"},
            {"pair": 2, "time": "10:30–11:50", "subject": "Паралельні та розподілені обчислення",
             "teacher": "доц. О. Чабан, доц. О. Папка", "room": "Т.Б. 126, 127"},
            {"pair": 4, "time": "13:50–15:10", "subject": "Самоменеджмент",
             "teacher": "доц. І. Саврас", "room": "Т.Б. 106", "elective": True},
            {"pair": 5, "time": "15:20–16:40", "subject": "Самоменеджмент",
             "teacher": "доц. І. Саврас", "room": "Т.Б. 106", "elective": True},
        ],
        "Thursday": [
            {"pair": 1, "time": "9:00–10:20", "subject": "Проектування інформаційних систем",
             "teacher": "проф. Г. Аніловська, ст. викл. М. Крутяк", "room": "М. 502"},
            {"pair": 2, "time": "10:30–11:50", "subject": "Проектування інформаційних систем",
             "teacher": "проф. Г. Аніловська, ст. викл. М. Крутяк", "room": "М. 502"},
        ],
        "Friday": [
            {"pair": 1, "time": "9:00–10:20", "subject": "Основи SMM",
             "teacher": "проф. Ю. Полякова", "room": "Т.Б. 212", "elective": True},
            {"pair": 2, "time": "10:30–11:50", "subject": "Основи SMM",
             "teacher": "проф. Ю. Полякова", "room": "Т.Б. 212", "elective": True},
            {"pair": 5, "time": "15:20–16:40", "subject": "Іспанська мова",
             "teacher": "доц. А. Степанов", "room": "М. 509", "elective": True},
            {"pair": 6, "time": "16:50–18:10", "subject": "Іспанська мова",
             "teacher": "доц. А. Степанов", "room": "М. 509", "elective": True},
        ],
    },
    "КН-352": {
        "Monday": [
            {"pair": 3, "time": "12:20–13:40", "subject": "Паралельні та розподілені обчислення",
             "teacher": "доц. О. Чабан, доц. О. Папка", "room": "Т.Б. 126, 127"},
            {"pair": 4, "time": "13:50–15:10", "subject": "Паралельні та розподілені обчислення",
             "teacher": "доц. О. Чабан, доц. О. Папка", "room": "Т.Б. 126, 127"},
        ],
        "Tuesday": [
            {"pair": 4, "time": "13:50–15:10",
             "subject": "Електроніка, комп'ютерна схемотехніка та архітектура комп'ютерів",
             "teacher": "доц. В. Пущак", "room": "С. 505"},
            {"pair": 5, "time": "15:20–16:40",
             "subject": "Електроніка, комп'ютерна схемотехніка та архітектура комп'ютерів",
             "teacher": "доц. В. Пущак", "room": "С. 505"},
            {"pair": 6, "time": "16:50–18:10",
             "subject": "Електроніка, комп'ютерна схемотехніка та архітектура комп'ютерів",
             "teacher": "доц. В. Пущак", "room": "С. 505"},
        ],
        "Wednesday": [
            {"pair": 4, "time": "13:50–15:10", "subject": "Самоменеджмент",
             "teacher": "доц. І. Саврас", "room": "Т.Б. 106", "elective": True},
            {"pair": 5, "time": "15:20–16:40", "subject": "Самоменеджмент",
             "teacher": "доц. І. Саврас", "room": "Т.Б. 106", "elective": True},
        ],
        "Thursday": [
            {"pair": 3, "time": "12:20–13:40", "subject": "Проектування інформаційних систем",
             "teacher": "проф. Г. Аніловська, ст. викл. М. Крутяк", "room": "М. 502"},
            {"pair": 4, "time": "13:50–15:10", "subject": "Проектування інформаційних систем",
             "teacher": "проф. Г. Аніловська, ст. викл. М. Крутяк", "room": "М. 502"},
        ],
        "Friday": [
            {"pair": 1, "time": "9:00–10:20", "subject": "Основи SMM",
             "teacher": "проф. Ю. Полякова", "room": "Т.Б. 212", "elective": True},
            {"pair": 2, "time": "10:30–11:50", "subject": "Основи SMM",
             "teacher": "проф. Ю. Полякова", "room": "Т.Б. 212", "elective": True},
            {"pair": 3, "time": "12:20–13:40", "subject": "Теорія прийняття рішень",
             "teacher": "доц. Р. Зацерковний, доц. Р. Олійник", "room": "М. 502"},
            {"pair": 4, "time": "13:50–15:10", "subject": "Теорія прийняття рішень",
             "teacher": "доц. Р. Зацерковний, доц. Р. Олійник", "room": "М. 502"},
            {"pair": 5, "time": "15:20–16:40", "subject": "Іспанська мова",
             "teacher": "доц. А. Степанов", "room": "М. 509", "elective": True},
            {"pair": 6, "time": "16:50–18:10", "subject": "Іспанська мова",
             "teacher": "доц. А. Степанов", "room": "М. 509", "elective": True},
        ],
    },
}


def get_day_schedule(group: str, day: str) -> list[dict]:
    if get_week() == "Лекційний тиждень":
        return LECTURES["Global"].get(day, [])
    return PRACTICE.get(group, {}).get(day, [])


def format_schedule(group: str, day: str) -> str:
    pairs = get_day_schedule(group, day)
    header = f"📅 {DAYS_UA.get(day, day)} — {group}\n🗓 {get_week()}\n"

    if not pairs:
        return header + "\nСьогодні занять немає 🎉"

    lines = [header]
    for p in sorted(pairs, key=lambda x: x["pair"]):
        mark = " В*" if p.get("elective") else ""
        lines.append(
            f"\n{p['pair']}️⃣ {p['time']}{mark}\n"
            f"   📖 {p['subject']}\n"
            f"   👤 {p['teacher']}\n"
            f"   🏫 {p['room']}"
        )
    if any(p.get("elective") for p in pairs):
        lines.append("\n\nВ* — вільний вибір здобувача")
    return "".join(lines)


def format_bells(course_key: str) -> str:
    data = BELLS[course_key]
    digits = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣"]
    lines = [f"🔔 Розклад дзвінків\n({data['title']})\n"]

    pairs = data["pairs"]
    for i, (start, end) in enumerate(pairs):
        lines.append(f"\n{digits[i]} Пара {i + 1}:  {start} — {end}")
        if i < len(pairs) - 1:
            next_start = pairs[i + 1][0]
            gap = _gap_minutes(end, next_start)
            lines.append(f"\n      ☕ перерва {gap} хв")
    return "".join(lines)


def _gap_minutes(end: str, next_start: str) -> int:
    fmt = "%H:%M"
    return int((datetime.strptime(next_start, fmt) - datetime.strptime(end, fmt)).total_seconds() // 60)


def main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📘 Розклад КН-351", callback_data="grp:КН-351")],
        [InlineKeyboardButton("📗 Розклад КН-352", callback_data="grp:КН-352")],
        [InlineKeyboardButton("🗓 Який зараз тиждень?", callback_data="week")],
        [InlineKeyboardButton("⏰ Розклад дзвінків", callback_data="bells")],
    ])


def bells_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎓 Бакалавр, 2–3 курс", callback_data="bell:bach23")],
        [InlineKeyboardButton("🎓 Бакалавр, 1 та 4 курс", callback_data="bell:bach14")],
        [InlineKeyboardButton("🎓 Магістр", callback_data="bell:master")],
        [InlineKeyboardButton("⬅️ Назад", callback_data="menu")],
    ])


def back_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔁 Обрати інший курс", callback_data="bells")],
        [InlineKeyboardButton("🏠 Головне меню", callback_data="menu")],
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Вибери дію:", reply_markup=main_menu())


async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "menu":
        await query.message.reply_text("Вибери дію:", reply_markup=main_menu())

    elif data.startswith("grp:"):
        group = data.split(":", 1)[1]
        await query.message.reply_text(
            format_schedule(group, current_day()),
            reply_markup=main_menu(),
        )

    elif data == "week":
        await query.message.reply_text(
            f"Теперішній тиждень: *{get_week()}*",
            parse_mode="Markdown",
            reply_markup=main_menu(),
        )

    elif data == "bells":
        await query.message.reply_text(
            "Оберіть курс для розкладу дзвінків:",
            reply_markup=bells_menu(),
        )

    elif data.startswith("bell:"):
        course_key = data.split(":", 1)[1]
        if course_key in BELLS:
            await query.message.reply_text(
                format_bells(course_key),
                reply_markup=back_menu(),
            )
        else:
            await query.message.reply_text("Курс не знайдено", reply_markup=bells_menu())

    else:
        await query.message.reply_text("Невідома кнопка", reply_markup=main_menu())


if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click))
    app.run_polling()
