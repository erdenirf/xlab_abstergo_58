from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import time

app = FastAPI()

def model_generate(prompt: str) -> str:

    time.sleep(10)   #sec

    return "./16742513.mp3"


@app.post("/generation/{prompt}", response_class=FileResponse)
def generation_prompt(prompt: str) -> str:
    
    return model_generate(prompt)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, log_level="debug", reload=False)