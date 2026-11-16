from typing import List, Optional, Any
from pydantic import BaseModel, Field, validator


class PostingRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=200)

    @validator("message")
    def message_must_contain_exactly_one_url(cls, v):
        import re
        url_pattern = r"https?://\S+"
        urls = re.findall(url_pattern, v)
        if len(urls) != 1:
            raise ValueError("Message must contain exactly one URL (CTA link)")
        from pydantic import HttpUrl
        try:
            HttpUrl(urls[0])
        except Exception:
            raise ValueError("The URL in the message is not valid")
        return v


class PlatformResult(BaseModel):
    platform: str
    status: str  # success / failed
    posted_url: Optional[str] = None
    public_access: bool = False
    date: Optional[str] = None
    time: Optional[str] = None
    error: Optional[str] = None


class PostingResponse(BaseModel):
    success: bool
    results: List[PlatformResult] = []


class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    detail: Optional[Any] = None
