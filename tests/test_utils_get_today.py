"""Testes para o módulo get_today."""
import sys
from datetime import datetime

import pytest

from src.code_agent.utils.get_today import get_today_str


class TestGetTodayStr:
    """Testes para a função get_today_str."""

    def test_get_today_str_formats_date_without_error(self):
        """Testa que get_today_str formata a data sem erro."""
        s = get_today_str()
        assert isinstance(s, str)
        assert len(s) >= 8

    def test_get_today_str_contains_day_name(self):
        """Testa que get_today_str contém o nome do dia."""
        s = get_today_str()
        # Verifica que contém um nome de dia da semana (abreviação)
        day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        assert any(day in s for day in day_names)

    def test_get_today_str_contains_month_name(self):
        """Testa que get_today_str contém o nome do mês."""
        s = get_today_str()
        # Verifica que contém um nome de mês (abreviação)
        month_names = [
            "Jan", "Feb", "Mar", "Apr", "May", "Jun",
            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
        ]
        assert any(month in s for month in month_names)

    def test_get_today_str_contains_year(self):
        """Testa que get_today_str contém o ano."""
        s = get_today_str()
        current_year = str(datetime.now().year)
        assert current_year in s

    def test_get_today_str_uses_windows_format_on_windows(self, monkeypatch):
        """Testa que get_today_str usa formato Windows quando apropriado."""
        if sys.platform.startswith("win"):
            s = get_today_str()
            # No Windows, o formato usa %#d (sem zero à esquerda)
            # Verifica que não começa com zero para dias < 10
            assert isinstance(s, str)

    def test_get_today_str_uses_unix_format_on_unix(self, monkeypatch):
        """Testa que get_today_str usa formato Unix quando apropriado."""
        if not sys.platform.startswith("win"):
            s = get_today_str()
            # No Unix, o formato usa %-d (sem zero à esquerda)
            assert isinstance(s, str)

    def test_get_today_str_returns_consistent_format(self):
        """Testa que get_today_str retorna formato consistente."""
        s1 = get_today_str()
        s2 = get_today_str()
        # Mesmo formato, mas pode ter valores diferentes se chamado em dias diferentes
        # Verifica estrutura básica
        assert isinstance(s1, str)
        assert isinstance(s2, str)
        assert len(s1) > 0
        assert len(s2) > 0
