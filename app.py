#app.py

from fastapi import FastAPI, Request, Response
import httpx

app = FastAPI()


@app.get('/')
def hello_world():
    return "Hello,World"

@app.post("/proxy")
async def proxy_request(req: Request):
    target_url = "https://target-api.com/endpoint"
    async with httpx.AsyncClient() as client:
        proxy_res = await client.request(
            method=req.method,
            url=target_url,
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