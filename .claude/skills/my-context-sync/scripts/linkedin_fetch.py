#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["requests", "python-dotenv"]
# ///
"""LinkedIn 정보 수집 스크립트

LinkedIn API를 사용하여 프로필, 활동, 메시지 등을 수집합니다.

사전 요구사항:
1. LinkedIn Developer Portal에서 앱 생성
   https://www.linkedin.com/developers/apps
2. OAuth 2.0 인증 설정
3. Access Token 발급

환경변수 (.env):
  LINKEDIN_ACCESS_TOKEN=your_access_token_here

Usage:
    python linkedin_fetch.py --days 7
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

import requests
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

LINKEDIN_API_BASE = "https://api.linkedin.com/v2"
ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")


class LinkedInAPI:
    """LinkedIn API 클라이언트"""

    def __init__(self, access_token: str):
        if not access_token:
            raise ValueError(
                "LINKEDIN_ACCESS_TOKEN 환경변수가 설정되지 않았습니다.\n"
                ".env 파일에 LINKEDIN_ACCESS_TOKEN을 추가하세요."
            )
        self.access_token = access_token
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0",
        }

    def _get(self, endpoint: str, params: dict = None) -> dict:
        """API GET 요청"""
        url = f"{LINKEDIN_API_BASE}/{endpoint}"
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                print(f"❌ 인증 오류: Access Token이 만료되었거나 유효하지 않습니다.", file=sys.stderr)
            elif e.response.status_code == 403:
                print(f"❌ 권한 오류: 이 API에 접근할 권한이 없습니다.", file=sys.stderr)
                print(f"   LinkedIn Developer Portal에서 앱 권한을 확인하세요.", file=sys.stderr)
            else:
                print(f"❌ API 오류: {e}", file=sys.stderr)
            raise
        except requests.exceptions.RequestException as e:
            print(f"❌ 네트워크 오류: {e}", file=sys.stderr)
            raise

    def get_profile(self) -> dict:
        """현재 사용자 프로필 조회

        필요 권한: r_liteprofile 또는 r_basicprofile
        """
        try:
            data = self._get("me")
            return {
                "id": data.get("id"),
                "firstName": data.get("localizedFirstName"),
                "lastName": data.get("localizedLastName"),
                "profilePicture": data.get("profilePicture", {}).get("displayImage"),
            }
        except Exception as e:
            print(f"⚠️  프로필 조회 실패: {e}", file=sys.stderr)
            return {}

    def get_ugc_posts(self, count: int = 20) -> list[dict]:
        """사용자 게시물 조회

        필요 권한: r_organization_social (조직 계정) 또는 w_member_social

        ⚠️  개인 계정의 경우 이 API는 제한적일 수 있습니다.
        LinkedIn Marketing Developer Platform 파트너십이 필요할 수 있습니다.
        """
        try:
            params = {
                "q": "authors",
                "authors": f"urn:li:person:{self.get_profile().get('id')}",
                "count": count,
            }
            data = self._get("ugcPosts", params=params)

            posts = []
            for element in data.get("elements", []):
                posts.append({
                    "id": element.get("id"),
                    "text": element.get("specificContent", {}).get("com.linkedin.ugc.ShareContent", {}).get("shareCommentary", {}).get("text"),
                    "created": element.get("created", {}).get("time"),
                    "likeCount": element.get("statistics", {}).get("likeCount", 0),
                    "commentCount": element.get("statistics", {}).get("commentCount", 0),
                })
            return posts
        except Exception as e:
            print(f"⚠️  게시물 조회 실패: {e}", file=sys.stderr)
            print(f"   개인 계정의 경우 이 API는 제한적입니다.", file=sys.stderr)
            return []

    def get_notifications_summary(self) -> dict:
        """알림 요약

        ⚠️  이 기능은 LinkedIn API v2에서 제한적입니다.
        공식 API로는 상세 알림 조회가 어렵습니다.
        """
        # LinkedIn API v2는 알림 조회를 공식적으로 지원하지 않음
        # 웹 스크래핑이나 비공식 방법이 필요할 수 있음
        return {
            "available": False,
            "message": "LinkedIn API는 알림 조회를 공식 지원하지 않습니다.",
        }


def format_output(profile: dict, posts: list[dict], notifications: dict) -> dict:
    """수집 결과를 포맷팅"""
    return {
        "collected_at": datetime.now().isoformat(),
        "profile": profile,
        "posts": {
            "count": len(posts),
            "items": posts,
        },
        "notifications": notifications,
        "summary": {
            "total_posts": len(posts),
            "total_engagement": sum(p.get("likeCount", 0) + p.get("commentCount", 0) for p in posts),
        },
    }


def main():
    parser = argparse.ArgumentParser(description="LinkedIn 정보 수집")
    parser.add_argument("--days", type=int, default=7, help="수집 기간 (일)")
    parser.add_argument("--output", type=str, help="출력 파일 경로 (JSON)")
    args = parser.parse_args()

    if not ACCESS_TOKEN:
        print("❌ 오류: LINKEDIN_ACCESS_TOKEN 환경변수가 설정되지 않았습니다.")
        print("\n다음 단계를 따라 설정하세요:")
        print("1. https://www.linkedin.com/developers/apps 에서 앱 생성")
        print("2. OAuth 2.0 인증 설정 및 Access Token 발급")
        print("3. .env 파일에 추가:")
        print("   LINKEDIN_ACCESS_TOKEN=your_access_token_here")
        sys.exit(1)

    print(f"📊 LinkedIn 정보 수집 시작 (최근 {args.days}일)")

    api = LinkedInAPI(ACCESS_TOKEN)

    try:
        # 1. 프로필 조회
        print("  - 프로필 조회 중...")
        profile = api.get_profile()
        if profile:
            print(f"    ✓ 프로필: {profile.get('firstName')} {profile.get('lastName')}")

        # 2. 게시물 조회
        print("  - 게시물 조회 중...")
        posts = api.get_ugc_posts(count=20)
        if posts:
            print(f"    ✓ 게시물: {len(posts)}개")
        else:
            print(f"    ⚠️  게시물 조회 제한됨 (권한 부족 또는 API 제한)")

        # 3. 알림 (제한적)
        print("  - 알림 확인 중...")
        notifications = api.get_notifications_summary()
        if not notifications.get("available"):
            print(f"    ⚠️  {notifications.get('message')}")

        # 결과 포맷팅
        result = format_output(profile, posts, notifications)

        # 출력
        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(json.dumps(result, indent=2, ensure_ascii=False))
            print(f"\n✅ 수집 완료: {output_path}")
        else:
            print("\n" + "=" * 60)
            print(json.dumps(result, indent=2, ensure_ascii=False))
            print("=" * 60)

    except Exception as e:
        print(f"\n❌ 수집 실패: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
