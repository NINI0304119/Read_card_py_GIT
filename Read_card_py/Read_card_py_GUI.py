import os
import string
import delphivcl
from delphivcl import *

from  Read_card_py_google_function import *
from  Read_card_py_cv import *

label_left = 10
label_right = 300
label_top = 10 

label_weight = 300
label_height = 30

button_left = 10
button_right = 300

button_weight = 90
button_height = 30

height_space = 20

login_user_text = "登入使用者帳號 :"
upload_file_name_text = "掃描檔案 :"
scan_file_state_text = "掃描檔案狀態 :"
login_user_auth_state_text ="授權狀態 :"
test_label_text = "測試 :"

py_to_exe = 1

unrecorded_text = "未紀錄"
unauth_text = "未授權"
auth_text = "已授權"

class MainForm(Form):
	os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
	def __init__(self, owner):
		self.Caption = "讀卡機"
		
		if py_to_exe == 0 :
			self.SetBounds(1200,500,500,400)
		else :
			self.SetBounds(10,10,500,400)
			self.position="poScreenCenter"
		self.OnClose=self.__on_form_close

		self.login_user = Label(self)
		self.login_user.SetProps(Parent=self,Caption = login_user_text)
		self.login_user.SetBounds(label_left, label_top, label_weight, label_height)

		self.login_user_auth_state = Label(self)
		self.login_user_auth_state.SetProps(Parent=self,Caption = login_user_auth_state_text)
		self.login_user_auth_state.SetBounds(label_right, label_top, label_weight, label_height)

		self.upload_file_name = Label(self)
		self.upload_file_name.SetProps(Parent=self,Caption = upload_file_name_text)
		self.upload_file_name.SetBounds(label_left, self.login_user.top + label_height + height_space, label_weight, label_height)

		self.scan_file_state = Label(self)
		self.scan_file_state.SetProps(Parent=self,Caption = scan_file_state_text)
		self.scan_file_state.SetBounds(label_left, self.upload_file_name.top + label_height + height_space, label_weight, label_height)

		self.Watermark = Label(self)
		self.Watermark.SetProps(Parent=self,Caption = "若有問題請洽 倪隆靖 \ne-mail : p880709@gmail.com \n電話 : 0976-252-864")
		self.Watermark.SetBounds(label_right, self.scan_file_state.top + label_height + height_space, label_weight, label_height+30)

		self.check_login_account = Button(self)
		self.check_login_account.SetProps(Parent=self, Caption="登入帳號", OnClick=self.check_login_accountClick)
		self.check_login_account.SetBounds(button_left, self.scan_file_state.top + label_height + height_space , button_weight, button_height)
		if os.path.exists('token.json'):
			self.login_user.Caption = login_user_text +  login_check()
			self.login_user_auth_state.Caption = login_user_auth_state_text + check_login_user_auth(login_check())
		

		self.select_file = Button(self)
		self.select_file.SetProps(Parent=self, Caption="選擇檔案", OnClick=self.select_fileClick)
		self.select_file.SetBounds(button_left, self.check_login_account.top + label_height + height_space , button_weight, button_height)

		self.scan_file = Button(self)
		self.scan_file.SetProps(Parent=self, Caption="開始掃描", OnClick=self.scan_fileClick)
		self.scan_file.SetBounds(button_left, self.select_file.top + label_height + height_space , button_weight, button_height)

		self.delete_login_account = Button(self)
		self.delete_login_account.SetProps(Parent=self, Caption="刪除帳號資料", OnClick=self.delete_login_accountClick)
		self.delete_login_account.SetBounds(button_right, self.scan_file.top + label_height + height_space , button_weight, button_height)

		self.sel = OpenDialog(self)
		self.sel.Filter = 'PDF files (*.pdf)|*.pdf'
		self.sel.InitialDir = os.getcwd()


	def check_login_accountClick(self, Sender):
		self.login_user.Caption = login_user_text + "登入中"
		user_name = login_check()
		self.login_user.Caption = login_user_text +  user_name	
		self.login_user_auth_state.Caption = login_user_auth_state_text + check_login_user_auth(user_name)
		
	

	def select_fileClick(self, Sender):
		self.sel.Execute()
		self.upload_file_name.Caption = upload_file_name_text + self.sel.FileName
		self.sel.Free

	def scan_fileClick(self, Sender):
		if self.sel.FileName == "":
			self.scan_file_state.Caption = scan_file_state_text + "未選擇掃描檔案"
		else:
			self.scan_file_state.Caption = scan_file_state_text + "掃描中"
			self.scan_file_state.Repaint()

			user_name = login_check()
			user_auth = check_login_user_auth(user_name)
			google_form_upload_result = json.loads(google_form_upload(user_name, get_pdf_num(self.sel.FileName), self.sel.FileName, check_login_user_auth(user_name)))	
			if user_auth == auth_text :
				if google_form_upload_result["status_code"] == 1 :
					add_output_folder(self.sel.FileName)
					scan_pdf(self.sel.FileName)
					self.scan_file_state.Caption = scan_file_state_text + "掃描完成"
					Application.MessageBox(r"scan_finish", 'read_card', MB_ICONINFORMATION)
				else :
					self.scan_file_state.Caption = scan_file_state_text + "掃描失敗_上傳記錄失敗"
			else :
				self.scan_file_state.Caption = scan_file_state_text + "掃描失敗_電子郵件" + user_auth


	def delete_login_accountClick(self, Sender):
		delete_login_token()
		self.login_user.Caption = login_user_text
		self.login_user_auth_state.Caption = login_user_auth_state_text
		self.scan_file_state.Caption = scan_file_state_text

	def __on_form_close(self,sender,action):
		#print("CLOSE")
		action.Value = caFree
		try:
			os.remove("read_card_credentials.json")
			#print("文件删除完毕")
		except(FileNotFoundError):
			#print("文件不存在")
			print("")
	
		#os.system("taskkill /f /im python.exe")
	
		


		
 

def main():
	Application.Initialize()
	Application.Title = "hello python"
	Main = MainForm(Application)
	Main.Show()
	FreeConsole()
	Application.Run()
	#Main.Destory()
main()











