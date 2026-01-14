# Завдання 1
# Напишіть додаток з чат ботом по допомозі з вивченням
# англійської мови.
#  Якщо користувач просить перекласти слово або
# фразу, то вивести переклад та приклад використання
# у речені
#  Якщо користувач просить перекласти речення, то
# вивести переклад та пояснення граматики, наприклад
# структура there is/are, пасивна форма дієслова, тощо

import streamlit as st
# ЧАТ-БОТ

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage,
)

# заголовок
st.title("English teacher")

# завантаження апі ключа за допомогою streamlit
api_key = st.secrets.get("GEMINI_API_KEY")

# створити llm
llm = ChatGoogleGenerativeAI(
    model='gemini-2.5-flash-lite',
    api_key=api_key,
)

user_query = st.chat_input("Ваше повідомлення")

# якщо це початок то створити історію в session state
if user_query is None:
    # історія повідомлень
    st.session_state['history'] = [
        # перше повідомлення з основними інструкціями(промпт)
        SystemMessage(
            """
            #### ROLE
            Ти — чат-бот-викладач англійської мови.
            
            #### TASK
            Твоя задача — допомагати користувачу вивчати англійську мову шляхом перекладу та пояснення граматики.
            
            #### INPUT TYPE
            Користувач може вводити:
            1) окреме слово або коротку фразу
            2) повне англійське речення
            
            #### INSTRUCTIONS
            Спочатку визнач тип запиту.
            
            Якщо це слово або коротка фраза:
            - Дай переклад українською
            - Наведи один приклад використання англійською
            - Додай переклад прикладу
            
            Використовуй формат:
            Слово/фраза: …
            Переклад: …
            Приклад: …
            Переклад прикладу: …
            
            Якщо це речення:
            - Дай повний переклад українською
            - Визнач граматичну структуру
            - Поясни правило простою мовою для початківця
            
            Використовуй формат:
            Речення: …
            Переклад: …
            Граматика: …
            Пояснення: …
            
           
            
            #### OUTPUT RULES
            - Відповідь повинна відповідати одному з форматів
            - Не додавай зайвих коментарів
            - Пояснення має бути простим та навчальним
            """
        )
    ]

# якщо повідомлення введено, то дати відповідь від моделі
if user_query:
    # переволимо повідомлення в HumanMessage
    human_message = HumanMessage(user_query)

    # добавляємо до історії повідомлень
    st.session_state['history'].append(human_message)

    # запускаємо модель
    response = llm.invoke(st.session_state['history'])

    # response -- AIMessage
    # добавляємо до історії повідомлень
    st.session_state['history'].append(response)


# вивести всю історію спілкування
for message in st.session_state['history']:
    # пропускаємо SystemMessage
    if isinstance(message, SystemMessage):
        continue

    # отримати вміст
    text = message.content

    # отримати роль
    if isinstance(message, HumanMessage):
        role = "human"
    else:
        role = 'ai'

    # вивести повідомлення з підписом
    with st.chat_message(role):
        st.markdown(text)