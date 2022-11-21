# pyevilemu

A python library to read and write memory of running emulators. This does not require cooperation from the emulator.

This is called evilemu, because accessing memory of another process is inherently evil, dangerous and very powerful.

Note that this library is currently limited to:
* Windows
* Gameboy (color) emulators

Both could be expanded in the future to include more emulators and operating systems.

## Installation

Install this library with:
```sh
    $ python3 setup.py install
```
## Usage

Using evilemu is not complicated. 

```python
import evilemu

for emulator in evilemu.find_gameboy_emulators():
    print("Found a running emulator:" , emulator)
    print("Title of the ROM:", emulator.read_rom(0x0134, 16))
```

Available functions of the emulator objects can be found at `evilemu/emulator.py`
