

import re


class MineSweeper:
    """
        Create an output file that detects surrounding mines for a set of data.

    """

    def __init__(self):
        """
        Initialize a MinSweeper instance.
        """
        self.__mines = "mines.txt"
        self.__read_minefield()
        self.__fields = []
        self.__generate_map()
        self.__create_output()

    def __read_minefield(self):
        """
        Open and read the mines file

        """
        with open(self.__mines, "r") as mines_files:
            contents = mines_files.read()

            self.__files = [file.strip() for file in re.split(r"\d", contents) if file.strip()]

    def __generate_hint(self, lines, x, y):
        """
        Determine the number of mines around point

        :param lines:list
        :param x:int
        :param y:int
        :return: int
        """

        surrounding = [(x - 1, y - 1), (x - 1, y),
                       (x - 1, y + 1), (x, y - 1),
                       (x, y + 1), (x + 1, y - 1),
                       (x + 1, y), (x + 1, y + 1)]
        num = 0
        for i, j in surrounding:
            if 0 <= i < len(lines) and 0 <= j < len(lines[0]):
                if lines[i][j] == "*":
                    num += 1

        return num

    def __generate_map(self):
        """
        Generate a map of mines
        """
        for i, file in enumerate(self.__files, start=1):
            lines = [list(line) for line in file.splitlines() if line.strip()]

            mines_map = []

            for x in range(len(lines)):
                rows = []

                for y in range(len(lines[x])):
                    if lines[x][y] == "*":
                        rows.append(lines[x][y])

                    elif lines[x][y]:

                        count = self.__generate_hint(lines, x, y)

                        rows.append(str(count))

                mines_map.append("".join(rows))

            self.__fields.append(f"Field #{i}:" + "\n" + "\n".join(mines_map) + "\n")

    def __create_output(self):
        """
        Create a file for all mines field
        """
        with open("minesweeper_output.txt", "w") as output:
            output.write("\n".join(self.__fields))


mines_read = MineSweeper()
