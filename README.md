# casio-registrations
Python library for handling Casio registration bank (.RBK) files

## Quick start

An example of how to use the library:

```python
from casio_rbk.casio_rbk import Atom, Part, RegistrationBank

with open("BANK01.RBK", "r+b") as f:
    # Read from file
    r = RegistrationBank.readFile(f)
    
    # Part L off, U1 & U2 full volume
    r.setVolumes(127, 127, 0)
    
    # Part U1 panned hard left, U2 hard right
    r.setPans(0, 127, 40)
    
    # Write back to file
    r.writeFile(f)
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
