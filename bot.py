from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import TOKEN
 
bot = TeleBot(TOKEN)
CHANNELS = ['@qsanerkus', '@vgr060', '@wrredniie']
 
CHANNEL_LINKS = {
    "match_tv": "https://t.me/VGR060Bot/matchtv",
    "match_football1": "https://t.me/VGR060Bot/football1",
    "match_football2": "https://t.me/VGR060Bot/football2",
    "match_football3": "https://t.me/VGR060Bot/football3",
    "match_fighter": "https://t.me/VGR060Bot/mboyets",
    "fast_sports": "https://t.me/VGR060Bot/fastlive",
    "fast_sports1": "https://t.me/VGR060Bot/fasttv1",
    "fast_sports2": "https://t.me/VGR060Bot/fastlive2",
    "setanta1": "https://t.me/VGR060Bot/set1anta",
    "setanta2": "https://t.me/VGR060Bot/2setanta"
}
 
CHANNEL_NAMES = {
    "match_tv": "Матч! ТВ",
    "match_football1": "Матч! Футбол 1",
    "match_football2": "Матч! Футбол 2",
    "match_football3": "Матч! Футбол 3",
    "match_fighter": "Матч! Боец",
    "fast_sports": "Fast Sports 🇦🇲",
    "fast_sports1": "Fast Sports 1 🇦🇲",
    "fast_sports2": "Fast Sports 2 🇦🇲",
    "setanta1": "Setanta Sports 1",
    "setanta2": "Setanta Sports 2"
}
 
def check_subs(user_id):
    for channel in CHANNELS:
        try:
            member = bot.get_chat_member(channel, user_id)
            if member.status in ['left', 'kicked']:
                return False
        except:
            return False
    return True
 
def show_subscription_required(chat_id, channel_type=None, message_id=None):
    channel_name = CHANNEL_NAMES.get(channel_type, "трансляцию") if channel_type else "трансляцию"
   
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("1️⃣", url="https://t.me/qsanerkus"))
    keyboard.add(InlineKeyboardButton("2️⃣", url="https://t.me/vgr060"))
    keyboard.add(InlineKeyboardButton("3️⃣", url="https://t.me/wrredniie"))
    keyboard.add(InlineKeyboardButton("✅ ՍՏՈւԳԵԼ ✅", callback_data=f"check_{channel_type}" if channel_type else "check_subs"))
   
    text = f"📢 {channel_name} հասանելիություն ստանալու համար անհրաժեշտ է բաժանորդագրվել մեր ալիքներին:"
   
    if message_id:
        bot.edit_message_text(
            text,
            chat_id,
            message_id,
            reply_markup=keyboard
        )
    else:
        bot.send_message(
            chat_id,
            text,
            reply_markup=keyboard
        )
 
def show_live_channels(message):
    keyboard = InlineKeyboardMarkup(row_width=2)
   
    keyboard.add(
        InlineKeyboardButton("Матч! ТВ", callback_data="match_tv"),
        InlineKeyboardButton("Матч! Футбол 1", callback_data="match_football1"),
        InlineKeyboardButton("Матч! Футбол 2", callback_data="match_football2"),
        InlineKeyboardButton("Матч! Футбол 3", callback_data="match_football3"))
   
    keyboard.add(InlineKeyboardButton("Матч! Боец", callback_data="match_fighter"))
   
    keyboard.add(InlineKeyboardButton("Fast Sports 🇦🇲", callback_data="fast_sports"),
        InlineKeyboardButton("Fast Sports 1 🇦🇲", callback_data="fast_sports1"))
   
    keyboard.add(InlineKeyboardButton("Fast Sports 2 🇦🇲", callback_data="fast_sports2"))
   
    keyboard.add(
        InlineKeyboardButton("Setanta Sports 1", callback_data="setanta1"),
        InlineKeyboardButton("Setanta Sports 2", callback_data="setanta2"))
   
    keyboard.add(InlineKeyboardButton("🎰 Խաղադրույք Կատարել 🎰", url="https://lkzq.cc/65ea"))
 
    bot.send_message(
        message.chat.id,
        text=f"""
        Բարի գալուստ 👋
Ուղիղ եթեր դիտելու համար ընտրեք ալիքը⬇️
        """,
        reply_markup=keyboard,
        parse_mode='HTML'
    )
 
@bot.message_handler(commands=['live'])
def live(message):
 
    show_live_channels(message)
 
@bot.callback_query_handler(func=lambda call: call.data.startswith(('match_', 'fast_', 'setanta')))
def handle_channel_selection(call):
 
    channel_type = call.data
 
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
   
    show_subscription_required(call.message.chat.id, channel_type)
 
