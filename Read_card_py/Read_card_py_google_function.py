from __future__ import print_function
from ast import Return
import os.path
import json
import requests
import pandas as pd
import io

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials 
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

unrecorded_text = "未紀錄"
unauth_text = "未授權"
auth_text = "已授權"


SCOPES = ['https://www.googleapis.com/auth/userinfo.email','openid']

read_cred_from = 2 #0 exist 1 add file from variable 2 flow from config

def login_check():
    user_addr_out = 'error_addr'
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
            try:
                creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            except:
                try:
                    os.remove("token.json")
                    #print("文件删除完毕")
                except(FileNotFoundError):
                    #print("文件不存在")
                    print("")
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
        if creds and creds.expired and creds.refresh_token: #creds == null 
            creds.refresh(Request())
        else:
            if read_cred_from == 0 :
                 flow = InstalledAppFlow.from_client_secrets_file('read_card_credentials.json', SCOPES)
            elif read_cred_from == 1 :
                read_card_credentials_json = {"installed":{"client_id":"788984340204-37f6buifjnsjoutk7vg1rt6m3tjp9iiv.apps.googleusercontent.com","project_id":"read-card-377222","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"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","redirect_uris":["http://localhost"]}}
                with open("read_card_credentials.json", "w") as outfile:
                    json.dump(read_card_credentials_json, outfile)
                flow = InstalledAppFlow.from_client_secrets_file('read_card_credentials.json', SCOPES)
            elif read_cred_from == 2:
                read_card_credentials_json = {"installed":{"client_id":"788984340204-37f6buifjnsjoutk7vg1rt6m3tjp9iiv.apps.googleusercontent.com","project_id":"read-card-377222","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"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","redirect_uris":["http://localhost"]}}
                flow = InstalledAppFlow.from_client_config(read_card_credentials_json, SCOPES)

            creds = flow.run_local_server(authorization_prompt_message='Please visit this URL: {url}', 
                                          success_message='授權完成，請關閉頁面')

        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    #gmail_service = build('gmail', 'v1', credentials=creds)
    user_info_service = build(serviceName='oauth2', version='v2',credentials=creds)

    # Call the API
    try:
        user_info = user_info_service.userinfo().get().execute()
    except:
        print('An error occurred: %s', e)
    if user_info and user_info.get('email'):
        #print("id" + str(user_info))
        user_addr_out =  user_info.get('email')
    return user_addr_out


def google_form_upload(upload_user_name, input_page_num, file_name, auth_state):
  url = "https://docs.google.com/forms/d/1DA53RQnGcn3g6_Su5B5U1Wo0JN8hZn--1NV5ZqJXoZw/formResponse?"
  user_name = upload_user_name
  pdf_page_num = str(input_page_num + 1)
  url += "entry.1785848439=" + user_name + "&entry.7634511=" + pdf_page_num + "&entry.981018494=" + file_name + "&entry.2097092888=" + auth_state
  r = requests.get(url)
  upload_form_status = 0

  if r.status_code == 200:  # if there have user_name pdf_page_num file_name input  else r.status_code ==400
      try:
        #print(r.headers['P3P']) #if the form is allow to response
        if (r.headers['P3P']) == 'CP="This is not a P3P policy! See g.co/p3phelp for more info."':
            upload_form_status = 1
      except :
        #print("FORM NOT ALLOW")
        upload_form_status = 0

  value = {
    "user_name": user_name,
    "file_name": file_name,
    "pdf_page_num": pdf_page_num,
    "status_code": upload_form_status
    }
  return json.dumps(value)


def delete_login_token():
    try:
        creds = None 
        os.remove("token.json")
        #print("文件删除完毕")
    except(FileNotFoundError):
        #print("文件不存在")
        print("")

def check_login_user_auth(user_name):
    csvURL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQYs_pxbx9uWK9aTEXG5jN41Moq5cMGq6dcHCORtsAcEIjffut8EV-o4HfS89W8NKiwODkOFR_CgjZW/pub?gid=1734462224&single=true&output=csv"
    r_csvURL = requests.get(csvURL)

    df = pd.read_csv(io.StringIO(r_csvURL.content.decode('utf-8')))
    filt_user_email = (df["user_email"] == user_name)
    filt_authorized = (df["authorized"] == "同意")

    if df.loc[filt_user_email].empty :
        #print(unrecorded_text)
        return unrecorded_text
    else :
        if df.loc[filt_user_email].loc[filt_authorized].empty:
            #print(unauth_text)
            return unauth_text
        else :
            #print(auth_text)
            return auth_text








