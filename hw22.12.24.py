import os
import dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage,
    BaseMessage
)
from typing import List

dotenv.load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
serper_api_key = os.getenv("SERPER_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=gemini_api_key,
)

searcher = GoogleSerperAPIWrapper(
    serper_api_key=serper_api_key,
    type="places"
)

def restaurant_search(query: str) -> str:
    """
    Пошук ресторанів за запитом.
    Повертає: назва, сайт (якщо є), рейтинг
    """
    results = searcher.results(query)

    formatted_result = ""

    for place in results.get("places", []):
        name = place.get("title", "Невідома назва")
        rating = place.get("rating", "Немає рейтингу")
        website = place.get("website", "Сайт відсутній")

        formatted_result += (
            f"Назва: {name}\n"
            f"Рейтинг: {rating}\n"
            f"Сайт: {website}\n"
            f"---------------------\n"
        )

    if not formatted_result:
        return "Немає відповідної інформації."

    return formatted_result



messages: List[BaseMessage] = [
    SystemMessage("""
    Ти — чат-бот з рекомендації ресторанів.
    Отримуй запит користувача та пропонуй ресторани.
    """)
]

while True:
    user_input = input("Введіть запит (наприклад: ресторани в Києві): ")

    if user_input == "":
        break

    messages.append(HumanMessage(user_input))

    restaurants = restaurant_search(user_input)

    ai_message = AIMessage(content=restaurants)
    messages.append(ai_message)

    print(ai_message.content)
