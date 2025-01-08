import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game.
    A sentence consists of a set of board cells,
    and a count of how many of those cells are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return self.cells
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.
        """
        # 1. Mark the cell as a move made
        self.moves_made.add(cell)

        # 2. Mark the cell as safe
        self.mark_safe(cell)

        # 3. Identify all neighbors (including known mines!)
        neighbors = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if (i, j) != cell and 0 <= i < self.height and 0 <= j < self.width:
                    neighbors.add((i, j))

        # Remove only known safe cells from neighbors
        neighbors -= self.safes

        # Construct a new sentence:
        #   We do NOT remove known mines from `neighbors`. Instead, we keep them
        #   so that this sentence accurately represents "count" mines among these neighbors.
        #   Then we immediately use `mark_mine` to update that sentence.
        new_sentence = Sentence(neighbors, count)

        # 4. "Mark" any known mines in the new sentence so that the sentence is consistent
        for known_mine in self.mines:
            new_sentence.mark_mine(known_mine)

        # 5. Add the new sentence to knowledge if non-empty
        if new_sentence.cells and new_sentence not in self.knowledge:
            self.knowledge.append(new_sentence)

        # 6. Mark additional cells as safe or mines based on existing sentences
        self.update_knowledge()

    def update_knowledge(self):
        """
        Repeatedly updates knowledge by:
         - Marking known safes/mines from each sentence
         - Combining sentences if one is a subset of another
         - Re-marking any additional safes/mines discovered
        """
        while True:
            found_something = False

            # a) Mark safes and mines in all sentences
            safes_to_mark = set()
            mines_to_mark = set()

            for sentence in self.knowledge:
                safes_to_mark |= sentence.known_safes()
                mines_to_mark |= sentence.known_mines()

            # Mark all found safes and mines
            for safe in safes_to_mark:
                if safe not in self.safes:
                    self.mark_safe(safe)
                    found_something = True
            for mine in mines_to_mark:
                if mine not in self.mines:
                    self.mark_mine(mine)
                    found_something = True

            # b) Subset-based inference
            new_inferences = []
            for s1 in self.knowledge:
                for s2 in self.knowledge:
                    if s1 != s2 and s1.cells.issubset(s2.cells):
                        inferred_cells = s2.cells - s1.cells
                        inferred_count = s2.count - s1.count
                        inferred = Sentence(inferred_cells, inferred_count)
                        if inferred not in self.knowledge and inferred not in new_inferences:
                            new_inferences.append(inferred)

            # c) Add new inferences
            for inferred in new_inferences:
                if inferred.cells:
                    self.knowledge.append(inferred)
                    found_something = True

            # d) If no new info was discovered, stop updating
            if not found_something:
                break

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        """
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        """
        all_cells = {(i, j) for i in range(self.height) for j in range(self.width)}
        valid_moves = list(all_cells - self.moves_made - self.mines)
        if valid_moves:
            return random.choice(valid_moves)
        return None
