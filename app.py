from fastapi import FastAPI, Request, Form
from bs4 import BeautifulSoup
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests,uvicorn

from utils import get_download_btn_template, get_download_url, get_urls


app = FastAPI()
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US;q=0.7",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36",
}
session = requests.Session()
templates = Jinja2Templates(directory="templates/", autoescape=False)


@app.get("/", response_class=HTMLResponse)
def start_page(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})


@app.post("/", response_class=HTMLResponse)
def download(request: Request, urls: str = Form(...)):
    urls = get_urls(urls)

    if len(urls) == 0:
        final_text = "No Urls Found"
        return templates.TemplateResponse(
            "index.html", context={"request": request, "final_text": final_text}
        )
    else:
        final_text = f"{len(urls)} Urls Found<br>"

    download_urls = []
    for u in urls:
        res = session.get(u, headers=headers)
        print(res.status_code)
        soup = BeautifulSoup(res.text, "html.parser")
        try:
            download_urls.append(get_download_url(u, soup))
        except Exception as e:
            print(e)
            pass

        final_text += f"{len(download_urls)} Downloadable Urls Found<br>"

    links = "<br>".join([get_download_btn_template(u) for u in download_urls])
    return templates.TemplateResponse(
        "index.html",
        context={"request": request, "final_text": final_text, "links": links},
    )

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)