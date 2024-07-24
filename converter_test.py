
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

    def test_real_world_plaintext_example(self):
        input = """d20	Purpose
1	Antechamber or waiting room for spectators
2–8	Guardroom fortified against intruders
9–11	Vault for holding important treasures, accessible only by locked or secret door (75 percent chance of being trapped)
12–14	Room containing a puzzle that must be solved to bypass a trap or monster
15–19	Trap designed to kill or capture creatures
20	Observation room, allowing guards or spectators to observe creatures moving through the dungeon
"""
        actual = convert(input)
        expected = """
---
Antechamber or waiting room for spectators
Guardroom fortified against intruders
Guardroom fortified against intruders
Guardroom fortified against intruders
Guardroom fortified against intruders
Guardroom fortified against intruders
Guardroom fortified against intruders
Guardroom fortified against intruders
Vault for holding important treasures, accessible only by locked or secret door (75 percent chance of being trapped)
Vault for holding important treasures, accessible only by locked or secret door (75 percent chance of being trapped)
Vault for holding important treasures, accessible only by locked or secret door (75 percent chance of being trapped)
Room containing a puzzle that must be solved to bypass a trap or monster
Room containing a puzzle that must be solved to bypass a trap or monster
Room containing a puzzle that must be solved to bypass a trap or monster
Trap designed to kill or capture creatures
Trap designed to kill or capture creatures
Trap designed to kill or capture creatures
Trap designed to kill or capture creatures
Trap designed to kill or capture creatures
Observation room, allowing guards or spectators to observe creatures moving through the dungeon

---"""


if __name__ == "__main__":
    unittest.main()
