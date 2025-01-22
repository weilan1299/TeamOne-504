import random
def generate_minefield(rows, cols, mine_percentage):
    minefield = [["." for _ in range(cols)] for _ in range(rows)]
    num_mines = int(mine_percentage/100 * rows *cols)

    for _ in range(num_mines):
        while True:
            row = random.randint(0, rows - 1)
            col = random.randint(0, cols - 1)
            if minefield[row][col] != "*":
                minefield[row][cols] = "*"
                break
    return minefield

def write_minefield_to_file(rows, cols, minefield, filename):
    with open(filename, "w") as file:
        file.write(f"{rows} {cols} \n")
        for row in minefield:
            file.write(' '.join(row) + '\n')

def main():
    while True:
        rows = int(input("Enter number of rows: "))
        cols = int(input("Enter number of columns: "))
        mine_percentage = float(input("Enter percentage of mines (e.g: 20): "))
        filename = "minefield.txt"

        minefield = generate_minefield(rows, cols, mine_percentage)
        write_minefield_to_file(rows, cols, minefield, filename)

        another_minefield = input("Would you like to play another mine? (y/n): ")
        if another_minefield.lower != "yes":
            break
if __name__ == "__main__":
    main()
