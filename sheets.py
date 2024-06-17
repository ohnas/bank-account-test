import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SERVICE_ACCOUNT_FILE = os.path.join(os.getcwd(), "service-account.json")
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "13nCB53t-9u4OnGV_js84XEXmyvN81rnzX0nSPtxkNDs"


def get_service():
    credentials = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    service = build("sheets", "v4", credentials=credentials)
    return service


def append_values(values):
    service = get_service()
    range_name = "account_in_out_DB!A1:M"

    service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=range_name,
        valueInputOption="USER_ENTERED",
        body={"values": values},
    ).execute()


def append_logs(date, result, error, type, stock):
    service = get_service()
    range_name = "logs!A1:E"

    service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=range_name,
        valueInputOption="USER_ENTERED",
        body={"values": [[date, result, error, type, stock]]},
    ).execute()
