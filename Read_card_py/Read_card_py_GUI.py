import os
import string
import delphivcl
from delphivcl import *

from  Read_card_py_cv import *

label_left = 10
label_right = 300
label_top = 10 

label_weight = 300
label_height = 30

button_left = 10
button_right = 300

button_weight = 120
button_height = 30

height_space = 20

font_size = 15
upload_file_name_text = "File Path :"
scan_file_state_text = "Scanning state :"

py_to_exe = 1


class MainForm(Form):
	os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
	def __init__(self, owner):
		self.Caption = "Scanner"
		
		if py_to_exe == 0 :
			self.SetBounds(1200,500,500,400)
		else :
			self.SetBounds(10,10,500,400)
			self.position="poScreenCenter"
		self.OnClose=self.__on_form_close
		
		self.upload_file_name = Label(self)
		self.upload_file_name.SetProps(Parent=self,Caption = "File Path :")
		self.upload_file_name.SetBounds(label_left, label_top, label_weight, label_height)
		self.upload_file_name.Font.Size = font_size



		self.select_file = Button(self)
		self.select_file.SetProps(Parent=self, Caption="Select File", OnClick=self.select_fileClick)
		self.select_file.SetBounds(button_left, self.top + label_height + height_space , button_weight, button_height)
		self.select_file.Font.Size = font_size

		self.scan_file_state = Label(self)
		self.scan_file_state.SetProps(Parent=self,Caption = "Scanning state :")
		self.scan_file_state.SetBounds(self.select_file.left + button_weight, self.upload_file_name.top + label_height + height_space, label_weight, label_height)
		self.scan_file_state.Font.Size = font_size

		self.scan_file = Button(self)
		self.scan_file.SetProps(Parent=self, Caption="Start scan", OnClick=self.scan_fileClick)
		self.scan_file.SetBounds(button_left, self.select_file.top + label_height + height_space , button_weight, button_height)
		self.scan_file.Font.Size = font_size

		self.Watermark = Label(self)
		self.Watermark.SetProps(Parent=self,Caption = "If you have any questions\nPlease contact NINI0304119 \ne-mail : p880709@gmail.com \n")
		self.Watermark.SetBounds(label_left, self.scan_file.top + button_height + height_space, label_weight, label_height+30)
		self.Watermark.Font.Size = font_size

		self.sel = OpenDialog(self)
		self.sel.Filter = 'PDF files (*.pdf)|*.pdf'
		self.sel.InitialDir = os.getcwd()
		
	def select_fileClick(self, Sender):
		self.sel.Execute()
		self.upload_file_name.Caption = upload_file_name_text + self.sel.FileName
		self.sel.Free

	def scan_fileClick(self, Sender):
		add_output_folder(self.sel.FileName)
		scan_pdf(self.sel.FileName)
		self.scan_file_state.Caption = scan_file_state_text + "Scan Finish"
		Application.MessageBox(r"scan_finish", 'read_card', MB_ICONINFORMATION)
		

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











