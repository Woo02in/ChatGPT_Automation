import sys
import time
import threading
import time
import re
import subprocess
import chromedriver_autoinstaller 
import pandas as pd
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumbase import SB
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit, QMessageBox, QListWidget, QFileDialog
)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
    
options = Options()
options.add_argument("disable-blink-features=AutomationControlled")  # 자동화 탐지 방지
options.add_experimental_option("excludeSwitches", ["enable-automation"])  # 자동화 표시 제거
options.add_experimental_option('useAutomationExtension', False)  # 자동화 확장 기능 사용 안 함

chromedriver_autoinstaller.install()

def openai_password_reset(email, password): 
   with SB(uc=True, test=True) as sb:
            # ChatGPT 로그인 페이지 이동
            sb.keep_alive = True                    
            url = "https://chatgpt.com/"            
            sb.open(url)
            sb.uc_gui_handle_captcha()

            time.sleep(2)
            sb.driver.switch_to.active_element.send_keys(Keys.ESCAPE)
            time.sleep(1)
            # ChatGPT 로그인 버튼 클릭
            try:
                chatgpt_login_button_selector = "#conversation-header-actions > div > div > button.btn.relative.btn-primary"
                chatgpt_login_button = WebDriverWait(sb.driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, chatgpt_login_button_selector))
                )
                chatgpt_login_button.click()
                print("로그인 버튼 클릭 완료")
                time.sleep(3)

            except Exception as e:
                print("로그인 버튼 클릭 실패:", e) 
            
            # 이메일 입력
            try:
                sb.type("input[type='email']", email)                
                print(email)
                time.sleep(1)                
            except Exception as e:
                print("이메일 입력 실패:", e)
                return False
            
            # 로그인 버튼 클릭
            try:                
                sb.driver.switch_to.active_element.send_keys(Keys.TAB)
                time.sleep(1)    
                sb.driver.switch_to.active_element.send_keys(Keys.ENTER)
                print("로그인 버튼 클릭 완료")

            except Exception as e:
                print("로그인 버튼 클릭 실패:", e) 
                return False
            
            # 비밀번호 입력
            try:
                sb.type("input[type='password']", password)                
                print(password)
                time.sleep(1)                
            except Exception as e:
                print("비밀번호 입력 실패:", e)
                return False
            
            # 계속 버튼 클릭
            
            try:        
                sb.driver.switch_to.active_element.send_keys(Keys.TAB)                              
                time.sleep(0.5)                
                sb.driver.switch_to.active_element.send_keys(Keys.TAB)                              
                time.sleep(0.2)                
                sb.driver.switch_to.active_element.send_keys(Keys.TAB)                              
                time.sleep(0.2)                
                sb.driver.switch_to.active_element.send_keys(Keys.RETURN)            
                print("계속 버튼 클릭 완료")

            except Exception as e:
                print("계속 버튼 클릭 실패:", e) 
                return False
            
            time.sleep(5)
            
            # 로그인 인증 없이 로그인 된 경우         
            #sb.driver.switch_to.active_element.send_keys(Keys.RETURN)      
            print("로그인 성공")          
            time.sleep(3)                                    
                   
            current_url = sb.driver.current_url 
            if "challenge" in current_url : 
                print("로그인 인증 필요")
                        
                sb.driver.switch_to.active_element.send_keys(Keys.TAB)                              
                time.sleep(0.5)                
                sb.driver.switch_to.active_element.send_keys(Keys.TAB)                              
                time.sleep(0.5)                
                sb.driver.switch_to.active_element.send_keys(Keys.RETURN) 
                time.sleep(1)                
                
                sb.driver.switch_to.active_element.send_keys(Keys.TAB)                              
                time.sleep(0.5)                
                sb.driver.switch_to.active_element.send_keys(Keys.TAB)                              
                time.sleep(0.5)                
                sb.driver.switch_to.active_element.send_keys(Keys.RETURN)
                
                # 로그인 인증을 위해 whois 사이트 이동
                whois_url ="https://desk.go.whoisworks.com/"    
                current_windows = sb.driver.window_handles # 현재 열린 창 개수 확인
                sb.driver.execute_script(f"window.open('{whois_url}');")  # 새 창 열기            
                        
                # 창 전환
                try:                  
                    WebDriverWait(sb.driver, 10).until(lambda d: len(d.window_handles) > len(current_windows)) #새로운 창이 열림
                    all_windows = sb.driver.window_handles
                    sb.driver.switch_to.window(all_windows[-1])
                    print(f"새 창으로 전환 완료: {sb.driver.current_url}")
                    time.sleep(3)
                            
                except Exception as e:
                    print("새 창 전환 실패")
                    return False
                                            
                # 이메일 입력
                try:
                    sb.type("input[type='email']", email)
                    print(email)
                    time.sleep(3)
                                    
                except Exception as e:
                    print("이메일 입력 실패:", e)
                    return False

                # 비밀번호 입력
                try:
                    sb.type("input[type='password']", "scopelabs2023!")
                    print("비밀번호 입력 완료")
                    time.sleep(3)
                        
                except Exception as e:
                    print("비밀번호 입력 실패:", e)
                    return False

                # 로그인 버튼 클릭
                try:
                    login_button_selector = "#loginForm > button"
                    login_button = WebDriverWait(sb.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, login_button_selector))
                    )
                    login_button.click()
                    print("로그인 버튼 클릭 성공")
                            
                except Exception as e:
                    print("로그인 버튼 클릭 실패: ", e)
                    return False


                try:
                    mail_selector = "#site-navbar-collapse > ul.nav.navbar-toolbar.navbar-toolbar-left.navbar-toolbar-count-6 > li:nth-child(3) > a"
                    mail_button = WebDriverWait(sb.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, mail_selector))
                    )
                    mail_button.click()
                    print("메일 버튼 클릭 성공")
                        
                except Exception as e:
                    print("메일 버튼 클릭 실패: ", e)
                    return False
                # 로그인 인증 메일 찾기
                
                
                cnt = 2
                while(True):
                    content_position = f"#list > tbody > tr:nth-child({cnt}) > td:nth-child(3) > div > div.col-lg-7.col-md-7 > a > span > span:nth-child(1)"
                                    
                    try:
                        click_content_selector = content_position
                        click_content = WebDriverWait(sb.driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, click_content_selector))
                        )            
                        search_string = "Your authentication code"
                        if search_string in click_content.text:
                            click_content.click()                            
                            print("메일 클릭 성공")                            
                            time.sleep(2)
                            try:                                
                                html = sb.driver.page_source
                                soup = BeautifulSoup(html, "html.parser")

                                # 전체 텍스트에서 6자리 숫자 추출
                                matches = re.findall(r"\b\d{6}\b", soup.get_text())
                                if matches:
                                    Login_code = matches[0]
                                    print("로그인 코드:", Login_code)
                                else:
                                    print("로그인 코드가 없습니다.")

                                    
                            except Exception as e:
                                print("로그인 코드 추출 실패:", e)
                                return False
                            break
                        else:
                            print(click_content.text)
                            cnt = cnt + 1
                            continue
                                        
                    except Exception as e:
                        print("메일 클릭 실패: ", e)
                        return False                                                          
                        
                all_windows = sb.driver.window_handles    
                for window in all_windows:
                    if window != all_windows[0]:
                        sb.driver.switch_to.window(window)
                        sb.driver.close()
                        
                    
                # 초기 창(ChatGPT 창)으로 이동
                try:                                    
                    sb.driver.switch_to.window(all_windows[0])
                    print(f"초기 창으로 전환 완료: {sb.driver.current_url}")
                    time.sleep(3)
                    
                except Exception as e:
                    print("페이지 이동 실패")    
                    return False
                            
                # 로그인 인증 코드 작성
                try:
                    sb.type("input[type='text']", Login_code)
                    print(Login_code)
                    time.sleep(3)
                                    
                except Exception as e:
                    print("로그인 코드 입력 실패:", e)
                    return False
                    
                time.sleep(3)
                # 로그인 인증 완료(계속) 버튼 클릭                              
                sb.driver.switch_to.active_element.send_keys(Keys.TAB)
                time.sleep(0.5)
                sb.driver.switch_to.active_element.send_keys(Keys.RETURN)
            
            elif "verification" in current_url : 
                print("로그인 인증 필요")                                
                
                # 로그인 인증을 위해 whois 사이트 이동
                whois_url ="https://desk.go.whoisworks.com/"    
                current_windows = sb.driver.window_handles # 현재 열린 창 개수 확인
                sb.driver.execute_script(f"window.open('{whois_url}');")  # 새 창 열기            
                        
                # 창 전환
                try:                  
                    WebDriverWait(sb.driver, 10).until(lambda d: len(d.window_handles) > len(current_windows)) #새로운 창이 열림
                    all_windows = sb.driver.window_handles
                    sb.driver.switch_to.window(all_windows[-1])
                    print(f"새 창으로 전환 완료: {sb.driver.current_url}")
                    time.sleep(3)
                            
                except Exception as e:
                    print("새 창 전환 실패")
                    return False
                                            
                # 이메일 입력
                try:
                    sb.type("input[type='email']", email)
                    print(email)
                    time.sleep(3)
                                    
                except Exception as e:
                    print("이메일 입력 실패:", e)
                    return False

                # 비밀번호 입력
                try:
                    sb.type("input[type='password']", "scopelabs2023!") # whois 비밀번호 여기에 입력
                    print("비밀번호 입력 완료")
                    time.sleep(3)
                        
                except Exception as e:
                    print("비밀번호 입력 실패:", e)
                    return False

                # 로그인 버튼 클릭
                try:
                    login_button_selector = "#loginForm > button"
                    login_button = WebDriverWait(sb.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, login_button_selector))
                    )
                    login_button.click()
                    print("로그인 버튼 클릭 성공")
                            
                except Exception as e:
                    print("로그인 버튼 클릭 실패: ", e)
                    return False


                try:
                    mail_selector = "#site-navbar-collapse > ul.nav.navbar-toolbar.navbar-toolbar-left.navbar-toolbar-count-6 > li:nth-child(3) > a"
                    mail_button = WebDriverWait(sb.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, mail_selector))
                    )
                    mail_button.click()
                    print("메일 버튼 클릭 성공")
                        
                except Exception as e:
                    print("메일 버튼 클릭 실패: ", e)
                    return False
                # 로그인 인증 메일 찾기
                
                
                cnt = 2
                while(True):
                    content_position = f"#list > tbody > tr:nth-child({cnt}) > td:nth-child(3) > div > div.col-lg-7.col-md-7 > a > span > span:nth-child(1)"
                                    
                    try:
                        click_content_selector = content_position
                        click_content = WebDriverWait(sb.driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, click_content_selector))
                        )            
                        search_string = "Your ChatGPT code is"
                        if search_string in click_content.text:
                            click_content.click()                            
                            print("메일 클릭 성공")                            
                            time.sleep(2)
                            try:                                
                                html = sb.driver.page_source
                                soup = BeautifulSoup(html, "html.parser")

                                # 전체 텍스트에서 6자리 숫자 추출
                                matches = re.findall(r"\b\d{6}\b", soup.get_text())
                                if matches:
                                    Login_code = matches[0]
                                    print("로그인 코드:", Login_code)
                                else:
                                    print("로그인 코드가 없습니다.")

                                    
                            except Exception as e:
                                print("로그인 코드 추출 실패:", e)
                                return False
                            break
                        else:
                            print(click_content.text)
                            cnt = cnt + 1
                            continue
                                        
                    except Exception as e:
                        print("메일 클릭 실패: ", e)
                        return False                                                          
                        
                all_windows = sb.driver.window_handles    
                for window in all_windows:
                    if window != all_windows[0]:
                        sb.driver.switch_to.window(window)
                        sb.driver.close()
                        
                    
                # 초기 창(ChatGPT 창)으로 이동
                try:                                    
                    sb.driver.switch_to.window(all_windows[0])
                    print(f"초기 창으로 전환 완료: {sb.driver.current_url}")
                    time.sleep(3)
                    
                except Exception as e:
                    print("페이지 이동 실패")    
                    return False
                            
                # 로그인 인증 코드 작성
                try:
                    sb.type("input[type='text']", Login_code)
                    print(Login_code)
                    time.sleep(3)
                                    
                except Exception as e:
                    print("로그인 코드 입력 실패:", e)
                    return False
                    
                time.sleep(3)
                # 로그인 인증 완료(계속) 버튼 클릭                              
                sb.driver.switch_to.active_element.send_keys(Keys.TAB)
                time.sleep(0.5)
                sb.driver.switch_to.active_element.send_keys(Keys.RETURN)
                
            elif current_url != "https://chatgpt.com/":
                print("인증 오류")
                return False
                
            time.sleep(20)
            sb.driver.switch_to.active_element.send_keys(Keys.TAB)
            time.sleep(0.5)
            sb.driver.switch_to.active_element.send_keys(Keys.TAB)
            time.sleep(0.5)
            sb.driver.switch_to.active_element.send_keys(Keys.TAB)
            time.sleep(0.5)
            sb.driver.switch_to.active_element.send_keys(Keys.TAB)
            time.sleep(0.5)
           
            # 워크스페이스 선택 및 랜덤하게 가끔 뜨는 팝업창 제거
            sb.driver.switch_to.active_element.send_keys(Keys.RETURN)
            time.sleep(2)
            # sb.driver.switch_to.active_element.send_keys(Keys.RETURN)
            # time.sleep(1)
            
            # 설정 화면으로 이동
            settings_url = "https://chatgpt.com/#settings/DataControls"
            sb.open(settings_url)
            time.sleep(3)                                  
            
            if sb.driver.current_url != "https://chatgpt.com/#settings/DataControls":
                sb.driver.switch_to.active_element.send_keys(Keys.TAB)                              
                sb.driver.switch_to.active_element.send_keys(Keys.RETURN)                
                time.sleep(3)                                      


            delete_buttons = sb.driver.find_elements(By.TAG_NAME, "button")
                
            for i, btn in enumerate(delete_buttons):
                if btn.text.strip() == "모두 아카이브에 보관하기":
                    
                    if i + 1 < len(delete_buttons) and delete_buttons[i + 1].text.strip() == "모두 삭제":
                        sb.driver.execute_script("arguments[0].click();", delete_buttons[i + 1])
                        print("모두 삭제 버튼 클릭 완료")
                    else:
                        print("다음 버튼이 '모두 삭제'가 아님")
                    break
                
            for cnt in range(3):
                sb.driver.switch_to.active_element.send_keys(Keys.TAB)                                  
                time.sleep(0.2)        
            sb.driver.switch_to.active_element.send_keys(Keys.ENTER)          
            print("내역 삭제 버튼 클릭 완료")    
            time.sleep(5)           
                                            
            # 보안 화면으로 이동                                        
            settings_security_url = "https://chatgpt.com/#settings/Security"
            sb.open(settings_security_url)                    
            time.sleep(3)
            
            if sb.driver.current_url != "https://chatgpt.com/#settings/Security":
                sb.driver.switch_to.active_element.send_keys(Keys.TAB)                              
                sb.driver.switch_to.active_element.send_keys(Keys.RETURN)                
                time.sleep(3)              
                                                 
            logout_buttons = sb.driver.find_elements(By.TAG_NAME, "button")
            for btn in logout_buttons:
                if "모두 로그아웃" in btn.text:
                    sb.driver.execute_script("arguments[0].click();", btn)
                    print("모두 로그아웃 버튼 클릭 완료")
                    break
            
            # for cnt in range(3):
            #     sb.driver.switch_to.active_element.send_keys(Keys.TAB)                                  
            #     time.sleep(0.2)        
            # sb.driver.switch_to.active_element.send_keys(Keys.ENTER)
            
            time.sleep(3)            
            
                        

