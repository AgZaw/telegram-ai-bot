# Self-Learning Telegram AI Agent

ဒီ Project ကတော့ ကိုယ်တိုင် လေ့လာသင်ယူနိုင်ပြီး ကိုယ်တိုင် ပြန်လည်ပြင်ဆင်နိုင်တဲ့ (Self-Learning & Self-Evolving) AI Agent တစ်ခုကို Telegram အတွက် တည်ဆောက်ထားတာ ဖြစ်ပါတယ်။

## Features

*   **Long-term Memory**: အသုံးပြုသူနဲ့ စကားပြောဖူးသမျှ အချက်အလက်တွေကို Database ထဲမှာ မှတ်သားထားပြီး နောက်ပိုင်းမှာ ပြန်အသုံးချနိုင်ပါတယ်။
*   **Self-Reflection**: AI Agent ကိုယ်တိုင်ရဲ့ လုပ်ဆောင်ချက်တွေကို ပြန်သုံးသပ်ပြီး သူ့ရဲ့ Instruction (System Prompt) တွေကို ပိုကောင်းအောင် ပြင်ဆင်နိုင်ပါတယ်။
*   **Knowledge Base (Placeholder)**: အသစ်အသစ်သော ဗဟုသုတတွေကို သိမ်းဆည်းထားနိုင်တဲ့ Database တစ်ခု ပါဝင်ဖို့ ရည်ရွယ်ထားပါတယ်။ (လက်ရှိ Version တွင် အပြည့်အစုံ မပါဝင်သေးပါ)

## Prerequisites (လိုအပ်ချက်များ)

ဒီ Bot ကို Run နိုင်ဖို့အတွက် အောက်ပါအချက်တွေ လိုအပ်ပါတယ်-

1.  **Python 3.9+**: သင့်စက်ထဲမှာ Python 3.9 သို့မဟုတ် အထက် Install လုပ်ထားဖို့ လိုအပ်ပါတယ်။
2.  **Telegram Bot Token**: Telegram မှာ @BotFather ကနေတစ်ဆင့် Bot အသစ်တစ်ခု တည်ဆောက်ပြီး ရရှိလာတဲ့ **HTTP API Token** ကို လိုအပ်ပါတယ်။
3.  **OpenAI API Key**: OpenAI ရဲ့ Chat Completion API ကို အသုံးပြုထားတာဖြစ်လို့ OpenAI API Key တစ်ခု လိုအပ်ပါတယ်။ (GPT-4o သို့မဟုတ် အခြား Model များကို အသုံးပြုနိုင်ရန်)

## Installation (ထည့်သွင်းခြင်း)

1.  **Project ကို Download လုပ်ပါ**: 
    ```bash
    git clone <repository_url> # သို့မဟုတ် ဒီ Code တွေကို Zip အနေနဲ့ Download လုပ်ပါ
    cd telegram_ai_agent
    ```

2.  **Dependencies များ Install လုပ်ပါ**: 
    ```bash
    pip install -r requirements.txt
    ```
    (လက်ရှိတွင် `requirements.txt` မရှိသေးပါ၊ အောက်ပါအတိုင်း install လုပ်နိုင်ပါတယ်)
    ```bash
    pip install python-telegram-bot openai sqlalchemy
    ```

## Setup (ပြင်ဆင်ခြင်း)

1.  **Environment Variables သတ်မှတ်ပါ**: 
    သင့်ရဲ့ `TELEGRAM_BOT_TOKEN` နဲ့ `OPENAI_API_KEY` များကို Environment Variables အနေနဲ့ သတ်မှတ်ပေးရပါမယ်။
    
    Linux/macOS အတွက်:
    ```bash
    export TELEGRAM_BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
    export OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
    ```
    
    Windows အတွက် (Command Prompt):
    ```bash
    set TELEGRAM_BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
    set OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
    ```
    
    (သို့မဟုတ်) `.env` file ကို အသုံးပြုနိုင်ပါတယ်။ `python-dotenv` library ကို install လုပ်ပြီး `bot.py` file ထဲမှာ `load_dotenv()` ကို ထည့်သွင်းအသုံးပြုနိုင်ပါတယ်။

## How to Run (အသုံးပြုပုံ)

Environment Variables တွေ သတ်မှတ်ပြီးသွားရင် အောက်ပါ Command နဲ့ Bot ကို စတင် Run နိုင်ပါတယ်-

```bash
python bot.py
```

Bot စတင်အလုပ်လုပ်ပြီဆိုရင် Telegram မှာ သင့် Bot ကို စတင်အသုံးပြုနိုင်ပါပြီ။

## Project Structure (Project ဖွဲ့စည်းပုံ)

*   `database.py`: SQLite Database ကို အသုံးပြုပြီး Conversation History, Knowledge Base နဲ့ Agent ရဲ့ System Prompt တွေကို သိမ်းဆည်းပါတယ်။
*   `agent.py`: Core AI Agent Logic တွေ ပါဝင်ပါတယ်။ OpenAI API ကို အသုံးပြုပြီး စကားပြောခြင်း၊ Conversation History ကို စီမံခန့်ခွဲခြင်း၊ Self-Reflection လုပ်ဆောင်ခြင်းတို့ ပါဝင်ပါတယ်။
*   `bot.py`: Telegram Bot ကို စတင်ခြင်း၊ User ရဲ့ Message တွေကို လက်ခံခြင်း၊ AI Agent ကို ခေါ်ယူပြီး ပြန်ဖြေခြင်းတို့ကို လုပ်ဆောင်ပါတယ်။

## Future Improvements (နောက်ထပ် တိုးတက်မှုများ)

*   **Enhanced Knowledge Base**: အချက်အလက်အသစ်တွေကို Bot ကိုယ်တိုင် ရှာဖွေပြီး Knowledge Base ထဲ ထည့်သွင်းနိုင်အောင် လုပ်ဆောင်ခြင်း။
*   **User Feedback Integration**: User တွေရဲ့ Feedback တွေကို အခြေခံပြီး Bot ရဲ့ စွမ်းဆောင်ရည်ကို တိုးတက်အောင် လုပ်ဆောင်ခြင်း။
*   **More Sophisticated Self-Reflection**: ပိုမိုရှုပ်ထွေးတဲ့ Self-Reflection Mechanism တွေ ထည့်သွင်းခြင်း။
*   **Error Handling and Logging**: ပိုမိုကောင်းမွန်တဲ့ Error Handling နဲ့ Logging စနစ်များ ထည့်သွင်းခြင်း။
