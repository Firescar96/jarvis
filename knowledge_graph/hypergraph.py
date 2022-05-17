import os
from graphbrain.memory.sqlite import SQLite
from graphbrain.hyperedge import Hyperedge

class Hypergraph(SQLite):
  def __init__(self, filename):
    super().__init__(filename)
    self.log_filename = os.path.splitext(filename)[0] + '.log'


  def add(self, edge, *args, **kwargs):
    super().add(edge, *args, **kwargs)
    with open(self.log_filename, 'a') as f:
        f.write(str(edge))
        f.write('\n')