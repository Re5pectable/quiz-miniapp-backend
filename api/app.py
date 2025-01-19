from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers.quiz import router as quiz_router
from .routers.quiz_question import router as quiz_questions_router
from .routers.quiz_question_answer import router as quiz_question_answer_router
from .routers.quiz_result import router as quiz_result_router
from .routers.session import router as session_router

app = FastAPI()
app.include_router(quiz_router, prefix="/quiz", tags=['Quiz'])
app.include_router(quiz_questions_router, prefix="/quiz/questions", tags=['Quiz Questions'])
app.include_router(quiz_question_answer_router, prefix="/quiz/questions/answers", tags=['Quiz Questions Answers'])
app.include_router(quiz_result_router, prefix="/quiz/results", tags=['Quiz Results'])
app.include_router(session_router, prefix="/session", tags=['Session'])

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://0.0.0.0:8080",
    "http://127.0.0.1:8080",
]
    
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# boto3.set_stream_logger(name='botocore')
# s3_client = boto3.client(
#     's3',
#     region_name="ru-central1",
#     endpoint_url=s3_config.S3_ENDPOINT,
#     aws_access_key_id=s3_config.S3_KEY_ID,
#     aws_secret_access_key=s3_config.S3_KEY_SECRET,
#     config=Config(signature_version='s3v4')
# )


# @app.post("/")
# async def new_qiuz(
#     # quiz_data: QuizCreate = Body(),
#     file: UploadFile = File(...),
# ):
#     for key in s3_client.list_objects(Bucket=s3_config.S3_BUCKET_NAME)['Contents']:
#         print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
#         print(key['Key'])
        
#     try:
#         local_file_path = f"./{file.filename}"
#         with open(local_file_path, "wb") as f:
#             f.write(file.file.read())

#         s3_client.upload_file(local_file_path, s3_config.S3_BUCKET_NAME, file.filename)
        
#         # s3_client.put_object(Bucket=s3_config.S3_BUCKET_NAME, Key='test/' + file.filename, Body=file.file)
#     except Exception as e:
#         raise HTTPException(400, str(e))


def main():
    import uvicorn
    uvicorn.run("api.app:app", reload=True, host='0.0.0.0', port=8000)