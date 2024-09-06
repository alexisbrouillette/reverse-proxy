#app.py

from fastapi import FastAPI, Request, Response
import httpx
from urllib.parse import urlparse, urlunparse

app = FastAPI()


@app.get('/')
def hello_world():
    return "Hello,World"

@app.post("/proxy{path:path}")
async def proxy_request(req: Request, path: str):
    target_url = "https://alexisbb-smartradio-api.hf.space"
    target_path = urlparse(req.url).path
    target_full_url = urlunparse((target_url, "", target_path, "", "", ""))
    async with httpx.AsyncClient() as client:
        proxy_res = await client.request(
            method=req.method,
            url=target_full_url,
            headers=req.headers,
            content=await req.body()
        )
    return Response(
        status_code=proxy_res.status_code,
        headers=dict(proxy_res.headers),
        content=proxy_res.content
    )

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)