from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .routers.quiz import router as quiz_router
from .routers.quiz_question import router as quiz_questions_router
from .routers.quiz_question_answer import router as quiz_question_answer_router
from .routers.quiz_result import router as quiz_result_router
from .routers.session import router as session_router
from .routers.games import router as game_router
from .routers.auth import router as auth_router
from .routers.share import router as share_router
from .config import DEBUG
from .routers.utils.middleware import TryExceptMiddleware

app = FastAPI()
app.include_router(quiz_router, prefix="/quiz", tags=['Quiz'])
app.include_router(quiz_questions_router, prefix="/quiz/questions", tags=['Quiz Questions'])
app.include_router(quiz_question_answer_router, prefix="/quiz/questions/answers", tags=['Quiz Questions Answers'])
app.include_router(quiz_result_router, prefix="/quiz/results", tags=['Quiz Results'])
app.include_router(session_router, prefix="/session", tags=['Session'])
app.include_router(game_router, prefix="/game", tags=['Game'])
app.include_router(auth_router, prefix="/auth", tags=['Auth'])
app.include_router(share_router, prefix="/share", tags=['Auth'])

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://0.0.0.0:8080",
    "http://127.0.0.1:8080",
    "https://quiz.kley.media/",
    "https://quiz.kley.media",
    "https://api.quiz.kley.media",
]
    
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(TryExceptMiddleware)

def main():
    import uvicorn
    uvicorn.run("api.app:app", reload=DEBUG, host='0.0.0.0', port=8000)