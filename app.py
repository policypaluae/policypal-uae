import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from openai import OpenAI

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
You are PolicyPal UAE, an AI legal and policy briefing assistant.

Use public information only.
Prioritize official sources such as:
- UAE Government Portal
- UAE Aid Agency public website
- Official ministry websites

Do not provide legal advice.
If you are unsure about a specific UAE law or decree, clearly state that the information may require verification from official UAE legal sources.
Avoid inventing legal provisions or details.

Always respond in this format:
1. Summary
2. Key Points / Obligations
3. Why It Matters
4. Public Source Note
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! How can I assist you today with information on UAE laws, public policies, or updates related to the UAE Aid Agency?"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        temperature=0.3
    )

    answer = response.choices[0].message.content

    await update.message.reply_text(answer)

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == "__main__":
    main()
