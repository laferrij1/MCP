#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  mcp23008.py
#  
#  Copyright 2020  <pi@raspberrypi>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

MCP23008_REG_IODIR						  = 0x00 # I/O DIRECTION-A Register
MCP23008_REG_IPOL						  = 0x01 # INPUT POLARITY PORT-A Register
MCP23008_REG_GPINTEN                      = 0x02 # INTERRUPT-ON-CHANGE-A PINS
MCP23008_REG_DEFVAL                       = 0x03 # DEFAULT VALUE-A Register
MCP23008_REG_INTCON                       = 0x04 # INTERRUPT-ON-CHANGE CONTROL-A Register
MCP23008_REG_IOCON                        = 0x05 # I/O EXPANDER CONFIGURATION-A Register
MCP23008_REG_GPPU                         = 0x06 # GPIO PULL-UP RESISTOR-A Register
MCP23008_REG_INTF                         = 0x07 # INTERRUPT FLAG-A Register
MCP23008_REG_INTCAP                       = 0x8  # INTERRUPT CAPTURED VALUE FOR PORT-A Register
MCP23008_REG_GPIO                         = 0x09 # GENERAL PURPOSE I/O PORT-A Register
MCP23008_REG_OLAT                         = 0x0A # OUTPUT LATCH-A Register 0

# MCP23008 I/O Direction Register Configuration
MCP23008_IODIR_PIN_7_INPUT                = 0x80 # Pin-7 is configured as an input
MCP23008_IODIR_PIN_6_INPUT                = 0x40 # Pin-6 is configured as an input
MCP23008_IODIR_PIN_5_INPUT                = 0x20 # Pin-5 is configured as an input
MCP23008_IODIR_PIN_4_INPUT                = 0x10 # Pin-4 is configured as an input
MCP23008_IODIR_PIN_3_INPUT                = 0x08 # Pin-3 is configured as an input
MCP23008_IODIR_PIN_2_INPUT                = 0x04 # Pin-2 is configured as an input
MCP23008_IODIR_PIN_1_INPUT                = 0x02 # Pin-1 is configured as an input
MCP23008_IODIR_PIN_0_INPUT                = 0x01 # Pin-0 is configured as an input
MCP23008_IODIR_PIN_INPUT                  = 0xFF # All Pins are configured as an input
MCP23008_IODIR_PIN_OUTPUT                 = 0x00 # All Pins are configured as an output


# MCP23008 Pull-Up Resistor Register Configuration
MCP23008_GPPU_PIN_7_EN                    = 0x80 # Pull-up enabled on Pin-7
MCP23008_GPPU_PIN_6_EN                    = 0x40 # Pull-up enabled on Pin-6
MCP23008_GPPU_PIN_5_EN                    = 0x20 # Pull-up enabled on Pin-5
MCP23008_GPPU_PIN_4_EN                    = 0x10 # Pull-up enabled on Pin-4
MCP23008_GPPU_PIN_3_EN                    = 0x08 # Pull-up enabled on Pin-3
MCP23008_GPPU_PIN_2_EN                    = 0x04 # Pull-up enabled on Pin-2
MCP23008_GPPU_PIN_1_EN                    = 0x02 # Pull-up enabled on Pin-1
MCP23008_GPPU_PIN_0_EN                    = 0x01 # Pull-up enabled on Pin-0
MCP23008_GPPU_PIN_EN                      = 0xFF # Pull-up enabled on All Pins
MCP23008_GPPU_PIN_DS                      = 0x00 # Pull-up disabled on All Pins

# MCP23008 General Purpose I/O Port Register
MCP23008_GPIO_PIN_7_HIGH                  = 0x80 # Logic-high on Pin-7
MCP23008_GPIO_PIN_6_HIGH                  = 0x40 # Logic-high on Pin-6
MCP23008_GPIO_PIN_5_HIGH                  = 0x20 # Logic-high on Pin-5
MCP23008_GPIO_PIN_4_HIGH                  = 0x10 # Logic-high on Pin-4
MCP23008_GPIO_PIN_3_HIGH                  = 0x08 # Logic-high on Pin-3
MCP23008_GPIO_PIN_2_HIGH                  = 0x04 # Logic-high on Pin-2
MCP23008_GPIO_PIN_1_HIGH                  = 0x02 # Logic-high on Pin-1
MCP23008_GPIO_PIN_0_HIGH                  = 0x01 # Logic-high on Pin-0
MCP23008_GPIO_PIN_HIGH					  = 0xFF # Logic-high on All Pins
MCP23008_GPIO_PIN_LOW 					  = 0x00 # Logic-low on All Pins


