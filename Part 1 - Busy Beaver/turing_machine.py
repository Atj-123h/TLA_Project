# -*- coding: utf-8 -*-
"""A Turing machine simulator skeleton.

    Accepting '#'
    =============

    >>> from turing_machine import TuringMachine

    Instantiate the machine with particular transitions.

    >>> one_hash = TuringMachine(
    ...     {
    ...         ('q0', '#'): ('saw_#', '#', 'R'),
    ...         ('saw_#', ''): ('qa', '', 'R'),
    ...     }
    ... )

    Check whether it accepts a string:

    >>> one_hash.accepts('#')
    True

    >>> one_hash.accepts('##')
    False

    Check whether it rejects a string:

    >>> one_hash.rejects('#')
    False

    >>> one_hash.rejects('##')
    True

"""

import logging
from itertools import islice


class TuringMachine:
    """Turing machine simulator class.

    A machine is instantiated with transitions, start, accept and reject states
    and a blank symbol. We assume that the input and the tape alphabet can be
    deducted from the transitions.

    :param dict transitions: a mapping from (state, symbol) tuples to (state,
    symbol, direction) tuple. Directions are either 'L' (for left) or 'R' (for right).

    :param start_state: the initial state of the machine.

    :param accept_state: the accept state.

    :param reject_state: the reject state.

    :blank_symbol: the special symbol that marks the tape cell to be empty.

    """

    def __init__(self, transitions, start_state='q0', accept_state='qa', reject_state='qr', blank_symbol=''):
        # TODO: Implement the constructor. Initialize transitions, start_state, accept_state,
        # reject_state, blank_symbol, and any other helpful structures.
        self.transitions = transitions
        self.start_state = start_state
        self.accept_state = accept_state
        self.reject_state = reject_state
        self.blank_symbol = blank_symbol

    def run(self, input_):
        """Execute the Turing machine for a particular input.

        :param input_: the input that is written on the tape. It can be a list
        of strings, or just a string, in which case each letter is treated as a symbol.

        This method MUST be a Python generator. It should yield a (action, configuration) tuple
        at each step of the computation.
        
        The action is either 'Accept', 'Reject' or None. 
        
        Configuration is a dictionary with the following keys:
        - 'state': the current state,
        - 'left_hand_side': list of symbols on the left hand side of the current position (closest first),
        - 'symbol': the current symbol under the head,
        - 'right_hand_side': list of symbols on the right hand side of the current position.

        """
        # TODO: Implement the simulator loop as a Python generator.
        # 1. Initialize the tape using two lists (left_hand_side and right_hand_side) and the current symbol.
        # 2. Yield the current step (action, configuration).
        # 3. Read transitions and update state, write symbols, and move the head ('L' or 'R').
        # 4. Handle tape expansion dynamically for both left and right directions (double-sided infinite tape).
        # 5. Log a warning using logging.warning() if the singly-infinite tape boundary is crossed before Part III.
        if isinstance(input_, str):
            input_ = list(input_)

        left = []
        if input_:
            symbol = input_[0]
            right = input_[1:]
        else:
            symbol = self.blank_symbol
            right = []
        
        state = self.start_state

        while True:
            configuration = {
                'state': state,
                'left_hand_side': left.copy(),
                'symbol': symbol,
                'right_hand_side': right.copy()
            }

            if state == self.accept_state:
                yield 'Accept', configuration
                return
            
            if state == self.reject_state:
                yield 'Reject', configuration
                return
            
            key = (state, symbol)
            if key not in self.transitions:
                yield 'Reject', configuration
                return
            
            new_state, written_symbol, direction = self.transitions[key]
            symbol = written_symbol
            if direction == 'R':
                left.insert(0, symbol)

                if right:
                    symbol = right.pop(0)
                else:
                    symbol = self.blank_symbol
            elif direction == 'L':
                if not left:
                    logging.warning("Crossing left boundary of singly-infinite tape.")

                right.insert(0, symbol)

                if left:
                    symbol = left.pop(0)
                else:
                    symbol = self.blank_symbol
            
            state = new_state
            yield None, configuration

    def accepts(self, input_, step_limit=100):
        """Check whether the Turing machine accepts a string.

        :param input_: the input string or list.
        :param step_limit: the maximum number of steps to simulate before stopping.
        :return: True if the machine halts in accept_state, False if it rejects,
                 or None if the step limit is reached without halting.
        """
        # TODO: Run the generator up to step_limit and check the action of the final yielded state.
        # Remember to log a warning if the step_limit is reached without halting.
        for action, i in islice(self.run(input_), step_limit):
            if action == 'Accept':
                return True
            if action == 'Reject':
                return False
            
        logging.warning('Step limit reached without halting.')
        return None


    def rejects(self, input_, **kwargs):
        """Check whether the Turing machine rejects a string.

        :param input_: the input string or list.
        :return: True if the machine rejects the string, False if it accepts.
        """
        # TODO: Determine rejection by checking if accepts() returns False.
        rej_determination = self.accepts(input_, **kwargs)
        if rej_determination is None:
            return None
        
        return not rej_determination


    def debug(self, input_, step_limit=100, colored=False):
        """Print the execution configuration of the machine per transition for debugging.

        :param input_: the input string or list.
        :param step_limit: the maximum number of steps to output.
        :param colored: True to output colored boundaries in terminal.
        """
        # TODO: Loop over the steps yielded by run() up to step_limit and print the tape configuration.
        # E.g., print the state and the tape with the head highlighted in brackets like: left[symbol]right
        for i, (action, configuration) in enumerate(islice(self.run(input_), step_limit)):
            left = ''.join(reversed(configuration['left_hand_side']))
            symbol = configuration['symbol'] or '$'
            right = ''.join(configuration['right_hand_side'])

            print(f'{i:03d}: {left}["{symbol}"]{right} | ({configuration["state"]})')
            if action:
                print('Result:', action)
                break

