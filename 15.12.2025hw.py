import os
import dotenv

from typing import List
from pydantic import BaseModel, Field
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser

dotenv.load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

llm = GoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=api_key,
)



class ExerciseResponse(BaseModel):
    exercises: List[str] = Field(description="Список вправ для досягнення мети тренування")


exercise_parser = PydanticOutputParser(pydantic_object=ExerciseResponse)
exercise_instructions = exercise_parser.get_format_instructions()

exercise_prompt = PromptTemplate.from_template(
    """
    Ти — професійний фітнес-тренер.

    На основі мети тренування згенеруй список вправ.

    Мета тренування:
    {goal}

    ### ФОРМАТ ВІДПОВІДІ
    {instructions}
    """,
    partial_variables={"instructions": exercise_instructions}
)

exercise_chain = exercise_prompt | llm | exercise_parser



class TrainingPlanResponse(BaseModel):
    plan: List[str] = Field(description="План тренувань по днях тижня")


plan_parser = PydanticOutputParser(pydantic_object=TrainingPlanResponse)
plan_instructions = plan_parser.get_format_instructions()

plan_prompt = PromptTemplate.from_template(
    """
    Ти — професійний фітнес-тренер.

    Склади детальний план тренувань на тиждень.

    Вправи:
    {exercises}

    Рівень підготовки: {level}
    Кількість часу на тиждень (години): {hours}

    ### ФОРМАТ ВІДПОВІДІ
    {instructions}
    """,
    partial_variables={"instructions": plan_instructions}
)

plan_chain = plan_prompt | llm | plan_parser




goal = input("Введіть мету тренування: ")
level = input("Введіть рівень підготовки (низький / середній / професіонал): ")
hours = input("Введіть кількість годин на тиждень: ")



exercise_response = exercise_chain.invoke(
    {
        "goal": goal
    }
)

plan_response = plan_chain.invoke(
    {
        "exercises": exercise_response.exercises,
        "level": level,
        "hours": hours
    }
)

print("\nСписок вправ:")
for ex in exercise_response.exercises:
    print("-", ex)

print("\nПлан тренувань:")
for day in plan_response.plan:
    print(day)
