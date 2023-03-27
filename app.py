import openai
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from starlette.staticfiles import StaticFiles
import os

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

class MessageInput(BaseModel):
    message: str


@app.get("/fix", response_class=HTMLResponse)
async def get_fix(request: Request):
    return templates.TemplateResponse("fix_form.html", {"request": request})


@app.post("/fix", response_class=HTMLResponse)
async def post_fix(request: Request, message: str = Form(...)):
    openai.api_key = OPENAI_API_KEY

    messages = [
        {"role": "system", "content": "You are a helpful grammar and tone correction assistant. You take input from non-native english speakers, you respond with a version of the message that appears to have been written by a highly professional customer service representative with excellent communication skills. It's important you don't change any of the underlying information, just the way it is communicated. Respond with nothing except for your improved version of the message, formatted with html."},
        {"role": "user", "content": message},
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )

    response_text = response.choices[0].message.content.strip()
    return templates.TemplateResponse("fix_form.html", {"request": request, "original_message": message, "response": response_text})

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8006)


