from unittest import TestCase
from spreadsheet import SpreadSheet

class TestSpreadSheet(TestCase):

    def test_spreadsheet_evaluate_integer_number(self):
        spreadsheet = SpreadSheet()
        spreadsheet.set("A1", "1")
        self.assertEqual(1, spreadsheet.evaluate("A1"))

    def test_spreadsheet_evaluate_non_integer_number(self):
        spreadsheet = SpreadSheet()
        spreadsheet.set("A1", "1.5")
        self.assertEqual("#Error", spreadsheet.evaluate("A1"))

    def test_spreadsheet_evaluate_valid_string(self):
        spreadsheet = SpreadSheet()
        spreadsheet.set("A1", "'Apple'")
        self.assertEqual("Apple", spreadsheet.evaluate("A1"))

    def test_spreadsheet_evaluate_string_with_missing_end_quote(self):
        spreadsheet = SpreadSheet()
        spreadsheet.set("A1", "'Apple")
        self.assertEqual("#Error", spreadsheet.evaluate("A1"))

    def test_spreadsheet_evaluate_string_with_missing_start_quote(self):
        spreadsheet = SpreadSheet()
        spreadsheet.set("A1", "Apple'")
        self.assertEqual("#Error", spreadsheet.evaluate("A1"))

    def test_spreadsheet_evaluate_simple_formula_with_integer(self):
        spreadsheet = SpreadSheet()
        spreadsheet.set("A1", "=1")
        self.assertEqual(1, spreadsheet.evaluate("A1"))

    def test_spreadsheet_evaluate_simple_formula_with_valid_string(self):
        spreadsheet = SpreadSheet()
        spreadsheet.set("A1", "='Apple'")
        self.assertEqual("Apple", spreadsheet.evaluate("A1"))

    def test_spreadsheet_evaluate_simple_formula_with_invalid_string(self):
        spreadsheet = SpreadSheet()
        spreadsheet.set("A1", "='Apple")
        self.assertEqual("#Error", spreadsheet.evaluate("A1"))

    def test_spreadsheet_evaluate_simple_formula_with_invalid_integer(self):
        spreadsheet = SpreadSheet()
        spreadsheet.set("A1", "=1.5")
        self.assertEqual("#Error", spreadsheet.evaluate("A1"))

    def test_spreadsheet_evaluate_formula_with_reference(self):
        spreadsheet = SpreadSheet()
        spreadsheet.set("B1", "42")
        spreadsheet.set("A1", "=B1")
        self.assertEqual(42, spreadsheet.evaluate("A1"))

    def test_spreadsheet_evaluate_formula_with_reference_to_float(self):
        spreadsheet = SpreadSheet()
        spreadsheet.set("B1", "42.5")
        spreadsheet.set("A1", "=B1")
        self.assertEqual("#Error", spreadsheet.evaluate("A1"))

    def test_spreadsheet_evaluate_formula_with_circular_reference(self):
        spreadsheet = SpreadSheet()
        spreadsheet.set("A1", "=B1")
        spreadsheet.set("B1", "=A1")
        self.assertEqual("#Circular", spreadsheet.evaluate("A1"))

    def test_spreadsheet_evaluate_arithmetic_addition(self):
        spreadsheet = SpreadSheet()
        spreadsheet.set("A1", "=1+3")
        self.assertEqual(4, spreadsheet.evaluate("A1"))

    def test_spreadsheet_evaluate_arithmetic_with_float(self):
        spreadsheet = SpreadSheet()
        spreadsheet.set("A1", "=1+3.5")
        self.assertEqual("#Error", spreadsheet.evaluate("A1"))

    def test_spreadsheet_evaluate_arithmetic_division_by_zero(self):
        spreadsheet = SpreadSheet()
        spreadsheet.set("A1", "=1/0")
        self.assertEqual("#Error", spreadsheet.evaluate("A1"))

    def test_spreadsheet_evaluate_arithmetic_with_precedence(self):
        spreadsheet = SpreadSheet()
        spreadsheet.set("A1", "=1+3*2")
        self.assertEqual(7, spreadsheet.evaluate("A1"))

    def test_spreadsheet_evaluate_formula_with_arithmetic_and_reference(self):
        spreadsheet = SpreadSheet()
        spreadsheet.set("B1", "3")
        spreadsheet.set("A1", "=1+B1")
        self.assertEqual(4, spreadsheet.evaluate("A1"))

    def test_spreadsheet_evaluate_formula_with_arithmetic_and_reference_to_float(self):
        spreadsheet = SpreadSheet()
        spreadsheet.set("B1", "3.1")
        spreadsheet.set("A1", "=1+B1")
        self.assertEqual("#Error", spreadsheet.evaluate("A1"))

    def test_spreadsheet_evaluate_formula_with_circular_reference_in_arithmetic(self):
        spreadsheet = SpreadSheet()
        spreadsheet.set("A1", "=1+B1")
        spreadsheet.set("B1", "=A1")
        self.assertEqual("#Circular", spreadsheet.evaluate("A1"))
