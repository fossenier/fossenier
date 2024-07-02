"""
The object representation of a Scotiabank fund.
"""

from typing import Dict


class Fund(object):
    def __init__(
        self,
        name: str = None,
        code: str = None,
        series: str = None,
        mer: float = None,
        years: Dict[int, float] = None,
    ) -> None:
        self.name = name  # the name of the fund
        self.code = code  # the distinguisihing code of the fund
        self.series = series  # the series of the fund
        self.MER = mer  # the (%) management expense ratio of the fund
        self.years = years  # the (%) performance of the fund by year
