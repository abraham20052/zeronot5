import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, LabeledPrice, PreCheckoutQuery
import json

# التوكن الشغال بتاعك
API_TOKEN = '6629310927:AAG0Y3Kvl73ktW9muFslhSHTme0rTCz9O4w'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    
    # رابط الـ GitHub Pages الملكي الشغال بتاعك
    web_app_url = "https://abraham20052.github.io/zeronot5/"
    
    web_app = WebAppInfo(url=web_app_url)
    button = InlineKeyboardButton(text="🎰 دخول كازينو النجوم", web_app=web_app)
    markup.add(button)
    
    bot.send_message(
        message.chat.id, 
        "مرحباً بك في كازينو النجوم! 🌟\nاضغط على الزر بالأسفل لفتح الواجهة الملكية مباشرة:", 
        reply_markup=markup
    )

# استقبال البيانات من الواجهة عند الضغط على الألعاب أو الشحن
@bot.message_handler(content_types=['web_app_data'])
def handle_web_app_data(message):
    try:
        data = json.loads(message.web_app_data.data)
        action = data.get("action")
        
        # 1- شحن النجوم
        if action == "deposit":
            prices = [LabeledPrice(label="شحن 50 نجمة", amount=50)]
            bot.send_invoice(
                chat_id=message.chat.id,
                title="🎯 شحن رصيد كازينو النجوم",
                description="شحن نجوم تليجرام للاستخدام داخل الكازينو",
                provider_token="",  # فارغ لأنها نجوم تليجرام XTR
                currency="XTR",
                prices=prices,
                invoice_payload="casino_payload"
            )
            
        # 2- الضغط على الألعاب
        elif action == "play_game":
            game = data.get("game")
            if game == "lucky_wheel":
                bot.send_message(message.chat.id, "🎡 لقد اخترت لعبة **عجلة الحظ**!\nجاري تجهيز السحب الملكي الخاص بك... اكتب المبلغ المراد المراهنة به.")
            elif game == "dice_pvp":
                bot.send_message(message.chat.id, "🎲 لقد اخترت **تحدي النرد PvP**!\nجاري البحث عن خصم متصل الآن لمنافسته...")
            elif game == "slot_machine":
                bot.send_message(message.chat.id, "🎰 لقد دخلت صالة **الـ Slot الملكي**!\nاسحب الذراع الآن لتجربة حظك.")
            elif game == "coin_flip_pvp":
                bot.send_message(message.chat.id, "🪙 لقد اخترت **ملك أو كتابة PvP**!\nاختر وجه العملة لبدء التحدي ضد لاعب آخر.")

    except Exception as e:
        print(f"Error handling web_app_data: {e}")

# تأكيد عملية الدفع قبل الخصم
@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query: PreCheckoutQuery):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

# رسالة نجاح الدفع بعد تحويل النجوم
@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    bot.send_message(message.chat.id, "🎉 تم الشحن بنجاح! تم إضافة 50 نجمة إلى رصيدك في الكازينو.")

if __name__ == '__main__':
    print("🚀 البوت جاهز ويعمل بنظام الـ Polling...")
    bot.remove_webhook()
    bot.polling(none_stop=True)
