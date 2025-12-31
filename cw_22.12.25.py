# # створення агентів
# # агент -- чат-бот(llm) + інструменти
#
# import os
# import dotenv
#
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_community.utilities import GoogleSerperAPIWrapper
# from langgraph.prebuilt import create_react_agent
# from langchain_core.messages import (
#     HumanMessage,
#     AIMessage,
#     SystemMessage,
#     trim_messages, BaseMessage
# )
#
# # завантаження апі ключа
# dotenv.load_dotenv()
# gemini_api_key = os.getenv("GEMINI_API_KEY")
# serper_api_key = os.getenv("SERPER_API_KEY")
#
# # створити llm
# llm = ChatGoogleGenerativeAI(
#     model='gemini-2.5-flash',
#     api_key=gemini_api_key,
# )
#
#
# # інструмент -- функція
# # обов'язкова документація
#
# def product(a: int, b: int) -> int:
#     """
#     Множить 2 цілих числа то повертає їхній добуток
#
#     :param a: перше число
#     :param b: друге число
#     :return: добуток чисел
#     """
#     print("hello from product")
#     return a * b
#
#
# def get_weather(city: str, time: str) -> str:
#     """
#     Повертає інформацію про погоду у місті в певний час доби
#
#     :param city: назва міста
#     :param time: час доби(наприклад ранок, вечір, 10:30, 4 години дня)
#     :return: інформація про погоду
#     """
#     print("hello from get_weather")
#     return f"У {city} о {time} буде сонячно"
#
#
# #---------------------------------------------------------------------------------------
# # Завдання 1
# # Напишіть функцію яка перевіряє складність паролю:
# #  кількість символів(>8)
# #  наявність хоча б однієї літери\цифри\спеціального символу
# #  наявність літер в різних регістрах
# # Функція повертає тест з описом паролю(що добре, а що погано)
# # На основі цієї функції створіть агента.
# def check_password(password: str) -> dict:
#     """
#     Функція перевіряє якість паролю по заданним критеріям
#
#
#     :param password: пароль від юзера для перевірки
#     :return: словник з данними по чому пароль  прозоде а по чому ні
#     """
#
#     password_info = {}
#     if len(password) <= 8:
#         password_info['довжинна паролю'] = "Погано,довжина має бути більшою за 8 сімволів"
#     else:
#         password_info['довжинна паролю'] = "добре!"
#
#     flag_alpha = False
#     flag_number = False
#     flag_special = False
#
#     for alpha in password:
#         if alpha.isalpha():
#             flag_alpha = True
#
#         elif alpha.isdigit():
#             flag_number = True
#
#         else:
#             flag_special = True
#
#     password_info['чи є буква'] = flag_alpha
#     password_info['чи є цифра'] = flag_number
#     password_info['чи є спец символ'] = flag_special
#
#     return password_info
#
#
# # інструмент для пошуку в інтернеті
# searcher = GoogleSerperAPIWrapper(serper_api_key=serper_api_key)
#
#
# def search(query: str) -> str:
#     """
#     Шукає інформацію в інтернеті за запитом користувача
#
#     :param query: запит користувача
#     :return: результати пошуку
#     """
#
#     results = searcher.results(query)
#     print(results)  # результати пошуку
#
#     return results
#
#
# #---------------------------------------------------------------------------------------
# # Завдання 2
# # Напишіть модель показує останні новини про певну людину. Якщо користувач вводить не ім’я людини, то вивести повідомлення «немає відповідної інформації»
# # Скористайтесь DuckDuckGoSearchRun
# def search_name(name: str) -> str:
#
#
#
#
# # створення агента
# agent = create_react_agent(
#     model=llm,  # мовна модель
#     tools=[product, get_weather, search, check_password]
# )
#
# # історія повідомлень + інструкції
#
# messages = [
#     SystemMessage(
#         """
#         Ти ввічлий чат-бот. Твоя задача давати інформативні та чіткі відповіді
#         на запити користувача.
#
#         У тебе є доступ до таких інструментів:
#         * product
#         * get_weather
#         * search -- завжди давай посилання на новини
#         """
#     )
# ]
#
# while True:
#     user_query = input("Ви: ")
#
#     if user_query == '':
#         break
#
#     # переводимо str рядок у  HumanMessage
#     human_message = HumanMessage(user_query)
#
#     # добавляємо повідослення користувача до історії
#     messages.append(human_message)
#
#     # застосування агента
#     # треба передавати словник
#     input_data = {
#         "messages": messages
#     }
#
#     response = agent.invoke(input_data)
#     # response -- словник з усією історією + відповідь моделі
#
#     # отримання всіє історії повідомлень
#     messages = response['messages']
#
#     # отримати фінальну відповідь моделі
#     answear = messages[-1]
#     print(answear.content)
#
#     # виведемння всієї історії
#     print()
#     print("Історія")
#
#     for message in messages:
#         print(repr(message))

