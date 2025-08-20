import sys
import time
import threading
import time
import subprocess
import chromedriver_autoinstaller 
import pandas as pd
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumbase import SB
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit, QMessageBox, QListWidget, QFileDialog
)
    
options = Options()
options.add_argument("disable-blink-features=AutomationControlled")  # 자동화 탐지 방지
options.add_experimental_option("excludeSwitches", ["enable-automation"])  # 자동화 표시 제거
options.add_experimental_option('useAutomationExtension', False)  # 자동화 확장 기능 사용 안 함

chromedriver_autoinstaller.install()

def openai_password_reset(email, method, new_password): 
    with SB(uc=True, test=True) as sb:
        url = "https://chatgpt.com/"    
        sb.uc_open_with_reconnect(url, reconnect_time = 5)
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
            time.sleep(2)                
        except Exception as e:
            print("이메일 입력 실패:", e)
            return False

        try:
            sb.driver.switch_to.active_element.send_keys(Keys.TAB)                              
            time.sleep(1)                
            sb.driver.switch_to.active_element.send_keys(Keys.RETURN)                
            print("로그인 버튼 클릭 완료")

        except Exception as e:
            print("로그인 버튼 클릭 실패:", e) 
            return False

        time.sleep(2)
            
        try:
            sb.driver.switch_to.active_element.send_keys(Keys.TAB)                              
            time.sleep(1)                
            sb.driver.switch_to.active_element.send_keys(Keys.TAB)                              
            time.sleep(1)                
            sb.driver.switch_to.active_element.send_keys(Keys.RETURN)  
            print("비밀번호 찾기 버튼 클릭 완료")
            
        except Exception as e:
            print("비밀번호 찾기 버튼 클릭 실패: ", e)
            return False

        time.sleep(1)

        try:
            sb.driver.switch_to.active_element.send_keys(Keys.TAB)                              
            time.sleep(1)                
            sb.driver.switch_to.active_element.send_keys(Keys.RETURN)  
            print("계속 버튼 완료")
            time.sleep(2)
            
        except Exception as e:
            print("계속 버튼 클릭 실패: ", e)
            return False
            
        # 현재 창 저장
        original_window_handle = sb.driver.current_window_handle
            
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

        try:
            sb.type("input[type='password']", "scopelabs2023!")
            
            print("비밀번호 입력 완료")
            time.sleep(3)
            
        except Exception as e:
            print("비밀번호 입력 실패:", e)
            return False

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
        
        time.sleep(2)
        
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
        
        cnt = 2
        reset_code = None

        while True:
            content_position = f"#list > tbody > tr:nth-child({cnt}) > td:nth-child(3) > div > div.col-lg-7.col-md-7 > a > span > span:nth-child(1)"

            try:
                click_content = WebDriverWait(sb.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, content_position))
                )
                mail_text = click_content.text.strip()
                
                if mail_text.startswith("ChatGPT 비밀번호 초기화 코드는"):
                    # 인증번호 추출
                    parts = mail_text.split()
                    if parts[-1].isdigit() and len(parts[-1]) == 6:
                        reset_code = parts[-1]
                        click_content.click()
                        print("메일 클릭 성공, 인증번호 추출:", reset_code)
                        time.sleep(3)
                        break
                    else:
                        print("형식 오류 또는 코드 없음:", mail_text)
                        cnt += 1
                        continue
                else:
                    print("다른 메일:", mail_text)
                    cnt += 1
                    continue

            except Exception as e:
                print("메일 클릭 실패:", e)
                return False

        # 초기 창(인증번호 입력 페이지)으로 돌아가기
        sb.driver.switch_to.window(original_window_handle) 
        time.sleep(2)

        # 인증번호 입력
        try:
            sb.type("input[type='text']", reset_code)
            print("인증번호 입력 완료:", reset_code)
            sb.driver.switch_to.active_element.send_keys(Keys.RETURN)
        except Exception as e:
            print("인증번호 입력 실패:", e)
            return False


        try:            
            sb.type("input[name='new-password']", new_password)
            print("새로운 비밀번호 입력 완료")
            time.sleep(3)
        except Exception as e:
            print("비밀번호 입력 실패:", e)
            return False
        
        try:
            sb.type("input[name='confirm-password']", new_password)
            print("새로운 비밀번호 확인 입력 완료")                    
            time.sleep(3)
        except Exception as e:
            print("비밀번호 입력 실패:", e)
            return False
        
        try:
            sb.driver.switch_to.active_element.send_keys(Keys.TAB)                              
            time.sleep(1)                
            sb.driver.switch_to.active_element.send_keys(Keys.TAB)                              
            time.sleep(1)                
            sb.driver.switch_to.active_element.send_keys(Keys.RETURN)            
            print("비밀번호 재설정 버튼 클릭 완료")
            time.sleep(3)
                            
        except Exception as e:
            print("비밀번호 재설정 버튼 클릭 실패: ", e)    
            return False
        
