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
     
        # ترانزیشن‌های قبلی

        # ('q0', '1') : ('q0', 'X', 'R'),
        # ('q0', '0') : ('q1', '0', 'R'),
        # ('q1', '1') : ('q1', 'Y', 'R'),
        # ('q1', '') : ('q2', '', 'L'),
        # ('q2', 'A') : ('q2', 'Y', 'L'),
        # ('q2', 'Y') : ('q2', 'Y', 'L'),
        # ('q2', 'X'): ('q2', 'X', 'L'),
        # ('q2', '0'): ('q2', '0', 'L'),
        # ('q2', ''): ('q3', '', 'R'),
        # ('q3', 'X'): ('q4', '', 'R'),
        # ('q3', '0'): ('q7', '', 'R'),
        # ('q4', 'X'): ('q4', 'X', 'R'),
        # ('q4', '0'): ('q4', '0', 'R'),
        # ('q4', ''): ('q2', '', 'L'),
        # ('q4', '1'): ('q2', '1', 'L'),
        # ('q4', 'Y'): ('q5', 'A', 'R'),
        # ('q5', 'Y'): ('q5', 'Y', 'R'),
        # ('q5', '1'): ('q5', '1', 'R'),
        # ('q5', ''): ('q6', '1', 'L'),
        # ('q6', 'Y'): ('q6', 'Y', 'L'),
        # ('q6', '1'): ('q6', '1', 'L'),
        # ('q6', 'A'): ('q4', 'A', 'R'),
        # ('q7', 'Y'): ('q7', '', 'R'),
        # ('q7', ''): ('qa', '', 'R'),
        # ('q7', '1'): ('qa', '1', 'L'),

        # ترانزیشن‌های جدید
        
        ('q0', '1'): ('q1', 'X', 'R'),            
        ('q0', '0'): ('q_erase_all', '', 'R'),   

        ('q_erase_all', '1'): ('q_erase_all', '', 'R'),
        ('q_erase_all', ''): ('qa', '', 'R'),

        ('q1', '1'): ('q1', '1', 'R'),
        ('q1', '0'): ('q2', '0', 'R'),

        ('q2', '1'): ('q3', 'Y', 'R'),            
        ('q2', 'Y'): ('q2', 'Y', 'R'),            
        ('q2', 'Z'): ('q4', 'Z', 'L'),            
        ('q2', ''):  ('q4', '', 'L'),            

        ('q3', '1'): ('q3', '1', 'R'),
        ('q3', 'Z'): ('q3', 'Z', 'R'),
        ('q3', ''):  ('q3_back', 'Z', 'L'),       

        ('q3_back', 'Z'): ('q3_back', 'Z', 'L'),
        ('q3_back', '1'): ('q3_back', '1', 'L'),
        ('q3_back', 'Y'): ('q2', 'Y', 'R'),      

        ('q4', 'Y'): ('q4', '1', 'L'),
        ('q4', '0'): ('q4_back', '0', 'L'),      

        ('q4_back', '1'): ('q4_back', '1', 'L'),
        ('q4_back', 'X'): ('q_loop', 'X', 'R'),  
     
        ('q_loop', '1'): ('q1', 'X', 'R'),      
        ('q_loop', '0'): ('q_clean_0', '', 'R'), 

        ('q_clean_0', '1'): ('q_clean_0', '', 'R'),
        ('q_clean_0', 'Z'): ('q_clean_Z', '1', 'R'),
        ('q_clean_0', ''):  ('q_clean_left', '', 'L'), 

        ('q_clean_Z', 'Z'): ('q_clean_Z', '1', 'R'),
        ('q_clean_Z', ''):  ('q_clean_left', '', 'L'),

        ('q_clean_left', '1'): ('q_clean_left', '1', 'L'),
        ('q_clean_left', ''):  ('q_clean_left', '', 'L'),
        ('q_clean_left', 'X'): ('q_clean_X', '', 'L'), 

        ('q_clean_X', 'X'): ('q_clean_X', '', 'L'),
        ('q_clean_X', ''):  ('qa', '', 'R'),     
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

