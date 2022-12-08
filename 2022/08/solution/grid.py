from solution.tree import Tree


class Grid:
    def __init__(self, lines: list[str]):
        assert lines, f"invalid input {lines}!"
        self._grid: list[list[Tree]] = []
        for line in lines:
            grid_line: list[Tree] = []
            for tree_height in line:
                grid_line.append(Tree(int(tree_height)))
            self._grid.append(grid_line)

    def get_viewable_trees(self) -> int:
        self._process_grid()
        return self._sum_viewable_trees()

    def get_max_scenic_score(self) -> int:
        scenic_score = 0
        for row_idx in range(len(self._grid)):
            for col_idx in range(len(self._grid[0])):
                scenic_score = max(scenic_score, self._get_scenic_score(row_idx, col_idx))
        return scenic_score

    def print(self):
        for row in self._grid:
            print([(" ", "X")[tree.visible] for tree in row])

    def _process_grid(self) -> None:
        # process the grid row by row
        for row in self._grid:
            self._process_row(row)
        # process the grid row by row reversed
        for row in reversed(self._grid):
            self._process_row(row)
        # process the grid col by col
        for row_idx in range(len(self._grid[0])):
            self._process_col(row_idx)

    def _process_row(self, row: list[Tree]) -> None:
        # process the grid from left to right
        height = -1
        for tree in row:
            height = self._process_tree(height, tree)
        # process the grid from right to left
        height = -1
        for tree in reversed(row):
            height = self._process_tree(height, tree)

    def _process_tree(self, height: int, tree: Tree) -> int:
        if tree.height > height:
            tree.visible = True
            height = tree.height
        return height

    def _process_col(self, row_idx: int) -> None:
        # process the grid from top to bottom
        height = -1
        for col_idx in range(len(self._grid)):
            tree = self._grid[col_idx][row_idx]
            height = self._process_tree(height, tree)
        # process the grid from bottom to top
        height = -1
        for col_idx in reversed(range(len(self._grid))):
            tree = self._grid[col_idx][row_idx]
            height = self._process_tree(height, tree)

    def _sum_viewable_trees(self) -> int:
        viewable_trees = 0
        for row in self._grid:
            viewable_trees += len([tree for tree in row if tree.visible])
        return viewable_trees

    def _get_scenic_score(self, tree_row_idx: int, tree_col_idx: int) -> int:
        tree_height = self._grid[tree_row_idx][tree_col_idx].height
        # calculate the score in up direction
        score_up = 0
        for row_idx in reversed(range(tree_row_idx)):
            score_up += 1
            if self._grid[row_idx][tree_col_idx].height >= tree_height:
                break
        # calculate the score in down direction
        score_down = 0
        for row_idx in range(tree_row_idx + 1, len(self._grid)):
            score_down += 1
            if self._grid[row_idx][tree_col_idx].height >= tree_height:
                break
        # calculate the score in left direction
        score_left = 0
        for col_idx in reversed(range(tree_col_idx)):
            score_left += 1
            if self._grid[tree_row_idx][col_idx].height >= tree_height:
                break
        # calculate the score in right direction
        score_right = 0
        for col_idx in range(tree_col_idx + 1, len(self._grid[0])):
            score_right += 1
            if self._grid[tree_row_idx][col_idx].height >= tree_height:
                break
        # calculate and return the scenic score
        return score_up * score_down * score_left * score_right
