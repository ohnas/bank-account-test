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


get_bank_account_info()
