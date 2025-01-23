from team_one_mines import MineSweeper
# Changed variable and method to public for unit test 
import unittest

# This class tests the team_one_mines.py
class TestMineSweeper(unittest.TestCase):

    def setUp(self): # Tests minefield input
        self.ms = MineSweeper("minefield.txt")

    def test__read_minefield(self): # Tests to read a file and generate right content
        self.assertEqual(self.ms.files , ['. . . .\n. . . .\n* . . .\n. . * .\n. . . .'])

    def test_generate_hint(self): # Tests the generator hint method
        self.assertEqual(self.ms.generate_hint(2, 1), 1)


    def test_generate_map(self): # Tests the generated map 
        self.assertEqual(self.ms.fields, ['Field #1:\n0000000\n1100000\n*101110\n1101*10\n0001110\n'])

    def test_create_output(self): # Tests the created output file and right content
        with open('minesweeper_output.txt', 'r') as f:
            contents = f.read()

            self.assertEqual(contents, 'Field #1:\n0000000\n1100000\n*101110\n1101*10\n0001110\n')



if __name__ =="__main__": # It is a unti test funtion
    unittest.main()

