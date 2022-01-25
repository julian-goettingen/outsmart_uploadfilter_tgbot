from manipulate import manipulate


import traceback
import os
import telegram
from telegram.ext import MessageHandler, Updater, CommandHandler
import json
from collections import defaultdict


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

    msg = f"""Hello {update['message']['chat']['first_name']}!\n\nSend me a file and I will send you a slightly modified version. It will look the same to a human but completely different to a machine. This can hopefully be used to circumvent online censorship such as upload-filters. Your file will be stored on my server only to process it - it will be deleted afterwards.\n\n(note that I am in an early stage of development...)"""

    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

def find_file_id_in_dict_rec(d, res):

    for k,v in d.items():
        assert(isinstance(k,str))
        if k=="file_id":
            assert(isinstance(v,str))
            res.append(v)
        elif isinstance(v,dict):
            find_file_id_in_dict_rec(v, res)
        elif isinstance(v,list):
            for item in v:
                find_file_id_in_dict_rec(item, res)

    return res

def find_file_id_in_dict(d):

    return find_file_id_in_dict_rec(d,res=[])
    

# returns a list of file_id in the update, quite possibly empty
def get_file_id(update):

    su = str(update)
    su = su.replace("'",'"')
    su = su.replace("False", "false")
    su = su.replace("True", "true")
    su = su.replace("None", "null")
    jsonu = json.loads(su)
    
    return find_file_id_in_dict(jsonu)
 

def num_files_str(num):

    if num == 0:
        return "no files"
    if num == 1:
        return "a file"
    return f"{num} files"


def handle_msg(update, context):


    to_delete = []
    try:
        pprint("context", context)
        pprint("update", update)
        pprint("chat_data", context.chat_data)

        text = update["message"]["text"]

        
        file_ids = get_file_id(update)
        if not file_ids:
            context.bot.send_message(chat_id=update.effective_chat.id, text="I received your message, but it doesnt seem to be a file")
            return
        
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"found {num_files_str(len(file_ids))} in your message (this might include things like thumbnails). Processing...")

        for fid in file_ids:

            received_file = context.bot.getFile(fid)
            dlf = received_file.download()
            to_delete.append(dlf)
            success, res = manipulate(dlf)

            if success:
                to_delete.append(res)
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
        for f in to_delete:
            os.remove(f)


    
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

