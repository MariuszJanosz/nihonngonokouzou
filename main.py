import sqlalchemy as sa
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from postgresql.database import engine
from postgresql.models import DictionaryEntry

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
@app.get("/search", response_class=HTMLResponse)
def search_page(q: str = "") -> str:
    page_content = '<form action="/search" method="get" ><input type="search" name="q" required></input><input type="submit"></input></form>'
    if q != "":
        stmt = sa.select(DictionaryEntry).where(
            DictionaryEntry.search_key.ilike("%" + q + "%")
        )
        with Session(engine) as session:
            for row in session.execute(stmt):
                page_content += "<br />Key:" + row[0].key
                page_content += "<br />Reading:" + row[0].reading
                page_content += "<br />" + row[0].entry
    page_wrapper = (
        f"<!DOCTYPE html><html><head></head><body>{page_content}</body></html>"
    )
    return page_wrapper
