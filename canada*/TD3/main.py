from prettytable import PrettyTable


class State:
    def __init__(self, name, index, outgoing, incoming):
        self.index = index  # it's index inside the main class
        self.name = name  # name of the state
        self.outgoing = outgoing  # i.e [(A,2),(C,5)] stores outgoing link and the number of time they've been used
        self.num_outgoing = 0  # total number of time the user used a outgoing link
        self.incoming = incoming  # same but for incoming links
        self.num_incoming = 0  # total number of time used a incoming link (aka passe by this node)

    def add_outgoing(self, name_to):
        self.num_outgoing += 1
        index = -1
        for item in self.outgoing:  # If the outgoing transition exist
            index += 1
            if item[0] == name_to:
                self.outgoing[index] = (item[0], item[1] + 1)  # add one to it's counter
                return  # ones it's done we leave the function
        self.outgoing.append((name_to, 1))  # if we don't find it, we append it to the end of the list

    def add_incoming(self, name_from):
        self.num_incoming += 1
        index = -1
        for item in self.incoming:  # If the incoming transition exist
            index += 1
            if item[0] == name_from:
                self.incoming[index] = (item[0], item[1] + 1)  # add one to it's counter
                return  # ones it's done we leave the function
        self.incoming.append((name_from, 1))  # if we don't find it, we append it to the end of the list


class HiddenMarkovModel:
    def __init__(self, num_state, states):
        self.num_state = num_state  # set size
        self.states = [State(states[i], i, [], []) for i in range(num_state)]  # Generating the different States

    def move(self, index_from, index_to):
        self.states[index_from].add_outgoing(self.states[index_to].name)
        self.states[index_to].add_incoming(self.states[index_from].name)

    def move_x(self, index_from, index_to, x):
        for i in range(0, x):
            self.move(index_from, index_to)  # do it x times

    def compute_outgoing_probs(self):
        for state in self.states:
            new_outgoing = []
            for outgoing in state.outgoing:  # First we count the number of outgoing
                # add the state with it's computed proba
                new_outgoing.append((outgoing[0], outgoing[1], (outgoing[1] / state.num_outgoing * 100)))
            state.outgoing = new_outgoing

    def compute_incoming_probs(self):
        for state in self.states:
            new_incoming = []
            for incoming in state.incoming:  # First we count the number of incoming
                # add the state with it's computed proba
                new_incoming.append((incoming[0], incoming[1], (incoming[1] / state.num_incoming * 100)))
            state.incoming = new_incoming

    def compute_probs(self):
        self.compute_outgoing_probs()
        self.compute_incoming_probs()

    def print_transition_table(self):
        headers = ['From \ To'] + [state.name for state in self.states] + ['Count']
        table = PrettyTable(headers)
        for state in self.states:
            row = [state.name]
            for s in self.states:
                count = 0
                prob = 0.0
                for out in state.outgoing:
                    if out[0] == s.name:
                        count = out[1]
                        prob = out[2]
                        break
                row.append(f'{prob:.2f} % ({count})')
            total_count = sum(out[1] for out in state.outgoing)
            row.append(total_count)
            table.add_row(row)
        print(table)


HMM = HiddenMarkovModel(3, ['A', 'B', 'C'])
HMM.move(0, 2)
HMM.move(2, 2)
HMM.move(2, 1)
HMM.move(1, 0)
HMM.move(0, 1)
HMM.move(1, 1)
HMM.move(1, 2)
HMM.move(2, 1)
HMM.compute_probs()
HMM.print_transition_table()
