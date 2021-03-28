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

A RegistrationBank class object bundles together a set of Registration objects. Depending on the model of keyboard, there are either 4 or 8 Registrations in each RegistrationBank.

A RegistrationBank should always be created by reading in a file with the `readFile()` function. There's no way to create one from scratch.

Member functions of this class:

#### readFile

Creates a new object with data from a .RBK file

Usage:  @classmember
        readFile(cls, fileHandle)
Parameters:  fileHandle     handle to a file that has been opened with binary read ("rb") or binary read/write ("r+b") mode
Returns:     a RegistrationBank object


Example:
```python
from casio_rbk import RegistrationBank
# Read from a file
with open("BANK01.RBK", "rb") as f1:
    MyRegBank = RegistrationBank.readFile(f1)
...
```

#### writeFile

Writes the data to a .RBK file

Usage:  writeFile(self, fileHandle)
Parameters:  fileHandle     handle to a file that has been opened with binary write ("wb") or binary read/write ("r+b") mode

Example:
```python
from casio_rbk import RegistrationBank
...
# Write to a file
with open("BANK02.RBK", "wb" as f2:
    MyRegBank.writeFile(f2)
```

### Registration

A Registration class object defines a collection of settings for a Casio keyboard. Member functions of this class:

#### setVolumes

Set volumes of the first three keyboard parts (U1, U2 and L):

Usage:  setVolumes(self, u1_vol, u2_vol, l_vol)
Parameters:  u1_vol    Volume to set on U1 part. Integer 0 -- 127
             u2_vol    Volume to set on U2 part. Integer 0 -- 127
             l_vol     Volume to set on L part (called "L1" on some keyboards). Integer 0 -- 127

Example:
```python
MyReg.setVolumes(127, 0, 127)    # Turn off U2 while leaving U1 & L at full volume
```

#### setPans

Set stereo pan of the first three keyboard parts (U1, U2 and L):

Usage:  setPans(self, u1_pan, u2_pan, l_pan)
Parameters:  u1_pan    Pan to set on U1 part. Integer 0 -- 127; centre pan is 64
             u2_pan    Pan to set on U2 part. Integer 0 -- 127; centre pan is 64
             l_pan     Pan to set on L part (called "L1" on some keyboards). Integer 0 -- 127; centre pan is 64

Example:
```python
MyReg.setPans(0, 127, 64)    # Pan U1 hard left and U2 hard right
```

#### getPatchBank

Gets the patch and bank settings on one of the first five parts.

Usage:   getPatchBank(self, part)
Parameters:   part   Part number to get the patch and bank for. Integer 0 -- 4.
Returns:      tuple (patch number, bank MSB number)

Example:
```python
from casio_rbk import Registration, Part
...
(patch, bankmsb) = MyReg.getPatchBank(Part.U2)
print(f"Patch number of U2 part = {patch}")
print(f"Bank MSB number of U2 part = {bankmsb}")
```

#### Iterating and subscripting

The Registration object looks like a Python dictionary which can be iterated or subscripted. Keys are integers in range 1 - 255 and values are bytestrings containing some data.

This is an advanced use-case for the class. In most cases the three functions above will do everything that's needed.

Example:
```python
from casio_rbk import Registration
...
# Change the Chorus type value to 6
# Atom 0x5E has a two-byte data value specifying Reverb type and Chous type
# Write the second byte, which is Chorus type:
MyReg[0x5E][1] = 6
```

### Atom

Defines possible values for subscripting a Registration object. Only 3 values are defined so far:

```python
Atom.Patch = 0x10
Atom.Volume = 0x11
Atom.Pan = 0x12
```

### Part

Defines possible `part` parameter values as input to the getPatchBank() function:

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
