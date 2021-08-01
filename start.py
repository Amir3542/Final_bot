from telegram.ext import *
from const import TOKEN
from func import *

u = Updater(token=TOKEN, workers=4)
d = u.dispatcher
d.add_handler(CommandHandler('start', callback=start, run_async=True))
d.add_handler(CommandHandler('help', callback=helpa, run_async=True))
d.add_handler(CallbackQueryHandler(pattern='rus', callback=rus))
d.add_handler(CallbackQueryHandler(pattern='eng', callback=eng))
d.add_handler(MessageHandler(Filters.text, txt_answ))
d.add_handler(MessageHandler(Filters.location, location))
u.start_polling(drop_pending_updates=True)
