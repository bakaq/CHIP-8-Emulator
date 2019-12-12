import sys
from chip8 import Chip8
import pygame
import time
from dc8 import deasm 

		

def main():
	
	def update_debug(cpu, c_addr):
		
		# Flags
		if DEBUG:
			d_flag = font.render("D", True, (0, 255,0),	d_color)
			debug_screen.blit(d_flag, (debug_screen.get_width()-1*scale, 0))
		
		# Disassembled code
		insts = 5
		for i in range(-insts, insts+1):
					
			if i == 0:
				back = (0,0,255)
			else:
				back = d_color
				
			if c_addr+i >= len(d_code) or c_addr+i < 0:
				inst = font.render("*"*19, True, (255, 255, 255), back)
				debug_screen.blit(inst, (2*scale, (i + insts + 2)*scale))
				continue
				
			txt = hex(cpu.pc + 2*i).upper()[2:] + ": " + d_code[c_addr+i]
			inst = font.render(txt, True, (255, 255, 255), back)
			debug_screen.blit(inst, (2*scale, (i + insts + 2)*scale))
		
		inst_height = 2*insts + 1
		
		# Registers
		for i in range(0x10):
			value = hex(cpu.V[i]).upper()[2:]
			value = "0"*(2 - len(value)) + value
			txt = "V"+ hex(i).upper()[2] + ": " + value 
			reg = font.render(txt, True, (255, 255, 255), d_color)
			debug_screen.blit(reg, (2*scale,(inst_height + 1 + i + 2)*scale))
		
		# I
		value = hex(cpu.I).upper()[2:]
		value = "0"*(3 - len(value)) + value
		txt = "I: " + value
		I = font.render(txt, True, (255, 255, 255), d_color)
		debug_screen.blit(I, (2*scale+7*scale,(inst_height + 1 + 2)*scale))
		
		# Memory
		for i in range(-insts, insts+1):
					
			if i == 0:
				back = (255,0,0)
			else:
				back = d_color
			
			if cpu.I+i >= len(cpu.memory) or cpu.I+i < 0:
				inst = font.render("*"*7, True, (255, 255, 255), back)
				debug_screen.blit(inst, (2*scale+7*scale, (inst_height + 3 + insts + i + 2)*scale))
				continue			

			I = hex(cpu.I+i).upper()[2:]
			I = "0"*(3 - len(I)) + I
			value = hex(cpu.memory[cpu.I+i]).upper()[2:]
			value = "0"*(2 - len(value)) + value
			txt = I + ": " + value
			inst = font.render(txt, True, (255, 255, 255), back)
			debug_screen.blit(inst, (2*scale+7*scale, (inst_height + 3 + insts + i + 2)*scale))
		
		# Timers
		value = hex(cpu.delay_timer).upper()[2:]
		value = "0"*(2 - len(value)) + value
		txt = "DT: " + value
		DT = font.render(txt, True, (255, 255, 255), d_color)
		debug_screen.blit(DT, (2*scale+7*scale,(inst_height*2 + 4 + 2)*scale))
		
		value = hex(cpu.sound_timer).upper()[2:]
		value = "0"*(2 - len(value)) + value
		txt = "ST: " + value
		ST = font.render(txt, True, (255, 255, 255), d_color)
		debug_screen.blit(ST, (2*scale+7*scale,(inst_height*2 + 5 + 2)*scale))
		
		
		
	
	DEBUG = True
	d_color = (0x33, 0x33, 0x33)
	
	# Initialize pygame for the graphics
	pygame.init()
	pygame.display.set_caption("CHIP-8")
	# notomono liberationmono
	font = pygame.font.SysFont("liberationmono", 10)
	
	# Create Screen
	scale = 10
	game_screen = pygame.Surface((64*scale,32*scale))
	debug_screen = pygame.Surface((15*scale,game_screen.get_height()))
	screen = pygame.display.set_mode((game_screen.get_width()+debug_screen.get_width(), game_screen.get_height()))
	
	# Initialize CHIP-8 cpu 
	cpu = Chip8()
	code = cpu.load_game(sys.argv[1])
	
	# Disassemble code
	d_code = deasm(code)
	
	# Clocks per timer
	cpt = 20
	
	# Keymap
	key_map = {
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
	
	# Main loop
	running = True
	
	while(running):
		
		for _ in range(cpt):
			
			if not running: break
		
			c_addr = int((cpu.pc-0x200)/2)
			
			# Emulate one cycle
			cpu.cycle()
			
			# If draw flag is set, update the game_screen
			if(cpu.draw_flag):
			
				for i in range(64):
					for j in range(32):
						if cpu.gfx[i][j]:
							pygame.draw.rect(game_screen, (255, 255, 255), (i*scale, j*scale, scale, scale))
						else:
							pygame.draw.rect(game_screen, (0, 0, 0), (i*scale, j*scale, scale, scale))
				screen.blit(game_screen, (0, 0))
				cpu.draw_flag = False
			
			# Check events
			for event in pygame.event.get():
				# Quit the game
				if event.type == pygame.QUIT:
					running = False
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_l:
						DEBUG = True
			
			# Debug screen
			debug_screen.fill(d_color)
			update_debug(cpu, c_addr)
				
			
			
			# Update the screen
			screen.blit(debug_screen, (game_screen.get_width(),0))
			pygame.display.flip()
			
			
			# Store keys
			keys = [0] * 16
			keys_pressed = pygame.key.get_pressed()
			for i in range(len(keys_pressed)):
				if i in key_map and keys_pressed[i] == 1:
					keys[key_map[i]] = 1
			
			cpu.set_keys(keys)
			
			if(DEBUG):
				waiting = True
				while waiting:
					for event in pygame.event.get():
						if event.type == pygame.QUIT:
							running = False
							DEBUG = False
							waiting = False
						if event.type == pygame.KEYDOWN:
							if event.key == pygame.K_l:
								DEBUG = False
							waiting = False
			else:
				time.sleep((1.0/60.0)/cpt)
		
		
		
		cpu.update_timers()
		
		
		

# Only run if this is the main script 
if __name__ == "__main__":
	main()
