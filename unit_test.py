from team_mines import MineSweeper
import unittest


class TestMineSweeper(unittest.TestCase):

    def setUp(self):
        self.ms = MineSweeper("minefield.txt")

    def test__read_minefield(self):
        self.assertEqual(self.ms.files , ['. . . .\n. . . .\n* . . .\n. . * .\n. . . .'])

    def test_generate_hint(self):
        self.assertEqual(self.ms.generate_hint(2, 1), 1)


    def test_generate_map(self):
        self.assertEqual(self.ms.fields, ['Field #1:\n0000000\n1100000\n*101110\n1101*10\n0001110\n'])

    def test_create_output(self):
        with open('minesweeper_output.txt', 'r') as f:
            contents = f.read()

            self.assertEqual(contents, 'Field #1:\n0000000\n1100000\n*101110\n1101*10\n0001110\n')



if __name__ =="__main__":
    unittest.main()
