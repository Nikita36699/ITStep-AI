# #LLM
# #LARGE LANGUAGE MODEL
# #Велика Мовна МОдель
#
#завантаження api key як змінну середовища
# import os
# import dotenv
#
#
#
# #завантаженна данних з файлу .env
# dotenv.load_dotenv()

#сам api key

# api_key = os.getenv('GEMINI_API_KEY')

#sama model LMM
import  langchain
from langchain_google_genai import GoogleGenerativeAI


# #створення моделі
# llm = GoogleGenerativeAI(
#     model='gemini-2.5-flash-lite', # назва моделі
#     api_key=api_key
# )
#
# #запуск моделі
# res = llm.invoke('привіт, що таке LLM?')
#
#
# print(res)


#як це працює
# ЗАПИТ: привіт, що таке LLM?
#Шматок відповіді: Привіт! LLM — це абревіатура від **Large Language Model**, що українською означає **Велика Мовна Модель**.

#Завдання моделі -- згенарувати наступне слове
# Для кожного відомого моделі слова генеруються ймовірность
#розшифрофуеться  30%
# це-             25%
# використовується 10%
# яблуко           0.00000001%


#
# #створення моделі,parametri kreativnosti
# llm = GoogleGenerativeAI(
#     model='gemini-2.5-flash-lite', # назва моделі
#     api_key=api_key,
#     top_k=10, # вибрати випадково наступне слово з 10 з найбільшою ймовірністю
#     top_p=0.8, # залишити ті слова, cума ймовырностей  яких не менше 80% та вибрати випадково наступне слово  серед них
#     temperature=1.2 # вища температура -- відсотки стають більш однаковими
#
# )

#temprature
# 0 - 0.3 -- низька креативність (відповіді як по медотичці)
# 0.7 - 1.2 -- cередня креативність(близько до людини)
#1.5 -  1.7 -- висока креативність(вигадає щось цікаве або збреше)
#>2 -- випадкові слова та 2 його максимум

# Завдання 1
# Підключіть модель LLM за допомогою свого API key.
# Попросіть модель згенерувати:
# ● відповідь на питання у вигляді одного слова(наприклад яка столиця Франції?)
# ● код python
# ● коротку історію
# Підберіть параметри креативності та довжини

#завантаження api key як змінну середовища
# import os
# import dotenv
# #sama model LMM
# from langchain_google_genai import GoogleGenerativeAI
#
#
#
# #завантаженна данних з файлу .env
# dotenv.load_dotenv()
#
# #сам api key
# api_key = os.getenv('GEMINI_API_KEY')
#
# #створення моделі
# llm = GoogleGenerativeAI(
#     model='gemini-2.5-flash-lite', # назва моделі
#     api_key=api_key,
#     temperature= 2
# )

# user_input = input('Your question: ')
# # response = llm.invoke(f'ДАЛЬШЕ ОТВЕТ НА ВОПРОС ЛИШЬ ОДНИМ СЛОВОМ!!!!!!САМ ВОПРОС ВОТ: {user_input}')
# # comand_py = 'write response as if you are IT-professor,but all i need is just a code'
# comand_story = 'напиши интересную историю не больше 5 предложени тему истории даю после двоиточия: '
#
# response = llm.invoke(comand_story + user_input)
# print(response)

# Завдання 2
# Прочитайте файл data\lesson9\rules.txt з правилами користування атракціону. Напишіть програму
# яка отримує від користувачі питання та дає відповідь на нього виходячи з текстового файлу.
# Для цього об’єднайте правила користування з питанням користувача.
# Користувач задає питання поки не введе порожній рядок.
# Змініть файл rules.txt, щоб переконатись що модель
# дійсно його читає.
#
# with open(r'data\lesson9\rules.txt', 'r', encoding='utf-8') as file:
#     rules =  file.read()
#
# user_question = input('enter your question: ')
#
#
# import os
# import dotenv
# #sama model LMM
# from langchain_google_genai import GoogleGenerativeAI
#
#
#
# #завантаженна данних з файлу .env
# dotenv.load_dotenv()
#
# #сам api key
# api_key = os.getenv('GEMINI_API_KEY')
#
# #створення моделі
# llm = GoogleGenerativeAI(
#     model='gemini-2.5-flash-lite', # назва моделі
#     api_key=api_key,
#     temperature= 0
# )
#
# respon = llm.invoke(f'give the answer on user question based only on {rules}, you giving anser on this question {user_question},'
#                     f' if the answer not connected with rules please say to user ask his question again ')
#
# print(respon)


# Завдання 3
# Створіть найпростіший чат бот. Напишіть моделі якого
# персонажа вона повинна вдавати(відомий актор, персонаж
# кіно\книги, тощо).
# Реалізуйте двома способами:
# 1. Модель отримує інструкцію в якому стилі відповідати
# та нове повідомлення.
# 2. Модель отримує інструкцію та історію попередніх
# повідомлень як від користувача, так і її власні відповіді у
# форматі
# Instruction: ….
# Human: massage1
# AI: message2
# Human: massage3
# AI: message4
# Human: massage5
# AI:

import os
import dotenv
#sama model LMM
from langchain_google_genai import GoogleGenerativeAI



#завантаженна данних з файлу .env
dotenv.load_dotenv()

#сам api key
api_key = os.getenv('GEMINI_API_KEY')

#створення моделі
llm = GoogleGenerativeAI(
    model='gemini-2.5-flash-lite', # назва моделі
    api_key=api_key,
    temperature= 0
)


history =  'Ты чат-бот которые отвечает от лица  Джеки Чана'

while True:
    user_question = input('enter your question: ')
    if user_question =='0':
        break
    else:
        history += f'\n Human: {user_question}'


    res = llm.invoke(f'{history} + {user_question}')
    print(res)
    history += f'\n AI: {res}'


