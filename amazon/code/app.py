from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from scraper import scrape_amazon_product

app = FastAPI()

class ScrapeRequest(BaseModel):
    url: str

@app.post("/scrape")
async def scrape_amazon(request: ScrapeRequest):
    """API endpoint to scrape Amazon product details."""
    url = request.url

    if not url:
        raise HTTPException(status_code=400, detail="URL is required")

    try:
        scrape_amazon_product(url)
        return {"message": "Scraping started successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
