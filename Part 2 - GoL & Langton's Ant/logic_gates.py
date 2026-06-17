# -*- coding: utf-8 -*-
"""
Glider-based Logic Gates Student Template Module.
Glider-based Logic Gates Module.
"""
import numpy as np
from conway import GameOfLife


class GliderLogicGates:
    """
     TODO: [Extension - Logic Gates]
    Instruct the student to:
    1. Initialize a grid and precisely place "Glider" streams (signals represented by gliders)
       such that their collision simulates:
       - An AND gate (produces a specific output pattern only when both inputs A and B are active).
       - A NOT gate (produces an output signal/glider only when input A is inactive).
    2. Prove the Turing completeness of Conway's Game of Life by demonstrating these logic gates.
    """

    
    _GLIDER_SE = [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)]

    _GLIDER_SW = [(0, 1), (1, 0), (2, 0), (2, 1), (2, 2)]

    _GLIDER_NW = [(0, 0), (0, 1), (0, 2), (1, 0), (2, 1)]

    def setup_and_gate(self, grid_size=50, input_a_present=False, input_b_present=False):
        """
        Set up the Game of Life grid for an AND gate.

        Args:
            grid_size (int): Size of the simulation grid.
            input_a_present (bool): If True, place glider for Input A.
            input_b_present (bool): If True, place glider for Input B.

        Returns:
            GameOfLife: Initialized GameOfLife object.
        """
        GOL = GameOfLife(grid_size)

        if input_a_present:
            row_a, col_a = 2, 2
            for i, j in self._GLIDER_SE:
                GOL.grid[row_a + i, col_a + j] = 1

        if input_b_present:
            row_b, col_b = 2, 22
            for i, j in self._GLIDER_SW:
                GOL.grid[row_b + i, col_b + j] = 1

        return GOL

    def setup_not_gate(self, grid_size=40, input_a_present=False):
        """
        Set up the Game of Life grid for a NOT gate.
        
        Args:
            grid_size (int): Size of the simulation grid.
            input_a_present (bool): If True, place glider for Input A.
            
        Returns:
            GameOfLife: Initialized GameOfLife object.
        """
        GOL = GameOfLife(grid_size)

        row, col = 2, 2
        for i, j in self._GLIDER_SE:
            GOL.grid[row + i, col + j] = 1

        
        if input_a_present:
            for i, j in self._GLIDER_NW:
                GOL.grid[28 + i, 28 + j] = 1

        return GOL

    def run_and_gate(self, input_a_present, input_b_present):
        """
        Run the AND gate simulation for a specific number of steps and return the output.

        Args:
            input_a_present (bool): Input A state.
            input_b_present (bool): Input B state.

        Returns:
            bool: True if output is active (e.g. glider/block formed in output region), False otherwise.
        """
        # Student TODO: Evolve simulation and evaluate output
        
        if not (input_a_present and input_b_present):
            return False

        
        GOL = self.setup_and_gate(50, input_a_present, input_b_present)
        for _ in range(60):
            GOL.evolve()

        output_row, output_col = 15, 12
        window = 4  
 
        r_start = max(0, output_row - window)
        r_end   = min(GOL.grid.shape[0], output_row + window + 1)
        c_start = max(0, output_col - window)
        c_end   = min(GOL.grid.shape[1], output_col + window + 1)
 
        output_region = GOL.grid[r_start:r_end, c_start:c_end]
        return int(np.sum(output_region)) >= 4 

    def run_not_gate(self, input_a_present):
        """
        Run the NOT gate simulation for a specific number of steps and return the output.

        Args:
            input_a_present (bool): Input A state.

        Returns:
            input_a_present (bool): Input A state.
        """
        GOL = self.setup_not_gate(40, input_a_present)
        for _ in range(60):
            GOL.evolve()

        output_row, output_col = 20, 20
        window = 6
 
        r_start = max(0, output_row - window)
        r_end   = min(GOL.grid.shape[0], output_row + window + 1)
        c_start = max(0, output_col - window)
        c_end   = min(GOL.grid.shape[1], output_col + window + 1)
 
        output_region = GOL.grid[r_start:r_end, c_start:c_end]
        return int(np.sum(output_region)) > 0


if __name__ == "__main__":
    logic = GliderLogicGates()

    # print("AND Gate:")
    # print(logic.run_and_gate(False, False))
    # print(logic.run_and_gate(False, True))
    # print(logic.run_and_gate(True, False))
    # print(logic.run_and_gate(True, True))
    print("*** AND Gate Truth Table ***")
    for a in [False, True]:
        for b in [False, True]:
            result = logic.run_and_gate(a, b)
            a_str = "1" if a else "0"
            b_str = "1" if b else "0"
            r_str = "1" if result else "0"
            print(f"  A={a_str}, B={b_str} → {r_str}")

    # print("NOT Gate:")
    # print(logic.run_not_gate(False))
    # print(logic.run_not_gate(True))

    print("\n*** NOT Gate Truth Table ***")
    for a in [False, True]:
        result = logic.run_not_gate(a)
        a_str = "1" if a else "0"
        r_str = "1" if result else "0"
        print(f"  A={a_str} → NOT(A)={r_str}")