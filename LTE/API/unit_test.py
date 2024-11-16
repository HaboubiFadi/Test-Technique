
'''

Purpose
The unit tests for the Processing_funs module ensure that each function performs its intended computations 
correctly and returns the expected outputs. By simulating database behavior using MagicMock, 
these tests validate the functions' logic in isolation, free from external dependencies.

How It Works
* Mocking Database Interaction:

* A mock object (MagicMock) simulates the database cursor.
    Predefined query results are set up for specific SQL queries to test the logic of each function.
* Testing Process:
    The function under test is executed with the mocked cursor.


Tests ensure that the functions handle unexpected or edge-case inputs gracefully.



'''



import unittest 
from unittest.mock import MagicMock
import pandas as pd
from Processing_funs import (
    Calcule_Profit,
    Calculate_Exceptional_charges_Groupby_year,
    Calcul_profitability_analysis,
    Calcul_Expense_per_categorie,
    Return_on_investiment_per_year,
)


class TestProcessingFunctions(unittest.TestCase):
    def test_calcule_profit(self):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            (2021, 200),
            (2022, 500),
        ]
        result = Calcule_Profit(mock_cursor)
        expected = pd.DataFrame({"Year": [2021, 2022], "Profit": [200, 500]})
        pd.testing.assert_frame_equal(result, expected)

    def test_calculate_exceptional_charges_groupby_year(self):
        # Mock cursor
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            (2021, "EXCEPTIONNEL", "CHARGES", 1000),
            (2021, "EXCEPTIONNEL", "CHARGES", 500),
            (2022, "EXCEPTIONNEL", "CHARGES", 800),
        ]
        # Call function
        result = Calculate_Exceptional_charges_Groupby_year(mock_cursor)
        # Expected result
        expected = pd.DataFrame({
            "exercice_comptable": [2021, 2022],
            "exceptional_charges": [1500, 800]
        })
        pd.testing.assert_frame_equal(result, expected)

    def test_calcul_profitability_analysis(self):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            (2021, 3000, 2000),
            (2022, 5000, 2500),
        ]
        result = Calcul_profitability_analysis(mock_cursor)
        expected = pd.DataFrame({
            "year": [2021, 2022],
            "Core_profit": [3000, 5000],
            "Core_cost": [2000, 2500],
        })
        pd.testing.assert_frame_equal(result, expected)

    def test_calcul_expense_per_categorie(self):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            (2021, "CHARGES DE FONCTIONNEMENT", 1000),
            (2021, "CHARGES FINANCIERES", 1500),
            (2022, "CHARGES DE FONCTIONNEMENT", 1200),
            (2022, "CHARGES FINANCIERES", 1800),
        ]
        result = Calcul_Expense_per_categorie(mock_cursor)
        expected = pd.DataFrame({
            "Year": [2021, 2021, 2022, 2022],
            "category": ["CHARGES DE FONCTIONNEMENT", "CHARGES FINANCIERES", "CHARGES DE FONCTIONNEMENT", "CHARGES FINANCIERES"],
            "Expense_EUR": [1000, 1500, 1200, 1800],
        })
        pd.testing.assert_frame_equal(result, expected)

    def test_return_on_investiment_per_year(self):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            (2021, 1000),
            (2022, 1500),
        ]
        result = Return_on_investiment_per_year(mock_cursor)
        expected = pd.DataFrame({
            "Year": [2021, 2022],
            "Profit_EUR": [1000, 1500],
        })
        pd.testing.assert_frame_equal(result, expected)

if __name__ == "__main__":
    unittest.main()