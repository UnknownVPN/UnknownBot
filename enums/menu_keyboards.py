from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from utilities.config_handler import *
from enums.prices import prices

cohandler = ConfigHandler()

ADMIN_HELLO_TEXT = """
سلام {} 🖐 
"""


BOT_SETTING = (
    """
💲 وضعیت خرید : {}
📢 کانال اسپانسر : {}
🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
    + """
"""
)
SEND_SPONSOR_CHANEL = """ایدی کانال اسپانسر را ارسال کنید
⚠️ توجه داشته باید که برای بررسی عضویت ربات باید در کانال ارسال شده حضور داشته باشد
"""
ADMIN_MAIN_MENU = ReplyKeyboardMarkup(
    [["📊 آمار ربات"], ["⚙️ تنظیمات"], ["📣 ارسال اعلان"]], resize_keyboard=True
)


SETTING_SETUP_BUTTON = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("وضعیت خرید", "change_buy_status")],
        [InlineKeyboardButton("کانال اسپانسر", "change_sponsor")],
    ]
)


HELLO_BEFORE_JOIN_TEXT = """سلام {} 🖐

🌿جهت استفاده از خدمات ربات، ابتدا در کانال ما عضو شوید

سپس روی دکمه ی "♻️ شروع دوباره ♻️" کلیک کنید.

🆔 @{}"""


SEND_PM_TEXT = """
لطفا پیام خود را ارسال کنید
"""


CONFIRM_SEND_PM = """
پیام ارسال شود؟
"""


BUTTON_BEFORE_JOIN = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text=cohandler.getconfig["bot"]["custom_name_fa"],
                url=f"https://t.me/{cohandler.getconfig['bot']['sponsor_channel']}",
            )
        ],
        [
            InlineKeyboardButton(
                text="♻️ شروع دوباره ♻️",
                url=f"https://t.me/{cohandler.getconfig['bot']['sponsor_bot']}?start=start",
            )
        ]
    ]
)

HELLO_TEXT = (
    f"""🐉 سلام به <a href="https://t.me/{cohandler.getconfig['bot']['sponsor_channel'].replace('https://t.me/','')}">ربات """+cohandler.getconfig["bot"]["custom_name_fa"]+"""</a> خوش آمدید 👋

📌 جهت استفاده از ربات لطفا یکی از موارد زیر را انتخاب کنید


🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

HELLO_BUTTONS = ReplyKeyboardMarkup(
    [
        [KeyboardButton(text="🐉 سرویس ها"), KeyboardButton(text="💸 خرید سرویس")],
        [KeyboardButton(text="🎺 تعرفه ها"), KeyboardButton(text="♾ حجم اضافه")],
        [KeyboardButton(text="📞 پشتیبانی"), KeyboardButton(text="💰 کیف پول")],
        [
            KeyboardButton(text="🏆 کسب درآمد"),
            KeyboardButton(text="💸 انتقال موجودی"),
            KeyboardButton(text="📧 ثبت ایمیل"),
        ],
        [
            KeyboardButton(text="💡 سوالات متدوال"),
            KeyboardButton(text="🔗 راهنمای اتصال"),
        ],
    ],
    resize_keyboard=True,
)

HELLO_BUTTONS_JSONIFY = ReplyKeyboardMarkup(
    [
        [KeyboardButton(text="🐉 سرویس ها"), KeyboardButton(text="💸 خرید سرویس")],
        [KeyboardButton(text="🎺 تعرفه ها"), KeyboardButton(text="♾ حجم اضافه")],
        [KeyboardButton(text="📞 پشتیبانی"), KeyboardButton(text="💰 کیف پول")],
        [KeyboardButton(text="🏆 کسب درآمد"), KeyboardButton(text="📧 ثبت ایمیل")],
        [
            KeyboardButton(text="💡 سوالات متدوال"),
            KeyboardButton(text="🔗 راهنمای اتصال"),
        ],
    ],
    resize_keyboard=True,
)


SLOW_DOWN = """
اخطار: اسپم ربات لطفا بعدا دوباره تلاش کنید
"""


QUESTIONS_TEXT = """<b>💡 سوالات متداول هنگام استفاده از سرویس """+cohandler.getconfig["bot"]["custom_name_fa"]+"""</b>

📌 """+cohandler.getconfig["bot"]["custom_name_fa"]+""" آیپی ثابته؟ میتونم برای صرافی های ارز دیجیتال استفاده کنم؟
🔆 بله؛ با خیال راحت میتوانید از """+cohandler.getconfig["bot"]["custom_name_fa"]+""" استفاده کنید. به هیچ عنوان آی پی شما تغییر نخواهد کرد و تمامی سرور ها آیپی ثابت هستند.

📌 اگر سرور های """+cohandler.getconfig["bot"]["custom_name_fa"]+""" برای مدتی در وضعیت 《بروزرسانی》 قرار گیرند چه اتفاقی می افتد؟ 
🔆 مقدار مصرف شده از سرویس کاربران در زمان بروزرسانی بعد از اتمام آن به زمان تمدید کاربران اضافه خواهد شد.

📌 ترافیک هر سرویس چقدره؟
🔆 شما می توانید به میزان مصرف مورد نیاز خود ترافیک خریداری کنید

📌 اگه به یک سرویس بیشتر از حد مجاز متصل شویم چه اتفاقی می افتد؟
🔆 در صورت اتصال بیشتر از میزان مجاز کانکشن خریداری شده، سرویس شما برای 6 ساعت مسدود خواهد شد.

📌 """+cohandler.getconfig["bot"]["custom_name_fa"]+""" از چه نوع سرویسی استفاده می کند؟
🔆 """+cohandler.getconfig["bot"]["custom_name_fa"]+""" از Vmess/Vless استفاده می کند و شما می توانید مدیریت کامل بر روی سرویس خریداری شده خود داشته باشید.

📌 """+cohandler.getconfig["bot"]["custom_name_fa"]+""" از چه کشور هایی سرویس ارائه می دهد؟
🔆 ما کشور هایی که کاربران درخواست می کنند را در کوتاه ترین زمان ممکن به لیست سرور ها اضافه می کنیم. برای درخواست سرور در کشور مورد نظر با پشتیبانی در ارتباط باشید.


📌 چطور باید از """+cohandler.getconfig["bot"]["custom_name_fa"]+""" استفاده کنم؟
🔆 شما میتوانید از برنامه های V2rayNG - V2rayN - Matsuri - Nekoray برنامه هایی که از لینک vmess/vless پشتیبانی می کنند استفاده کنید و همچنین می توانید آموزش های اتصال و برنامه های مورد نیاز را در کانال تلگرامی ما دنبال کنید.

📌 """+cohandler.getconfig["bot"]["custom_name_fa"]+""" سرعت اینترنت را بالا می برد؟
🔆 سرویس ما همه اپراتور ها را برای افزایش سرعت پشتیبانی نمی کند ولی بصورت کلی برای بعضی از اپراتور ها باعث افزایش سرعت می شود.

📌 آیا از """+cohandler.getconfig["bot"]["custom_name_fa"]+""" برای بازی های آنلاین هم می شود استفاده کرد؟
🔆 بله؛ تیم ما در تلاش است که همه بازی هارا برای سرویس بهینه سازی کند ولی تضمین برای کارکرد قطعی نمی شود.

📌 کدام لوکیشن ها سرعت و پینگ بهتری دارد؟
🔆 کشور هایی که در همسایگی ایران هستند نسبت به بقیه کشور ها پینگ و سرعت بهتری دارند و شما میتوانید از کانال تلگرامی نتیجه تست سرعت لوکیشن های مختلف را مشاهده نمائید.

📌 اگر اکانت تلگرامم دیلیت بشه چطور میتونم به سرویس هایم دسترسی داشته باشم؟
🔆 باید از قبل دیلیت کردن اکانت خود با پشتیبانی تماس بگیرید و درخواست انتقال سرویس های خود به اکانت دیگر را بدهید درغیر این صورت راهی برای دسترسی به سرویس هایتان نخواهد بود.

✅ در صورتی که جواب سوالات خود را پیدا نکردید می توانید به (پشتیبانی ربات) مراجعه نمائید."""

QUESTIONS_BUTTONS = InlineKeyboardMarkup(
    [
        # [InlineKeyboardButton(text="🛠 مشکلات متداول 🛠",callback_data="problems_text")],
        [
            InlineKeyboardButton(
                text="🔗 راهنمای اتصال به سرویس 🔗", callback_data="how_connect"
            )
        ]
    ]
)

PROBLEMS_TEXT = """⚒ مشکلات متداول کاربران

📌 سرویس با اینترنت دیگه وصل میشه ولی با مودم وصل نمیشه چکار کنم؟
🔆 برخی از ISP ها با سرویس cloudflare اختلال دارند به همین دلیل امکان اتصال با لینک داخل ربات نیست شما میتوانید با ارتباط با پشتیبانی لینک مخصوص دریافت کنید

📌 لینک نیم بها متصل نمیشه ولی مستقیم متصل میشه مشکل چیه؟
🔆 در بعضی از مواقع پورت ها در برنامه هایی مثل اوتلاین دچار اختلال میشوند و امکان اتصال نیست برای رفع این مشکل کافی است یک بار تغییر لوکیشن و سپس تغییر لینک اتصال بدید تا مشکل شما حل بشه

📌 سرویس پینگ بالایی داخل بازی میده مشکل چی هست؟
🔆 لوکیشن های ترکیه برای گیم هستند و بقیه لوکیشن ها برای دانلود در صورتی که از لوکیشن های دیگه برای گیم استفاده میکنید پینگ بالایی دریافت میکنید، لینک مستقیم مناسب افرادی هست که کیفیت اینترنت خوبی دارند ولی بصورت کلی پیشنهاد ما لینک نیم بها هست چون پینگ و پکت بهتری نسبت به لینک مستقیم ارائه میده

📌 به سرویس که متصل میشم نیم بها حساب نمیکنه چکار کنم؟
🔆 در صورت مشکل میتوانید با پشتیبانی در ارتباط باشید و در صورت پشتیبانی نشدن اپراتور شما میتوانید از بقیه قابلیت ها مثل کاهش پینگ و رفع تحریم و.... استفاده کنید

📌 زمانی که به سرویس متصل میشم هم نیم بها حساب میشه هم تمام بها مشکل از چی هست؟
🔆 برخی از ISP ها پروتکل UDP رو نیم بها حساب نمیکنن و برنامه هایی مثل اینستاگرام از حالت UDP برای اتصال استفاده میکنند، شما میتوانید از بخش سرویس ها اقدام به غیرفعال سازی حالت udp بکنید

📌 از لینک نیم بها استفاده میکنم ولی مشکل پینگ از بین نرفته چکار کنم؟
🔆 اگر با اندروید یا IOS از سرویس استفاده میکنید پیشنهاد ما برای اندروید برنامه رسمی شادوساکس و برای IOS برنامه Outline هست و اگر با PC هستید و از SSTAP استفاده میکنید این برنامه مصرف cpu بالایی داره و مناسب سیستم های ضعیف نیست در این شرایط برنامه Outline مناسب هست، اگر همچنان این مشکل وجود داره با استفاده از سایت speedtest از پینگ مناسب داخلی بدون اتصال به سرویس اطمینان یابید و در صورت مشکل با پشتیبانی در ارتباط باشید

📌 بسته داخلی خرید کردم ولی سرویس متصل نمیشه راه حل چیه؟
🔆 برای بسته های داخلی فقط لینک نیم بها فعال هست و اگر از لینک مستقیم استفاده میکنید امکان اتصال به سرویس نیست و اگر همچنان مشکل وجود داشت با پشتیبانی در ارتباط باشید تا لینک اتصال با استفاده از آیپی براتون ارسال بشه

✅ در صورتی که مشکل شما رفع نشد می توانید به (پشتیبانی ربات) مراجعه نمائید"""

PROBLEMS_BUTTONS = InlineKeyboardMarkup(
    [[InlineKeyboardButton(text="🔙 برگشت", callback_data="back_to_questions")]]
)

HOWCONNECT_TEXT = (
    """📌 شما میتوانید برای راهنمای اتصال به سرویس کانال رسمی مارا دنبال کنید و همچنین از دکمه های زیر میتوانید برنامه های مورد نیاز هر سیستم عامل را دانلود کنید

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

HOWCONNECT_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("🤖 Android", "androidcon"),
            InlineKeyboardButton("📱 IOS", "ioscon"),
        ],
        [InlineKeyboardButton("🐧Linux", "linuxcon")],
        [
            InlineKeyboardButton("💻 Windows", "windowscon"),
            InlineKeyboardButton("🖥 Mac", "maccon"),
        ],
    ]
)

BUTTON_BACK_CONNECT = InlineKeyboardMarkup(
    [[InlineKeyboardButton("🔙 بازگشت", "back_how_connect")]]
)

ANDROID_TEXT = (
    """📱 برنامه هایی که با آن در سیستم عامل اندروید میتوانید به سرویس ما متصل شوید

📌 جهت اتصال به پروتکل های vmess/vlessمیتوانید از برنامه های زیر استفاده کنید

🔸 <a href="https://t.me/"""
    + cohandler.getconfig["bot"]["sponsor_channel"]
    + """">V2rayNg</a> - <a href="https://t.me/"""
    + cohandler.getconfig["bot"]["sponsor_channel"]
    + """">Clash</a>

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

WINDOWS_TEXT = (
    """💻 برنامه هایی که با آن در سیستم عامل ویندوز میتوانید به سرویس ما متصل شوید

📌 جهت اتصال به پروتکل های vmess/vless میتوانید از برنامه های زیر استفاده کنید


🔸 <a href="https://t.me/"""
    + cohandler.getconfig["bot"]["sponsor_channel"]
    + """">Clash Verge</a> - <a href="https://t.me/"""
    + cohandler.getconfig["bot"]["sponsor_channel"]
    + """">Netch</a>


🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

MAC_TEXT = (
    """📌 برنامه هایی که با آن در سیستم عامل مک میتوانید به سرویس ما متصل شوید 👇

📌 جهت اتصال به پروتکل های vmess/vless میتوانید از برنامه های زیر استفاده کنید


🔸 <a href="https://t.me/"""
    + cohandler.getconfig["bot"]["sponsor_channel"]
    + """">ShadowRocket</a> - <a href="https://t.me/"""
    + cohandler.getconfig["bot"]["sponsor_channel"]
    + """">Clash Verge</a> - <a href="https://t.me/"""
    + cohandler.getconfig["bot"]["sponsor_channel"]
    + """">OneClick</a>


🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

IOS_TEXT = (
    """📌 برنامه هایی که با آن در سیستم عامل IOS میتوانید به سرویس ما متصل شوید 👇

📌 جهت اتصال پروتکل Vmess/Vless میتوانید از برنامه های زیر استفاده کنید


🔹<a href="https://t.me/"""
    + cohandler.getconfig["bot"]["sponsor_channel"]
    + """">NapsternetV</a> - <a href="https://t.me/"""
    + cohandler.getconfig["bot"]["sponsor_channel"]
    + """">ShadowRocket</a>


🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

LINUX_TEXT = (
    """📌 برنامه هایی که با آن در سیستم عامل لینوکس میتوانید به سرویس ما متصل شوید 👇

📌 جهت اتصال به پروتکل های vmess و shadowsocks میتوانید از برنامه های زیر استفاده کنید
🔸 Clash Verge <a href="https://github.com/zzzgydi/clash-verge/releases/download/v1.0.5/clash-verge_1.0.5_amd64.AppImage">Download</a>

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

SUPPORT_TEXT = (
    """✅ نیاز به کمک دارید؟ پشتیبانی ما آماده پاسخگویی است!

🔗 برای ارتباط با تیم پشتیبانی، به آیدی زیر پیام دهید:
📌 @"""
    + cohandler.getconfig["bot"]["sponsor_admin"]
    + """

⚠️ قبل از ارسال پیام، لطفاً بخش [💡 سوالات متداول] را بررسی کنید تا سریع‌تر به پاسخ سوال خود برسید.

🔍 برای اخبار و اطلاعات بیشتر، به کانال ما بپیوندید:
🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_channel"]
)

REFERRAL_TEXT = (
    """🚀 اینترنتت رو دوبرابر کن 🚀

⚡️ ناشناس وی پی ان چیست؟ سرویسی هست که مصرف اینترنت خارجی شمارو داخلی و نیم بها میکنه، یعنی چی؟ یعنی اینکه به ازای یک گیگ مصرف اینترنت از شما 500 مگ کم میشه و همچنین تحریم و فیلتر های اعمال شده برای ایران با این سرویس دور زده میشه

📌 قابلیت های سرویس ما 👇

🔹 شبکه امن و سریع
🔸 کاهش پینگ و رفع تحریم ها
🔹 اتصال به سریع ترین سرور ها در سراسر دنیا
🔸 نیم بها شدن مصرف اینترنت
🔹 مناسب برای تماشا فیلم ، وبگردی ، بازی های انلاین و....
🔸 ایپی ثابت برای تریدر ها
🔹 مسدود سازی تبلیغات و لینک های مخرب
🔸 پشتیبانی سریع و 24/7
🔹 دارای سرور های مختلف از سراسر جهان

💎 جهت خرید میتوانید به ربات ما مراجعه کنید 👇

🆔 <a href="{}">@"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
    + """</a>"""
)

REFFERAL_HINT = (
    """به اشتراک گذاشتن این بنر و هر خریدی که از لینک شما انجام شود، به شما امکان کسب 50% سهم از فروش به صورت اعتبار رایگان را می‌دهد. 😁


اگر با دعوت دوستانتان موجودی کیف پولتان به بیش از 300,000 تومان برسد، قادر به برداشت نقدی و واریز مستقیم به حساب بانکی‌تان خواهید بود – فرآیند کاملاً اتوماتیک!

📌 استفاده از اعتبار
اعتبار کسب شده را می‌توانید برای خرید یا تمدید سرویس‌های ما استفاده کنید.

⚠️ توجه
لطفاً در متن بنر تغییری ایجاد نکنید. لینک زیرمجموعه‌گیری به صورت اینلاین در بنر آمده است. فقط از لینک زیر استفاده نمایید: 👇

🔗 https://t.me/{}?start={}

🤝 افراد عضو شده: {} نفر
💳 خرید انجام شده: {} خرید
💎 جمع مبلغ هدیه: {} تومان

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

REQUEST_PHONE_TEXT = (
    """📌 کاربر گرامی برای استفاده از ربات باید حساب کاربری خود را تایید کنید

🐉 به این مظور باید شماره خود را توسط دکمه زیر با ما به اشتراک بگذارید

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

REQUEST_PHONE_BUTTONS = ReplyKeyboardMarkup(
    [[KeyboardButton("📱 ارسال شماره", request_contact=True)]], resize_keyboard=True
)

VERIFIED_PHONE_NUMBER_TEXT = (
    """✅ شماره شما با موفقیت تایید شد

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

INVALID_PHONE_NUMBER_TEXT = (
    """❌ شماره ارسالی باید برای ایران باشد

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

ERROR_PHONE_NUMBER_TEXT = (
    """❌ لطفا از دکمه زیر برای ارسال شماره استفاده کنید

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

PRICE_PRODUCTS_TEXT = (
    f"""📣 تعرفه‌های سرویس‌های """
    + cohandler.getconfig["bot"]["custom_name"]
    + f""" 🚀

<b>⏰ سرویس های یک ماهه</b>

🔸 {prices.str_conf[0][2]} کاربره: {prices.str_conf[0][0]["size"]} گیگ | {prices.str_conf[0][0]["price"]} تومان
🔹 {prices.str_conf[0][2]} کاربره: {prices.str_conf[0][1]["size"]} گیگ | {prices.str_conf[0][1]["price"]} تومان

🔸 {prices.str_conf[1][2]} کاربره: {prices.str_conf[1][0]["size"]} گیگ | {prices.str_conf[1][0]["price"]} تومان
🔹 {prices.str_conf[1][2]} کاربره: {prices.str_conf[1][1]["size"]} گیگ | {prices.str_conf[1][1]["price"]} تومان

🔸 {prices.str_conf[2][2]} کاربره: {prices.str_conf[2][0]["size"]} گیگ | {prices.str_conf[2][0]["price"]} تومان
🔹 {prices.str_conf[2][2]} کاربره: {prices.str_conf[2][1]["size"]} گیگ | {prices.str_conf[2][1]["price"]} تومان

🔸 {prices.str_conf[3][2]} کاربره: {prices.str_conf[3][0]["size"]} گیگ | {prices.str_conf[3][0]["price"]} تومان
🔹 {prices.str_conf[3][2]} کاربره: {prices.str_conf[3][1]["size"]} گیگ | {prices.str_conf[3][1]["price"]} تومان


☎️ در صورت هرگونه سوال یا نیاز به راهنمایی، با ما تماس بگیرید: @"""
    + cohandler.getconfig["bot"]["sponsor_admin"]
    + """

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

RULES_TEXT = (
    """🏛 قوانین استفاده از سرویس

🔸 بعد از خرید سرویس امکان برگشت وجه نیست، لطفا سرویس خود را با دقت انتخاب کنید.

🔹 سرویس خریداری شده اگر بعد از گذشت مدت زمان سرویس تمدید نشود بعد از 3 روز حذف میشود.

🔸 شما موظف هستید که اگر سرویس یک کاربره گرفته اید فقط با یک آیپی متصل شود در صورت رعایت نکردن بعد از اخطار سرویس شما به مدت 6 ساعت مسدود میشود

🔹 تیم مدیریت میتواند به دلیل تخلف (فحاشی - دیداس - فیشینگ و....) اکانت شما را مسدود کند.

🔸 بعد از اتمام آستانه مصرف منصفانه در صورت باقی ماندن مدت زمان سرویس شما میتوانید سرویس را تمدید یا حجم اضافه خریداری کنید.

🔹 در سرویس های خریداری شده یا افزایش اعتبار کیف پول به هیچ وجه بازگشت وجهی صورت نمیگیرد و مسئولیت آن به عهده کاربر است.

📌 در صورتی سوال یا ابهامی دارید میتوانید ابتدا بخش سوالات متداول را مطالعه کنید و در صورت مشکل با پشتیبانی در ارتباط باشید

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

RULES_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="تایید قوانین و ادامه خرید", callback_data="igree_rules"
            )
        ]
    ]
)

CANT_BUY_TEXT = (
    """❌ بخش خرید موقتا غیرفعال می باشد لطفا بعدا تلاش کنید

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)


CANT_BUY_TEXT_RAW = """❌ بخش خرید موقتا غیرفعال می باشد"""

SERVERS_TEXT = (
    """‏💎 جهت خرید سرویس، یکی از کشور های زیر را انتخاب کنید

📌 بعد از خرید میتوانید لوکیشن خود را بدون محدودیت و به صورت رایگان تغییر دهید و همچنین جهت مشاهده قیمت ها میتوانید به بخش تعرفه ها مراجعه کنید

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

SERVER_DISABLED_RAW = """❌ خرید از این لوکیشن در حال حاضر غیرفعال میباشد"""

TIME_SERVICE_TEXT = (
    """🌿 لطفا مدت زمان سرویس را مشخص کنید

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

USERS_COUNT_TEXT = (
    """🌿 لطفا تعداد کاربر سرویس را مشخص کنید

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

SIZES_TEXT = (
    """🌿 لطفا حجم سرویس را مخشص کنید

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

FINAL_STAGE_TEXT = (
    """🔰 سرویس شما اماده خرید است

🌿 شناسه صورتحساب: {}
📍 لوکیشن: {}
⏳ مدت زمان: {}
🔌 تعداد کاربر: {} کاربره
💾 حجم سرویس: {} گیگ (مصرف منصفانه)
💰 قیمت : {} تومان

📌 برای پرداخت یکی از روش های زیر را انتخاب کنید


🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

CHOICE_COIN_TEXT = (
    """🔵 لطفا یکی از ارز های زیر را برای پرداخت انتخاب کنید

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

ERROR_LOW_VALUE_RAW = """❌ پرداخت با این ارز در حال حاضر در دسترس نیست"""

ERROR_TEXT = """❌ ERROR IN CREATE PAYMENT
❌ Status : False
❌ StatusCode : {}
❌ Code : {}
❌ Message : {}"""


CRYPTO_PAY_TEXT = (
    """🔍 وضعیت سفارش: در انتظار پرداخت
📌 شناسه پرداخت: <code>{}</code>
🔘 شماره سفارش: <code>{}</code>
⏳ توضیحات : {}
💵 قیمت : {}

🔍 وضعیت پرداخت: پرداخت نشده
◽️ مبلغ پرداخت: <code>{}</code> {}
◽️ شبکه پرداخت : <b>{}</b>
◽️ آدرس پرداخت: <code>{}</code>
◽️ ممو : {}

📍 نکته : تنها هنگام ارسال ارزهای  XRP و ATOM و XLM و BNB Mainnet و سایر ارزهایی که ممو دارند ، حتما ممو یا برچسب را وارد کنید تا پرداخت شما تایید شود!

⏱ مهلت پرداخت: {}

⚠️ هشدار : لطفا دقیقا به اندازه فاکتور پرداخت نمایید در صورت کمتر پرداخت کردن ممکن است تراکنش تایید نشود و امکان بازگشت وجه وجود نداشته باشد.

‼️ شما میتوانید با استفاده از دکمه زیر وضعیت تراکنش خود را ببینید


🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)


BUY_REPORT = (
    """
✅ خرید سرویس جدید :
🌿 شناسه صورتحساب: {}
⏳ مدت زمان: {} ماهه
🔌 تعداد کاربر: {} کاربره
💾 حجم سرویس: {} گیگ (مصرف منصفانه)

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

SUCCESSFULL_BUY = (
    """✅ پرداخت با موفقیت انجام شد و سرویس شما ایجاد شده است

🌿 شناسه صورتحساب: {}
⏳ مدت زمان: {} ماهه
🔌 تعداد کاربر: {} کاربره
💾 حجم سرویس: {} گیگ (مصرف منصفانه)

📥 جهت دریافت لینک اتصال به سرویس به بخش سرویس ها مراجعه کنید

🧑‍🦯 شما میتوانید شیوه اتصال را در بخش راهنما مطالعه کنید

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

REF_BUY_SUCESSS = (
    """🎁 مبلغ {} تومان جهت خرید یکی از زیر مجموعه های شما به کیف پول شما اضافه شد 😃

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

RIAL_PAY_TEXT = (
    """🔰 سرویس شما اماده خرید است

🌿 شناسه صورتحساب: {}
⏳ مدت زمان: {}
🔌 تعداد کاربر: {} کاربره
💾 حجم سرویس: {} گیگ (مصرف منصفانه)
💰 قیمت : {} تومان

📌 برای پرداخت روی دکمه زیر کلیک کنید

⚠️ این لینک فقط تا نیم ساعت بعد فعال می باشد و بعد از پرداخت منقضی میشود

‏🇮🇷 پرداخت فقط با آیپی ایران امکان پذیر است، اگر vpn شما روشن است لطفا خاموش کنید و مجددا وارد درگاه شوید

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

EXPIRED_MESSAGE_CRYPTO = (
    """❌ پرداخت انجام نشد و مهلت به پایان رسید و ادرس باطل شد

📌 شناسه پرداخت : <code>{}</code>

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

BALANCE_MESSAGE = (
    """👤 شناسه کاربری شما : <code>{}</code>
📌 اعتبار کیف پول شما: {} تومان

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

BALANCE_BUTTONS = InlineKeyboardMarkup(
    [[InlineKeyboardButton(text="➕ افزایش اعتبار ➕", callback_data="add_balance")]]
)

ADD_BALANCE_TEXT = (
    """📌 جهت افزایش اعتبار کیف پول مبلغ مورد نظر را به تومان ارسال کنید

🤝 در ارسال مبلغ دقت کنید زیرا بازگشت وجهی صورت نمیگیرد و تنها در صورت پرداخت ناموفق وجه بازگشت میخورد

⚠️ توجه: رقم اخر مبلغ ارسالی باید 0 باشد

🌿 مثال: 5350

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

ADD_BALANCE_CANCEL_BUTTON = ReplyKeyboardMarkup(
    [[KeyboardButton("🔙 بازگشت")]], resize_keyboard=True
)

CANCEL_ADD_BALANCE_TEXT = (
    """✅ شما با موفقیت به منوی اصلی ربات برگشتید

📌 جهت استفاده از ربات لطفا یکی از موارد زیر را انتخاب کنید

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

INVALID_ADD_BALANCE_VALUE_MESSAGE = (
    """❌ مبلغ ارسالی نامعتبر است

⚠️ مبلغ ارسالی باید بین 10000 تا 5000000 تومان باشد

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

LAST_NUMBER_ERROR_TEXT = (
    """❌ مبلغ ارسالی نامعتبر است

⚠️ توجه: رقم آخر مبلغ ارسالی باید 0 باشد 

🌿 مثال: 5350

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

ADD_BALANCE_FINAL_TEXT = (
    """✅ شما میتوانید مبلغ {} تومان را به صورت ریال یا رمز ارز پرداخت کنید

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)


RIAL_MAX_LIMIT_TEXT = """⚠️ حداکثر مبلغ خرید برای درگاه بانکی {} است"""
RIAL_MIN_LIMIT_TEXT = """⚠️ حداقل مبلغ خرید برای درگاه بانکی {} است"""

RIALERROR_TEXT = """❌ خطا در درگاه  بانکی لطفا بعدا دوباره تلاش کنید"""


ADD_RIAL_TEXT = (
    """✅ لطفا مبلغ {} تومان را از طریق لینک زیر پرداخت کنید

⚠️ این لینک فقط تا نیم ساعت بعد فعال می باشد و بعد از پرداخت منقضی میشود

‏🇮🇷 پرداخت فقط با آیپی ایران امکان پذیر است، اگر vpn شما روشن است لطفا خاموش کنید و مجددا وارد درگاه شوید

📌 شماره سفارش: <code>{}</code>


🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

TRANSACTION_RECEIVED_TEXT = (
    """✅ کاربر گرامی تراکنش شما در شبکه شناسایی شد. لطفا منتظر تایید تراکنش باشید

♻️ این مرحله بسته به شبکه ممکن است کمی طول بکشد لطفا شکیبا باشید

📌 شناسه پرداخت: <code>{}</code>

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

TRANSACTION_FAILED_TEXT = (
    """❌ تراکنش با خطا روبرو شد. در صورت مشکل با پشتیبانی در ارتباط باشید

📌 شناسه پرداخت: <code>{}</code>

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

TRANSACTION_PARTIALLY_PAID = (
    """⚠️ تراکنش به صورت کامل پرداخت نشده است!

📌 شناسه پرداخت: <code>{}</code>

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)


TRANSACTION_WATING = "🔍 در انتظار پرداخت"

TRANSACTION_REFUNDED_TEXT = (
    """☑️ مبلغ تراکنش به ولت شما ریفاند شده است

📌 شناسه پرداخت: <code>{}</code>

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

SUCCESSFULL_ADD_BALANCE = (
    """✅ پرداخت با موفقیت انجام شد و کیف پول شما شارژ شد

📌 شناسه پرداخت: <code>{}</code>

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

EXPIRED_CARD_PAYMENT = (
    """⚠️ زمان کارت به کارت کردن شما به پایان رسید!

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)


ADDMOREUSERFAILED = (
    """❌ مشکلی در خرید کاربر اضافه با  رخ داده است بعدا دوباره تلاش کنید
🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)


LESS_BALANCE_TEXT = """❌ شما موجودی کافی برای خرید این سرویس ندارید"""


BALANCE_EXCEPT_BUY = (
    """⚠️ با توجه به این که خرید سرویس توسط مدیریت بسته شده است، به جای سرویس به کیف پول شما در بات موجودی اضافه شده است.

📌 شناسه پرداخت: <code>{}</code>

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

BALANCE_EXCEPT_BUY2 = (
    """⚠️ با توجه به این که ظرفیت سرور انتخابی شما پر شده است، به جای سرویس به کیف پول شما در بات موجودی اضافه شده است.

📌 شناسه پرداخت: <code>{}</code>

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)


BALANCE_EXCEPT_BUY3 = (
    """⚠️ در ایجاد سرویس خطایی رخ داد به جای سرویس به کیف پول شما در بات موجودی اضافه شده است  


📌 شناسه پرداخت: <code>{}</code>

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)


SERVER_FULL_TEXT = """❌ در حال حاضر ظرفیت این سرور پر شده است"""

UNKNOWN_ERROR = """❌ خطای ناشناخته"""

NOT_REGISTERED_USER_ERROR = """❌مشکلی رخ داده است لطفا ربات را /start کنید"""


MANAGE_SERVICES_TEXT = (
    """🐉 جهت مدیریت سرویس، سرویس مورد نظر را انتخاب کنید

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

NO_SERVICES_TEXT = (
    """❌ شما در حال حاضر هیچ سرویس فعالی ندارید

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

GOT_FREE_BEFORE_TEXT = (
    """❌ کابر گرامی شما قبلا اکانت رایگان را فعال کرده اید

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

NO_FREE_SERVICE_TEXT = (
    """❌ در حال حاضر هیچ سرور رایگانی وجود ندارد. لطفا بعدا تلاش کنید

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

FREE_SERVICE_ACTIVATED_TEXT = (
    """✅ سرویس رایگان شما فعال شد 

📥 جهت دریافت لینک اتصال به سرویس به بخش سرویس ها مراجعه کنید

⭐️ شما میتوانید شیوه اتصال را در بخش راهنما مطالعه کنید

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

FREE_SERVICES_FULL_TEXT = (
    """❌ در حال حاضر ظرفیت سرورهای رایگان پر شده است لطفا بعدا تلاش کنید

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

SERVICE_INFO_TEXT2 = (
    """🌿 نام سرویس: {}
‏🇺🇳 لوکیشن: ‌‏{}
🔥 پروتکل سرویس: {} - {}
💹 وضعیت: {}
‏🆔 شناسه سرویس : <code>{}</code>
‏🪪 لایسنس سرویس : <code>{}</code>

📌 شما میتوانید با استفاده از دکمه های زیر سرویس خود را مدیریت کنید

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

SERVICE_INFO_TEXT = (
    """🌿 نام سرویس: {}
‏🇺🇳 لوکیشن: ‌‏{}
🔥 پروتکل سرویس: {} - {}
💹 وضعیت: {}
‏🆔 شناسه سرویس : <code>{}</code>

📌 شما میتوانید با استفاده از دکمه های زیر سرویس خود را مدیریت کنید

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

CHANGE_SERVICE_NAME_TEXT = (
    """📝 جهت تغییر نام سرویس، نام مورد نظر خود را ارسال کنید

📌 مثال: Test-1234

⚠️ توجه: نام ارسالی فقط باید اعداد و حروف انگلیسی باشد

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

CHANGE_SERVICE_BACK = ReplyKeyboardMarkup(
    [[KeyboardButton("🔙 بازگشت")]], resize_keyboard=True
)


MoreUserButton = ReplyKeyboardMarkup(
    [[KeyboardButton("✅ تایید")], [KeyboardButton("🔙 بازگشت")]], resize_keyboard=True
)


CANCEL_CHANGE_SERVICE_NAME_TEXT = """❌ تغییر نام سرویس کنسل شد"""

SHORT_NAME_TEXT = (
    """❌ نام ارسالی باید بین 5 تا 16 کاراکتر باشد

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

BAD_NAME_TEXT = (
    """❌ نام ارسالی باید فقط از عدد و حروف انگلیسی تشکیل شده و از فاصله استفاده نشده باشد

📌 استفاده از - مجاز است

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

USED_NAME_TEXT = (
    """❌ این نام قبلا استفاده شده است

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)


CHNAGE_NAME_FAST = (
    """❌تغییر نام هر 3 دقیقه  یکبارامکان پذیر است

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

CHANGED_NAME_SUCCESS_TEXT = (
    """✅ تغییر نام سرویس از "{}" به "{}" با موفقیت انجام شد

📌 لینک اتصال تغییر کرده است، شما میتوانید لینک جدید را دریافت کنید یا از لینک قدیمی استفاده کنید

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

GET_SERVICE_INFO_TEXT = (
    """🌿 نام سرویس: {}
‏🇺🇳 لوکیشن: ‌‏{}
💹 وضعیت: {}
🔥 پروتکل سرویس: {} - {}
⏳ اعتبار: {} روز دیگر
🔌 تعداد کاربر: {} کاربره
♾ آستانه مصرف: {} گیگابایت
📊 حجم مصرف شده: {} گیگابایت
🧮 حجم باقی مانده: {} گیگابایت
📌 پلن انتخابی: {}
💰 قیمت سرویس: {} تومان

📅 تاریخ خرید/تمدید: {}
🕘 ساعت خرید/تمدید: {}

⚠️ در صورت مغایرت در حجم ده دقیقه تا نیم ساعت دیگر دوباره بررسی کنید.

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

GET_SERVICE_INFO_TEXT_SELLERS = """🌿 نام سرویس: {}
‏🇺🇳 لوکیشن: ‌‏{}
💹 وضعیت: {}
🔥 پروتکل سرویس: {} - {}
⏳ اعتبار: {} روز دیگر
🔌 تعداد کاربر: {} کاربره
♾ آستانه مصرف: {} گیگابایت
📊 حجم مصرف شده: {} گیگابایت
🧮 حجم باقی مانده: {} گیگابایت
📌 پلن انتخابی: {}

⚠️ در صورت مغایرت در حجم ده دقیقه تا نیم ساعت دیگر دوباره بررسی کنید.

📅 تاریخ خرید/تمدید: {}
🕘 ساعت خرید/تمدید: {}"""

NIMBAHA_LINK_TEXT = (
    """📌 لینک اتصال نیم بها شما 👇

🔗 Link (IP): <code>{}</code>

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

NIMBAHA_LINK_VLESS_TEXT = (
    """📌 لینک اتصال نیم بها شما 👇

🔗 Link (IP): <code>{}</code>

🔗 Nekoray Link (IP): <code>{}</code>

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

DIRECT_LINK_WARNING = """⛔️ در صورت اختلال در اینترنت یا اینترانت لینک مستقیم وصل نمیشود لذا از اینک نیمبها استفاده کنید"""

DIRECT_LINK_TEXT = (
    """📌 لینک اتصال مستقیم شما 👇

🔗 Link (IP): <code>{}</code>

⚠️ توجه:  این لینک بدون نیم بها شدن بصورت مستقیم به سرور خارج از کشور است، مصرف شما با این لینک تمام بها میشود ولی ممکن است از سرعت بهتری برخوردار شوید!

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

DIRECT_LINK_VLESS_TEXT = (
    """📌 لینک اتصال مستقیم شما 👇

🔗 Link (IP): <code>{}</code>

🔗 Nekoray Link (IP): <code>{}</code>

⚠️ توجه:  این لینک بدون نیم بها شدن بصورت مستقیم به سرور خارج از کشور است، مصرف شما با این لینک تمام بها میشود ولی ممکن است از سرعت بهتری برخوردار شوید!

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

NO_NIMBAHA_LINK_TEXT = """❌ در حال حاضر لینک نیم بها برای این سرویس در دسترس نیست"""

CONFIRM_CHANGE_LINK_TEXT = (
    """📌 آیا تغییر لینک اتصال را تایید میکنید؟

⚠️ بعد از تغییر لینک اتصال تمامی افراد متصل قطع میشوند و لینک قبلی غیرفعال میشود

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

CHANGED_LINK_SUCCESSFULLY_TEXT = (
    """✅ لینک اتصال با موفقیت تغییر کرد، شما میتوانید از دکمه زیر برای دریافت لینک جدید اقدام کنید

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

MORE_USER_TEXT = (
    """➕ لطفا تعداد کاربر اضافه را انتخاب کنید:

⚠️ توجه: بعد از تمدید سرویس تعداد کاربر اضافی خریداری شده 0 میشود و تعداد کاربر اصلی پلن انتخابی تنظیم میشود

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

MORE_USER_FINAL_TEXT = (
    """📌 کاربر اضافی انتخابی 👇

👤 تعداد کاربر: {} کاربره

💳 اعتبار کیف پول شما:  {} تومان
💵 قیمت کاربر اضافی: {} تومان

⭐️ شما میتوانید به مراحل قبل برگردید و تعداد کاربر را تغییر دهید یا از همین مرحله خرید خود را تایید کنید


🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

SUCCESSFULL_ADD_MORE_USER_TEXT = (
    """✅ کاربر اضافی با موفقیت به سرویس شما اضافه شد


🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

CHANGE_LOCATION_TEXT = (
    """‏🇺🇳 جهت تغییر لوکیشن سرویس، یکی از کشور های زیر را انتخاب کنید


🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

CONFIRM_CHANGE_LOCATION_TEXT = (
    """📌 آیا تغییر لوکیشن را تایید میکنید؟

⚠️ بعد از تغییر لوکیشن ممکن است افراد متصل قطع شوند، با همان لینک قبلی میتوانید به سرویس متصل شوید


🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

ALREADY_THIS_LOCATION_TEXT = """❌ در حال حاضر لوکیشن شما روی این سرور میباشد"""

LOCATION_CHANGED_SUCCESSFULLY_TEXT = (
    """✅ لوکیشن سرویس شما با موفقیت به لوکیشن مورد نظر شما تغییر کرد، شما میتوانید با لینک قبلی به سرویس خود متصل شوید یا از طریق دکمه زیر لینک اتصال را دریافت کنید

⚠️ توجه: لینک های اتصال منقضی شده اند، شما میتواند لینک های جدید از طریق دکمه های زیر دریافت کنید


🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

AUTO_REPAY_TEXT = (
    """♾ شما میتوانید با دکمه های زیر تمدید خودکار را فعال یا غیرفعال کنید

⚠️ توجه: برای استفاده از این قابلیت باید کیف پول خود را به اندازه لازم برای تمدید سرویس شارژ نمایید


🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

SHOW_ALERTS_TEXT = (
    """📣 شما میتوانید با دکمه های زیر اعلان های اتصال را فعال یا غیرفعال کنید

⚠️ توجه: غیرفعال سازی اعلان های اتصال فقط برای این سرویس انجام میشود

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)


CHANGE_BUY_STATUS = (
    """📣 شما میتوانید با دکمه های زیر وضعیت  خرید را فعال یا غیرفعال کنید

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)


SHOW_SUBSCRIPTION_LINK = (
    """📍 لینک اشتراک چیست؟ شما با وارد کردن این لینک در بخش subscribe کلاینت های مختلف میتوانید بصورت خودکار لیست سرویس های خود را بروز نگه دارید

⭐️ لینک اشتراک کلش 👇
🔗 Link: <code>{}</code>

⭐️ لینک اشتراک اندروید و WingsX و Nekoray 👇
🔗 Link: <code>{}</code>

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

SHOW_SUBSCRIPTION_WS_VMESS_LINK = (
    """📍 لینک اشتراک چیست؟ شما با وارد کردن این لینک در بخش subscribe کلاینت های مختلف میتوانید بصورت خودکار لیست سرویس های خود را بروز نگه دارید

⭐️ لینک اشتراک کلش 👇
🔗 Link: <code>{}</code>

⭐️ لینک اشتراک اندروید و WingsX و Nekoray 👇
🔗 Link: <code>{}</code>

⭐️ لینک اشتراک SurfBoard 👇
🔗 Link: <code>{}</code>

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

SHOW_SUBSCRIPTION2_LINK = (
    """📍 لینک اشتراک چیست؟ شما با وارد کردن این لینک در بخش subscribe کلاینت های مختلف میتوانید بصورت خودکار لیست سرویس های خود را بروز نگه دارید

⭐️ لینک اشتراک اندروید و WingsX و Nekoray 👇
🔗 Link: <code>{}</code>

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

CHANGE_SUBSCRIPTION_TEXT = (
    """📌 آیا تغییر لینک اشتراک را تایید میکنید؟

⚠️ بعد از تغییر لینک اشتراک قبلی منقضی میشود

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

CHANGE_SUBSCRIPTION_SUCCESSFULL_TEXT = (
    """✅ لینک اشتراک سرویس با موفقیت تغییر کرد، شما میتوانید از دکمه زیر برای دریافت لینک جدید اقدام کنید

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

CHANGE_PROTOCOL_TEXT = (
    """🔥 جهت تغییر پروتکل ارتباطی با سرور ها میتوانید یکی از پروتکل های زیر را انتخاب کنید

📌 شما میتوانید آموزش اتصال به هر پروتکل را در بخش راهنمای اتصال یا در چنل تلگرام مشاهده کنید

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

CHANGE_PROTOCOL_SUCCESSFULL_TEXT = (
    """✅ پروتکل سرویس شما با موفقیت تغییر پیدا کرد

📌 لطفا لینک اتصال خود را برای این پروتکل از طریق دکمه های زیر دریافت کنید

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

INCREASE_SIZE_TEXT = (
    """♾ جهت خرید حجم اضافه حجم مورد نظر خود را ارسال کنید : 

📌 مثال: 50

⚠️ توجه: مقدار عدد ارسالی 'گیگ' می باشد و هر گیگ 3000 تومان است

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

MAIN_MENU_TEXT = (
    """✅ شما با موفقیت به منوی اصلی ربات برگشتید

📌 جهت استفاده از ربات لطفا یکی از موارد زیر را انتخاب کنید

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

INVALID_SIZE_ERROR = (
    """❌ خطا: حجم ارسالی نامعتبر است

📌 مثال: 25

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

INCREASE_SIZE_RANGE_ERROR_TEXT = (
    """❌ خطا: حجم ارسالی نامعتبر است

📌 حجم ارسالی باید بین 1 تا 600 باشد

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

CHOOSE_SERVICE_ADD_SIZE_TEXT = (
    """♾ لطفا سرویس مورد نظر خود را برای خرید حجم اضافه انتخاب کنید

📌 حجم اضافه: {} گیگ

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)


FINAL_ADD_SIZE_TEXT = (
    """📌 حجم اضافه برای سرویس زیر 👇

🌿 نام سرویس: {}
♾ حجم انتخابی: {} گیگ

💳 اعتبار کیف پول شما:  {} تومان
💵 قیمت سرویس: {} تومان

⭐️ شما میتوانید به مراحل قبل برگردید و سرویس انتخابی را تغییر دهید یا از همین مرحله خرید خود را تایید کنید

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

SUCCESSFULL_ADD_SIZE_USER_TEXT = (
    """✅ حجم اضافه با موفقیت به سرویس شما اعمال شد

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

NOT_AVAILABLE_FOR_FREE_SERVICES = """❌ این قابلیت برای سرویس های رایگان در دسترس نیست"""

QRCODE_STRING = (
    """📌 لینک اتصال داخلی شما ({}) 👇

<code>{}</code>

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

VLESS_TEXT = """📌 لینک اتصال داخلی شما 👇
🔗 Nekoray Link (IP): <code>{}</code>

🆔 @"""+cohandler.getconfig["bot"]["sponsor_bot"]

EXPIRING_SERVICE_TEXT = (
    """⏳ کاربر گرامی تنها {} از سرویس {} باقی مانده است، لطفا در اسرع وقت اقدام به تمدید سرویس خود نمایید.

🐉 سرویس ها > سرویستون رو انتخاب کنید > تمدید سرویس

📌 اگر تا 3 روز بعد از پایان سرویس اقدام به تمدید آن نفرمایید سرویس بطور کامل حذف می شود.

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

EXPIRED_SERVICE_TEXT = (
    """⭕️ کاربر گرامی مهلت سرویس {} تمام شده است. اگر تا 3 روز اینده سرویس تمدید نشود برای همیشه حذف خواهد شد.

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

EXPIRING_SERVICE_FREE_TEXT = (
    """⏳ کاربر گرامی تنها {} از سرویس رایگان {} باقی مانده است. در صورت تمایل از بخش "خرید سرویس" میتوانید سرویس جدید خریداری کنید.

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

EXPIRED_SERVICE_FREE_TEXT = (
    """⭕️ کاربر گرامی مهلت سرویس رایگان {} تمام شده است. 

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

NO_BALANCE_FOR_AUTO_PAY_TEXT = (
    """⭕️ کاربر گرامی کیف پول شما مبلغ کافی برای تمدید خودکار سرویس {} ندارد. لذا سرویس شما تا تمدید سرویس غیرفعال میشود. 

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)


NO_BALANCE_FOR_MORE_USER = (
    """⭕️ کاربر گرامی کیف پول شما مبلغ کافی برای کاربر اضافه   
ندارد.

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)


SUCCESSFULL_AUTO_PAY_TEXT = (
    """✅ سرویس {} به طور خودکار تمدید شد

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

DELETED_SERVICE_TEXT = (
    """⭕️ سرویس {} به علت عدم تمدید حذف شد

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

CANT_EXTENSION_TEXT = (
    """⭕️ تنها در 5 روز مانده به اتمام سرویس میتوانید آن را تمدید کنید"""
)

EXTENSION_SERVICE_TEXT = (
    """📌 تمدید سرویس

🌿 نام سرویس: {}

💳 اعتبار کیف پول شما:  {} تومان
💵 قیمت سرویس: {} تومان

⭐️ شما میتوانید به مراحل قبل برگردید و سرویس انتخابی را تغییر دهید یا از همین مرحله خرید خود را تایید کنید

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)


SUCCESSFULL_EXTENSION_TEXT = (
    """✅ سرویس {} تمدید شد

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

SERVICE_EXPIRED_ERROR_TEXT = (
    """❌ این سرویس منقضی شده است. لطفا سرویس را تمدید کرده سپس دوباره تلاش کنید"""
)


SERVICE_SIZE_85_TEXT = (
    """⚠️ کاربر گرامی شما 85 درصد از حجم سرویس {} را مصرف کرده اید

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

SERVICE_SIZE_99_TEXT = (
    """⚠️ کاربر گرامی شما 99 درصد از حجم سرویس {} را مصرف کرده اید

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

SERVICE_SIZE_ENDED_TEXT = (
    """⚠️ کاربر گرامی حجم سرویس {} به اتمام رسیده است. در صورت تمایل میتوانید سرویس خود را تمدید کنید.

♾ حجم اضافه > مقدار حجمی که میخواید > انتخاب سرویس > پرداخت از کیف پول 

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

SERVICE_MORE_CONNS_WARN_TEXT = (
    """🔴 کاربر گرامی تعداد کانکشن های شما به سرویس {} بیشتر از حد مجاز میباشد.

⭕️ تعداد اخطار : {}

⚠️ در صورتی که تعداد کانکشن غیر مجاز شما به 3 بار برسد، سرویس شما برای 6 ساعت مسدود خواهد شد.

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

SERVICE_BANNED_TEXT = (
    """🚫 سرویس {} به علت تعداد کانکشن بیش از حد به مدت 6 ساعت مسدود میشود.

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

SERVICE_UNBANNED_TEXT = (
    """⚠️ سرویس {} آن بن شد. توجه کنید در صورت تکرار کانکشن بیش از حد دوباره سرویس شما به مدت 6 ساعت مسدود خواهد شد.

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

SERVICE_BANNED_RAW_TEXT = """❌ این سرویس مسدود شده است"""

NO_CONS_TO_SERVICE = (
    """❌ اتصالی به سرویس وجود ندارد

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

SERVICE_CONNECTIONS_TEXT = (
    """🧬 آخرین آیپی های متصل به سرویس ({}) 👇

{}
⚠️ توجه: لیست بالا آخرین افراد متصل به سرویس را نشان میدهد و به معنای افرادی که همینک به سرویس متصل هستند نیست

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

MESSAGE_EXPIRED_TEXT = """❌ این پیام منقضی شده است لطفا دوباره به این بخش مراجعه کنید"""

UNSUPPORTED_CLASH_LINK_TEXT = """❌ لینک اشتراک برای پروتوکل vless پشتیبانی نمیشود"""

SPAM_ALERT_TEXT = (
    """⚠️ اخطار: کاربر گرامی در صورت تکرار اسپم توسط آنتی اسپم بن میشوید

🎚 حداکثر اخطار: 10
➕ اخطار های داده شده: {}

⛔️ اگر تعداد اخطار های شما به حداکثر رسید از ربات بن میشوید

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

SPAM_BANNED_TEXT = (
    """🚫 حساب شما به علت اسپم بیش از حد مسدود شده است

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

FREE_SERVICE_DISABLED_TEXT = (
    """❌ بخش سرویس رایگان توسط مدیریت غیرفعال شده است

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

ALERT_CONNECTION_TEXT = (
    """⚡️ اتصال به سرویس {}

📌 آیپی: <a href="https://check-host.net/ip-info?host={}">{}</a>

⚠️ توجه: تکرار پیام اتصال برای یک آیپی به معنی اختلال در اینترنت فرد است شما میتوانید در بخش سرویس ها هشدار های اتصال را غیرفعال کنید

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

CHANGE_LOCATION_FAST_TEXT = """❌ تغییر لوکیشن هر 5 دقیقه یکبار امکان پذیر است"""

CHANGE_LINK_FAST_TEXT = """❌ تغییر لینک هر 3 دقیقه یکبار امکان پذیر است"""

CHANGE_PROTOCOL_FAST = """❌ تغییر پروتوکل هر 3 دقیقه یکبار امکان پذیر است"""
SERVICE_EXPIRED = """❌ سرویس منقضی شده است"""


CHANGE_TYPE_FAST = """❌ تغییر نوع کانکشن هر 3 دقیقه یکبار امکان پذیر است"""
MORE_USER_FAST = """❌ خرید کاربر اضافه هر 3 دقیقه یکبار امکان پذیر است"""


CANT_ADD_SIZE_ERROR = """❌ این سرویس کمتر از یک روز اعتبار دارد، ابتدا سرویس را تمدید کنید سپس دوباره اقدام کنید"""

CANT_PAY_RIAL = """❌ این روش پرداخت فعلا در دسترس نمیباشد"""


ADD_SIZE_ERROR = """❌ این سرویس در دسترسی نیست"""


FREE_SERVICE_SIZE_ENDED_TEXT = (
    """⚠️ حجم سرویس رایگان {} تمام شده است.

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

PAY_CARD_TEXT = """🏖 کاربر گرامی لطفا مبلغ {} تومان را به بصورت دقیق به شماره کارت زیر واریز کنید.

⚠️ نیازی به ارسال عکس یا فیش واریزی نیست. ( فرآیند اتوماتیک انجام میشود )

‏💳  <code>{}</code>
✏️ {}

✅ پرداخت شما حداکثر تا 5 دقیقه بعد از ارسال وجه تایید خواهد شد

جهت ارتباط با پشتیبانی 👇
@"""+ cohandler.getconfig["bot"]["sponsor_admin"] + """ 

🆔 @""" + cohandler.getconfig["bot"]["sponsor_bot"]

PAY_CARD_BUTTONS = ReplyKeyboardMarkup(
    [[KeyboardButton(text="🔙 بازگشت")]], resize_keyboard=True
)

ENTER_CARD_TEXT = (
    """✍️ لطفا شماره کارت مبدا را بدون فاصله وارد کنید.

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

INVALID_CARD_NUMBER = """❌ شماره کارت وارد شده اشتباه است"""

TIME_TO_PAY_ENDED = (
    """❌ مهلت شما برای واریز وجه به اتمام رسید. لطفا دیگر وجهی ارسال نکنید

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

CARD_PAYMENT_CREDITED = (
    """✅ کیف پول شما شارژ شد.

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)


JUST_CRYPTO_OR_CARD_TEXT = (
    """❇️ لطفا برای خرید از طریق کارت به کارت یا ارز دیجیتال اقدام نمایید"""
)

JUST_CRYPTO_OR_RIAL_TEXT = (
    """❇️ لطفا برای خرید از طریق درگاه بانکی یا ارز دیجیتال اقدام نمایید"""
)

ENTER_EMAIL_BUTTONS = ReplyKeyboardMarkup(
    [[KeyboardButton(text="🔙 بازگشت")]], resize_keyboard=True
)

CURRENT_EMAIL_TEXT = (
    """📨 ایمیل فعلی شما : {}

📝 برای تغییر ایمیل فعلی ، ایمیل جدید را وارد کنید.

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

ENTER_EMAIL_TEXT = (
    """📨  لطفا ادرس ایمیل خود را وارد کنید.

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

INVALID_EMAIL_TEXT = """❌ فرمت ایمیل اشتباه است"""

UNSUPPORTED_DOMAIN_EMAIL_TEXT = """❌ دامین ایمیل شما پشتیبانی نمی شود"""

UNSUPPORTED_EMAIL_TEXT = """❌ این ایمیل پشتیبانی نمیشود"""

EMAIL_SUBMITED_TEXT = (
    """✅ ایمیل شما ثبت شد

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

ONE_SERVICE_REQUIRED_TEXT = (
    """❌ برای ثبت ایمیل باید حداقل یک سرویس خریداری کرده باشید"""
)

CANT_GET_DATA_ERROR_TEXT = (
    """❌ مشکلی در تغییر لوکیشن به وجود آمد. لطفا بعدا امتحان کنید"""
)

MAINTENANCE_TEXT = (
    """🛠 ربات در حال تعمیرات و نگهداری میباشد لطفا بعدا تلاش کنید.

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

MAINTENANCE_RAW_TEXT = """🛠 ربات در حال تعمیرات و نگهداری میباشد لطفا بعدا تلاش کنید."""

GATEWAY_ERROR_TEXT = (
    """❌ مشکلی در ارتباط با درگاه پرداخت به وجود آمد لطفا بعدا امتحان کنید"""
)

CHANGE_TYPE_TEXT = (
    """🔥 جهت تغییر نوع کانکشن ارتباطی با سرور ها میتوانید یکی از کانکشن های زیر را انتخاب کنید

⚠️ تنها در صورتی که روی tcp قطعی و وصلی دارید یا از آیفون ورژن قدیمی استفاده میکنید نوع کانکشن را به ws تغییر دهید.
⚠️ با تغییر نوع کانکشن به ws به احتمال 30 تا 95 درصد سرعت شما کمتر ولی کانکشن استیبل تر میشود.

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

CHANGE_TYPE_SUCCESSFULL_TEXT = (
    """✅ نوع کانکشن سرویس شما با موفقیت تغییر پیدا کرد

📌 لطفا لینک اتصال خود را برای این پروتکل از طریق دکمه های زیر دریافت کنید

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

MAINTENANCE_SERVER_TEXT = """⚠️ کاربر گرامی سرور این سرویس در حال تعمیر میباشد"""

LICENSE_BOT_TEXT = (
    """🔆 لایسنس سرویس {} 👇

🎫 License : <code>{}</code> 🔴

⚠️ علامت 🟢 به این معناست که یوزر لایسنس را در بات نمایندگی وارد کرده است و علامت 🔴 به این معناست که هنوز استفاده نشده است.

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

LICENSE_BOT_USED_TEXT = (
    """🔆 لایسنس سرویس {} 👇

🎫 License : <code>{}</code> 🟢
👤 User ID : <code>{}</code>
🗣 Name : {}
👁‍🗨 Username : @{}

⚠️ علامت 🟢 به این معناست که یوزر لایسنس را در بات نمایندگی وارد کرده است و علامت 🔴 به این معناست که هنوز استفاده نشده است.

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

LICENSE_NOT_FOUND = """❌ لایسنس یافت نشد"""

HELLO_BUTTONS_SELLERS = ReplyKeyboardMarkup(
    [
        [KeyboardButton(text="🐉 سرویس ها")],
        [KeyboardButton(text="🔥 اکانت رایگان")],
    ],
    resize_keyboard=True,
)

LICENSE_ADDED_TEXT = """✅ لایسنس شما با موفقیت اعتبار سنجی شد.

🔆 جهت دریافت لینک اتصال و مدیریت سرویس از بخش سرویس ها اقدام نمایید"""

MAIN_MENU_TEXT_SELLERS = """🔶 جهت فعال کردن سرویس، لایسنس سرویس خود را وارد کنید."""

LICENSE_ENTERED_TEXT = """✅ لایسنس سرویس {} فعال شد.

🎫 License : <code>{}</code>
👤 User ID : <code>{}</code>
🗣 Name : {}
👁‍🗨 Username : @{}"""

PROTOCOL_IS_SAME = """❌تغییری ایجاد نشد"""


UNAVAILABLE_TEXT = """❌ در دسترس نیست"""

INVALID_NAME_TEXT = """❌ اسم اشتباه"""

SERVICE_NOT_FOUND_TEXT = """❌ سرویس یافت نشد"""

MANUAL_TEXT = (
    """🤖😅دوست خوبم به مشکل خوردی!؟

بیا باهم مشکلتو حل کنیم هم منو خسته نکنی هم خودتو🥴

اول بهم بگو که اندروید هستی و یا Ios

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

ANDROID_MANUAL_TEXT = (
    """به بخش راهنمایی خوش اومدید کاربر گرامی (اندروید)😄 خوشحالم که همراهی کردی

چطور میتونم کمکت کنم 😃

( 1 ) وصل بود ولی یک باره دیگه متصل نشد

یک بار ببرید موبایلتون رو حالت هواپیما مجدد در بیارید  اگر نشد یک بار اینترنتتون رو ببرید حالت 2g مجدد ببرید 4g و تست کنید و اینکه لینک نیم بها و مستقیم جفتشو داشته باشید هر کدوم پایداری بهتری داشت براتون با همون متصل بمونید

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

IOS_MANUAL_TEXT = (
    """به بخش راهنمایی خوش اومدید کاربر گرامی (Ios)😄 خوشحالم که همراهی کردی

چطور میتونم کمکت کنم 😃

(1) گوشیم ورژنش پایینه نمیتونم برنامه رو نصب کنم 

شما میتونید با استفاده از برنامه FairVpn این مشکل رو بر طرف کنید فقط قبلش داخل ربات تغییر نوع کانکشن بدید به ws و بعدش تغییر پروتکل بدید به vless

(2) مشکل عدم اتصال دارم و وصل نمیشه 

از داخل تنظیمات تغییر پروتکل بدید به vless و مجدد تست کنید 


(3) کند هستش و قطعی دارم
 جفت لینک های مستقیم و نیم بها رو داشته باشید هر کدوم که پایداری بهتر احساس کردید متصل بشید

( 4 ) وصل هستش ولی فقط اینستاگرام باز نمیشه
شما باید تنظیمات اینترنت گوشیتون رو ریست کنید

به ترتیب وارد بخش های مورد نظر بشید
Genreal 
Transfer Or Reset Iphone
Reset 
Reset Network Setting

و ریست میکنید تنظیمات اینترنت شما مجدد پیکربندی میشه

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

MANUAL_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Android", callback_data="manual_android"),
            InlineKeyboardButton("Ios", callback_data="manual_ios"),
        ]
    ]
)

BACK_MANUAL_BUTTONS = InlineKeyboardMarkup(
    [[InlineKeyboardButton("🔙 برگشت", callback_data="show_manual")]]
)

APIKEY_TEXT = (
    """🪪 Api key : <code>{}</code>
🔗 <a href="https://documenter.getpostman.com/view/25344455905/2s5548ZDSdR3q#intro">Documentation</a>

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

LINK_CHANGED_TEXT = (
    """⚠️<b> لینک سرویس {} (نیمبها و مستقیم) توسط مدیریت تغییر یافته است لطفا اقدام به دریافت لینک جدید نمایید.

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
    + """</b>"""
)

DELETE_SERVICE_PROMPT_TEXT = (
    """⚠️ آیا از حذف این سرویس اطمینان دارید؟

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

SERVICE_WILL_BE_DELETED_TEXT = (
    """✔️ این سرویس تا ده دقیقه دیگر حذف خواهد شد.

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

TRANSFER_BALANCE_TEXT = (
    """💸 در این بخش میتوانید موجودی خودتان را به سایر کابران انتقال دهید.

موجودی شما: {} تومان

مقداری که میخواهید منتقل کنید را به تومان وارد کنید.

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

CANCEL_TRANSFER_BUTTONS = ReplyKeyboardMarkup(
    [[KeyboardButton("انصراف")]], resize_keyboard=True
)


INVALID_VALUE_TEXT = (
    """❌ عدد ارسالی اشتباه میباشد.

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

NO_BALANCE_TEXT = (
    """❌ موجودی شما کافی نمیباشد.

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

TRANSFER_USERID_TEXT = (
    """🛑 توجه: عملیات انتقال موجودی غیرقابل بازگشت است!

👈 درصورتی که درخواست انتقال {} تومان مورد تاییدتان است، شناسه کاربری مقصد را ارسال کنید.

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

INVALID_USERID_TEXT = (
    """⚠️ شناسه کاربری مقصد نامعتبر است و یا انتقال موجودی به کاربر موردنظر ممکن نیست.

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

COINS_TRANSFERED_TEXT = (
    """<code>✅ مقدار {} تومان در تاریخ {} ساعت {} با موفقیت به کاربر {} انتقال داده شد.</code>

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

ALARM_COINS_RECEIVED_TEXT = (
    """<code>✅ مقدار {} تومان در تاریخ {} ساعت {} با موفقیت از کاربر {} دریافت شد.</code>

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

TRANSFER_NOT_AVAILABLE_TEXT = (
    """❌ این بخش فعلا در دسترس نمیباشد.

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

CANT_TRANSFER_SELF_TEXT = (
    """❌ نمیتوانید به خودتان موجودی منتقل کنید.

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

TIME_INCREASED_TEXT = (
    """🔆 مدت زمان سرویس {} به مدت {} روز توسط مدیریت افزایش یافته است.

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

TIME_INCREASED_NOROZ_TEXT = (
    """🔆 مدت زمان سرویس {} به مدت {} روز توسط افزایش یافته است.

هدیه از سمت مدیریت بابت اختلالات اخیر و عید نوروز 

پیشاپیش عید نوروز مبارک 💜

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

NIMBAHA_EXISTS_TEXT = """❌ در حال حاضر لینک نیم بها برای این سرویس تنظیم شده است"""

PROBLEM_NIMBAHA_TEXT = (
    """❌ مشکلی در تنظیم لینک نیمبها وجود دارد لطفا بعدا امتحان کنید"""
)

NIMBAHA_SET_COMPLETED = """✅ لینک نیم بها با موفقیت تنظیم شد"""

NO_HISTORY_TEXT = """⚠️ دیتایی یافت نشد"""

HISTORY_IPS_TEXT = """🔅 تاریخچه افراد متصل به سرویس <b>{}</b>
🔅 شناسه سرویس : <code>{}</code>"""

CHANGE_LOCATION_UNAVAILBE_TEXT = """⚠️ تغییر لوکیشن در حال حاضر در دسترس نیست"""

THIS_SECTION_DISACTIVATED = (
    """⚠️ این بخش توسط مدیریت غیرفعال شده است

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

CONNECTION_TYPE_DISABLED = """⚠️ این نوع کانکشن توسط مدیریت غیرفعال شده است"""

DEPRECATED_CONNECTION_TYPE = (
    """⚠️ ابتدا نوع کانکشن سرویس خود را به tcp تغییر داده سپس دوباره تلاش کنید"""
)

SERVICE_SIZE_ENDED_RAW_TEXT = """⚠️ حجم این سرویس به اتمام رسیده است. ابتدا سرویس خود را تمدید کنید سپس دوباره تلاش کنید"""

DISABLED_PLAN_TEXT = "⚠️ این پلن غیرفعال میباشد"

HISTORY_IPS_LINK_TEXT = (
    """🔅 شما میتوانید تاریخچه افراد متصل به سرویس {} را از لینک زیر مشاهده کنید:

<a href="{}">🔗 تاریخچه افراد متصل</a>

🆔 @"""
    + cohandler.getconfig["bot"]["sponsor_bot"]
)

CARD_IN_USE = """❌این کارت با اکانت دیگری در حال استفاده میباشد. شما نمی‌توانید از یک کارت برای دو پرداخت همزمان استفاده کنید. لطفا پس از زمان مشخص شده تراکنش دوباره امتحان کنید.

🆔 @"""+ cohandler.getconfig["bot"]["sponsor_bot"]

NEW_SERVICE_LOG = """💳 Buy Service with {}

🆔 User ID: {}
💲 Payment ID: {}
⚙️ Service License: {}
📝 Service Name: {}
⌛️ Service Time: {}
🔹 User Count: {}
🔸 Size: {} GB
💰 Amount: {}
💳 Card Number: {}

#{}
#{}"""

PAYEMNT_SUCCESS_LOGGER = '''✅ یک تراکنش بانکی باموفقیت انجام شد. {}

💳 کارت: {}
💵 مقدار: {}
🔅 آیدی تراکنش: {}
⚜ آیدی کاربر: {}'''