#app.py

from fastapi import FastAPI, Request, Response
import httpx
from urllib.parse import urlparse, urlunparse, unquote

app = FastAPI()


@app.get('/')
def hello_world():
    return "Hello,World"

@app.post("/reverse-proxy{path:path}")
async def proxy_request(req: Request, path: str):
    target_url = "https://alexisbb-smartradio.hf.space"
    print(target_url+ path)
    target_path = target_url+ path
    print(target_path)
    async with httpx.AsyncClient() as client:
        proxy_res = await client.request(
            method=req.method,
            url=target_path,
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
    uvicorn.run("app:app", host="127.0.0.1", port=8080, reload=True)