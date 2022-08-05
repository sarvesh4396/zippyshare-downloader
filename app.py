from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


app = FastAPI()

templates = Jinja2Templates(directory="templates/")


@app.get("/", response_class=HTMLResponse)
def start_page(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})


def download(request: Request, urls: str = Form(...)):
    urls = [u.strip() for u in urls.split("\n") if u.strip() != ""]

    if len(urls) == 0:
        final_text = "No Urls Found"
    else:
        final_text = f"{len(urls)} Urls Found"

    return templates.TemplateResponse(
        "index.html", context={"request": request, "final_text": final_text}
    )
