import logging
from enum import Enum
from typing import Optional
from datetime import timedelta, datetime


class SyncHealthStatus(Enum):
    OK = "ok"
    MISSING = "missing"
    STALE = "stale"

class SyncFunctionHealthReport:
    def __init__(
        self,
        function_name: str,
        alert_threshold: timedelta,
        last_synced_at: Optional[datetime],
        logger: logging.Logger
    ):
        self.function_name = function_name
        self.alert_threshold = alert_threshold
        self.last_synced_at = last_synced_at
        self.logger = logger

    def _calculate_data_age(self, current_time: datetime) -> Optional[timedelta]:
        if not self.last_synced_at:
            return None
        return current_time - self.last_synced_at

    def _evaluate_status(self, age: Optional[timedelta]) -> SyncHealthStatus:
        if not self.last_synced_at:
            return SyncHealthStatus.MISSING
        if age < self.alert_threshold:
            return SyncHealthStatus.OK
        return SyncHealthStatus.STALE

    def emit_telemetry(self, current_time: datetime):
        age = self._calculate_data_age(current_time)
        status = self._evaluate_status(age)
        self.logger.info("Sync health check", extra={
            "custom_dimensions": {
                "function_name": self.function_name,
                "status": status.value,
                "last_synced_at": str(self.last_synced_at) if self.last_synced_at else None,
                "age_days": round(age.total_seconds() / 86400, 2) if age else None,
                "time_now": current_time.isoformat()
            }
        })