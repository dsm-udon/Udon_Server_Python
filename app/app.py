from apscheduler.schedulers import SchedulerAlreadyRunningError, SchedulerNotRunningError
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.core.config import get_setting
from app.disaster.text import scheduler

app = FastAPI()

secretKey = get_setting().SECRET_KEY


class SecretKey(BaseModel):
    secret_key: str


@app.post(f"/start")
async def schedulingStart(request: SecretKey):

    if secretKey != request.secret_key:
        raise HTTPException(status_code=403, detail='Key Not Matched')

    try:
        scheduler.start()
        return {'message': 'Scheduling Started'}
    except SchedulerAlreadyRunningError:
        raise HTTPException(status_code=204, detail='Scheduling Already Started')


@app.post(f"/shutdown")
async def schedulingEnd(request: SecretKey):
    if secretKey != request.secret_key:
        raise HTTPException(status_code=403, detail='Key Not Matched')
    try:
        scheduler.shutdown()
        return {'message': 'Scheduling Shut Downed'}
    except SchedulerNotRunningError:
        raise HTTPException(status_code=204, detail='Scheduling Already Shut Downed')