class Worker(QObject):
        """ 비밀번호 재설정을 실행하는 백그라운드 작업 스레드 """
        update_status_signal = pyqtSignal(str)
        task_finished_signal = pyqtSignal(str)

        def __init__(self, email_list):
            super().__init__()
            self.email_list = email_list
            self.running = True # 스레드 종료 체크 변수

        def run(self):
            """ 비밀번호 재설정 작업 실행 """
            failed_list = []

            for i, (email, password, new_password) in enumerate(self.email_list):
                if not self.running:
                    return
                method = "back" if i % 2 == 0 else "url"
                success = openai_password_reset(email, method, new_password)

                if not success:
                    failed_list.append(email)
                    continue

            if failed_list:
                failed_text = "\n".join(failed_list)
                self.update_status_signal.emit(failed_text)
                self.task_finished_signal.emit("작업 완료, 실패한 이메일을 확인해주세요.")
            else:
                self.update_status_signal.emit("모든 이메일 처리 완료")
                self.task_finished_signal.emit("모든 이메일 처리 완료")  
    
def stop(self):
    """스레드 강제 종료"""
    self.running = False
        
        
class EmailAutomationApp(QWidget):
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
        self.setWindowTitle("ChatGPTPasswordResetAPP")
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

        # 변경할 비밀번호 입력 필드
        self.new_password_label = QLabel("바꿀 비밀번호 입력:")
        self.new_password_input = QLineEdit()
        layout.addWidget(self.new_password_label)
        layout.addWidget(self.new_password_input)
        
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
            
        current_password = "scopelabs2023!"
        
        # 변경할 새 비밀번호 가져오기
        new_password = self.new_password_input.text().strip()
        if not new_password:
            QMessageBox.warning(self, "입력 오류", "새로운 비밀번호를 입력하세요")
            return
        
        try:
            df = pd.read_excel(self.selected_file, sheet_name=sheet_name, header=None)
        
            email_column = df.iloc[:, 1] # 엑셀 2번째 열에서 이메일 가져오기
            
            start_idx = int(start_row) - 1
            end_idx = int(end_row)
            
            extracted_emails = email_column.iloc[start_idx : end_idx].dropna().tolist() # 시작 행부터 끝 행 가져오기
            
            if not extracted_emails:
                QMessageBox.warning(self, "엑셀 오류", "선택한 범위에서 이메일을 찾을 수 없습니다.")
                return
            
            # 이메일 리스트 초기화, 현재 비밀번호 적용
            #self.email_list.clear()            
            
            for email in extracted_emails:
                    self.email_list.append((email, current_password, new_password))    
            
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

        for email, password, new_password in self.email_list:
            self.email_list_display.addItem(f"{email} / whois password : {password} / new ChatGPT password : {new_password}")
    
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
    window = EmailAutomationApp()
    window.show()
    sys.exit(app.exec_())