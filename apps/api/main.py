from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="JD Queue Relay")

# IMPORTANT: CORS allows your Chrome Extension to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Our in-memory mailbox
jd_queue = []

class JDData(BaseModel):
    jd: str

@app.get("/")
async def health_check():
    return {"status": "online", "items_in_queue": len(jd_queue)}

@app.post("/submit-jd")
async def submit_jd(data: JDData):
    if not data.jd:
        raise HTTPException(status_code=400, detail="No content provided")
    
    jd_queue.append(data.jd)
    return {"message": "JD queued successfully", "queue_size": len(jd_queue)}

@app.get("/get-next")
async def get_next():
    if not jd_queue:
        return {"jd": None, "message": "Queue is empty"}
    
    # Removes and returns the oldest JD (FIFO)
    return {"jd": jd_queue.pop(0)}