# створення агентів
# агент -- чат-бот(llm) + інструменти

import os
import dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import GoogleSerperAPIWrapper
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage,
    trim_messages, BaseMessage
)

# завантаження апі ключа
dotenv.load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
serper_api_key = os.getenv("SERPER_API_KEY")

# створити llm
llm = ChatGoogleGenerativeAI(
    model='gemini-2.5-flash-tts',
    api_key=gemini_api_key,
)


# інструмент -- функція
# обов'язкова документація
searcher = GoogleSerperAPIWrapper(serper_api_key=serper_api_key)



# ---------------------------------------------------------------------------------------
# Завдання 2
# Напишіть модель показує останні новини про певну людину. Якщо користувач вводить не ім’я людини, то вивести повідомлення «немає відповідної інформації»
# Скористайтесь DuckDuckGoSearchRun
def search_name(name: str) -> str:
    """
    Шукає інформацію в інтернеті останні новини  про певну людину

    :param name: ім'я людини
    :return:  результати пошуки
    """

    result = searcher.run(f"останні новини про {name}")
    return result



# створення агента
agent = create_react_agent(
    model=llm,  # мовна модель
    tools=[search_name]
)

# історія повідомлень + інструкції

messages = [
    SystemMessage(
        """
        Ти агент з пошуку інформації про людей.Твоя задача знайти в інтернеті інформацію про людину по її імені.
        Якщо користувач вводить не ім’я людини, то вивести повідомлення «немає відповідної інформації»
        
        У тебе є доступ до таких інструментів:
        *search_name
        """
    )
]

while True:
    user_query = input("Ви: ")

    if user_query == '':
        break

    # переводимо str рядок у  HumanMessage
    human_message = HumanMessage(user_query)

    # добавляємо повідослення користувача до історії
    messages.append(human_message)

    # застосування агента
    # треба передавати словник
    input_data = {
        "messages": messages
    }

    response = agent.invoke(input_data)
    # response -- словник з усією історією + відповідь моделі

    # отримання всіє історії повідомлень
    messages = response['messages']

    # отримати фінальну відповідь моделі
    answear = messages[-1]
    print(answear.content)

    # виведемння всієї історії
    print()
    print("Історія")

    for message in messages:
        print(repr(message))





#---------------------------------------------------------------------------------------
# Завдання 3
# Напишіть модель яка конвертує одну валюту в іншу за нинішнім курсом. Для цього напишіть функції, яка отримує номінал та курс і робить конвертацію.
# Практичне завдання
# Реалізуйте 2 ланцюга:
#  перший отримує назви валют та шукає курс в
# інтернеті
#  другий отримує номінал та курс і застосовує функцію
# ковертації


#---------------------------------------------------------------------------------------
# Завдання 4
# Напишіть модель яка рекомендує міста для проведення
# вихідних. Користувач вводить назву країни та стиль
# відпочинку.
# Перший агент шукає популярні міста для відпочинку в
# потрібному стилі.
# Другий агент перевіряє погоду в цих містах та відсіює
# невдалі варіанти
# Третій агент виводить кожне місто що залишилось, та
# причину чому його варто відвідати(коротко)


