import sys

def nyi(opcode):
	return "Not yet implemented"

# 0x00E0
def cls(opcode):
	return "CLS"

# 0x00EE
def ret(opcode):
	return "RET"


def op0x0(opcode):
	if opcode & 0x0FFF == 0x0E0:
		return cls(opcode)
	elif opcode & 0x0FFF == 0x0EE:
		return ret(opcode)
	else:
		return nyi(opcode)
		
		
# 0x1NNN
def jmp(opcode):
	return "JMP $" + hex(opcode & 0x0FFF).upper()[2:]

# 0x2NNN
def call(opcode):
	return "CALL $" + hex(opcode & 0x0FFF).upper()[2:]

# 0x3XRR
def skeq_xr(opcode):
	RR = hex(opcode & 0x00FF).upper()[2:]
	RR = "0"*(2-len(RR)) + RR
	return "SKEQ V" + hex((opcode & 0x0F00) >> 8).upper()[2] + ", $" + RR

# 0x4XRR
def skne_xr(opcode):
	RR = hex(opcode & 0x00FF).upper()[2:]
	RR = "0"*(2-len(RR)) + RR
	return "SKNE V" + hex((opcode & 0x0F00) >> 8).upper()[2] + ", $" + RR

# 0x5XY0
def skeq_xy(opcode):
	if opcode & 0x000F != 0:
		return nyi(opcode)
		
	return "SKEQ V" + hex((opcode & 0x0F00) >> 8).upper()[2] + ", V" + hex((opcode & 0x00F0) >> 4).upper()[2]
	
# 0x6XRR
def ld_xr(opcode):
	RR = hex(opcode & 0x00FF).upper()[2:]
	RR = "0"*(2-len(RR)) + RR
	return "LD V" + hex((opcode & 0x0F00) >> 8).upper()[2] + ", $" + RR

# 0x7XRR
def add_xr(opcode):
	RR = hex(opcode & 0x00FF).upper()[2:]
	RR = "0"*(2-len(RR)) + RR
	return "ADD V" + hex((opcode & 0x0F00) >> 8).upper()[2] + ", $" + RR

# 0x8XY0
def ld_xy(opcode):
	return "LD V" + hex((opcode & 0x0F00) >> 8).upper()[2] + ", V" + hex((opcode & 0x00F0) >> 4).upper()[2]

# 0x8XY1
def or_xy(opcode):
	return "OR V" + hex((opcode & 0x0F00) >> 8).upper()[2] + ", V" + hex((opcode & 0x00F0) >> 4).upper()[2]

# 0x8XY1
def or_xy(opcode):
	return "OR V" + hex((opcode & 0x0F00) >> 8).upper()[2] + ", V" + hex((opcode & 0x00F0) >> 4).upper()[2]

# 0x8XY2
def and_xy(opcode):
	return "AND V" + hex((opcode & 0x0F00) >> 8).upper()[2] + ", V" + hex((opcode & 0x00F0) >> 4).upper()[2]

# 0x8XY3
def xor_xy(opcode):
	return "XOR V" + hex((opcode & 0x0F00) >> 8).upper()[2] + ", V" + hex((opcode & 0x00F0) >> 4).upper()[2]

# 0x8XY4
def add_xy(opcode):
	return "ADD V" + hex((opcode & 0x0F00) >> 8).upper()[2] + ", V" + hex((opcode & 0x00F0) >> 4).upper()[2]

# 0x8XY5
def sub_xy(opcode):
	return "SUB V" + hex((opcode & 0x0F00) >> 8).upper()[2] + ", V" + hex((opcode & 0x00F0) >> 4).upper()[2]

# 0x8X06
def shr_x(opcode):
	if (opcode & 0x00F0) >> 4 != 0:
		return nyi(opcode)
	else:
		return "SHR V" + hex((opcode & 0x0F00) >> 8).upper()[2]

# 0x8XY7
def subn_xy(opcode):
	return "SUBN V" + hex((opcode & 0x0F00) >> 8).upper()[2] + ", V" + hex((opcode & 0x00F0) >> 4).upper()[2]

# 0x8X0E
def shl_x(opcode):
	if (opcode & 0x00F0) >> 4 != 0:
		return nyi(opcode)
	
	return "SHL V" + hex((opcode & 0x0F00) >> 8).upper()[2]


opcodes0x8 = {
	0x0: ld_xy,
	0x1: or_xy,
	0x2: and_xy,
	0x3: xor_xy,
	0x4: add_xy,
	0x5: sub_xy,
	0x6: shr_x,
	0x7: subn_xy,
	0xE: shl_x,
}

def op0x8(opcode):
	return opcodes0x8.get(opcode & 0x000F, nyi)(opcode)
	

