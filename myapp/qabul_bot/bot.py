from django.conf import settings
from django.db.models import Q
from telegram import Bot, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters

from ..models import *

bot = Bot(token='5374320609:AAEn4Cic91-QCG5EgdUCGBmyhRGOLz_W07A')

hostname = f'{settings.HOST}/bot/'
print(f'Working host at: {hostname}')
bot.set_webhook(hostname)

dispatcher: Dispatcher = Dispatcher(bot, None)

help_dict = {}


def start(update, context):
    update.message.reply_text(f'Salom {update.effective_user.first_name}{update.effective_user.last_name}\n\n'
                              f'BuxPXTI botiga Xush kelibsiz!')

    return contact_handler(update, context)


def contact_handler(update, context):
    update.message.reply_text('Test javoblarini bilish uchun pastdagi\ntugmani bosib, telefon raqamingizni jo`nating',
                              reply_markup=ReplyKeyboardMarkup(
                                  [[KeyboardButton('Telefon raqam yuborish', request_contact=True)]],
                                  resize_keyboard=True))


def helper(update, context):
    a = str(update.message.contact.phone_number)
    print(update.message.chat.id)
    assa = update.message.chat.id
    help_dict[assa] = a
    print(help_dict)
    shart = Pasport.objects.filter(Q(telefon_raqam=a[-9:]) | Q(telefon_raqam_2=a[-9:]))
    if shart:
        for x in shart.values():
            update.message.bot.send_photo(update.message.chat.id, open(x['photo'], 'rb'),
                                          caption=f"Ism: {x['ism']}\nFamiliya: {x['familiya']}\nOtasining ismi: {x['sharif']}\n"
                                                  f"Telefon raqam: +998{x['telefon_raqam']}",
                                          reply_markup=ReplyKeyboardMarkup(
                                              [[KeyboardButton('Mening ma`lumotlarim')]],
                                              resize_keyboard=True))
    else:
        update.message.reply_text('Ma`lmotlaringiz bazada aniqlanmadi!')


def message_handler(update, context):
    if 'Mening ma`lumotlarim' == update.message.text:
        aa = update.message.chat.id
        shart = Pasport.objects.filter(Q(telefon_raqam=help_dict[aa][-9:]) | Q(telefon_raqam_2=help_dict[aa][-9:]))
        if shart:
            for x in shart.values():
                millat = Millat.objects.get(id=int(x['millat_id_id']))
                viloyat = Viloyat.objects.get(id=int(x['doimiy_viloyat_id']))
                tuman = Tuman.objects.get(id=int(x['doimiy_tuman_id']))
                talim_shakli = TalimShakli.objects.get(id=x['talim_shakli_id'])
                talim_yunalishi = YonalishOTM.objects.get(id=x['talim_yunalishi_id'])
                update.message.bot.send_photo(update.message.chat.id, open(x['photo'], 'rb'),
                                              caption=f"Ism: {x['ism']}\n"
                                                      f"Familiya: {x['familiya']}\n"
                                                      f"Otasining ismi: {x['sharif']}\n"
                                                      f"Pasport ma`lumoti: {x['pass_seriya']} {x['pass_raqam']}\n"
                                                      f"Millati: {millat}\n"
                                                      f"Telefon raqam: +998{x['telefon_raqam']}\n"
                                                      f"Yashash viloyati: {viloyat}\n"
                                                      f"Yashash tumani: {tuman}\n"
                                                      f"Doimiy manzil: {x['doimiy_manzil']}\n"
                                                      f"Ta`lim shakli: {talim_shakli}\n"
                                                      f"Ta`lim yo`nalishi: {talim_yunalishi}",
                                              reply_markup=ReplyKeyboardMarkup(
                                                  [[KeyboardButton('Mening ma`lumotlarim')]],
                                                  resize_keyboard=True))
        else:
            update.message.reply_text('Ma`lmotlaringiz bazada aniqlanmadi!')
    else:
        pass


dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(MessageHandler(Filters.contact, helper))
dispatcher.add_handler(MessageHandler(Filters.text, message_handler))