class Worker(QObject):
    """ 백그라운드 작업 스레드 """
    update_status_signal = pyqtSignal(str)
    task_finished_signal = pyqtSignal(str)

    def __init__(self, email_list):
        super().__init__()
        self.email_list = email_list
        self.running = True # 스레드 종료 체크 변수

    def run(self):
        """ 검색 기록 지우기 실행 """
        failed_list = []

        for i, (email, password) in enumerate(self.email_list):
            if not self.running:
                return
        
            success = openai_password_reset(email, password)

            # if not success:
            #     failed_list.append(email)
            #     continue        

        # if failed_list:
        #     failed_text = "\n".join(failed_list)
        #     self.update_status_signal.emit(failed_text)
        #     self.task_finished_signal.emit("작업 완료, 실패한 이메일을 확인해주세요.")
        # else:
        self.update_status_signal.emit("모든 이메일 처리 완료, 로그를 확인해주세요")
        self.task_finished_signal.emit("모든 이메일 처리 완료, 로그를 확인해주세요")  
    
    def stop(self):
        """스레드 강제 종료"""
        self.running = False
        
        
class ResetAutomationApp(QWidget):
    """ PyQt5 GUI 애플리케이션 """

    def __init__(self):
        super().__init__()
        self.initUI()
        self.email_list = []
        self.worker = None

    def closeEvent(self, event):
        """ X 버튼 클릭 시 종료 확인 """
        reply = QMessageBox.question(
            self, "프로그램 종료", "정말 종료하시겠습니까?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.safe_exit() # 스레드 종료 후 프로그램 종료
            event.accept()
            #sys.exit()
        else:
            event.ignore()
    
    def safe_exit(self):
        """프로그램 종료 전 스레드 확인"""
        if self.worker:
            self.worker.stop()                        
        self.close()
        
    def initUI(self):
        """ UI 초기화 """
        self.setWindowTitle("ChatGPTResetRecordAPP")
        self.setGeometry(200, 200, 700, 700)

        layout = QVBoxLayout()

        # 엑셀 파일 선택 버튼
        self.file_select_button = QPushButton("엑셀 파일 선택")
        self.file_select_button.clicked.connect(self.select_excel_file)
        layout.addWidget(self.file_select_button)
        
        # 선택된 파일 경로 표시
        self.selected_file_label = QLabel("선택된 파일: 없음")
        layout.addWidget(self.selected_file_label)
        
        # 시트 이름 입력 필드
        self.sheet_name_label = QLabel("시트 이름:")
        self.sheet_name_input = QLineEdit()
        layout.addWidget(self.sheet_name_label)
        layout.addWidget(self.sheet_name_input)

        # 시작 행 번호 입력 필드
        self.start_row_label = QLabel("시작 행 번호:")
        self.start_row_input = QLineEdit()
        layout.addWidget(self.start_row_label)
        layout.addWidget(self.start_row_input)

        # 끝 행 번호 입력 필드
        self.end_row_label = QLabel("끝 행 번호:")
        self.end_row_input = QLineEdit()
        layout.addWidget(self.end_row_label)
        layout.addWidget(self.end_row_input)       
        
        # 엑셀에서 이메일 등록 버튼
        self.load_excel_button = QPushButton("엑셀에서 이메일 등록")
        self.load_excel_button.clicked.connect(self.load_emails_from_excel)
        layout.addWidget(self.load_excel_button)

        # 이메일 리스트 표시
        self.email_list_display = QListWidget()
        layout.addWidget(self.email_list_display)

        # 선택한 이메일 삭제 버튼
        self.remove_email_button = QPushButton("선택한 이메일 삭제")
        self.remove_email_button.clicked.connect(self.remove_selected_email)
        layout.addWidget(self.remove_email_button)

        # 실행 버튼
        self.run_button = QPushButton("실행")
        self.run_button.clicked.connect(self.run_script)
        layout.addWidget(self.run_button)

        self.setLayout(layout)

    def select_excel_file(self):
        """ 엑셀 파일 선택 """
        file_path, _ = QFileDialog.getOpenFileName(self, "엑셀 파일 선택", "")
        if file_path:
            self.selected_file_label.setText(f"선택된 파일: , {file_path}")
            self.selected_file = file_path
        else:
            self.selected_file = None 
            
    def load_emails_from_excel(self):
        """ 엑셀에서 이메일을 읽어 리스트에 추가 """   
        if not hasattr(self, 'selected_file') or not self.selected_file:
            QMessageBox.warning(self, "파일 오류", "엑셀 파일을 먼저 선택하세요")
            return
        
        sheet_name = self.sheet_name_input.text().strip()
        start_row = self.start_row_input.text().strip()
        end_row = self.end_row_input.text().strip()
        
        if not sheet_name or not start_row.isdigit() or not end_row.isdigit():
            QMessageBox.warning(self, "입력 오류", "시트 이름과 시작/끝 행 번호를 입력해주세요")
            return                        
        
        try:
            df = pd.read_excel(self.selected_file, sheet_name=sheet_name, header=None)
        
            email_column = df.iloc[:, 1] # 엑셀 2번째 열에서 이메일 가져오기
            password_colum = df.iloc[:,2] # 엑셀 3번째 열에서 비밀번호 가져오기
            
            start_idx = int(start_row) - 1
            end_idx = int(end_row)
            
            extracted_emails = email_column.iloc[start_idx : end_idx].dropna().tolist() # 시작 행부터 끝 행 가져오기
            extracted_password = password_colum.iloc[start_idx : end_idx].dropna().tolist() 
            
            if not extracted_emails:
                QMessageBox.warning(self, "엑셀 오류", "선택한 범위에서 이메일을 찾을 수 없습니다.")
                return
            
            # 이메일 리스트 초기화
            self.email_list.clear()            
            
            for email, password in zip(extracted_emails, extracted_password):
                    self.email_list.append((email, password))    
            
            self.update_email_list_display()    
            QMessageBox.information(self, "완료", f"{len(extracted_emails)}개의 이메일이 추가되었습니다.")
                    
        except Exception as e:
            QMessageBox.critical(self, "엑셀 오류", f"엑셀을 읽는 중 오류 발생 : {str(e)}")
            
    
    def remove_selected_email(self):
        """ 선택된 이메일 삭제 """
        selected_items = self.email_list_display.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "삭제 오류", "삭제할 이메일을 선택하세요.")
            return

        for item in selected_items:
            email_text = item.text()            
            email_info = email_text.split(" / ")[0]  # 이메일 주소만 추출

            # `self.email_list`에서 완전히 삭제
            self.email_list = [entry for entry in self.email_list if entry[0] != email_info]            
            self.email_list_display.takeItem(self.email_list_display.row(item))

        QMessageBox.information(self, "삭제 완료", "선택한 이메일이 삭제되었습니다")
        self.update_email_list_display()
    
    def update_email_list_display(self):
        """ 내부 리스트(self.email_list)를 UI 리스트(QListWidget)에 동기화 """
        self.email_list_display.clear()

        for email, password in self.email_list:
            self.email_list_display.addItem(f"{email} / ChatGPT password : {password}")
    
    def run_script(self):
        """ 비밀번호 재설정 실행 (백그라운드 스레드) """
        if not self.email_list:
            QMessageBox.warning(self, "실행 오류", "이메일을 최소 1개 이상 추가하세요")
            return
        
        
        # 기존 스레드가 실행 중이면 종료 후 새로 시작
        if self.worker and self.worker.is_alive():
            self.worker.stop()
            self.worker.quit()
            self.worker.wait()        
        
        # Worker 스레드 생성 및 연결
        self.worker = Worker(self.email_list)        
        self.worker.task_finished_signal.connect(self.show_completion_modal)

        thread = threading.Thread(target=self.worker.run)
        thread.start()
    

    def show_completion_modal(self, message):
        """ 작업 완료 후 모달 창 띄우기 """
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("완료")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ResetAutomationApp()
    window.show()
    sys.exit(app.exec_())                        
                                                

