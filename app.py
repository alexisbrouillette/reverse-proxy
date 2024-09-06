#app.py

from fastapi import FastAPI, Request, Response
import httpx

app = FastAPI()


@app.get('/')
def hello_world():
    return "Hello,World"

@app.post("/reverse-proxy")
async def proxy_request(req: Request):
    target_url = "https://alexisbb-smartradio.hf.space/get_radio_audio"
    async with httpx.AsyncClient(timeout=1000) as client:
        proxy_res = await client.post(target_url+"/", content=await req.body())
        print(f"Request sent: {req.method} {req.url}")
        print(f"Target URL response: {proxy_res.status_code} {proxy_res.content}")
        print(f"Proxy URL response: {proxy_res.url}")
    return Response(
        status_code=proxy_res.status_code,
        headers=dict(proxy_res.headers),
        content=proxy_res.content
    )

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8080, reload=True)