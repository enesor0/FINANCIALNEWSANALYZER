import unittest

from financial_news_analyzer.src.presentation.support import (
    SUPPORT_EMAIL,
    build_support_mailto,
    validate_support_request,
)


class SupportRequestTests(unittest.TestCase):
    def test_valid_request_has_no_validation_error(self):
        self.assertIsNone(validate_support_request("Ada Lovelace", "ada@example.com", "The data table is not loading on my browser."))

    def test_invalid_request_is_rejected(self):
        self.assertEqual(validate_support_request("A", "not-an-email", "short"), "Please enter your name.")

    def test_mailto_includes_recipient_and_encoded_message(self):
        url = build_support_mailto("Bug report", "Ada", "ada@example.com", "The market table does not load in Safari.")
        self.assertTrue(url.startswith(f"mailto:{SUPPORT_EMAIL}?"))
        self.assertIn("subject=Financial+News+Analyzer", url)
        self.assertIn("body=Name%3A+Ada", url)
