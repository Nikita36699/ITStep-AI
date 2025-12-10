# Завдання 1
# Прочитайте файл data\lesson9\return_policy.txt Та
# напишіть простий чат бот для відповідей на питання
# користувачів стосовно повернення товару. Діалог завершується
# коли користувач вводить порожній рядок.
# Передавайте усю історію спілкування у форматі:
# Instruction: ….
# Human: massage1
# AI: message2
# Human: massage3
# AI: message4
# Human: massage5
# AI:



import os
import dotenv
from langchain_google_genai import GoogleGenerativeAI

dotenv.load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

llm = GoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    api_key=api_key,
    temperature=0
)


with open(r"data\lesson9\return_policy.txt", "r", encoding="utf-8") as file:
    return_policy = file.read()


instruction = (
    "Ти чат-бот служби підтримки магазину. "
    "Всі твої відповіді повинні строго відповідати правилам повернення товару. "
    "Правила повернення:\n"
    f"{return_policy}\n\n"
    "Якщо питання не стосується повернення товару - ввічливо попроси ставити запитання "
    "лише з теми повернення.\n"
    "Формат діалогу:\n"
    "Instruction: ...\n"
    "Human: ...\n"
    "AI: ...\n"
)

history = f"Instruction: {instruction}\n"

while True:
    user_question = input("Enter your question: ")

    if user_question == "":
        print("Діалог завершено.")
        break

    history += f"Human: {user_question}\n"

    response = llm.invoke(history)
    print(response)
    history += f"AI: {response}\n"
