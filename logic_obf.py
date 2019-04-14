import re

import numpy as np


class Node:

    def __init__(self, node_id, sa0, sa1):
        self.node_id = node_id
        self.sa0 = sa0
        self.sa1 = sa1
        self.testability = self.sa0 + self.sa1


class LogicObf:

    def __init__(self, netlist_filename, output_filename, num_keys):
        self.netlist_filename = netlist_filename
        self.output_filename = output_filename
        self.output_file = open(self.output_filename, "r")
        self.netlist_file = open(self.netlist_filename, "r")
        self.nodes = list()
        self.num_keys = num_keys

    def run(self):
        self.create_nodes()
        self.sort_nodes()
        self.add_key_gates()

    def create_nodes(self):
        for line in self.output_file:
            if line == '\n':
                break
            node_id = line.rstrip()
            next(self.output_file)
            next(self.output_file)
            sa0 = int(next(self.output_file).split("T(sa0): ")[1].rstrip())
            sa1 = int(next(self.output_file).split("T(sa1): ")[1].rstrip())
            self.nodes.append(Node(node_id, sa0, sa1))

    def sort_nodes(self):
        nodes = self.nodes
        nodes.sort(key=lambda node: node.testability, reverse=True)
        self.nodes = nodes

    def get_nodes(self):
        return self.nodes

    def add_key_gates(self):
        file = self.netlist_file.readlines()
        for i in range(self.num_keys):
            file.append('INPUT(key' + str(i) + ')')
            node = self.nodes[i]
            if '_' in node.node_id:
                keygate_input = node.node_id.split('_')[0]
                keygate_output = node.node_id.split('_')[1].split('[')[1].split(']')[0]
                keygate_type = np.random.choice(['XOR', 'XNOR'])
                file.append('keygate' + str(i) + ' = ' + keygate_type + '(key' + str(i) + ', ' + keygate_input + ')')
                # modify the line to take keygate as input
                for line in range(len(file)):
                    if file[line].split('=')[0].split(' ')[0] == keygate_output:
                        match = keygate_input + "(?P<character>\,|\))"
                        regex = re.compile(r"" + match)
                        file[line] = regex.sub(r"" + "keygate" + str(i) + "\g<character>", file[line])
            else:
                keygate_type = np.random.choice(['XOR', 'XNOR'])
                keygate_input = node.node_id.split(':')[0]
                for line in range(len(file)):
                    match = keygate_input + "(?P<character>\,|\))"
                    regex = re.compile(r"" + match)
                    file[line] = regex.sub(r"" + "keygate" + str(i) + "\g<character>", file[line])
                file.append('keygate' + str(i) + ' = ' + keygate_type + '(key' + str(i) + ', ' + keygate_input + ')')
        with open(self.netlist_filename.split('.')[0] + "_obf.bench.txt", 'w') as f:
            for line in file:
                f.write("%s\n" % line)


def main():
    logic_obf = LogicObf("c432.bench.txt", "c432_SCOAP_Output.txt", 8)
    logic_obf.run()
    nodes = logic_obf.get_nodes()


if __name__ == "__main__":
    main()
