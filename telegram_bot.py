from telethon import TelegramClient, events
import asyncio
import os
import re
import requests

# اطلاعات حساب تلگرام از طریق متغیرهای محیطی (برای امنیت بیشتر)
api_id = int(os.getenv("API_ID", "6590627"))  # API ID
api_hash = os.getenv("API_HASH", "f817aeb5cc76ccb664f7df6a49e6fa9a")  # API Hash
telegram_session = os.getenv("TELEGRAM_SESSION", "session_name")  # نام یا مسیر فایل جلسه

# شناسه کانال/گروه مبدا و مقصد
source_channel = os.getenv("SOURCE_CHANNEL", "MsgCod")  # گروه مبدا
destination_channel = os.getenv("DESTINATION_CHANNEL", "PubgRules")  # گروه مقصد

# لینک‌های مجاز
allowed_links = [
    "https://example.com",
    "https://another-allowed-link.com"
]

# آیدی‌های مجاز
allowed_usernames = [
    "@Reall", "@Tapjpiti"
]

# لیست کلمات فیلتر شده
filtered_words = [
    "📄 توضیحات فروشنده:", "💵 قیمت:", "هزار تومان", "👨‍💻جهت خرید با آیدی",
    "در ارتباط باشید‌👨‍💻", "👨‍💻جهت خرید با آیدی در ارتباط باشید‌👨‍💻", "آیدی واسطه",
    "آیدی واسطه :", "واسطه", "واسطه:", "ایدی", "آیدی:", "ایدی:", "ایدی :", "آیدی ",
    "قیمت", "قیمت:", "قیمت ‌:", "واسطه", "واسطه:", "واسطه  :", 
    "UiD", "UID", "UiD:", "UiD :", "UID:", "UID :", "🔸 دارای بتل پس فصل های:",
    "🔹 بتل پس مکس فصل های:", "🔸ریجن:", "🔹 لینک شده بر روی:", "🔸 لول اکانت:",
    "🔹 بالاترین رنک مولتی:", "🔸 بالا ترین رنک بتل:", "🔹 مقدار C اکانت:", "بتل",
    "یو ایدی", "یو آیدی", "ایدی فروشنده", "فروشنده", "حاج سعید", "سعید", "حاج", 
    "میلیون", "فروشنده","[buy legal CP with the cheapest and 6 trust symbols]",
    "خرید سی پی قانونی با ارزان ترین قیمت و ۶ نماد اعتماد",
    "یادم", "نیست", "یادم نیست"  # کلمات جدید اضافه شدند
]

# اضافه کردن جمله‌ای که با "خرید" شروع و با "اعتماد" تمام می‌شود
filtered_phrases = [
    r"خرید.*اعتماد$"
]

# راه‌اندازی تلگرام کلاینت
client = TelegramClient(telegram_session, api_id, api_hash)

# تابع ترجمه با استفاده از API غیررسمی Google Translate
def translate_to_english(text):
    try:
        response = requests.post("https://translate.googleapis.com/translate_a/single", params={
            "client": "gtx",
            "sl": "fa",
            "tl": "en",
            "dt": "t",
            "q": text
        })
        if response.status_code == 200:
            translated_text = ''.join([item[0] for item in response.json()[0]])
            return translated_text
        else:
            print(f"خطا در ترجمه: {response.status_code}")
            return text
    except Exception as e:
        print(f"❌ خطا در ترجمه متن: {e}")
        return text

# تابع اصلی
async def main():
    try:
        await client.start()
        print("✅ ربات با موفقیت متصل شد!")

        # دریافت پیام‌ها از کانال مبدا
        @client.on(events.NewMessage(chats=source_channel))
        async def handler(event):
            try:
                message = event.message
                if message.media:
                    media = message.media
                    caption = message.text or ""

                    # حذف لینک‌های غیرمجاز
                    caption = re.sub(r"http\S+", lambda match: match.group(0) if match.group(0) in allowed_links else "", caption)

                    # حذف آیدی‌ها به جز آیدی‌های مجاز
                    caption = re.sub(r"@\w+", lambda match: match.group(0) if match.group(0) in allowed_usernames else "", caption)

                    # فیلتر کردن کلمات
                    for word in filtered_words:
                        caption = caption.replace(word, "")

                    # فیلتر کردن جملات مشخص‌شده با regex
                    for phrase in filtered_phrases:
                        caption = re.sub(phrase, "", caption)

                    # ترجمه متن به انگلیسی
                    translated_caption = translate_to_english(caption)

                    # بررسی کلمات برای synced on:
                    sync_keywords = ["Facebook", "Activision", "line", "google", "فیسبوک", "اکتیویژن", "لاین", "گوگل"]
                    
                    # ترجمه کلمات فارسی به انگلیسی
                    translated_sync_items = [
                        translate_to_english(keyword) if re.search(r'[آ-ی]', keyword) else keyword
                        for keyword in sync_keywords if keyword.lower() in caption.lower()
                    ]

                    # ساختن عبارت synced on:
                    synced_on_field = f"🔗 | Synced on: {', '.join(translated_sync_items)}" if translated_sync_items else "🔗 | Synced on:"

                    # ساخت کپشن جدید با فرمت نهایی
                    final_caption = (
                        "🔻 Has a barcode to prevent abuse & fraud\n"
                        "\n"
                        "#account_number\n"
                        "\n"
                        "Status🟢\n"
                        "\n"
                        f"{synced_on_field}\n"
                        "\n"
                        "✅| Description:\n"
                        "\n"
                        f"{translated_caption}\n"
                        "\n"
                        "#COD #CODBUY #CODSELL #CALLOFDUTY #CALL_OF_DUTY #ACCOUNTCOD\n"
                        "\n\n"
                        "COD BUY SELL\n\n"
                        "💰| Account Price:\n\n"
                        "Mediator @Reall💳\n\n"
                        "Payment by invoice or digital currency 😀"
                    )

                    # حذف فاصله‌های اضافی (بدون تغییر فاصله‌های دوتایی)
                    final_caption = '\n\n'.join([line for line in final_caption.split('\n\n') if line.strip()])

                    # بررسی طول کپشن
                    if len(final_caption) > 1024:  # اگر کپشن طولانی بود
                        # ارسال رسانه بدون کپشن
                        await client.send_file(
                            destination_channel,
                            media
                        )
                        print("⚠️ کپشن طولانی بود. رسانه بدون کپشن ارسال شد.")
                        
                        # ارسال کپشن در پیام جداگانه
                        await client.send_message(
                            destination_channel,
                            final_caption
                        )
                        print("✅ کپشن جداگانه ارسال شد.")
                    else:  # اگر کپشن نرمال بود
                        # ارسال رسانه همراه با کپشن
                        await client.send_file(
                            destination_channel,
                            media,
                            caption=final_caption
                        )
                        print("✅ رسانه همراه با کپشن ارسال شد.")
                else:
                    print("⚠️ پیام بدون رسانه دریافت شد و ارسال نشد.")
            except Exception as e:
                print(f"❌ خطا در پردازش پیام: {e}")

        # اجرای ربات
        await client.run_until_disconnected()
    except Exception as e:
        print(f"❌ خطا در اتصال: {e}")

if __name__ == "__main__":
    asyncio.run(main())
                    
