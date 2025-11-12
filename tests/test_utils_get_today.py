from src.code_agent.utils.get_today import get_today_str


def test_get_today_str_formats_date_without_error():
    s = get_today_str()
    assert isinstance(s, str) and "," in s and len(s) >= 8


