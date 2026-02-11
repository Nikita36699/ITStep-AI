import os
import re
import dotenv
import streamlit as st

from sqlalchemy import create_engine
from pinecone import Pinecone

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore

from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit

from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langgraph.prebuilt import create_react_agent



# Streamlit (FIRST COMMAND)

st.set_page_config(page_title="Car Rental Bot", page_icon="🚗", layout="centered")



# ENV

dotenv.load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

DB_USER = os.getenv("user")
DB_PASSWORD = os.getenv("password")
DB_HOST = os.getenv("host")
DB_PORT = os.getenv("port")
DB_NAME = os.getenv("dbname")

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    "?sslmode=require"
)
engine = create_engine(DATABASE_URL)



# Pinecone + RAG

INDEX_NAME = "car-rules"
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(INDEX_NAME)

emb_query = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    google_api_key=GEMINI_API_KEY,
    task_type="RETRIEVAL_QUERY",
    output_dimensionality=768,
)

vector_store = PineconeVectorStore(index=index, embedding=emb_query)


@tool
def rules_search(query: str, k: int = 4) -> str:
    """Поиск по регламенту аренды (RAG Pinecone). Возвращает релевантные фрагменты текста."""
    docs = vector_store.similarity_search(query, k=k)
    if not docs:
        return "EMPTY"
    return "\n\n---\n\n".join(d.page_content for d in docs)



# LLM + SQL Toolkit

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    google_api_key=GEMINI_API_KEY,
    temperature=0.2,
)

db = SQLDatabase(
    engine,
    include_tables=["cars", "brands"],
    sample_rows_in_table_info=2,
)

sql_toolkit = SQLDatabaseToolkit(db=db, llm=llm)
sql_tools = sql_toolkit.get_tools()

tools = sql_tools + [rules_search]
agent = create_react_agent(llm, tools=tools)


SYSTEM = SystemMessage(content="""
#### ROLE
Ты — ассистент сервиса аренды автомобилей.

#### DATA SOURCES
- База данных (Postgres/Supabase): таблицы cars, brands. Доступ через SQL tools.
- Регламент (Pinecone): доступ через rules_search.

#### CURRENCY (IMPORTANT)
- Любые суммы/цены в диалоге считай в долларах США.
- Всегда показывай цены как USD, используй символ $.
- Не задавай уточняющих вопросов про валюту, просто явно отмечай это в ответе.

#### IMPORTANT DB NOTES 
- В таблице cars поле status хранится как "availible" (опечатка + иногда с кавычками).
  Поэтому для доступных авто используй фильтр:
  REPLACE(LOWER(status), '\"', '') = 'availible'
- transmission в БД часто 'auto' / 'manual'
- class в БД: economy / comfort / business / premium / suv / minivan
- “легковой / легковушка / седан” = НЕ suv и НЕ minivan
  => WHERE LOWER(class) NOT IN ('suv','minivan')

#### BRAND DESCRIPTION
- Текстовое описание есть в brands.description (это описание БРЕНДА).
- В cars поля description НЕТ.
- Если пользователь просит "описание машины" — делай JOIN на brands и возвращай:
  (1) параметры авто из cars + (2) brands.description как описание бренда.

#### JOIN RULE
- Если в cars есть brand_id (uuid) — JOIN строго по FK:
  LEFT JOIN brands b ON b.id = c.brand_id
- Если brand_id отсутствует/пустой, то JOIN по названию:
  LEFT JOIN brands b ON LOWER(c.brand)=LOWER(b.name)
- Если не уверен, используй безопасный вариант с COALESCE (см. SQL ниже).

#### TOOL BUDGET (HARD LIMIT)
- На 1 ответ: максимум 1 SQL SELECT с LIMIT.
- На 1 ответ: максимум 1 rules_search.
- Если вопрос про правила/штрафы/залог/возврат/страховку — rules_search ОБЯЗАТЕЛЕН.
- Никаких UPDATE/DELETE/CREATE.

#### TOOL USAGE POLICY
1) Про машины / наличие / подбор / параметры конкретных моделей -> SQL tools
2) Про штрафы / залог / возврат / правила -> rules_search
3) Всегда делай SELECT с LIMIT (обычно 10).

#### OUTPUT STYLE (STRICT)
- Если пользователь пишет "привет/здравствуйте" без запроса:
  коротко поздоровайся и предложи 3 типа вопросов: подбор авто, бренд, правила.
  добавь: "Все суммы считаю в USD ($)."
  спроси: "Что именно интересует?"

- Для подбора авто (ОБЯЗАТЕЛЬНЫЙ ФОРМАТ):
  1) первая строка: "Нашёл вариантов: N (все цены в USD $)"
  2) далее КАЖДАЯ машина СТРОГО с новой строки и СТРОГО начиная с "-- ":
     -- BRAND MODEL — CLASS | $PRICE/день | SEATS мест | FUEL | TRANSMISSION
  3) пустая строка
  4) вопрос: "Подходит ли один из вариантов? Если нет — уточните бюджет ($)/класс/места/коробку."

- Для вопросов по конкретным моделям:
  ответь конкретно по каждой модели (коробка + места), построчно, каждая строка с "-- ".

#### NO GARBAGE
- Не показывай сырой SQL и не показывай сырые словари Python.
- Не склеивай несколько машин в одну строку.
- Не выдумывай факты.
""".strip())



# Streamlit UI

st.title("🚗 Чат-бот аренды авто")

if "messages" not in st.session_state:
    st.session_state.messages = []  # {"role": "user"/"assistant", "content": str}

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("🧹 Очистить чат"):
        st.session_state.messages = []
        st.rerun()
with col2:
    st.caption("Supabase + Pinecone + Gemini")

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"].replace("\n", "  \n"))

user_text = st.chat_input("Напиши запрос: например «Подбери легковую до 100$»")


def as_text(msg) -> str:
    c = getattr(msg, "content", msg)
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        out = []
        for part in c:
            if isinstance(part, dict) and part.get("type") == "text":
                out.append(part.get("text", ""))
        return "\n".join(out).strip()
    return str(c)


def prettify_answer(text: str) -> str:
    t = (text or "").strip()
    # гарантируем, что каждый пункт начинается с новой строки "-- "
    t = re.sub(r"(?<!^)\s*--\s*", "\n-- ", t).lstrip()
    # чуть сжать лишние пустые строки
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t


if user_text:
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)

    history = st.session_state.messages[-12:]
    agent_messages = [SYSTEM]
    for m in history:
        if m["role"] == "user":
            agent_messages.append(HumanMessage(content=m["content"]))
        else:
            agent_messages.append(AIMessage(content=m["content"]))

    with st.chat_message("assistant"):
        with st.spinner("Думаю..."):
            result = agent.invoke(
                {"messages": agent_messages},
                config={"recursion_limit": 4},
            )

            msgs = result["messages"]
            answer = ""
            for msg in reversed(msgs):
                txt = as_text(msg).strip()
                if txt:
                    answer = txt
                    break

            if not answer:
                answer = "Не смог сформировать ответ. Уточните, что именно по возврату интересует?"

            answer = prettify_answer(answer)
            st.markdown(answer.replace("\n", "  \n"))

    st.session_state.messages.append({"role": "assistant", "content": answer})



