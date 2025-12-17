import os
import dotenv

from typing import List
from pydantic import BaseModel, Field
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser

# завантаження апі ключа
dotenv.load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# створити llm
llm = GoogleGenerativeAI(
    model='gemini-2.5-flash',
    api_key=api_key,
)


# Користувач задає питання.
# Потрібно дати відповіть та запропопонувати цікаві факти по тій
# же темі що і питання

# # варіант 1 -- все в один промпт
# prompt = PromptTemplate.from_template(
#     """
#     Ти -- чатбот для навчання. Твоя задача давати відповідь на питання.
#     Також потрібно запропонувати декілька цікавих фактів по тій же темі
#     що і питання
#
#     ### Питання
#     {question}
#     """
# )
#
# chain1 = prompt | llm
#
# response = chain1.invoke({
#     "question": "Коли була висадка на місяць"
# })
#
# print(response)


# варіант 2 -- розьити на 2 кроки
# дати відповідь та визначити тему питання
# згенерувати цікаві факти по темі

# пишемо парсер

# структура відповіді
class ParserResult(BaseModel):
    question_answer: str = Field(description="Answer to user question")
    topics: List[str] = Field(description="список пов'язаних тем до питання")


# створення парсера
parser = PydanticOutputParser(pydantic_object=ParserResult)

# інструкція для llm як має виглядати відповідь
instructions = parser.get_format_instructions()

prompt = PromptTemplate.from_template(
    """
    Ти -- чатбот для навчання. Твоя задача давати відповідь на питання.
    Також потрібно визначити теми які відносяться до цього питання

    ### Питання
    {question}

    ### ФОРМАТ ВІДПОВІДІ
    {instructions}
    """,
    partial_variables={"instructions": instructions}  # одразу передаємо інструкції
)

chain = prompt | llm | parser

question = input("Введіть питання: ")

response = chain.invoke({
    "question": question,
})

print(f"Відповідь: {response.question_answer}")


# print(response)
# print(type(response))
#
# print(response.question_answer)
# print(response.topics)

# генерація цікавих фактів на основі тем
class FactResponse(BaseModel):
    facts: List[str] = Field(description="список цікавих фактів розом з їхнім описом")


# створення парсера
parser = PydanticOutputParser(pydantic_object=FactResponse)

# інструкція для llm як має виглядати відповідь
instructions = parser.get_format_instructions()

prompt = PromptTemplate.from_template(
    """
    Ти -- генератор цікавих фактів. Твоя задача навести 5 цікавих фактів 
    на задані теми

    ### ТЕМИ
    {topics}

    ### ФОРМАТ ВІДПОВІДІ
    {instructions}
    """,
    partial_variables={"instructions": instructions}  # одразу передаємо інструкції
)

chain2 = prompt | llm | parser

response = chain2.invoke(
    {
        "topics": response.topics
    }
)

facts = response.facts

print("Цікаві факти")
for fact in facts:
    print(fact)

whole_chain = chain | chain2