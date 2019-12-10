import sys
from chip8 import Chip8
import pygame
import time


DEBUG = False



def main():
	
	# Initialize pygame for the graphics
	pygame.init()
	pygame.display.set_caption("CHIP-8")
	
	# Create Screen
	scale = 10
	screen = pygame.display.set_mode((64*scale,32*scale))
	
	# Initialize CHIP-8 cpu 
	cpu = Chip8()
	cpu.load_game(sys.argv[1])

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
			# Emulate one cycle
			cpu.cycle()
			
			# If draw flag is set, update the screen
			if(cpu.draw_flag):
			
				for i in range(64):
					for j in range(32):
						if cpu.gfx[i][j]:
							pygame.draw.rect(screen, (255, 255, 255), (i*scale, j*scale, scale, scale))
						else:
							pygame.draw.rect(screen, (0, 0, 0), (i*scale, j*scale, scale, scale))
				pygame.display.flip()
				cpu.draw_flag = False
			
			# Check quit
			for event in pygame.event.get():
				# Quit the game
				if event.type == pygame.QUIT:
					running = False
			
			
			# Store keys
			keys = [0] * 16
			keys_pressed = pygame.key.get_pressed()
			for i in range(len(keys_pressed)):
				if i in key_map and keys_pressed[i] == 1:
					keys[key_map[i]] = 1
			
			cpu.set_keys(keys)
			
			if(DEBUG):
				input()
			else:
				time.sleep((1.0/60.0)/cpt)
		
		cpu.update_timers()
		
		
		

# Only run if this is the main script 
if __name__ == "__main__":
	main()
