from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


app = FastAPI()

templates = Jinja2Templates(directory="templates/")


@app.get("/", response_class=HTMLResponse)
def start_page(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})


