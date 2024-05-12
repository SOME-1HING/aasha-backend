from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI
import os
from dotenv import load_dotenv
import google.generativeai as genai

# load G-API key
load_dotenv()
genai.configure(api_key=os.getenv("G_API_KEY"))

# load model
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])


# get response from gemini
def get_response(question):
    response = chat.send_message(question)
    return response.text  # Return the response directly without filtering


def roi_prediction(org_name: str, org_serv: str):

    conversational_prompt = (
        "You are a financial expert who can tell a rough ROI figure just by knowing the company and its services. Tell me the estimated ROI for a business named "
        + org_name
        + " that provides services in "
        + org_serv
        + ". Also, give me 5 key pointers for improvement and growth. You'll need to provide a rough ROI percentage (at least on a scale of 100) based on the idea. Please keep your response short, concise, and direct."
    )

    # print response
    response = get_response(conversational_prompt)
    return response


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


class DataItem(BaseModel):
    project_name: str
    project_desc: str


@app.post("/roi")
async def roi(data_item: DataItem):
    return roi_prediction(data_item.project_name, data_item.project_desc)
