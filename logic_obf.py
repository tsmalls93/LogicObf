class Node:

    def __init__(self, node_id, sa0, sa1):
        self.node_id = node_id
        self.sa0 = sa0
        self.sa1 = sa1
        self.testability = self.sa0 + self.sa1


class LogicObf:

    def __init__(self, netlist_filename, output_filename):
        self.netlist_filename = netlist_filename
        self.output_filename = output_filename
        self.file = self.open_file()
        self.nodes = list()

    def run(self):
        self.create_nodes()
        self.sort_nodes()

    def open_file(self):
        return open(self.output_filename, "r")

    def create_nodes(self):
        for line in self.file:
            if line == '\n':
                break
            node_id = line.rstrip()
            next(self.file)
            next(self.file)
            sa0 = int(next(self.file).split("T(sa0): ")[1].rstrip())
            sa1 = int(next(self.file).split("T(sa1): ")[1].rstrip())
            self.nodes.append(Node(node_id, sa0, sa1))

    def sort_nodes(self):
        nodes = self.nodes
        nodes.sort(key=lambda node: node.testability, reverse=True)
        self.nodes = nodes

    def get_nodes(self):
        return self.nodes


def main():
    logic_obf = LogicObf("c432.bench", "c432_SCOAP_Output.txt")
    logic_obf.run()
    nodes = logic_obf.get_nodes()


if __name__ == "__main__":
    main()
