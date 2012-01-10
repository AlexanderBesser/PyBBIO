"""
 PyBBIO - bbio.py - rev 0.1
 Created: 12/2011
 Author: Alexander Hiam - ahiam@marlboro.edu - http://www.alexanderhiam.com
 Website: https://github.com/alexanderhiam/PyBBIO

 A Python library for hardware IO support on the TI Beaglebone.
 At the moment it is quite limited, only providing API for simple
 digital IO functionality. I have big plans for this, however, so
 keep checking the github page for updates.  

 Copyright (c) 2012 - Alexander Hiam

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version. 

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>. 
"""

import struct, os, sys
from mmap import mmap

CONFIG_FILE="%s/.pybbio/bbio.cfg" % os.environ['HOME']

config = open(CONFIG_FILE, 'r').read()
assert ('MMAP_OFFSET' in config) and ('MMAP_SIZE' in config),\
      "*Config file '%s' must contain values MMAP_OFFSET and MMAP_SIZE" %\
                                                                config_file
exec(config)


class BeagleBone(object):
  def __init__(self):
    f = open("/dev/mem", "r+b")
    self.mem = mmap(f.fileno(), MMAP_SIZE, offset=MMAP_OFFSET) 
    f.close() # Only needed to make map

  def pinMode(self, gpio_pin, direction):
    """ Sets given digital pin to input if direction=1, output otherwise. """
    if (direction):
      reg = self._getReg(gpio_pin[0]+GPIO_OE)
      self._setReg(gpio_pin[0]+GPIO_OE, reg | gpio_pin[1])
      return
    reg = self._getReg(gpio_pin[0]+GPIO_OE)
    self._setReg(gpio_pin[0]+GPIO_OE, reg & ~gpio_pin[1])

  def digitalWrite(self, gpio_pin, state):
    """ Writes given digital pin low if state=0, high otherwise.  """
    if (state):
      reg = self._getReg(gpio_pin[0]+GPIO_DATAOUT)
      self._setReg(gpio_pin[0]+GPIO_DATAOUT, reg | gpio_pin[1])
      return
    reg = self._getReg(gpio_pin[0]+GPIO_DATAOUT)
    self._setReg(gpio_pin[0]+GPIO_DATAOUT, reg & ~gpio_pin[1])

  def digitalRead(self, gpio_pin):
    """ Returns pin state as 1 or 0. """
    return self._getReg(gpio_pin[0]+GPIO_DATAIN) & gpio_pin[1]

  def toggle(self, gpio_pin):
    """ Toggles the state of the given digital pin. """
    reg = self._getReg(gpio_pin[0]+GPIO_DATAOUT)
    self._setReg(gpio_pin[0]+GPIO_DATAOUT, reg ^ gpio_pin[1])

  def _getReg(self, address):
    """ Returns unpacked 32 bit register value starting from address. """
    return struct.unpack("<L", self.mem[address:address+4])[0]

  def _setReg(self, address, new_value):
    """ Sets 32 bits at given address to given value. """
    self.mem[address:address+4] = struct.pack("<L", new_value)

