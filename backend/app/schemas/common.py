from datetime import date, datetime, time

from pydantic import BaseModel, ConfigDict


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class MessageResponse(BaseModel):
    message: str


class ChartPoint(BaseModel):
    date: date
    value: float


class DateRangeQuery(BaseModel):
    start_date: date
    end_date: date


class TimeWindow(BaseModel):
    start_time: time | None = None
    end_time: time | None = None


class TimestampFields(ORMModel):
    created_at: datetime
    updated_at: datetime
