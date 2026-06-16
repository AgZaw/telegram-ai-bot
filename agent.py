import requests
import json
from database import save_message, get_history, update_system_prompt, get_system_prompt

class AIAgent:
    def __init__(self, openai_api_key):
        # .env ထဲက OPENAI_API_KEY နေရာမှာ Gemini API Key ထည့်ထားတာမို့ ၎င်းကိုပဲ ဆက်သုံးပါမယ်
        self.api_key = openai_api_key
        self.system_prompt = get_system_prompt()
        # Google Gemini API Endpoint URL သို့ ပြောင်းလဲခြင်း
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={self.api_key}"

    def _get_llm_response(self, messages):
        headers = {
            "Content-Type": "application/json"
        }
        
        # OpenAI Format မှ Gemini Format သို့ ပြောင်းလဲတည်ဆောက်ခြင်း
        contents = []
        system_instruction = None

        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            
            if role == "system":
                system_instruction = {"parts": [{"text": content}]}
            elif role == "user":
                contents.append({"role": "user", "parts": [{"text": content}]})
            elif role == "assistant":
                contents.append({"role": "model", "parts": [{"text": content}]})

        # Request Data တည်ဆောက်ခြင်း
        data = {
            "contents": contents,
            "generationConfig": {
                "temperature": 0.7
            }
        }
        
        if system_instruction:
            data["systemInstruction"] = system_instruction

        try:
            response = requests.post(self.api_url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            # Gemini ရဲ့ Response JSON မှ စာသားကို ဆွဲထုတ်ခြင်း
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        except Exception as e:
            print(f"Error getting Gemini LLM response: {e}")
            return "Sorry, I'm having trouble processing that right now."

    def process_message(self, user_id, user_message):
        save_message(user_id, "user", user_message)
        history = get_history(user_id, limit=5)
        
        messages = [{"role": "system", "content": self.system_prompt}]
        for msg in history:
            messages.append(msg)
        messages.append({"role": "user", "content": user_message})

        ai_response = self._get_llm_response(messages)
        save_message(user_id, "assistant", ai_response)
        
        # Self-reflection logic
        try:
            self.reflect_and_improve(user_id, user_message, ai_response)
        except:
            pass
            
        return ai_response

    def reflect_and_improve(self, user_id, user_message, ai_response):
        reflection_prompt = (
            f"Evaluate the assistant's response and suggest a better system prompt in JSON format: "
            f"{{\"evaluation\": \"...\", \"suggestion\": \"...\"}}. "
            f"User: {user_message} Assistant: {ai_response}"
        )
        reflection_messages = [
            {"role": "system", "content": "You are a performance evaluator for AI agents."},
            {"role": "user", "content": reflection_prompt}
        ]
        
        reflection_result = self._get_llm_response(reflection_messages)
        try:
            # Clean potential markdown
            if "```json" in reflection_result:
                reflection_result = reflection_result.split("```json")[1].split("```")[0].strip()
            elif "```" in reflection_result:
                reflection_result = reflection_result.split("```")[1].split("```")[0].strip()
            
            reflection_data = json.loads(reflection_result)
            suggestion = reflection_data.get("suggestion", "")
            
            if suggestion and "system prompt" in suggestion.lower():
                new_prompt = self._get_llm_response([
                    {"role": "system", "content": "Write a concise system prompt (max 2 sentences) based on this suggestion. Only return the text."},
                    {"role": "user", "content": suggestion}
                ])
                if new_prompt and len(new_prompt) > 5:
                    update_system_prompt(new_prompt)
                    self.system_prompt = new_prompt
        except:
            pass
