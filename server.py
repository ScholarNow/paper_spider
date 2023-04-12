from fastapi import FastAPI
from pydantic import BaseModel

from paper_spider import crawl as crawl_paper


class Paper(BaseModel):
    title: str


app = FastAPI()


@app.post("/crawl")
def crawl(paper: Paper):
    title = paper.title
    result = crawl_paper(title)
    return result
