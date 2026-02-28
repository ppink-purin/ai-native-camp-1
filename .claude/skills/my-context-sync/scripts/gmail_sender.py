#!/usr/bin/env python3
"""
Gmail Sender for LinkedIn Recommendations
이 스크립트는 LinkedIn 추천 결과를 Gmail로 전송합니다.
"""

import os
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle

# Gmail API 스코프
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def get_gmail_service():
    """Gmail API 서비스 객체를 반환합니다."""
    creds = None
    token_path = 'token.pickle'

    # 저장된 토큰이 있으면 로드
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    # 토큰이 없거나 만료되었으면 재인증
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # credentials.json이 필요합니다
            if not os.path.exists('credentials.json'):
                raise FileNotFoundError(
                    "credentials.json 파일이 필요합니다.\n"
                    "Google Cloud Console에서 OAuth 2.0 클라이언트 ID를 생성하고\n"
                    "credentials.json 파일을 이 디렉토리에 저장하세요.\n\n"
                    "설정 방법:\n"
                    "1. https://console.cloud.google.com/ 접속\n"
                    "2. 프로젝트 생성 또는 선택\n"
                    "3. 'API 및 서비스' > '사용 설정된 API 및 서비스' > '+ API 및 서비스 사용 설정'\n"
                    "4. 'Gmail API' 검색 후 사용 설정\n"
                    "5. '사용자 인증 정보' > '+ 사용자 인증 정보 만들기' > 'OAuth 클라이언트 ID'\n"
                    "6. 애플리케이션 유형: '데스크톱 앱'\n"
                    "7. credentials.json 다운로드\n"
                )

            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # 토큰 저장
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    return build('gmail', 'v1', credentials=creds)

def create_message(to, subject, body_text, body_html=None):
    """이메일 메시지를 생성합니다."""
    if body_html:
        message = MIMEMultipart('alternative')
        message['to'] = to
        message['subject'] = subject

        # 텍스트 버전
        part1 = MIMEText(body_text, 'plain')
        # HTML 버전
        part2 = MIMEText(body_html, 'html')

        message.attach(part1)
        message.attach(part2)
    else:
        message = MIMEText(body_text)
        message['to'] = to
        message['subject'] = subject

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw}

def send_email(to, subject, body_text, body_html=None):
    """Gmail을 통해 이메일을 전송합니다."""
    try:
        service = get_gmail_service()
        message = create_message(to, subject, body_text, body_html)

        result = service.users().messages().send(
            userId='me',
            body=message
        ).execute()

        print(f"✅ 이메일 전송 성공! Message ID: {result['id']}")
        return result

    except FileNotFoundError as e:
        print(f"❌ 인증 설정 필요: {e}")
        return None
    except Exception as e:
        print(f"❌ 이메일 전송 실패: {e}")
        return None

def convert_markdown_to_html(markdown_text):
    """간단한 마크다운을 HTML로 변환합니다."""
    # 간단한 변환만 수행 (제목, 링크, 볼드)
    html = markdown_text

    # 제목 변환
    import re
    html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)

    # 볼드 변환
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)

    # 링크 변환
    html = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', html)

    # 개행 변환
    html = html.replace('\n', '<br>\n')

    return f"<html><body>{html}</body></html>"

def send_linkedin_recommendations(recommendations_file, recipient_email):
    """LinkedIn 추천 마크다운 파일을 읽어서 이메일로 전송합니다."""
    try:
        # 마크다운 파일 읽기
        with open(recommendations_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()

        # HTML 변환
        html_content = convert_markdown_to_html(markdown_content)

        # 제목 추출 (첫 번째 줄에서)
        first_line = markdown_content.split('\n')[0].replace('#', '').strip()
        subject = first_line if first_line else "LinkedIn 피드 추천"

        # 이메일 전송
        return send_email(
            to=recipient_email,
            subject=subject,
            body_text=markdown_content,
            body_html=html_content
        )

    except FileNotFoundError:
        print(f"❌ 파일을 찾을 수 없습니다: {recommendations_file}")
        return None
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return None

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("사용법: python gmail_sender.py <마크다운_파일> <받는_사람_이메일>")
        print("예시: python gmail_sender.py sync/2026-02-28-linkedin-recommendations.md user@example.com")
        sys.exit(1)

    recommendations_file = sys.argv[1]
    recipient_email = sys.argv[2]

    send_linkedin_recommendations(recommendations_file, recipient_email)
