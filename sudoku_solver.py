from itertools import product, chain
from more_itertools import flatten, distribute, chunked

grille = [
['', '', '', '', '', '', 6, 8, ''],
['', '', '', '', 7, 3, '', '', 9],
[3, '', 9, '', '', '', '', 4, 5],
[4, 9, '', '', '', '', '', '', ''],
[8, '', 3, '', 5, '', 9, '', 2],
['', '', '', '', '', '', '', 3, 6],
[9, 6, '', '', '', '', 3, '', 8],
[7, '', '', 6, 8, '', '', '', ''],
['', 2, 8, '', '', '', '', '', '']
]

class sudokuSolver:

    def __init__(self, grid):
        self.grid = grid
        self.everyPositions = set(product(range(1, 10), range(1, 10)))

    def divide_grid_in_blocs(self, grid):
        """
        Permet de diviser une grille en
        neuf blocs différents
        :returns: list
        """
        return list(flatten(map(lambda row: map(list, distribute(3, chunked(row, 3))), chunked(flatten(grid), 27))))

    def isValid(self, grid, position, num):
        """
        Méthode vérifiant si la présence de 'num'
        dans la case 'position' est légale
        :returns: bool
        """
        n, i, j = position
        bloc, line, row = flatten(self.divide_grid_in_blocs(grid)[n]), grid[i-1], (line[j-1] for line in grid)

        return num not in chain(bloc, line, row)

    def emptyCell(self, grid):
        """
        Méthode qui trouve une case vide et
        retourne sa position
        :returns: (n, i, j) = (bloc, line, row)
        """
        for i, line in enumerate(grid, start=1):
            for j, num in enumerate(line, start=1):
                if not num:
                    blocs = enumerate(self.divide_grid_in_blocs(chunked(sorted(self.everyPositions), 9)))
                    for index, bloc in blocs:
                        if (i, j) in flatten(bloc):
                            n = index # bloc numéro n
                            break
                    return (n, i, j)
        return None

    def solver(self, grid):
        """
        Méthode permettant de résoudre le sudoku
        si une solution existe.
        :returns: grid
        """
        cell = self.emptyCell(self.grid)
        if not cell:
            return True

        n, i, j = cell
        for num in range(1, 10):
            if self.isValid(self.grid, (n, i, j), num):
                # placement d'un chiffre
                self.grid[i-1][j-1] = num
                # vérifions si ce placement mène à une solution
                if self.solver(self.grid):
                    return True
                # échec, on remet la case vide et on recommence avec le prochain chiffre
                self.grid[i-1][j-1] = ''

        return False

    def displayGrid(self, grid):
        return '\n'.join(' '.join(str(spot) if spot else ' ' for spot in line) for line in grid)
