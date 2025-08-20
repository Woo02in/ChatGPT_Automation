# ChatGPT 자동화 도구

이 프로젝트는 ChatGPT 계정 관리와 관련된 자동화 도구들을 포함하고 있습니다.

## 📁 프로젝트 구조

```
ChatGPT_Automation_wooin/
├── Change_Password/          # ChatGPT 비밀번호 변경 자동화
│   ├── app.py               # 메인 애플리케이션 파일
│   ├── downloaded_files/    # 다운로드된 파일들
│   └── venv/               # Python 가상환경
└── Reset_Record/            # ChatGPT 기록 초기화 자동화
    ├── reset_record.py     # 메인 애플리케이션 파일
    ├── downloaded_files/   # 다운로드된 파일들
    └── venv/              # Python 가상환경
```

## 🔧 각 폴더별 기능

### Change_Password/
ChatGPT 계정의 비밀번호를 자동으로 변경하는 도구입니다.

**주요 기능:**
- ChatGPT 웹사이트 자동 로그인
- 비밀번호 재설정 프로세스 자동화
- PyQt5 기반 GUI 인터페이스
- Selenium을 사용한 웹 자동화
- 자동화 탐지 방지 기능

**사용 기술:**
- Python
- Selenium WebDriver
- PyQt5 (GUI)
- ChromeDriver Autoinstaller
- SeleniumBase

### Reset_Record/
ChatGPT 계정의 대화 기록을 자동으로 초기화하는 도구입니다.

**주요 기능:**
- ChatGPT 계정 자동 로그인
- 대화 기록 삭제 자동화
- PyQt5 기반 GUI 인터페이스
- Selenium을 사용한 웹 자동화
- 자동화 탐지 방지 기능

**사용 기술:**
- Python
- Selenium WebDriver
- PyQt5 (GUI)
- ChromeDriver Autoinstaller
- SeleniumBase
- BeautifulSoup

## 🚀 설치 및 실행

### Change_Password 실행
```bash
cd Change_Password
# 가상환경 활성화 (Windows)
venv\Scripts\activate
# 또는 (Linux/Mac)
source venv/bin/activate

# 필요한 패키지 설치
pip install -r requirements.txt

# 애플리케이션 실행
python app.py
```

### Reset_Record 실행
```bash
cd Reset_Record
# 가상환경 활성화 (Windows)
venv\Scripts\activate
# 또는 (Linux/Mac)
source venv/bin/activate

# 필요한 패키지 설치
pip install -r requirements.txt

# 애플리케이션 실행
python reset_record.py
```

## 📋 필요한 패키지

두 프로젝트 모두 다음 패키지들이 필요합니다:
- selenium
- seleniumbase
- PyQt5
- pandas
- chromedriver-autoinstaller
- beautifulsoup4 (Reset_Record만)

## ⚠️ 주의사항

1. **자동화 탐지**: 이 도구들은 자동화 탐지를 우회하기 위한 기능이 포함되어 있지만, ChatGPT의 정책 변경으로 인해 작동하지 않을 수 있습니다.

2. **계정 보안**: 자동화 도구 사용 시 계정 보안에 주의하시기 바랍니다.

3. **합법적 사용**: 이 도구는 개인적인 용도로만 사용하시고, ChatGPT의 이용약관을 준수하시기 바랍니다.

4. **Chrome 브라우저**: Chrome 브라우저가 설치되어 있어야 합니다.

## 🔒 보안 고지사항

이 도구들은 교육 및 개인 사용 목적으로 제작되었습니다. 상업적 용도나 불법적인 활동에 사용하지 마시기 바랍니다. 사용자의 책임 하에 사용하시기 바랍니다.
