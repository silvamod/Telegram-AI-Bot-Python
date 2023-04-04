import telegram.ext
import requests
Token = "INSERT_TOKEN_HERE"
updater = telegram.ext.Updater("INSERT_TOKEN_HERE",use_context=True)
dispatcher = updater.dispatcher

def start(update,context):
    update.message.reply_text("Hello, what can i do for you?\nType /ask and your request after")

def help(update,context):
    update.message.reply_text("To start using this bot, type /ask and your request after")

def ask(update,context):
    input_txt = update.message.text
    saveLogs(update)
    if(len(input_txt.split('/ask ')) == 1):
        update.message.reply_text("Please enter your request after the command /ask with a space.")
    else:
        input_txt_value = input_txt.split('/ask ')[1]
        context.bot.send_chat_action(chat_id= update.effective_message.chat_id, action=telegram.ChatAction.TYPING)
        r = requests.get('https://api.mcai.lol/get-result?query='+ input_txt_value)
        update.message.reply_text(r.text.replace("\\n","\n").replace("\"","") + "\n \n@WhosaAI")
        
def saveLogs(update):
    file = open('logs.txt', 'a', encoding="utf-8")
    if(update.message.chat.type == "private"):
        Type = ""
    else:
        Type = update.message.chat.title
    chat_id = str(update.message.from_user.id) if(update.message.from_user.id) else ""
    first_name = str(update.message.from_user.first_name) if(update.message.from_user.first_name) else ""
    last_name = str(update.message.from_user.last_name) if(update.message.from_user.last_name) else ""
    username = str(update.message.from_user.username) if(update.message.from_user.username) else ""
    file.write("Group: "+ Type +" Chat_id = " +chat_id +" first_name = " + first_name +" last_name = "+last_name + " username = "+ username +" Msg = ")
    file.write(update.message.text)
    file.write("\n")
    file.close()
    print(update.message)


dispatcher.add_handler(telegram.ext.CommandHandler("start",start))
dispatcher.add_handler(telegram.ext.CommandHandler("help",help))
dispatcher.add_handler(telegram.ext.CommandHandler("ask",ask))

updater.start_polling()
updater.idle()
