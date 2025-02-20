from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from scraper import scrape_amazon_product
import uvicorn

app = FastAPI()

@app.post("/scrape")
async def scrape_amazon(request: Request):
    """
    API endpoint to scrape Amazon product details.
    Expects a JSON request body with a 'url' key.
    """
    data = await request.json()
    url = data.get("url")

    if not url:
        return JSONResponse(content={"error": "URL is required"}, status_code=400)

    try:
        scrape_amazon_product(url)
        return JSONResponse(content={"message": "Scraping started successfully!"})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
