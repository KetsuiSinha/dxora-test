import httpx
from app.config import settings
from app.platforms.base import BasePlatform


class FacebookPlatform(BasePlatform):
    name = "Facebook"

    def post(self, message: str) -> dict:
        if not settings.facebook_access_token or not settings.facebook_page_id:
            return self._result("failed", error="FACEBOOK_ACCESS_TOKEN or FACEBOOK_PAGE_ID not configured")
        try:
            with httpx.Client(timeout=20) as client:
                resp = client.post(
                    f"https://graph.facebook.com/{settings.facebook_page_id}/feed",
                    data={"message": message, "access_token": settings.facebook_access_token},
                )
            if resp.status_code == 200:
                data = resp.json()
                post_id = data.get("id")
                return self._result("success", posted_url=f"https://facebook.com/{post_id}" if post_id else None, public_access=True)
            return self._result("failed", error=f"Facebook API error {resp.status_code}: {resp.text[:200]}")
        except Exception as exc:
            return self._result("failed", error=str(exc))
