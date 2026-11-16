import httpx
from app.config import settings
from app.platforms.base import BasePlatform


class InstagramPlatform(BasePlatform):
    name = "Instagram"

    def post(self, message: str) -> dict:
        if not settings.instagram_access_token or not settings.instagram_business_account_id:
            return self._result("failed", error="INSTAGRAM_ACCESS_TOKEN or INSTAGRAM_BUSINESS_ACCOUNT_ID not configured")
        try:
            with httpx.Client(timeout=20) as client:
                # Instagram Graph API requires creating a media container then publishing.
                resp = client.post(
                    f"https://graph.facebook.com/v18.0/{settings.instagram_business_account_id}/media",
                    data={
                        "image_url": "https://example.com/placeholder.jpg",
                        "caption": message,
                        "access_token": settings.instagram_access_token,
                    },
                )
                if resp.status_code != 200:
                    return self._result("failed", error=f"Instagram container error {resp.status_code}: {resp.text[:200]}")
                creation_id = resp.json().get("id")
                publish = client.post(
                    f"https://graph.facebook.com/v18.0/{settings.instagram_business_account_id}/media_publish",
                    data={"creation_id": creation_id, "access_token": settings.instagram_access_token},
                )
            if publish.status_code == 200:
                return self._result("success", posted_url="https://instagram.com", public_access=True)
            return self._result("failed", error=f"Instagram publish error {publish.status_code}: {publish.text[:200]}")
        except Exception as exc:
            return self._result("failed", error=str(exc))
