import os
from dotenv import load_dotenv
from popbill import EasyFinBankService, PopbillException

# load .env
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


def get_bank_account_info():
    try:
        CorpNum = "1468701679"
        BankCode = "0004"
        AccountNumber = "67493700004937"
        UserID = "rdmts7"
        result = easyFinBankService.getBankAccountInfo(
            CorpNum=CorpNum,
            BankCode=BankCode,
            AccountNumber=AccountNumber,
            UserID=UserID,
        )
        print(result.state)
        print(result.accountNumber)
        print(result.accountType)
    except PopbillException as PE:
        print(PE)


def request_job():
    try:
        CorpNum = "1468701679"
        BankCode = "0004"
        AccountNumber = "67493700004937"
        SDate = "20240607"
        EDate = "20240607"
        UserID = "rdmts7"
        result = easyFinBankService.requestJob(
            CorpNum=CorpNum,
            BankCode=BankCode,
            AccountNumber=AccountNumber,
            SDate=SDate,
            EDate=EDate,
            UserID=UserID,
        )
        return result
    except PopbillException as PE:
        print(PE)


def get_job_state():
    try:
        CorpNum = "1468701679"
        JobID = request_job()
        UserID = "rdmts7"
        result = easyFinBankService.getJobState(
            CorpNum=CorpNum,
            JobID=JobID,
            UserID=UserID,
        )
        return result.jobState
    except PopbillException as PE:
        print(PE)


def account_search():
    try:
        CorpNum = "1468701679"
        JobID = request_job()
        JobState = get_job_state()
        TradeType = ["I", "O"]
        SearchString = ""
        Page = 1
        Perpage = 500
        Order = "D"
        UserID = "rdmts7"
        if JobState == 3:
            result = easyFinBankService.search(
                CorpNum=CorpNum,
                JobID=JobID,
                UserID=UserID,
                TradeType=TradeType,
                SearchString=SearchString,
                Page=Page,
                PerPage=Perpage,
                Order=Order,
            )
            print(result.code)
            print(result.message)
            print(result.total)
            print(result.perPage)
            print(result.pageNum)
            print(result.pageCount)
            print(result.balance)
            for l in result.list:
                print(l.tid)
                print(l.trdate)
                print(l.trseral)
                print(l.trdt)
                print(l.accIn)
                print(l.accOut)
                print(l.balance)
                print(l.remark1)
                print(l.remark2)
                print(l.remark3)
                print(l.remark4)
                print(l.regDT)
    except PopbillException as PE:
        print(PE)


account_search()
