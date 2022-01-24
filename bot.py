from manipulate import manipulate


import traceback
import os
import telegram
from telegram.ext import MessageHandler, Updater, CommandHandler
import json


def pprint(name, obj):

    try:
        s = json.dumps(obj, indent=4)
    except Exception as e:
        s = "no json: " + str(obj)

    print("---")
    print(name, ": ", s)
    print("---")

def hello(update, context):
    
    pprint("context", context)
    pprint("update", update)
    pprint("chat_data", context.chat_data)

    text = update["message"]["text"]
    print(text)

    msg = f"""Hello {update['message']['chat']['first_name']}!\n\nSend me a file and I will send you a slightly modified version. It will look the same to a human but completely different to a machine. This can hopefully be used to circumvent online censorship such as upload-filters. Your file will be stored on my server only to process it - it will be deleted afterwards.\n\n(note that this I am in an early stage of development...)"""

    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)



def handle_msg(update, context):
 

    try:
        res_set = False
        dlf_set = False
        text = update["message"]["text"]

        try:
            fid = update["message"]["document"]["file_id"]
        except:
            context.bot.send_message(chat_id=update.effective_chat.id, text="I received your message, but it doesnt seem to be a file")
            return

        fid = update["message"]["document"]["file_id"]
        received_file = context.bot.getFile(fid)
        dlf = received_file.download()
        dlf_set = True
        success, res = manipulate(dlf)

        if success:
            res_set = True
            with open(res, "rb") as f:
                context.bot.send_document(chat_id=update.effective_chat.id, document=f,disable_content_type_detection=True)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text=res)
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text="server error")
        print("<<<<<<<<<<<<ERROR:")
        pprint("context", context)
        pprint("update", update)
        pprint("chat_data", context.chat_data)
        print(traceback.format_exc())
        print("ERROR>>>>>>>>>>>>>>")
    finally:
        if res_set:
            os.remove(res)
        if dlf_set:
            os.remove(dlf)

    
def main():

    api_key = os.getenv("TELEGRAM_BOT_TOKEN")
    bot = telegram.Bot(token=api_key)
    print(bot.get_me())

    updater = Updater(token=api_key, use_context=True)

    start_handler = CommandHandler("start", hello)
    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(MessageHandler(telegram.ext.filters.Filters.update,callback=handle_msg))
    updater.start_polling()


if __name__=="__main__":
    main()

