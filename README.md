# casio-registrations
Python library for handling Casio registration bank (.RBK) files

## Quick start

An example of how to use the library:

```python
from casio_rbk.casio_rbk import RegistrationBank, Part
from casio_rbk.patch_name import patch_name
import warnings

with open("BANK01.RBK", "r+b") as f:
    # Read from file
    rb = RegistrationBank.readFile(f)
    
    # For the first three registrations in the bank (out of either 4 or 8)
    for r in rb[0:3]:
    
        # Part L off, U1 full volume, U2 unchanged
        vols = r.getVolumes()
        r.setVolumes(127, vols[1], 0)
    
        if not r.isMonoCompatible():
          # If any patches are not mono compatible, may wish to raise a warning
          # message here. Not required.
          raise Warning("Not mono compatible, panning will not give fully mono channel separation")
    
        # Part U1 panned hard left, U2 hard right, L unchanged
        pans = r.getPans()
        r.setPans(0, 127, pans[2])
    
    # Write the bank back to file
    rb.writeFile(f)
    
    # Print the instrument patch name of the U1 part
    print("Patch in U1 of first Reg is: " + patch_name(*rb[0].getPatchBank(Part.U1)))
```

## Documentation

### RegistrationBank

A RegistrationBank class object bundles together a set of Registration objects. Depending on the model of keyboard, there are either 4 or 8 Registrations in each RegistrationBank.

A RegistrationBank should always be created by reading in a file with the `readFile()` function. There's no way to create one from scratch.

Member functions of this class:

#### readFile()

Creates a new object with data from a .RBK file

:blue_square: Usage:
* @classmember readFile(cls, fileHandle)

:blue_square: Parameters:
* fileHandle &emsp; handle to a file that has been opened with binary read ("rb") or binary read/write ("r+b") mode

:blue_square: Returns:
* a RegistrationBank object


Example:
```python
from casio_rbk import RegistrationBank
# Read from a file
with open("BANK01.RBK", "rb") as f1:
    MyRegBank = RegistrationBank.readFile(f1)
...
```

#### writeFile()

Writes the data to a .RBK file

:blue_square: Usage:
* writeFile(self, fileHandle)

:blue_square: Parameters:
* fileHandle  &emsp; handle to a file that has been opened with binary write ("wb") or binary read/write ("r+b") mode

Example:
```python
from casio_rbk import RegistrationBank
...
# Write to a file
with open("BANK02.RBK", "wb") as f2:
    MyRegBank.writeFile(f2)
```

#### Iterating and subscripting

The RegistrationBank contains 4 or 8 Registration objects, which can be accessed by iteration or subscripts (like an array).

Example:
```python
for MyReg in MyRegBank1:
    ...  # do something with the Registration
```

### Registration

A Registration class object defines a collection of settings for a Casio keyboard. Settings include volume and pan for each keyboard part and lots of other stuff. Member functions of this class:

#### setVolumes()

Set volumes of the first three keyboard parts (U1, U2 and L):

:blue_square: Usage:
* setVolumes(self, u1_vol, u2_vol, l_vol)

:blue_square: Parameters:
* u1_vol  &emsp; Volume to set on U1 part. Integer 0 -- 127
* u2_vol  &emsp; Volume to set on U2 part. Integer 0 -- 127
* l_vol   &emsp; Volume to set on L part (called "L1" on some keyboards). Integer 0 -- 127

Example:
```python
MyRegBank[0].setVolumes(127, 0, 127)    # Turn off U2 while leaving U1 & L at full volume
```

The setVolumes() function is equivalent to:
```python
from casio_rbk.casio_rbk import Registration, Atom
import struct
...
b = reg[Atom.Volume]
reg[Atom.Volume] = struct.pack('3B', u1_vol, u2_vol, u3_vol) + b[3:]
```


#### setPans()

Set stereo pan of the first three keyboard parts (U1, U2 and L):

:blue_square: Usage:
* setPans(self, u1_pan, u2_pan, l_pan)

:blue_square: Parameters:
* u1_pan  &emsp; Pan to set on U1 part. Integer 0 -- 127; centre pan is 64
* u2_pan  &emsp; Pan to set on U2 part. Integer 0 -- 127; centre pan is 64
* l_pan   &emsp; Pan to set on L part (called "L1" on some keyboards). Integer 0 -- 127; centre pan is 64

