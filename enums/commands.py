from enum import Enum
from pyrogram import filters


class BotCommands:
    admin = filters.command("admin")
    start = filters.command("Start")
    statics = filters.regex("^📊 آمار ربات$")
    settings = filters.regex("^⚙️ تنظیمات$")
    notification = filters.regex("^📣 ارسال اعلان$")
    emailsubmit = filters.regex("^📧 ثبت ایمیل$")
    question = filters.regex("^💡 سوالات متدوال$")
    con_helper = filters.regex("^🔗 راهنمای اتصال$")
    support = filters.regex("^📞 پشتیبانی$")
    pricese = filters.regex("^🎺 تعرفه ها$")
    buy_service = filters.regex("^💸 خرید سرویس$")
    refferal = filters.regex("^🏆 کسب درآمد$")
    balancetransfer = filters.regex("^💸 انتقال موجودی$")
    Canceltransfer = filters.regex("^انصراف$")
    userServices = filters.regex("^🐉 سرویس ها$")
    balance = filters.regex("^💰 کیف پول$")
    addsize = filters.regex("^♾ حجم اضافه$")
    modeBalance = filters.command("modbalance")
    admin_add_balance = filters.regex("^/addb ")
