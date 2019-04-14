# LogicObf

## Using the program

```python
# instantiate the class by passing bench file and output from testability measurement tool
logic_obf = LogicObf("c432.bench", "c432_SCOAP_Output.txt", 8)
# run the algorithm: sorts nodes and inserts key gates (in this case 8 of them)
logic_obf.run()
# get list of sorted nodes
nodes = logic_obf.get_nodes()
```
