
import os
from pathlib import Path
import unittest

from converter import convert, convert_single_words, copy_encounter_tables


class TableConverterTest(unittest.TestCase):
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
        self.assertEqual(actual, expected)

    def test_handles_spaces_in_ranges(self):
        input = """d20	Purpose
1- 2	One
3	Two
4 - 6	Three
7	Four
8	Five
9 -10	Six"""
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

class SingleWordTableTest(unittest.TestCase):
    def test_single_word_rows_converted_to_table(self):
        input = """1. One 2. Two 3. Three 4. Four 5. Five 6. Six 7. Seven 8. Eight 9. Nine 10. Ten"""
        actual = convert_single_words(input)
        expected = """
---
One
Two
Three
Four
Five
Six
Seven
Eight
Nine
Ten

---"""
        self.assertEqual(actual, expected)

class EncounterTablesTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        os.chdir("test-data")

    def tearDown(self) -> None:
        super().tearDown()
        os.chdir("..")

    def test_encounters_copies_files_with_replacements(self):
        copy_encounter_tables("Forest", "Coastal")
        self.assertFileContents("Coastal - Easy.md", """
---
{Ref/Monster_Coastal/CR1_8}, 2x {Ref/Monster_Coastal/CR0}
{Ref/Monster_Coastal/CR1_4}, {Ref/Monster_Coastal/CR0}
{Ref/Monster_Coastal/CR1_2}

---""")
        self.assertFileContents("Coastal - Medium.md", """
---
{Ref/Monster_Coastal/CR1_4}, 2x {Ref/Monster_Coastal/CR1_8}
2x {Ref/Monster_Coastal/CR1_8}, {Ref/Monster_Coastal/CR1_4}
{Ref/Monster_Coastal/CR1}

---""")
        
    def assertFileContents(self, filename: str, file_contents: str) -> None:
        p = Path(filename)
        self.assertTrue(p.is_file(), f"File {filename} does not exist, but expected it to")
        with p.open() as f:
            contents = f.read()
            self.assertEqual(contents, file_contents, f"Contents of file {filename} don't match what was expected")

if __name__ == "__main__":
    unittest.main()
