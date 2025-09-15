from groq import Groq
from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv

load_dotenv("sai.env")  
app= Flask(__name__)

API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise ValueError("API_KEY is missing! Please set it in sai.env or Render env variables.")

client = Groq(api_key=API_KEY)

conversation=[
    {"role":"system", "content":"You are a helpful assistant."}
]

def chat_with_groq(prompt):
    
    conversation.append({"role":"user", "content": str(prompt)})
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  
        messages=conversation
        # [
        #     {"role": "system", "content": "You are a helpful assistant."},
        #     {"role": "user", "content": prompt}
        # ]
    )
    bot_reply= response.choices[0].message.content # .strip()
    if not bot_reply or not isinstance(bot_reply, str):
        bot_reply = "Sorry, I couldn’t generate a response."
    
    conversation.append({"role":"assistant", "content":bot_reply})
    print("Conversation so far:", conversation)
    return bot_reply


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    # data= request.get_json()
    user_prompt= request.json["message"]
    bot_reply= chat_with_groq(user_prompt)
    
    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(debug=True, port=5001)

    
    # while True:
    #     user_input = input("Sir - ")
    #     if user_input.lower() in ["exit", "quit", "bye","bye jarvis"]:
    #         break
    #     print("Bot -", chat_with_groq(user_input))
