from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
# from pydantic import BaseModel
import csv
import io
import os
import pytz
from datetime import datetime


#-------AI 안썻어요-------#
#구글링은 조금 했어요
#코드 즉석에서 해석 가능 :)
'''
저는 고통스럽지 않습니다. 하하하
새벽 4시 32분에 이 슬라이드를 복사해오신 고통은 유감이시네요
감사합니다
빠른API 기초 수업 마무리~
'''
#개선점
#csv로 제출한거 저장하기

# class anaform(BaseModel):
    # name: str
    # student_id: str
    # phone: str
    # why_apply: str
    # my_goal: str

app = FastAPI()
upload_dir = "upload"
os.makedirs(upload_dir,exist_ok=True)
result_dir = "result"
os.makedirs(result_dir,exist_ok=True)

@app.post("/ana-apply")
async def upload_file(name: str, student_id: str, phone: str, why_apply: str, my_goal: str,portpolio: UploadFile = File(...)):
    now = datetime.now(pytz.timezone('Asia/Seoul')).strftime("%Y%m%d_%H%M%S_%f")
    now_date = datetime.now(pytz.timezone('Asia/Seoul')).strftime("%Y%m%d")
    contents = await portpolio.read()
    portpolio_spot = os.path.abspath(f"{upload_dir}/{now}_{name}_{portpolio.filename}")
    result_spot = os.path.abspath(f"{result_dir}/{now_date}.csv")
    try:
        with open(result_spot,"a",newline='',encoding='utf-8') as file:
            cw = csv.writer(file)#csv_writer
            cw.writerow([now,name,student_id,phone,why_apply,my_goal,portpolio_spot])
        with open(portpolio_spot,"wb") as f:
            f.write(contents)
        return {"status":"업로드 성공","info":{"name":portpolio.filename,"content_type": portpolio.content_type, "size": len(contents)}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"지원서 제출 실패 {e}")