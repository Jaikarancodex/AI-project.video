from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import uuid
import os

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

@app.post("/generate-video/")
def generate_video(request: PromptRequest):
    prompt = request.prompt
    video_id = str(uuid.uuid4())[:8]
    output_path = f"../AnimateDiff/output/{video_id}.mp4"

    try:
        result = subprocess.run(
            ["python", "generate.py", prompt, output_path],
            cwd="../AnimateDiff",
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=result.stderr)

        return {"video_path": f"/videos/{video_id}.mp4"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Static file serving (optional, if you want to serve videos)
from fastapi.staticfiles import StaticFiles
if not os.path.exists("../AnimateDiff/output"):
    os.makedirs("../AnimateDiff/output")
app.mount("/videos", StaticFiles(directory="../AnimateDiff/output"), name="videos")