class mcp23008():
	def __init__(self, smbus, kwargs = {}):
		self.__dict__.update(kwargs)
		if not hasattr(self, 'address'):
			self.address = MCP23008_DEFAULT_ADDRESS

		self.smbus = smbus
  
		if hasattr(self, 'gpio_output_map'):
			for cmap in self.gpio_output_map:
				register_byte = 255
				for channel in cmap:
					register_byte = register_byte ^ 1 << channel
				if(register_byte != 255):
					self.set_output_register(register_byte)

	def set_output_register(self, register_value):
		self.smbus.write_byte_data(self.address, MCP23008_REG_IODIR, register_value)

	def set_bank_status(self, status_value):
		self.smbus.write_byte_data(self.address, MCP23008_REG_GPIO, status_value)
  
	def set_gpio_high(self, target_gpio, status = None):
		#print ("set_high address = ",self.address," target = ",target_gpio)
		if(status == None):
			status = self.get_gpio_bank_status()
		new_status_byte = status | (1 << target_gpio)
		#print ("new byte = ",new_status_byte)
		self.smbus.write_byte_data(self.address, MCP23008_REG_GPIO, new_status_byte)

	def turn_on_relay(self, target_relay, status = None):
		self.set_gpio_high(target_relay, status)

	def set_gpio_high_by_index(self, target_gpio):
		while target_gpio > 7:
			target_gpio = target_gpio - 8
		self.set_gpio_high(target_gpio)

	def set_gpio_low(self, target_gpio, status = None):
		#print ("set_low address = ",self.address," target = ",target_gpio)
		if(status == None):
			status = self.get_gpio_bank_status()
		new_status_byte = status & (~(1 << target_gpio))
		self.smbus.write_byte_data(self.address, MCP23008_REG_GPIO, new_status_byte)

	def reset_gpio(self):
		for bank in range(1,3):
			self.set_gpio_low(0,0)

	def turn_off_relay(self, target_relay, status = None):
		self.set_gpio_low(target_relay, status)

	def set_gpio_low_by_index(self, target_gpio):
		while target_gpio > 7:
			target_gpio = target_gpio - 8
		self.set_gpio_low(target_gpio)

	def toggle_gpio(self,target_gpio):
		target_byte_value = 1 << target_gpio
		status = self.get_gpio_bank_status()
		if(status & target_byte_value != 0):
			self.set_gpio_low(target_gpio)
		else:
			self.set_gpio_high(target_gpio)

	def toggle_relay(self,target_relay):
		self.toggle_gpio(target_relay)

	def toggle_gpio_by_index(self, target_gpio):
		while target_gpio > 7:
			target_gpio = target_gpio - 8
		self.toggle_gpio(target_gpio)

	def get_single_gpio_status(self,target_gpio):
		status = self.get_gpio_bank_status()
		target_byte_value = 1 << target_gpio
		return (status & target_byte_value) != 0

	def get_single_gpio_status_by_index(self, target_gpio):
		while target_gpio > 7:
			target_gpio = target_gpio - 8
		return self.get_single_gpio_status(target_gpio)

	def get_gpio_bank_status(self):
		return self.smbus.read_byte_data(self.address, MCP23008_REG_GPIO)

	def get_gpio_bank_resistor_settings(self):
		return self.smbus.read_byte_data(self.address, MCP23008_REG_GPPU)

	def pull_up_gpio(self,target_gpio):
		target_byte_value = 1 << target_gpio
		status = self.get_gpio_bank_resistor_settings()
		new_status_byte = status | target_byte_value
		self.smbus.write_byte_data(self.address, MCP23008_REG_GPPU, new_status_byte)
