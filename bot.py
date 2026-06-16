import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from agent import AIAgent

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

agent = AIAgent(openai_api_key=OPENAI_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "မင်္ဂလာပါ! ကျွန်တော်က သင်နဲ့ စကားပြောရင်း ကိုယ်တိုင် သင်ယူနိုင်တဲ့ AI Agent တစ်ခု ဖြစ်ပါတယ်။ "
        "ကျွန်တော့်ကို ဘာမဆို မေးမြန်းနိုင်သလို၊ ကျွန်တော့်ကို ပိုကောင်းအောင်လည်း အကြံပေးနိုင်ပါတယ်ခင်ဗျာ။"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
        
    user_id = update.effective_user.id
    user_message = update.message.text

    try:
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        ai_response = agent.process_message(user_id, user_message)
        await update.message.reply_text(ai_response)
    except Exception as e:
        logging.error(f"Error handling message: {e}")
        await update.message.reply_text("တောင်းပန်ပါတယ်၊ တစ်ခုခု မှားယွင်းသွားလို့ နောက်မှ ပြန်ကြိုးစားပေးပါခင်ဗျာ။")

if __name__ == '__main__':
    if not TELEGRAM_BOT_TOKEN or not OPENAI_API_KEY:
        print("Error: Please check your .env file for TELEGRAM_BOT_TOKEN and OPENAI_API_KEY.")
    else:
        application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
        
        application.add_handler(CommandHandler('start', start))
        application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
        
        print("Bot is running...")
        application.run_polling()