# 0x9XY0
def skne_xy(opcode):
	if opcode & 0x000F != 0:
		return nyi(opcode)
	
	return "SKNE V" + hex((opcode & 0x0F00) >> 8).upper()[2] + ", V" + hex((opcode & 0x00F0) >> 4).upper()[2]

# 0xANNN
def ld_i(opcode):
	return "LD I, $" + hex(opcode & 0x0FFF).upper()[2:]

# 0xBNNN
def jmp_v0(opcode):
	return "JMP V0, $" + hex(opcode & 0x0FFF).upper()[2:]

# 0xCXRR
def rnd_xr(opcode):
	RR = hex(opcode & 0x00FF).upper()[2:]
	RR = "0"*(2-len(RR)) + RR
	return "RND V" + hex((opcode & 0x0F00) >> 8).upper()[2] + ", $" + RR

# 0xDXYN
def drw_xyn(opcode):
	return "DRW V" + hex((opcode & 0x0F00) >> 8).upper()[2] + ", V" + hex((opcode & 0x00F0) >> 4).upper()[2] + ", $" + hex(opcode & 0x000F).upper()[2]

# 0xEX9E
def skpr_x(opcode):
	return "SKPR V" + hex((opcode & 0x0F00) >> 8).upper()[2]

# 0xEXA1
def skup_x(opcode):
	return "SKUP V" + hex((opcode & 0x0F00) >> 8).upper()[2]


def op0xE(opcode):
	if opcode & 0x00FF == 0x9E:
		return skpr_x(opcode)
	elif opcode & 0x00FF == 0xA1:
		return skup_x(opcode)
	else:
		return nyi(opcode)

# 0xFX07
def ld_xd(opcode):
	return "LD V" + hex((opcode & 0x0F00) >> 8).upper()[2] + ", DT"

# 0xFX0A
def ld_xk(opcode):
	return "LD V" + hex((opcode & 0x0F00) >> 8).upper()[2] + ", K"

# 0xFX15
def ld_dx(opcode):
	return "LD DT, V" + hex((opcode & 0x0F00) >> 8).upper()[2]

# 0xFX18
def ld_sx(opcode):
	return "LD ST, V" + hex((opcode & 0x0F00) >> 8).upper()[2]

# 0xFX1E
def add_ix(opcode):
	return "ADD I, V" + hex((opcode & 0x0F00) >> 8).upper()[2]

# 0xFX29
def font_x(opcode):
	return "FONT V" + hex((opcode & 0x0F00) >> 8).upper()[2]

# 0xFX33
def bcd_x(opcode):
	return "BCD V" + hex((opcode & 0x0F00) >> 8).upper()[2]

# 0xFX55
def str_x(opcode):
	return "STR " + hex((opcode & 0x0F00) >> 8).upper()[2]

# 0xFX65
def ldr_x(opcode):
	return "LDR " + hex((opcode & 0x0F00) >> 8).upper()[2]

opcodes0xF = {
	0x07: ld_xd,
	0x0A: ld_xk,
	0x15: ld_dx,
	0x18: ld_sx,
	0x1E: add_ix,
	0x29: font_x,
	0x33: bcd_x,
	0x55: str_x,
	0x65: ldr_x,
}

def op0xF(opcode):
	return opcodes0xF.get(opcode & 0x00FF, nyi)(opcode)
		
		
opcodes = {
	0x0: op0x0,
	0x1: jmp,
	0x2: call,
	0x3: skeq_xr,
	0x4: skne_xr,
	0x5: skeq_xy,
	0x6: ld_xr,
	0x7: add_xr,
	0x8: op0x8,
	0x9: skne_xy,
	0xA: ld_i,
	0xB: jmp_v0,
	0xC: rnd_xr,
	0xD: drw_xyn,
	0xE: op0xE,
	0xF: op0xF,
}

def deasm_line(opcode):
	return opcodes.get((opcode & 0xF000) >> 12, nyi)(opcode)

def deasm(code):
	
	d_code = []	
	
	for addr in range(0, len(code), 2):
		opcode = (code[addr] << 8) + code[addr+1]
		d_code.append(deasm_line(opcode))
	
	return d_code

def main():
	
	with open(sys.argv[1], "rb") as code_file:
		code = code_file.read()

	for addr in range(0, len(code), 2):
		opcode = (code[addr] << 8) + code[addr+1]
		addr_s = hex(addr+0x200).upper()[2:]
		op_s = hex(opcode).upper()[2:]
		op_s = "0"*(4 - len(op_s)) + op_s
		print(addr_s + ": " + op_s + " | " + deasm_line(opcode))

if __name__ == "__main__":
	main()
