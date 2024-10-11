import asyncio
from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton

# Developer Haider, mention your rights, oh goat
bot_token = input("أدخل توكن البوت: ")
user_id = int(input("أدخل ID المستخدم: "))

app = Client("auto_poster_bot", bot_token=bot_token)

user_settings = {user_id: {"phone": None, "interval": 60, "message": "هذا هو المنشور التلقائي"}}

@app.on_message(filters.private & filters.command("start"))
async def start(client, message):
    buttons = [
        [KeyboardButton("تسجيل رقم الهاتف")],
        [KeyboardButton("تعيين فترة النشر")],
        [KeyboardButton("تعيين كليشة النشر")]
    ]
    
   # by Haider
    await message.reply(
        "مرحباً! لاستخدام هذا البوت، يرجى تسجيل رقم الهاتف وتعيين الإعدادات المطلوبة.",
        reply_markup=ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize_keyboard=True)
    )

@app.on_message(filters.private & filters.text)
async def handle_input(client, message):
    text = message.text
    
    if text == "تسجيل رقم الهاتف":
        await message.reply("من فضلك أرسل رقم الهاتف:")
    elif text == "تعيين فترة النشر":
        await message.reply("أدخل الفترة الزمنية بين المنشورات بالثواني:")
    elif text == "تعيين كليشة النشر":
        await message.reply("أدخل الكليشة التي ترغب في نشرها:")
    elif user_settings[user_id]["phone"] is None:
        user_settings[user_id]["phone"] = text
        await message.reply("تم تسجيل رقم الهاتف بنجاح!")
    elif user_settings[user_id]["interval"] == 60:
        try:
            user_settings[user_id]["interval"] = int(text)
            await message.reply(f"تم تعيين فترة النشر إلى {user_settings[user_id]['interval']} ثانية.")
        except ValueError:
            await message.reply("الرجاء إدخال رقم صحيح.")
    else:
        user_settings[user_id]["message"] = text
        await message.reply("تم تعيين الكليشة بنجاح!")

async def auto_publish():
    while True:
        try:
            await app.send_message(user_id, user_settings[user_id]["message"])
            await asyncio.sleep(user_settings[user_id]["interval"])
        except Exception as e:
            print(f"فشل في النشر للمستخدم {user_id}: {e}")
        await asyncio.sleep(60) 

if __name__ == "__main__":
    app.start()
    loop = asyncio.get_event_loop()
    loop.create_task(auto_publish())
    app.idle()
