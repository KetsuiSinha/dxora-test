import httpx
from app.config import settings
from app.platforms.base import BasePlatform


class TelegramPlatform(BasePlatform):
    name = "Telegram"

    def post(self, message: str) -> dict:
        if not settings.telegram_bot_token or not settings.telegram_chat_id:
            return self._result("failed", error="TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not configured")
        try:
            with httpx.Client(timeout=20) as client:
                resp = client.post(
                    f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage",
                    data={"chat_id": settings.telegram_chat_id, "text": message, "disable_web_page_preview": False},
                )
            if resp.status_code == 200:
                data = resp.json()
                if data.get("ok"):
                    msg = data.get("result", {})
                    return self._result("success", posted_url="https://t.me/", public_access=True)
                return self._result("failed", error=f"Telegram API error: {data.get('description')}")
            return self._result("failed", error=f"Telegram API error {resp.status_code}: {resp.text[:200]}")
        except Exception as exc:
            return self._result("failed", error=str(exc))