@bot.callback_query_handler(func=lambda call: call.data.startswith('check_'))
def check_subs_callback(call):
    if call.data.startswith('check_'):
        channel_type = call.data.replace('check_', '')
        if channel_type == "subs":
            channel_type = None
    else:
        channel_type = None
   
    if check_subs(call.from_user.id):
 
        if channel_type and channel_type in CHANNEL_LINKS:
            channel_link = CHANNEL_LINKS[channel_type]
            channel_name = CHANNEL_NAMES.get(channel_type, "Трансляция")
           
   
            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton(
                f"▶️ Открыть {channel_name}",
                url=channel_link  
            ))
            keyboard.add(InlineKeyboardButton("📺 Ընտրել մեկ այլ ալիք", callback_data="back_to_list"))
           
 
            bot.edit_message_text(
                f"✅ Բաժանորդագրությունը հաստատված է\n🎬 Ուղիղ եթերի հղումը ստորև է\n👇\nՍեղմեք կոճակը՝ դիտումը սկսելու համար",
                call.message.chat.id,
                call.message.message_id,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
           
 
            try:
                bot.answer_callback_query(
                    call.id,
                    f"✅ Подписка подтверждена! Открываем {channel_name}..."
                )
            except:
                pass
           
        else:
 
            bot.edit_message_text(
                f"✅ {call.from_user.first_name}, вы подписаны на все каналы!",
                call.message.chat.id,
                call.message.message_id
            )
    else:
        bot.answer_callback_query(call.id, "❌ Դուք դեռևս բաժանորդագրված չեք բոլոր ալիքներին! ❌", show_alert=True)
 
        channel_name = CHANNEL_NAMES.get(channel_type, "трансляцию") if channel_type else "трансляцию"
       
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("1️⃣", url="https://t.me/qsanerkus"))
        keyboard.add(InlineKeyboardButton("2️⃣", url="https://t.me/vgr060"))
        keyboard.add(InlineKeyboardButton("3️⃣", url="https://t.me/wrredniie"))
        keyboard.add(InlineKeyboardButton("✅ ՍՏՈւԳԵԼ ✅", callback_data=f"check_{channel_type}" if channel_type else "check_subs"))
       
        bot.edit_message_text(
            f"❌ Դուք դեռ չեք բաժանորդագրվել բոլոր ալիքներին!\n📢 {channel_name}-ին հասանելիություն ստանալու համար անհրաժեշտ է բաժանորդագրվել:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=keyboard
        )
 
@bot.callback_query_handler(func=lambda call: call.data == "back_to_list")
def back_to_list(call):
    """Возврат к списку каналов"""
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
 
    show_live_channels(call.message)
 

@bot.callback_query_handler(func=lambda call: call.data == "check_subs")
def check_subs_general(call):
    """Общая проверка подписки (без указания канала)"""
    if check_subs(call.from_user.id):
        bot.edit_message_text(
            f"✅ {call.from_user.first_name}, вы подписаны на все каналы!",
            call.message.chat.id,
            call.message.message_id
        )
    else:
        bot.answer_callback_query(call.id, "❌ Դուք դեռևս բաժանորդագրված չեք բոլոր ալիքներին! ❌", show_alert=True)
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("Канал 1", url="https://t.me/qsanerkus"))
        keyboard.add(InlineKeyboardButton("Канал 2", url="https://t.me/vgr060"))
        keyboard.add(InlineKeyboardButton("Канал 3", url="https://t.me/wrredniie"))
        keyboard.add(InlineKeyboardButton("✅ Проверить подписку", callback_data="check_subs"))
       
        bot.edit_message_text(
            "❌ Դուք դեռ չեք բաժանորդագրվել բոլոր ալիքներին!\n📢 {channel_name}-ին հասանելիություն ստանալու համար անհրաժեշտ է բաժանորդագրվել:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=keyboard
        )
 
@bot.message_handler(commands=['start'])
def start(message):
    user_name = message.from_user.first_name or "игрок"
   
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text="🎰 ՍՏԱՆԱԼ🎰", url="https://lkzq.cc/65ea")
    button2 = InlineKeyboardButton(text="💸 ԲՈՆՈւՍ 💸", url="https://t.me/+NQ1o4RUEEUU5ZWEy")
    keyboard.add(button)
    keyboard.add(button2)
   
 
    bot.send_message(message.chat.id,
        text=f"""<b>🎰 Բարի գալուստ {user_name}
 
Պատրա՞ստ ես փորձել քո բախտը և բացել մեծ շահումների դուռը 💰</b>
 
<b>🎁 Քեզ սպասում է՝</b>
🔥 50 FREE SPINS
🔥 500% բոնուս առաջին դեպոզիտի վրա
 
✅ Առանց անձնագրի
✅ Առանց հաստատման
✅ Միայն նոր օգտվողների համար
 
<b>⚠️ ՇԱՏ ԿԱՐԵՎՈՐ</b>
Բոնուսը և հաղթելու հնարավորությունը ակտիվանում են
միայն եթե օգտագործես պրոմոկոդը 👇
 
🎯 ՊՐՈՄՈԿՈԴ՝<code> VGR060</code>""",
        reply_markup=keyboard,
        parse_mode='HTML')
 
if __name__ == '__main__':
    print("✅ Бот запущен!")
    bot.polling(none_stop=True)


TOKEN = '8300645219:AAEqm5VpwLYRL1pC8ATCOUuTFUOO16AC
