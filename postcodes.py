"""
Converts a file from one format to another.
This example shows how to write objects to a file.
"""

import osmium as o

import sys

ways = set()
nodes = set()

class Relation(o.SimpleHandler):

    def __init__(self, writer):
        super(Relation, self).__init__()
        self.writer = writer

    def relation(self, r):
        if r.tags.get('type') == 'boundary' and "postal_code" in r.tags and r.tags.get("postal_code_level") == "8":
            for member in r.members:
                if member.ref:
                    ways.update([member.ref])
            self.writer.add_relation(r)

class Way(o.SimpleHandler):

    def __init__(self, writer):
        super(Way, self).__init__()
        self.writer = writer

    def way(self, w):
        if w.id in ways :
            for node in w.nodes:
                if node.ref:
                    nodes.update([node.ref])
            self.writer.add_way(w)

class Node(o.SimpleHandler):

    def __init__(self, writer):
        super(Node, self).__init__()
        self.writer = writer

    def node(self, n):
        if n.id in nodes :
            self.writer.add_node(n.replace(tags={}))


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python convert.py <infile> <outfile>")
        sys.exit(-1)
    
    writer = o.SimpleWriter(sys.argv[2])
    relationHandler = Relation(writer)
    relationHandler.apply_file(sys.argv[1])
    wayHandler = Way(writer)
    wayHandler.apply_file(sys.argv[1])
    nodeHandler = Node(writer)
    nodeHandler.apply_file(sys.argv[1])


    writer.close()

    print("done!")

    #writer.close()
