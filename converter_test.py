
import unittest

from converter import convert


class TableConverterTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
    
    
    def test_converts_plaintext_table_with_single_entries(self):
        input = """d20	Purpose
1	One
2	Two
3	Three
4	Four
5	Five
6	Six"""
        actual = convert(input)
        expected = """
---
One
Two
Three
Four
Five
Six

---"""
        self.assertEqual(actual, expected)
    
    def test_converts_plaintext_table_with_range_entries(self):
        input = """d20	Purpose
1-2	One
3	Two
4-6	Three
7	Four
8	Five
9-10	Six"""
        actual = convert(input)
        expected = """
---
One
One
Two
Three
Three
Three
Four
Five
Six
Six

---"""
        self.assertEqual(actual, expected)
    
    def test_converts_markdown_table_with_single_entries(self):
        input = """|[**d20**](http://some.url)|Purpose|
|---|---|
|1|One|
|2|Two|
|3|Three|
|4|Four|
|5|Five|
|6|Six|"""
        actual = convert(input)
        expected = """
---
One
Two
Three
Four
Five
Six

---"""
        self.assertEqual(actual, expected)
    
    def test_converts_markdown_table_with_range_entries(self):
        input = """|[**d20**](http://some.url)|Purpose|
|---|---|
|1-2|One|
|3|Two|
|4-6|Three|
|7|Four|
|8|Five|
|9-10|Six|"""
        actual = convert(input)
        expected = """
---
One
One
Two
Three
Three
Three
Four
Five
Six
Six

---"""
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
