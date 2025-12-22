import os
import dotenv
from typing import List
from pydantic import BaseModel, Field

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage,
    BaseMessage
)
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser


dotenv.load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    api_key=api_key,
)



messages: List[BaseMessage] = [
    SystemMessage("""
    Ти — ввічливий чат-бот.
    Даєш зрозумілі, логічні та корисні відповіді.
    """)
]



class SummarySchema(BaseModel):
    summary: str = Field(description="Короткий підсумок всієї розмови з максимумом деталей")


summary_parser = PydanticOutputParser(pydantic_object=SummarySchema)
summary_instructions = summary_parser.get_format_instructions()

summary_prompt = PromptTemplate.from_template(
    """
    Ти — модель для підсумовування діалогу.
    Підсумуй розмову у декількох реченнях, зберігаючи якомога більше деталей.

    ### ДІАЛОГ
    {conversation}

    ### ФОРМАТ ВІДПОВІДІ
    {instructions}
    """,
    partial_variables={"instructions": summary_instructions}
)

summary_chain = summary_prompt | llm | summary_parser




while True:
    user_input = input("Ви: ")

    if user_input == "":
        break

    messages.append(HumanMessage(user_input))

    response = llm.invoke(messages)
    messages.append(response)

    print(f"AI: {response.content}")



    human_ai_messages = [
        m for m in messages if isinstance(m, (HumanMessage, AIMessage))
    ]

    if len(human_ai_messages) > 4:
        conversation_text = ""
        for m in human_ai_messages:
            role = "User" if isinstance(m, HumanMessage) else "AI"
            conversation_text += f"{role}: {m.content}\n"

        summary = summary_chain.invoke(
            {"conversation": conversation_text}
        )

        messages = [
            messages[0],  # SystemMessage
            AIMessage(content=f"Підсумок розмови: {summary.summary}")
        ]

        print("\n--- РОЗМОВУ ПІДСУМОВАНО ---\n")
