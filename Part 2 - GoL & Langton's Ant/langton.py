# -*- coding: utf-8 -*-
"""
Langton's Ant Student Template Module.
"""
import numpy as np


class LangtonsAnt:
    """
    TODO: [Part 2 - Langton's Ant]
    Create the LangtonsAnt class.
    
    Instruct students to:
    1. Implement the core rules:
       - If on a white square, toggle the color of the square and turn 90 degrees clockwise ('R'), then move forward one unit.
       - If on a black square, toggle the color of the square and turn 90 degrees counter-clockwise ('L'), then move forward one unit.
    2. Extend it to handle multi-color states (representing rulesets like RLR, LLRR, LRRRRRLLR, etc.).
       - A ruleset dictionary maps: {current_color: (next_color, turn_direction)}
       - Where turn_direction is 'R' or 'L'.
    3. Ensure wrapping at the boundaries (toroidal grid).
    """

    def __init__(self, N, ant_position, rules, start_dir='U'):
        """
        Initialize the Langton's Ant simulation.
        
        Args:
            N (int): The grid size (NxN).
            ant_position (tuple): Starting coordinate of the ant as (r, c).
            rules (dict): Dictionary defining transition rules.
                          Format: {current_color: (next_color, turn_direction)}
        """
        # Student TODO: Implement initialization
        self.N = N
        self.grid = np.zeros((N, N), dtype=int)
        self.ant_position = ant_position
        self.row, self.col = ant_position
        self.rules = rules
        self.directions = ['U', 'R', 'D', 'L']
        if start_dir in self.directions:
            self.dir_index = self.directions.index(start_dir)
        else:
            self.dir_index = 0

    def get_states(self):
        """
        Returns the current state grid of the cells.
        
        Returns:
            np.ndarray: The NxN cellular grid.
        """
        # Student TODO: Return grid state
        return self.grid

    def get_current_position(self):
        """
        Returns the ant's current position as a tuple (r, c).
        
        Returns:
            tuple: Current coordinates of the ant.
        """
        # Student TODO: Return current position
        return (self.row, self.col)

    def step(self):
        """
        Perform a single simulation step following the ruleset.
        """
        # Student TODO: Implement the ant's movement and cell state updates
        current_color = self.grid[self.row, self.col]
        next_color, turn = self.rules[current_color]
        self.grid[self.row, self.col] = next_color
        
        if turn == 'R':
            self.dir_index = (self.dir_index + 1)%4
        else:
            self.dir_index = (self.dir_index - 1)%4
        
        direction = self.directions[self.dir_index]
        if direction == 'U':
            self.row = (self.row - 1)%self.N
        elif direction == 'D':
            self.row = (self.row + 1) % self.N
        elif direction == 'L':
            self.col = (self.col - 1) % self.N
        elif direction == 'R':
            self.col = (self.col + 1) % self.N    

    def update(self):
        """
        Alias for step() to support standard animation.
        """
        self.step()
