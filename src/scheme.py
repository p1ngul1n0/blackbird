from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field, HttpUrl, PositiveInt


class Metadata(BaseModel):
    type: str
    key: str
    value: str


class Site(BaseModel):
    id: PositiveInt
    app: str
    method: str
    headers: Optional[str] = None
    json_: Optional[str] = Field(default=None, alias='json')
    url: str
    valid: str
    metadata: List[Metadata] = Field(default_factory=lambda: [])


class ReportStatus(str, Enum):
    FOUND = 'FOUND'
    NOT_FOUND = 'NOT FOUND'
    ERROR = 'ERROR'


class Report(BaseModel):
    id: int
    app: str
    url: HttpUrl
    response_status: Optional[str] = Field(default=None, alias='response-status')
    status: ReportStatus
    error_message: Optional[str] = Field(default=None, alias='error-message')
    metadata: List[Dict[str, str]]

    class Config:
        allow_population_by_field_name = True