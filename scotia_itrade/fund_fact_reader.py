"""
Reads Scotiabank Fund Facts and pulls out the performance data.
"""

from pdfminer.layout import LAParams, LTPage, LTTextBoxHorizontal
from pdfminer.high_level import extract_pages

