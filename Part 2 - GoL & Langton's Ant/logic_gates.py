# -*- coding: utf-8 -*-
"""
Glider-based Logic Gates Student Template Module.

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

    def setup_and_gate(self, grid_size=35, input_a_present=False, input_b_present=False):
        """
        Set up the Game of Life grid for an AND gate.
        
        Args:
            grid_size (int): Size of the simulation grid.
            input_a_present (bool): If True, place glider for Input A.
            input_b_present (bool): If True, place glider for Input B.
            
        Returns:
            GameOfLife: Initialized GameOfLife object.
        """
        # Student TODO: Setup glider(s) on the grid
        GOL = GameOfLife(grid_size)
        grid = GOL.grid

        # glider = [
        #     (0,1),
        #     (1,2),
        #     (2,0),(2,1),(2,2)
        # ]
        glider_a = [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
        glider_b = [(0, 1), (1, 0), (2, 0), (2, 1), (2, 2)]

        if input_a_present:
            row_a = 2
            col_a = 2
            for i, j in glider_a:
                grid[row_a+i, col_a+j] = 1

        if input_b_present:
            row_b, col_b = 2, 22
            for i, j in glider_b:
                grid[row_b+i, col_b+j] = 1

        return GOL

    def setup_not_gate(self, grid_size=35, input_a_present=False):
        """
        Set up the Game of Life grid for a NOT gate.
        
        Args:
            grid_size (int): Size of the simulation grid.
            input_a_present (bool): If True, place glider for Input A.
            
        Returns:
            GameOfLife: Initialized GameOfLife object.
        """
        # Student TODO: Setup control glider and input glider(s)
        GOL = GameOfLife(grid_size)
        grid = GOL.grid

        glider = [
            (0,1),
            (1,2),
            (2,0),(2,1),(2,2)
        ]

        row, col = 2, 2
        for i, j in glider:
            grid[row+i, col+j] = 1

        if input_a_present:
            input_glider = [(10, 10), (11, 11), (12, 9), (12, 10), (12, 11)]
            for i, j in input_glider:
                grid[i, j] = 1

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
        GOL = self.setup_and_gate(35, input_a_present, input_b_present)

        initial_population = np.sum(GOL.grid)
        
        for i in range(60):
            GOL.evolve()
        
        final_population = np.sum(GOL.grid)

        if input_a_present and input_b_present:
            return final_population < initial_population

        return False
    
    def run_not_gate(self, input_a_present):
        """
        Run the NOT gate simulation for a specific number of steps and return the output.
        
        Args:
            input_a_present (bool): Input A state.
            
        Returns:
            bool: True if output is active, False otherwise.
        """
        # Student TODO: Evolve simulation and evaluate output
        GOL = self.setup_not_gate(35, input_a_present)

        for i in range(50):
            GOL.evolve()

        total_cells = np.sum(GOL.grid)
        if not input_a_present:
            
            return total_cells == 5
        else:
            
            return total_cells < 5

if __name__ == "__main__":
    logic = GliderLogicGates()

    print("AND Gate:")
    print(logic.run_and_gate(False, False))
    print(logic.run_and_gate(False, True))
    print(logic.run_and_gate(True, False))
    print(logic.run_and_gate(True, True))

    print("NOT Gate:")
    print(logic.run_not_gate(False))
    print(logic.run_not_gate(True))