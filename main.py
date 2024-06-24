import os
import time
from dotenv import load_dotenv
from popbill import EasyFinBankService, PopbillException
from sheets import append_values, append_logs
from tools import format_converter, get_yesterday

load_dotenv()

LINK_ID = os.environ.get("LinkID")
SECRET_KEY = os.environ.get("SecretKey")
IS_TEST = bool(os.environ.get("IsTest"))
IP_RESTRICT_ON_OFF = bool(os.environ.get("IPRestrictOnOff"))
USE_STATIC_IP = bool(os.environ.get("UseStaticIP"))
USE_LOCAL_TIME_YN = bool(os.environ.get("UseLocalTimeYN"))

# settings.py 작성한 LinkID, SecretKey를 이용해 EasyFinBankService 서비스 객체 생성
easyFinBankService = EasyFinBankService(LINK_ID, SECRET_KEY)

# 연동환경 설정값, 개발용(True), 상업용(False)
easyFinBankService.IsTest = IS_TEST

# 인증토큰 IP제한기능 사용여부, 권장(True)
easyFinBankService.IPRestrictOnOff = IP_RESTRICT_ON_OFF

# 팝빌 API 서비스 고정 IP 사용여부, true-사용, false-미사용, 기본값(false)
easyFinBankService.UseStaticIP = USE_STATIC_IP

# 로컬시스템 시간 사용여부, 권장(True)
easyFinBankService.UseLocalTimeYN = USE_LOCAL_TIME_YN

YESTERDAY = get_yesterday()


def request_job():
    try:
        corp_num = "1468701679"
        bank_code = "0004"
        account_number = "67493700004937"
        s_date = YESTERDAY
        e_date = YESTERDAY
        user_id = "rdmts7"
        result = easyFinBankService.requestJob(
            CorpNum=corp_num,
            BankCode=bank_code,
            AccountNumber=account_number,
            SDate=s_date,
            EDate=e_date,
            UserID=user_id,
        )
        return result
    except PopbillException as PE:
        append_logs(YESTERDAY, "fail", PE, "request_job", "Popbill")


def get_job_state():
    try:
        job_id = request_job()
        corp_num = "1468701679"
        user_id = "rdmts7"
        result = easyFinBankService.getJobState(
            CorpNum=corp_num,
            JobID=job_id,
            UserID=user_id,
        )
        return job_id, result.jobState
    except PopbillException as PE:
        append_logs(YESTERDAY, "fail", PE, "get_job_state", "Popbill")


def account_search():
    try:
        job_id, job_state = get_job_state()
        corp_num = "1468701679"
        trade_type = ["I", "O"]
        search_string = ""
        page = 1
        per_page = 500
        order = "A"
        user_id = "rdmts7"
        if job_state == 3:
            results = easyFinBankService.search(
                CorpNum=corp_num,
                JobID=job_id,
                UserID=user_id,
                TradeType=trade_type,
                SearchString=search_string,
                Page=page,
                PerPage=per_page,
                Order=order,
            )
            if results.list:
                for result in results.list:
                    try:
                        values = [
                            [
                                result.tid,
                                format_converter(result.trdate),
                                result.trseral,
                                format_converter(result.trdt),
                                result.accIn,
                                result.accOut,
                                result.balance,
                                result.remark1,
                                result.remark2,
                                result.remark3,
                                result.remark4,
                                result.regDT,
                                result.memo,
                            ]
                        ]
                        append_values(values)
                    except Exception as err:
                        append_logs(
                            YESTERDAY, "fail", err, "account_search_list", "Popbill"
                        )
                    finally:
                        time.sleep(1)
            append_logs(
                YESTERDAY, "success", results.total, "account_search_list", "Popbill"
            )
    except PopbillException as PE:
        append_logs(YESTERDAY, "fail", PE, "account_search", "Popbill")


account_search()
