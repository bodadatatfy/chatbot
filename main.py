from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from chat import get_response
import uvicorn

app = FastAPI(title="Chatbot API", description="Simple Chatbot with FastAPI")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Model for chat request
class ChatRequest(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse, tags=["Frontend"])
async def chat_page(request: Request):
    """Serve the chat interface"""
    return templates.TemplateResponse("chat.html", {"request": request})

@app.post("/api/chat", tags=["API"])
async def chat_endpoint(chat_request: ChatRequest):
    """Handle chat messages and return bot response"""
    try:
        user_message = chat_request.message
        bot_response = get_response(user_message)
        return JSONResponse(content={"response": bot_response})
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"response": "Sorry, I encountered an error. Please try again."}
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)