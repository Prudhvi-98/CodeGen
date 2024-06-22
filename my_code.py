from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import google.generativeai as genai 

app = FastAPI()  # Changed from 'App' to 'app'
templates = Jinja2Templates(directory="templates")

GOOGLE_API_KEY = "AIzaSyCyq0jbEgSC9C-TykrFFVUK5_wQVhpjnS8"

class Item(BaseModel):
    prompt: str
    language: str
def generate_content_with_genAI(prompt, language):
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    if isinstance(prompt, list):
        prompt = ' '.join(prompt)
    response = model.generate_content(
        prompt + " in " + language , stream=True)
    content = ""
    for i in response:
        content = content + i.text
    return content

@app.post("/generate/", response_class=HTMLResponse)
async def generate_code(request: Request, prompt: str = Form(...), language: str = Form(...)):
    content = generate_content_with_genAI(prompt, language)
    return templates.TemplateResponse("code.htm", {"request": request, "content": content})

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("code.htm", {"request": request})