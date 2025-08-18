import csv
import os
import yaml
from pathlib import Path

class FileUtils:
    @staticmethod
    def read_csv(path_obj: Path):
        """
        Reads a CSV and returns a list of dicts.
        """
        rows = []
        with open(path_obj, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                rows.append(row)
        return rows

    @staticmethod
    def get_data_for_test(test_name: str, path_obj: Path):
        """
        Fetch a single row from CSV that matches the test_case_name column.
        """
        rows = FileUtils.read_csv(path_obj)
        for row in rows:
            if row.get("test_case_name") == test_name:
                return row
        raise ValueError(f"No test data found for {test_name} in {path_obj}")


    @staticmethod
    def read_yaml(path_obj: Path):
        with open(path_obj, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    @staticmethod
    def get_locator(page: str, locator_name: str, path_obj: Path) -> str:
        locators = FileUtils.read_yaml(path_obj)
        try:
            return locators[page][locator_name]
        except KeyError:
            raise ValueError(f"Locator '{locator_name}' not found for page '{page}' in {path_obj}")

