#app.py

from fastapi import FastAPI, Request, Response
from httpx import fetch

app = FastAPI()


@app.get('/')
def hello_world():
    return "Hello,World"

@app.post("/proxy")
async def proxy_request(req: Request):
    target_url = "https://target-api.com/endpoint"
    proxy_req = Request(
        method=req.method,
        url=target_url,
        headers=req.headers,
        body=await req.body()
    )
    proxy_res = await fetch(proxy_req)
    return Response(
        status_code=proxy_res.status,
        headers=dict(proxy_res.headers),
        content=proxy_res.body
    )

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)