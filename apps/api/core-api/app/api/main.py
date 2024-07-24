from fastapi import APIRouter, HTTPException, Depends, Header, Request
from fastapi.responses import StreamingResponse, FileResponse, JSONResponse

from app.engine import create_podcast_script, text_to_voice, create_content_suggestions, create_article
import json
import logging

router = APIRouter()

@router.get("/agent")
async def get_template():
  try:
      with open('/app/app/agent_template.json', 'r') as file:
          template_data = json.load(file)
      return JSONResponse(content={"data": template_data}, media_type="application/json")
  except Exception as e:
    logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.error(f"An error occurred: {e}")
    raise HTTPException(status_code=500, detail=str(e))

@router.post("/agent")
async def update_agent(request: Request):
  try:
    params = await request.json()
    with open('/app/app/agent_template.json', 'w') as file:
        json.dump(params, file)
    return JSONResponse(content={
            "config": "content"
        }, media_type="application/json")
  except Exception as e:
    logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.error(f"An error occurred: {e}")
    raise HTTPException(status_code=500, detail=str(e))

@router.get("/config")
async def config():
  try:
      with open('/app/app/config.json', 'r') as file:
          config_data = json.load(file)
      return JSONResponse(content={"data": config_data}, media_type="application/json")
  except Exception as e:
    logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.error(f"An error occurred: {e}")
    raise HTTPException(status_code=500, detail=str(e))

@router.post("/config")
async def config(request: Request):
  try:
    params = await request.json()

    return JSONResponse(content={
            "config": "content"
        }, media_type="application/json")
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))

# @router.post("/podcast")
# async def chat_with_model(request: Request):
#   try:
#     scheme = request.url.scheme
#     netloc = request.url.netloc
#     params = await request.json()
#     prompt = params.get("prompt")
#     text = create_podcast_script(prompt)

#     filePath = text_to_voice(text, file_path_full, speaker)
#     full_url = f"{scheme}://{netloc}{filePath}"

#     return JSONResponse(content={
#             "full_url": full_url
#         }, media_type="application/json")
#   except Exception as e:
#     logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
#     logging.error(f"An error occurred: {e}")
#     raise HTTPException(status_code=500, detail=str(e))

@router.post("/podcast")
async def chat_llama(request: Request) -> StreamingResponse:
  try:
      data = await request.json()
      prompt = data.get("prompt")
      
      scheme = request.url.scheme
      netloc = request.url.netloc

      text = create_podcast_script(prompt)
      filePath = text_to_voice(text)
      full_url = f"{scheme}://{netloc}{filePath}"

      return JSONResponse(content={
        "full_url": full_url
      }, media_type="application/json")
  except Exception as e:
    logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.error(f"An error occurred: {e}")
    raise HTTPException(status_code=500, detail=str(e))


@router.post("/article")
async def chat_llama(request: Request) -> StreamingResponse:
  try:
      data = await request.json()
      prompt = data.get("prompt")
      article_content = create_article(prompt)
      return JSONResponse(content={"data": f"{article_content}"}, media_type="application/json")
  except Exception as e:
    logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.error(f"An error occurred: {e}")
    raise HTTPException(status_code=500, detail=str(e))

  
@router.post("/suggest")
async def chat_with_model(request: Request):
  try:
    params = await request.json()
    config = params.get("config")
    prompt = params.get("prompt")
    json_res = create_content_suggestions(prompt)

    return JSONResponse(content={"data": json_res}, media_type="application/json")
  except Exception as e:
    logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.error(f"An error occurred: {e}")
    raise HTTPException(status_code=500, detail=str(e))