Example:
```python
MyRegBank[1].setPans(0, 127, 64)    # Pan U1 hard left and U2 hard right
```

The setPans() function is equivalent to:
```python
from casio_rbk.casio_rbk import Registration, Atom
import struct
...
b = reg[Atom.Pan]
reg[Atom.Pan] = struct.pack('3B', u1_pan, u2_pan, u3_pan) + b[3:]
```

#### isMonoCompatible()

Checks the stereo pan compatibility of the first three keyboard parts (U1, U2, L). If any
is not compatible it returns False, otherwise True. Panning can still be used, but
will not result in fully mono-left or mono-right channel separation.

:blue_square: Usage:
* isMonoCompatible(self)

:blue_square: Parameters:
None

Example:
```python
import warnings
if not MyRegBank[1].isMonoCompatible():
  raise Warning("Panning will not give fully mono channel separation")
```

#### getVolumes()

Get volume settings of the first three keyboard parts (U1, U2 and L):

:blue_square: Usage:
* getVolumes(self)

:blue_square: Returns:
* 3-tuple of integers 0 -- 127

Example:
```python
vols = MyRegBank[1].getVolumes()
print(f"U1 volume is {vols[0]}")
print(f"U2 volume is {vols[1]}")
```


#### getPans()

Get stereo pan settings of the first three keyboard parts (U1, U2 and L):

:blue_square: Usage:
* getPans(self)

:blue_square: Returns:
* 3-tuple of integers 0 -- 127; centre pan is 64

Example:
```python
pans = MyRegBank[1].getPans()
print(f"U1 pan is {pans[0]}")
print(f"L  pan is {pans[2]}")
```


#### getPatchBank()

Gets the patch and bank settings on one of the first five parts.

:blue_square: Usage:
* getPatchBank(self, part)

:blue_square: Parameters:
* part  &emsp; Part number to get the patch and bank for. Integer 0 - 4.

:blue_square: Returns:
* tuple (patch number, bank MSB number)

Example:
```python
from casio_rbk import RegistrationBank, Part
...
(patch, bankmsb) = MyRegBank[2].getPatchBank(Part.U2)
print(f"Patch number of U2 part = {patch}")
print(f"Bank MSB number of U2 part = {bankmsb}")
```

The getPatchBank() function is equivalent to:
```python
from casio_rbk.casio_rbk import Registration, Atom
import struct
...
(patch, bankmsb) = struct.unpack_from('2B', reg[Atom.Patch], 2*part)
```

#### Iterating and subscripting

The Registration object looks like a Python dictionary which can be iterated or subscripted. Keys are integers in range 1 - 255 and values are bytestrings containing some data.

This is an advanced use-case for the class. In most cases the three functions above will do everything that's needed.

Example:
```python
from casio_rbk import Registration, Atom, Part
...
# Change the Volume of U2 part to 115. ADVANCED - SHOULD NORMALLY USE setVolumes() INSTEAD!!
vols = bytearray(MyReg[Atom.Volume])
vols[Part.U2] = 115
MyReg[Atom.Volume] = bytes(vols)
```

### Atom

Defines possible values for subscripting a Registration object. Only 3 values are defined so far:

```python
Atom.Patch = 0x10
Atom.Volume = 0x11
Atom.Pan = 0x12
```

### Part

Defines possible `part` parameter values for input to the getPatchBank() function:

```python
Part.U1 = 0
Part.U2 = 1
Part.L = 2
Part.Auto_Harmony = 4
```

### patch_name

The `patch_name` module translates Patch and Bank MSB values into instrument names specific to the CT-X keyboards. It has only one function defined:

#### patch_name()

:blue_square: Usage:
* patch_name(patch, bank_msb)

:blue_square: Parameters:
* patch   &emsp; Patch number. Integer 0 - 127
* bank_msb  &emsp;  Bank MSB number. Integer 0 - 120
              
:blue_square: Returns:
* String giving the patch name

The tuples returned from function `getPatchBank` can be used as input provided they are preceded by an asterisk "*".

Example:

```python
from casio_rbk.casio_rbk import RegistrationBank, Part
from casio_rbk.patch_name import patch_name
...
print("Patch in U1 is: " + patch_name(*MyRegBank[0].getPatchBank(Part.U1)))
```

## Unit Tests

Run unit tests by calling

```bash
python -m unittest casio_rbk/tests/tests.py
```
