from lexer import *


def compile(src) -> str:
	toks = tokenise(src)
	#for tok in toks:
	#	print(tok.fmt())
	return compiler(toks)

def compiler(toks: list[Token]) -> str:
	to_ret = """BITS 8\nMINHEAP 0\nMINSTACK 256\nMINREG 10\n"""

	ctr = 0
	is_reg_instruction = False

	i = 0
	register = 1


	loop_stack: list[str] = []

	while i < toks.__len__():
		match toks[i].type:
			case TokenType.ADD:
				is_reg_instruction = True
				ctr += 1
				
			case TokenType.SUB:
				is_reg_instruction = True
				ctr -= 1
				
			case TokenType.PUSH:
				if is_reg_instruction:
					to_ret += "ADD R1 R1 " + ctr.__str__() + '\n'
					is_reg_instruction = False
					ctr = 0
				to_ret += "PSH R1\n"
				
			case TokenType.POP:
				if is_reg_instruction:
					is_reg_instruction = False
					ctr = 0
				to_ret += "POP R1" + '\n'
			
			case TokenType.START_INFINITE_LOOP:
				if is_reg_instruction:
					to_ret += "ADD R1 R1 " + ctr.__str__() + '\n'
					is_reg_instruction = False
					ctr = 0
				loop_stack.append("infinite_loop " + i.__str__())
				to_ret += ".infinite_loop" + i.__str__() + '\n'
			
			case TokenType.HEX_LOOP:
				if is_reg_instruction:
					to_ret += "ADD R1 R1 " + ctr.__str__() + '\n'
					is_reg_instruction = False
					ctr = 0
				
				register += 1

				to_ret += "IMM R" + register.__str__() + ' 0x' + toks[i].content + '\n'
				loop_stack.append("hex_loop 0x" + toks[i].content + ' ' + register.__str__() + ' ' + i.__str__())
				to_ret += "BRZ .hex_end" + i.__str__() + " R1\n"
				to_ret += ".hex_loop" + i.__str__() + '\n'
			
			case TokenType.END_LOOP:
				if is_reg_instruction:
					to_ret += "ADD R1 R1 " + ctr.__str__() + '\n'
					is_reg_instruction = False
					ctr = 0
				loop = loop_stack.pop()
				type_and_val = loop.split()
				match type_and_val[0]:
					case "infinite_loop":
						to_ret += "JMP .infinite_loop" + type_and_val[1] + '\n'
					
					case "hex_loop":
						to_ret += "DEC R" + type_and_val[2] + " R" + register.__str__() + '\n'
						to_ret += "BNE .hex_loop" + type_and_val[3] + " R" + type_and_val[2] + ' 0\n'
						to_ret += ".hex_end" + type_and_val[3] + '\n'
						register -= 1
					
					case "reg_loop":
						to_ret += "DEC R" + type_and_val[2] + " R" + type_and_val[2] + '\n'
						to_ret += "BNZ .reg_loop" + type_and_val[1] + " R" + type_and_val[2] + '\n'
						to_ret += ".reg_end" + type_and_val[1] + '\n'
						register -= 1
			
			case TokenType.LOOP_COUNTER:
				if is_reg_instruction:
					is_reg_instruction = False
					ctr = 0
				to_ret += "MOV R1 R" + register.__str__() + '\n'


			case TokenType.HEX_PORT_OUT:
				if is_reg_instruction:
					to_ret += "ADD R1 R1 " + ctr.__str__() + '\n'
					is_reg_instruction = False
					ctr = 0
				to_ret += "OUT 0x" + toks[i].content + " R1\n"
			
			case TokenType.HEX_PORT_IN:
				if is_reg_instruction:
					is_reg_instruction = False
					ctr = 0
				to_ret += "IN R1 0x" + toks[i].content + '\n'

			case TokenType.PORT_OUT:
				if is_reg_instruction:
					to_ret += "ADD R1 R1 " + ctr.__str__() + '\n'
					is_reg_instruction = False
					ctr = 0
				to_ret += "OUT " + toks[i].content + " R1\n"
			
			case TokenType.PORT_IN:
				if is_reg_instruction:
					is_reg_instruction = False
					ctr = 0
				
				to_ret += "IN R1 " + toks[i].content + '\n'
			
			case TokenType.OUT_REG_ASCII:
				if is_reg_instruction:
					to_ret += "ADD R1 R1 " + ctr.__str__() + '\n'
					is_reg_instruction = False
					ctr = 0
				to_ret += "OUT %TEXT R1\n"
			
			case TokenType.IN_REG_ASCII:
				if is_reg_instruction:
					is_reg_instruction = False
					ctr = 0
				
				to_ret += "IN R1 %TEXT\n"

			case TokenType.REGISTER_LOOP:
				if is_reg_instruction:
					to_ret += "ADD R1 R1 " + ctr.__str__() + '\n'
					is_reg_instruction = False
					ctr = 0
				register += 1
				to_ret += "MOV R" + register.__str__() + " R1\n"
				to_ret += "BRZ .reg_end" + i.__str__() + " R1\n"
				to_ret += ".reg_loop" + i.__str__() + '\n'
				loop_stack.append("reg_loop " + i.__str__() + ' ' + register.__str__())
			
			case _: continue
		i += 1
	return to_ret