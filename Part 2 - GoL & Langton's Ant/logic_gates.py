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

    
    GLIDER_SE = [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)]

    GLIDER_SW = [(0, 1), (1, 0), (2, 0), (2, 1), (2, 2)]

    GLIDER_NW = [(0, 0), (0, 1), (0, 2), (1, 0), (2, 1)]

    def place_glider(self, grid, shape, anchor_r, anchor_c):
        
        for i, j in shape:
            r, c = anchor_r + i, anchor_c + j
            if 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]:
                grid[r, c] = 1
    
    def cells_in_window(self, grid, row, col, window):
        
        r0 = max(0, row - window)
        r1 = min(grid.shape[0], row + window + 1)
        c0 = max(0, col - window)
        c1 = min(grid.shape[1], col + window + 1)
        return int(np.sum(grid[r0:r1, c0:c1]))

    AND_ANCHOR_A  = (0,  0)   
    AND_ANCHOR_B  = (4, 20)   
    AND_OUTPUT    = (15, 12)  
    AND_STEPS     = 80        
    AND_THRESHOLD = 4 
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
            self.place_glider(GOL.grid, self.GLIDER_SE, *self.AND_ANCHOR_A)
        if input_b_present:
            self.place_glider(GOL.grid, self.GLIDER_SW, *self.AND_ANCHOR_B)
        return GOL


    NOT_CTRL_ANCHOR = (2,  2)   
    NOT_INP_ANCHOR  = (20, 20) 
    NOT_OUTPUT      = (18, 18)  
    NOT_STEPS       = 60  

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

        self.place_glider(GOL.grid, self.GLIDER_SE, *self.NOT_CTRL_ANCHOR)

        
        if input_a_present:
            self.place_glider(GOL.grid, self.GLIDER_NW, *self.NOT_INP_ANCHOR)

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
        
        GOL = self.setup_and_gate(50, input_a_present, input_b_present)
        for _ in range(self.AND_STEPS):
            GOL.evolve()

        live = self.cells_in_window(GOL.grid, *self.AND_OUTPUT, window=4)
        return live >= self.AND_THRESHOLD

    def run_not_gate(self, input_a_present):
        """
        Run the NOT gate simulation for a specific number of steps and return the output.

        Args:
            input_a_present (bool): Input A state.

        Returns:
            input_a_present (bool): Input A state.
        """
        GOL = self.setup_not_gate(40, input_a_present)
        for _ in range(self.NOT_STEPS):
            GOL.evolve()
            
        live = self.cells_in_window(GOL.grid, *self.NOT_OUTPUT, window=5)
        return live > 0


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