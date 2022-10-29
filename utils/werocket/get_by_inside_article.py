
import datetime as dt
import os

from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build

load_dotenv()


def get_service(credentials):
    service = build('sheets', 'v4', credentials=credentials)
    return service


def get_all_rows(month, spreadsheet_id, year=2022, service=None):
    range_name = f'{month}.{year}'
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id,
                                range=f'{range_name}!A:GS', majorDimension='ROWS').execute()

    values = result.get('values', [])
    return values


def get_inside_article_from_rows(rows, article):
    for row in rows:
        if row[5] == article:
            return row[6]


def get_article_by_inside_article(inside_article):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    credentials_file = os.path.join(base_dir, 'credentials_service.json')
    credentials = service_account.Credentials.from_service_account_file(
        credentials_file, scopes=['https://www.googleapis.com/auth/spreadsheets'])
    service = get_service(credentials)
    rows = get_all_rows(dt.datetime.now().strftime('%m'), os.getenv('WEROCKET_SHEET_ID'), service=service)
    return get_inside_article_from_rows(rows, inside_article)
