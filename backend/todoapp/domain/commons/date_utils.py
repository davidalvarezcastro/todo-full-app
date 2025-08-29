from datetime import UTC, datetime


def get_utc_now() -> datetime:
    return datetime.now(tz=UTC)


def to_iso_format_with_z(date_to_convert: datetime) -> str:
    return date_to_convert.isoformat().replace("+00:00", "Z")
