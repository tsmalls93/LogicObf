# LogicObf

## Using the program

```python
# instantiate the class by passing bench file and output from testability measurement tool
# the bench file is not used yet, but may be in the future
logic_obf = LogicObf("c432.bench", "c432_SCOAP_Output.txt")
# run the algorithm: currently just parses and sorts nodes
logic_obf.run()
# get list of sorted nodes
nodes = logic_obf.get_nodes()
```
