# casio-registrations
Python library for handling Casio registration bank (.RBK) files

## Quick start

An example of how to use the library:

```python
from casio_rbk.casio_rbk import Atom, Part, RegistrationBank

with open("BANK01.RBK", "r+b") as f:
    # Read from file
    rb = RegistrationBank.readFile(f)
    
    # For the first three registrations in the bank (out of either 4 or 8)
    for r in rb[0:3]:
    
        # Part L off, U1 & U2 full volume
        r.setVolumes(127, 127, 0)
    
        # Part U1 panned hard left, U2 hard right
        r.setPans(0, 127, 40)
    
    # Write the bank back to file
    rb.writeFile(f)
```

## Documentation

### RegistrationBank

### Registration

### Atom

```python
Atom.Patch = 0x10
Atom.Volume = 0x11
Atom.Pan = 0x12
```

### Part

```python
Part.U1 = 0
Part.U2 = 1
Part.L = 2
Part.Auto_Harmony = 4
```

## Unit Tests

Run unit tests by calling

```bash
python -m unittest casio_rbk/casio_rbk/tests.py
```
