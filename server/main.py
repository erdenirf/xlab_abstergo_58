from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.responses import StreamingResponse
from tasks import ai_model_get_filename, is_exist, get_filename, model_generate
import uuid

app = FastAPI()


# @app.get("/audio/{id}")
# async def get_file(id: str) -> FileResponse:

#     if not is_exist(id):
#         raise HTTPException(status_code=404, detail=f"File not found. ID: {id}")

#     filename = get_filename(id)    
#     if filename is None:
#         raise HTTPException(status_code=400, detail="File is processing. Wait a little bit.")
    
#     return FileResponse(filename)


# @app.post("/generation/{prompt}")
# async def generation(prompt: str) -> str:

#     new_id = str(uuid.uuid4())
#     ai_model_get_filename.delay(prompt, filename_id = new_id)

#     return new_id




@app.post("/generation/{prompt}", response_class=FileResponse)
def generation_prompt(prompt: str) -> str:

    new_id = str(uuid.uuid4())
    
    return ai_model_get_filename(prompt, filename_id = new_id) #model_generate(prompt, new_id)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, log_level="debug", reload=False)