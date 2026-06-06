# -*- coding: utf-8 -*-
from turing_machine import TuringMachine
from test_turing_machine_example1 import print_states

#create the Turing machine
transitions = {
        # TODO: Part II b) - Write your transition rules here as entries to a Python dictionary
        # For example, the key will be a pair (state, character)
        # The value will be the triple (next state, character to write, move head L or R)
        # such as ('q0', '1'): ('q1', '0', 'R'), which says if current state is q0 and 1 encountered
        # then transition to state q1, write a 0 and move head right.
        ('q0', '1') : ('q0', 'X', 'R'),
        ('q0', '0') : ('q1', '0', 'R'),

        ('q1', '1') : ('q1', 'Y', 'R'),
        ('q1', '') : ('q2', '', 'L'),

        ('q2', 'A') : ('q2', 'Y', 'L'),
        ('q2', 'Y') : ('q2', 'Y', 'L'),
        ('q2', 'X'): ('q2', 'X', 'L'),
        ('q2', '0'): ('q2', '0', 'L'),
        ('q2', ''): ('q3', '', 'R'),

        ('q3', 'X'): ('q4', '', 'R'),
        ('q3', '0'): ('q7', '', 'R'),

        ('q4', 'X'): ('q4', 'X', 'R'),
        ('q4', '0'): ('q4', '0', 'R'),
        ('q4', ''): ('q2', '', 'L'),
        ('q4', '1'): ('q2', '1', 'L'),
        ('q4', 'Y'): ('q5', 'A', 'R'),

        ('q5', 'Y'): ('q5', 'Y', 'R'),
        ('q5', '1'): ('q5', '1', 'R'),
        ('q5', ''): ('q6', '1', 'L'),

        ('q6', 'Y'): ('q6', 'Y', 'L'),
        ('q6', '1'): ('q6', '1', 'L'),
        ('q6', 'A'): ('q4', 'A', 'R'),

        ('q7', 'Y'): ('q7', '', 'R'),
        ('q7', ''): ('qa', '', 'R'),
        ('q7', '1'): ('qa', '1', 'L'),

}

if __name__ == "__main__":
    print_states(transitions)
    machine = TuringMachine(transitions)

    def run(input_):
        w = input_
        print("Input:",w)
        print("Accepted" if machine.accepts(w) else "Rejected")
        machine.debug(w, step_limit=1000)

        print()

    # SHOULD ACCEPT
    run("110111")
    # outputs 111111

    # SHOULD ACCEPT
    run("11101111")
    # outputs 111111111111

    run("01111")
