"""Use case for one instrument's detailed profile."""

from __future__ import annotations

import re

from ...domain.entities.market_data import InstrumentProfile
from ..ports.market_data_provider import InstrumentProfileProvider


class GetInstrumentProfileUseCase:
    """Validate a symbol before requesting its detailed provider profile."""

    _symbol_pattern = re.compile(r"^[A-Z0-9.^=-]{1,20}$")

    def __init__(self, provider: InstrumentProfileProvider) -> None:
        self._provider = provider

    def execute(self, symbol: str) -> InstrumentProfile:
        normalized_symbol = symbol.strip().upper()
        if not self._symbol_pattern.fullmatch(normalized_symbol):
            raise ValueError("The symbol format is not supported.")
        return self._provider.get_instrument_profile(normalized_symbol)
