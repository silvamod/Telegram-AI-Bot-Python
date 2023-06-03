import telegram.ext
import requests
import constants
Token = constants.TOKEN
updater = telegram.ext.Updater(Token,use_context=True)
dispatcher = updater.dispatcher

def start(update,context):
    update.message.reply_text(constants.START_MSG)

def help(update,context):
    update.message.reply_text(constants.HELP_MSG)

def ask(update,context):
    input_txt = update.message.text
    saveLogs(update)
    split_input = input_txt.split(constants.COMMAND_SPLIT)
    if(len(split_input) == 1):
        update.message.reply_text(constants.COMMAND_ERROR_MSG)
    else:
        input_txt_value = split_input[1]
        context.bot.send_chat_action(chat_id= update.effective_message.chat_id, action=telegram.ChatAction.TYPING)
        r = requests.get(constants.GET_PROMPT_URL+ input_txt_value)
        update.message.reply_text(r.text.replace("\\n","\n").replace("\"",constants.EMPTY_STR) + "\n \n@WhosaAI")
        
def saveLogs(update):
    file = open(constants.LOG_FILE_PATH, 'a', encoding= constants.UTF_ENCODE)
    if(update.message.chat.type == constants.PRIVATE_CHAT_TYPE):
        Type = constants.EMPTY_STR
    else:
        Type = update.message.chat.title
    chat_id = str(update.message.from_user.id) if(update.message.from_user.id) else constants.EMPTY_STR
    first_name = str(update.message.from_user.first_name) if(update.message.from_user.first_name) else constants.EMPTY_STR
    last_name = str(update.message.from_user.last_name) if(update.message.from_user.last_name) else constants.EMPTY_STR
    username = str(update.message.from_user.username) if(update.message.from_user.username) else constants.EMPTY_STR
    file.write("Group: "+ Type +" Chat_id = " +chat_id +" first_name = " + first_name +" last_name = "+last_name + " username = "+ username +" Msg = ")
    file.write(update.message.text)
    file.write("\n")
    file.close()
    print(update.message)


dispatcher.add_handler(telegram.ext.CommandHandler(constants.START,start))
dispatcher.add_handler(telegram.ext.CommandHandler(constants.HELP,help))
dispatcher.add_handler(telegram.ext.CommandHandler(constants.ASK,ask))

updater.start_polling()
updater.idle()