from __future__ import print_function
import os.path
import requests
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://mail.google.com/']

def main():
    login_flag = 0
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time

    if login_flag == 0: # 0 use token if have  1 always run login web
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    elif login_flag == 1:
        try:
            os.remove("token.json")
            #print("文件删除完毕")
        except(FileNotFoundError):
            #print("文件不存在")
            print("")

        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'read_card_credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    gmail_service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API

    results = gmail_service.users().getProfile(userId='me').execute()
    user_addr_out = results.get('emailAddress', [])
    print(user_addr_out)
    resulttt = json.loads(google_form_upload("ASD",10,"ZXC.PDF"))
    print(resulttt["user_name"])




def google_form_upload(upload_user_name,input_page_num,file_name):
  url = "https://docs.google.com/forms/d/1DA53RQnGcn3g6_Su5B5U1Wo0JN8hZn--1NV5ZqJXoZw/formResponse?"
  user_name = upload_user_name
  pdf_page_num = str(input_page_num + 1)
  url += "entry.1785848439=" + user_name + "&entry.7634511=" + pdf_page_num + "&entry.981018494=" + file_name
  r = requests.get(url)
  #print(r.status_code)
  if 0:
    print("使用者 : " + user_name)
    print("上傳檔名 : " + file_name)
    print("掃描頁數 : " + pdf_page_num)
    if r.status_code == 200 :
        print("上傳成功")
        return True
    else :
       print("上傳失敗")
       return False
  else :
    value = {
        "user_name": user_name,
        "file_name": file_name,
        "pdf_page_num": pdf_page_num,
        "status_code": r.status_code
        }

  return json.dumps(value)




if __name__ == '__main__':
    main()