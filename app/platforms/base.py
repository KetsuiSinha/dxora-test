from abc import ABC, abstractmethod
from typing import Optional
from datetime import datetime


class BasePlatform(ABC):
    name: str = "Base Platform"

    @abstractmethod
    def post(self, message: str) -> dict:
        """Post a message. Returns a PlatformResult-compatible dict."""

    def _result(self, status: str, posted_url: Optional[str] = None,
                public_access: bool = False, error: Optional[str] = None) -> dict:
        now = datetime.utcnow()
        return {
            "platform": self.name,
            "status": status,
            "posted_url": posted_url,
            "public_access": public_access,
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M:%S"),
            "error": error,
        }
