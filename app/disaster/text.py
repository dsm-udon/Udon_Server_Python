import requests
import json
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

from app.core.config import get_setting

scheduler = BackgroundScheduler(daemon=True, timezone='Asia/Seoul')

logging.basicConfig(level='INFO')

secretKey = get_setting().SECRET_KEY


def crawlDisasterText():

    logging.info("Job Called")

    today = datetime.now()

    req = requests.post(
        url="https://www.safekorea.go.kr/idsiSFK/sfk/cs/sua/web/DisasterSmsList.do",
        json={
            "searchInfo": {
                "pageIndex": "1",
                "pageUnit": "10",
                "pageSize": "10",
                "firstIndex": "1",
                "lastIndex": "1",
                "recordCountPerPage": "10",
                "searchBgnDe": str(today)[:11],
                "searchEndDe": str(today)[:11],
                "searchGb": "1",
                "searchWrd": "",
                "rcv_Area_Id": "",
                "dstr_se_Id": "",
                "c_ocrc_type": "",
                "sbLawArea1": "",
                "sbLawArea2": "",
                "sbLawArea3": ""
            }
        }
    )

    for i in json.loads(req.text)["disasterSmsList"]:

        logging.info(i)

        if (today - datetime.strptime(i['CREAT_DT'], '%Y/%m/%d %H:%M:%S')).seconds < 15 and i['DSSTR_SE_NM'] != '기타':
            requests.post(
                url="http://java:8080/send-notification",
                json={
                    "secretKey": secretKey,
                    "title": i['DSSTR_SE_NM'],
                    "body": i['MSG_CN'],
                    "area": i['RCV_AREA_NM'],
                    "message": "행동 요령과 대피소를 확인하세요.",
                    "token": "eu0ygbEFRKqt3usnIQP1he:APA91bH1_O2-RQ0ULRkDctKIZ6VKQ4lSUUbK0jZhYbujPco84wGPlK3DatjQgtce_lMZdJZlDBZTDGO67oMQUE1bpyBhGCXr4JkhE36nrxWh227unfiXfhINPlbk3kte4q_U0TjYJzL0",
                }
            )
            logging.info("Request Success")


scheduler.add_job(crawlDisasterText, 'interval', seconds=15)
