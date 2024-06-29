import unittest
from unittest.mock import patch, MagicMock
from typing import List
from dataclasses import dataclass

from wavealign.utility.dict_to_dataclass_converter import DictToDataclassConverter


@dataclass
class OneLayerDataClass:
    field1: int
    field2: str


@dataclass
class NestedDataClass:
    field1: int
    nested: OneLayerDataClass


@dataclass
class NestedDataClassWithList:
    field1: int
    nested_list: List[OneLayerDataClass]


class TestConvertDictToDataClass(unittest.TestCase):
    def setUp(self):
        self.logger_patch = patch(
            "wavealign.utility.dict_to_dataclass_converter.logging.getLogger"
        )
        self.mock_get_logger = self.logger_patch.start()
        self.mock_logger = MagicMock()
        self.mock_get_logger.return_value = self.mock_logger
        self.converter = DictToDataclassConverter()

    def tearDown(self):
        self.logger_patch.stop()

    def test_extra_fields(self):
        data = {"field1": 1, "field2": "test", "extra_field": "extra"}
        result = self.converter.process(OneLayerDataClass, data)

        self.assertIsNone(result)
        self.mock_logger.debug.assert_called_with(
            "Additional field 'extra_field' found in the data dictionary."
        )

    def test_non_dataclass_conversion(self):
        result = self.converter.process(str, {})

        self.assertIsNone(result)
        self.mock_logger.debug.assert_called_with(
            f"class to convert to has to be of type dataclass. "
            f"Current conversion target {str} is of type {type(str)}."
        )

    def test_one_layer_conversion(self):
        data = {"field1": 1, "field2": "test"}

        result = self.converter.process(OneLayerDataClass, data)
        self.assertEqual(result, OneLayerDataClass(field1=1, field2="test"))

    def test_nested_conversion(self):
        data = {"field1": 1, "nested": {"field1": 2, "field2": "nested_test"}}

        result = self.converter.process(NestedDataClass, data)
        self.assertEqual(
            result,
            NestedDataClass(
                field1=1, nested=OneLayerDataClass(field1=2, field2="nested_test")
            ),
        )

    def test_nested_list_conversion(self):
        data = {
            "field1": 1,
            "nested_list": [
                {"field1": 2, "field2": "test1"},
                {"field1": 3, "field2": "test2"},
            ],
        }

        result = self.converter.process(NestedDataClassWithList, data)
        self.assertEqual(
            result,
            NestedDataClassWithList(
                field1=1,
                nested_list=[
                    OneLayerDataClass(field1=2, field2="test1"),
                    OneLayerDataClass(field1=3, field2="test2"),
                ],
            ),
        )


if __name__ == "__main__":
    unittest.main()
