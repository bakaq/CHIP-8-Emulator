import sys
from time import time
import random
import pygame


class Chip8:

	# Setting all the necessary variables

	opcode = 0
	
	# 4K memory
	# 0x000-0x1FF - Chip 8 interpreter (contains font set in emu)
	# 0x050-0x0A0 - Used for the built in 4x5 pixel font set (0-F)
	# 0x200-0xFFF - Program ROM and work RAM
	memory = [0] * 4096
	
	
	# Hex font
	memory[0:(5*16)] = [
		0xF0, 0x90, 0x90, 0x90, 0xF0, # 0
		0x20, 0x60, 0x20, 0x20, 0x70, # 1 
		0xF0, 0x10, 0xF0, 0x80, 0xF0, # 2
		0xF0, 0x10, 0xF0, 0x10, 0xF0, # 3
		0x90, 0x90, 0xF0, 0x10, 0x10, # 4
		0xF0, 0x80, 0xF0, 0x10, 0xF0, # 5
		0xF0, 0x80, 0xF0, 0x90, 0xF0, # 6
		0xF0, 0x10, 0x20, 0x40, 0x40, # 7
		0xF0, 0x90, 0xF0, 0x90, 0xF0, # 8
		0xF0, 0x90, 0xF0, 0x10, 0xF0, # 9
		0xF0, 0x90, 0xF0, 0x90, 0x90, # A
		0xE0, 0x90, 0xE0, 0x90, 0xE0, # B
		0xF0, 0x80, 0x80, 0x80, 0xF0, # C
		0xE0, 0x90, 0x90, 0x90, 0xE0, # D
		0xF0, 0x80, 0xF0, 0x80, 0xF0, # E
		0xF0, 0x80, 0xF0, 0x80, 0x80, # F
	]


	# Registers
	V = [0] * 16

	# Index and program counter
	I = 0
	pc = 0x200

	# 64 x 32 graphics gfx[x][y]
	gfx = [[0]*32 for _ in range(64)]

	# Timers
	delay_timer = 0
	sound_timer = 0

	# Stack
	stack = [0] * 16
	sp = 0 

	# Keys
	key = [0] * 16


	draw_flag = False
	
	
	def load_game(self, game_file_name):
		with open(game_file_name, "rb") as game_file:
			game = game_file.read()
			for i in range(len(game)):
				self.memory[0x200 + i] = game[i]
		return game



	# === Opcodes implementations ===
	
	# Default, do nothing
	def _null(self, dump):
		self.pc += 2
		
	# 0x00E0
	def _cls(self):
		self.gfx = [0] * (64 * 32)
		self.draw_flag = True
		self.pc += 2
	
	# 0x00EE
	def _rts(self):
		self.sp -= 1
		self.pc = self.stack[self.sp] + 2
	
	_opcodes0x0 = {
		0x0E0: _cls,
		0x0EE: _rts,
	}
	
	# 0x0***
	def _op0x0(self):
		return self._opcodes0x0.get(self.opcode & 0x0FFF, self._null)(self)
		
	# 0x1NNN
	def _jmp(self):
		self.pc = self.opcode & 0x0FFF
	
	# 0x2NNN
	def _jsr(self):
		self.stack[self.sp] = self.pc
		self.sp += 1
		self.pc = self.opcode & 0x0FFF
		
	# 0x3XRR
	def _skeq_xr(self):
		if self.V[(self.opcode & 0x0F00) >> 8] == (self.opcode & 0x00FF):
			self.pc += 4
		else:
			self.pc += 2
	
	# 0x4XRR
	def _skne_xr(self):
		if self.V[(self.opcode & 0x0F00) >> 8] != (self.opcode & 0x00FF):
			self.pc += 4
		else:
			self.pc += 2
	
	# 0x5XY0
	def _skeq_xy(self):
		if self.V[(self.opcode & 0x0F00) >> 8] == self.V[(self.opcode & 0x00F0) >> 4]:
			self.pc += 4
		else:
			self.pc += 2
	
	# 0x6XRR
	def _mov_xr(self):
		self.V[(self.opcode & 0x0F00) >> 8] = (self.opcode & 0x00FF)
		self.pc += 2
	
	# 0x7XRR
	def _add_xr(self):
		self.V[(self.opcode & 0x0F00) >> 8] += (self.opcode & 0x00FF)
		self.V[(self.opcode & 0x0F00) >> 8] = self.V[(self.opcode & 0x0F00) >> 8] & 0xFF
		self.pc += 2
		
	# 0x8XY0
	def _mov_xy(self):
		self.V[(self.opcode & 0x0F00) >> 8] = self.V[(self.opcode & 0x00F0) >> 4]
		self.pc += 2
	
	# 0x8XY1
	def _or_xy(self):
		self.V[(self.opcode & 0x0F00) >> 8] |= self.V[(self.opcode & 0x00F0) >> 4]
		self.pc += 2
	
	# 0x8XY2
	def _and_xy(self):
		self.V[(self.opcode & 0x0F00) >> 8] &= self.V[(self.opcode & 0x00F0) >> 4]
		self.pc += 2
	
	# 0x8XY3:
	def _xor_xy(self):
		# Vx = Vx XOR Vy 
		self.V[(self.opcode & 0x0F00) >> 8] ^= self.V[(self.opcode & 0x00F0) >> 4]
		self.pc += 2
		
	# 0x8XY4
	def _add_xy(self):
		s = self.V[(self.opcode & 0x0F00) >> 8] + self.V[(self.opcode & 0x00F0) >> 4]
		if s > 0xFF:
			self.V[0xF] = 1
			s &= 0xFF
		else:
			self.V[0xF] = 0
		self.V[(self.opcode & 0x0F00) >> 8] = s 
		self.pc += 2 
	
	# 0x8XY5
	def _sub_xy(self):
		if self.V[(self.opcode & 0x0F00) >> 8] > self.V[(self.opcode & 0x00F0) >> 4]:
			self.V[0xF] = 1
		else:
			self.V[0xF] = 0
		self.V[(self.opcode & 0x0F00) >> 8] = self.V[(self.opcode & 0x0F00) >> 8] - self.V[(self.opcode & 0x00F0) >> 4]
		self.pc += 2
	
	# 0x8X06
	def _shr_x(self):
		self.V[0xF] = self.V[(self.opcode & 0x0F00) >> 8] & 0x01
		self.V[(self.opcode & 0x0F00) >> 8] = self.V[(self.opcode & 0x0F00) >> 8] >> 1
		self.pc += 2
	
	# 0x8XY7
	def _rsb_xy(self):
		if self.V[(self.opcode & 0x00F0) >> 4] > self.V[(self.opcode & 0x0F00) >> 8]:
			self.V[0xF] = 1
		else:
			self.V[0xF] = 0
		self.V[(self.opcode & 0x0F00) >> 8] = self.V[(self.opcode & 0x00F0) >> 4] - self.V[(self.opcode & 0x0F00) >> 8]
		self.pc += 2
	
	# 0x8X0E
	def _shl_x(self):
		self.V[0xF] = self.V[(self.opcode & 0x0F00) >> 8] & 0x80
		self.V[(self.opcode & 0x0F00) >> 8] = self.V[(self.opcode & 0x0F00) >> 8] << 1
		self.pc += 2
	
	
	_opcodes0x8 = {
		0x0: _mov_xy,
		0x1: _or_xy,
		0x2: _and_xy,
		0x3: _xor_xy,
		0x4: _add_xy,
		0x5: _sub_xy,
		0x6: _shr_x,
		0x7: _rsb_xy,
		0xE: _shl_x,
	}
	
	# 0x8***
	def _op0x8(self):
		return self._opcodes0x8.get(self.opcode & 0x000F, self._null)(self)
	
	
	# 0x9XY0
	def _skne_xy(self):
		if self.V[(self.opcode & 0x0F00) >> 8] != self.V[(self.opcode & 0x00F0) >> 4]:
			self.pc += 4
		else:
			self.pc += 2
	
	# 0xANNN
	def _mvi(self):
		self.I = self.opcode & 0xFFF
		self.pc += 2
	
	# 0xBNNN
	def _jmi(self):
		self.pc = (self.opcode & 0xFFF) + self.V[0x0]
	
	# 0xCXKK
	def _rand_xk(self):
		self.V[(self.opcode & 0x0F00) >> 8] = random.randint(0x00, 0xFF) & (self.opcode & 0x00FF)
		self.pc += 2
	
	# 0xDXYN
	def _sprite_xyn(self):
		
		n = self.opcode & 0x000F
		x = self.V[(self.opcode & 0x0F00) >> 8]
		y = self.V[(self.opcode & 0x00F0) >> 4]
		
		
		self.V[0xF] = 0
		for i in range(n):
			pixel = self.memory[self.I + i]
			for j in range(8):
				if pixel & (0x80 >> j) != 0:
					if self.gfx[(x + j) % 64][(y + i) % 32] == 1:
						self.V[0xF] = 1
					self.gfx[(x + j) % 64][(y + i) % 32] ^= 1
		
		self.draw_flag = True
		self.pc += 2
		
	# 0xEK9E
	def _skpr_k(self):
		if self.key[self.V[(self.opcode & 0x0F00) >> 8]] == 1:
			self.pc += 4
		else:
			self.pc += 2
			
	# 0xEKA1
	def _skup_k(self):
		if self.key[self.V[(self.opcode & 0x0F00) >> 8]] == 0:
			self.pc += 4
		else:
			self.pc += 2
	
	_opcodes0xE = {
		0x9E: _skpr_k,
		0xA1: _skup_k,
	}
	
	# 0xE***
	def _op0xE(self):
		return self._opcodes0xE.get(self.opcode & 0x00FF, self._null)(self)
	
	
	# 0xFR07
	def _gdelay_r(self):
		self.V[(self.opcode & 0x0F00) >> 8] = self.delay_timer
		self.pc += 2
	
	_key_map = {
		pygame.K_1: 0x1,
		pygame.K_2: 0x2,
		pygame.K_3: 0x3,
		pygame.K_4: 0xC,
		pygame.K_q: 0x4,
		pygame.K_w: 0x5,
		pygame.K_e: 0x6,
		pygame.K_r: 0xD,
		pygame.K_a: 0x7,
		pygame.K_s: 0x8,
		pygame.K_d: 0x9,
		pygame.K_f: 0xE,
		pygame.K_z: 0xA,
		pygame.K_x: 0x0,
		pygame.K_c: 0xB,
		pygame.K_v: 0xF,
	}
	
	# 0xFR0A
	def _key_r(self):
		waiting = True
		while(waiting):
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					self.V[(self.opcode & 0x0F00) >> 8] = self._key_map[event.key]
					waiting = False
					
		
	# 0xFR15
	def _sdelay_r(self):
		self.delay_timer = self.V[(self.opcode & 0x0F00) >> 8]
		self.pc += 2
	
	# 0xFR18
	def _ssound_r(self):
		self.sound_timer = self.V[(self.opcode & 0x0F00) >> 8]
		self.pc += 2
		
	# 0xFR1E
	def _adi_r(self):
		self.I += self.V[(self.opcode & 0x0F00) >> 8]
		self.pc += 2
	
	# 0xFR29
	def _font_r(self):
		self.I = self.V[(self.opcode & 0x0F00) >> 8]*5
		self.pc += 2
		
	# 0xFR33
	def _bcd_r(self):
		self.memory[self.I] = self.V[(self.opcode & 0x0F00) >> 8] // 100
		self.memory[self.I + 1] = (self.V[(self.opcode & 0x0F00) >> 8] % 100) // 10
		self.memory[self.I + 2] = (self.V[(self.opcode & 0x0F00) >> 8] % 100) % 10 
		self.pc += 2
	
	# 0xFR55
	def _str_r(self):
		for i in range(((self.opcode & 0x0F00) >> 8) + 1):
			self.memory[self.I + i] = self.V[i]
		self.I += ((self.opcode & 0x0F00) >> 8) + 1
		self.pc += 2
	
	# 0xFR65
	def _ldr_r(self):
		for i in range(((self.opcode & 0x0F00) >> 8) + 1):
			self.V[i] = self.memory[self.I + i]
		self.I += ((self.opcode & 0x0F00) >> 8) + 1
		self.pc += 2
	
	_opcodes0xF = {
		0x07: _gdelay_r,
		0x0A: _key_r,
		0x15: _sdelay_r,
		0x18: _ssound_r,
		0x1E: _adi_r,
		0x29: _font_r,
		0x33: _bcd_r,
		0x55: _str_r,
		0x65: _ldr_r,
	}
	
	# 0xF***
	def _op0xF(self):
		return self._opcodes0xF.get(self.opcode & 0x00FF, self._null)(self)
	
	
	
		
	# Opcode dictionary
	_opcodes = {
		0x0: _op0x0,
		0x1: _jmp,
		0x2: _jsr,
		0x3: _skeq_xr,
		0x4: _skne_xr,
		0x5: _skeq_xy,
		0x6: _mov_xr,
		0x7: _add_xr,
		0x8: _op0x8,
		0x9: _skne_xy,
		0xA: _mvi,
		0xB: _jmi,
		0xC: _rand_xk,
		0xD: _sprite_xyn,
		0xE: _op0xE,
		0xF: _op0xF,
	}

	def cycle(self):
		
		# Fetch opcode
		self.opcode = self.memory[self.pc] << 8 | self.memory[self.pc + 1]
		
		# Debug
		#print(hex(self.pc), hex(self.opcode), hex(self.sp), hex(self.stack[self.sp]), self.draw_flag, hex(self.I), self.key)		
		
		# Run opcode
		self._opcodes.get((self.opcode & 0xF000) >> 12, self._null)(self)
		

		
	def update_timers(self):	
		# Update timers
		if self.delay_timer > 0:
			self.delay_timer -= 1
		
		if self.sound_timer > 0:
			self.sound_timer -= 1
			print("\a")
	

	def set_keys(self, keys):
		self.key = keys 


	
	
