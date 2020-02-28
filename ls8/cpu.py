"""CPU functionality."""

import sys

SP = 7


MUL = 0b10100010
LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
PUSH = 0b01000101
POP = 0b01000110
CMP = 0b10100111
JMP = 0b01010100
JNE = 0b01010110
JEQ = 0b01010101

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.flag = [0] * 8
        self.reg = [0] * 8
        self.ram = [0] * 256   
        self.pc = 0
        self.branch_table = {
            LDI: self.LDI_op,
            PRN: self.PRN_op,
            MUL: self.MUL_op,
            HLT: self.HLT_op,
            PUSH: self.PUSH_op,
            POP: self.POP_op,
            JEQ: self.JEQ_op,
            JNE: self.JNE_op,
            JMP: self.JMP_op,
            CMP: self.CMP_op

        }

    def LDI_op(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b
        self.pc += 3

    def PRN_op(self, operand_a, operand_b):
        print(self.reg[operand_a])
        self.pc += 2

    def MUL_op(self, operand_a, operand_b):
        self.reg[operand_a] = self.reg[operand_a] * self.reg[operand_b]
        self.pc += 3

    def HLT_op(self, operand_a, operand_b):
        sys.exit(0)

    def PUSH_op(self, operand_a, operand_b):
        self.push(self.reg[operand_a])
        self.pc += 2

    def POP_op(self, operand_a, operand_b):
        self.reg[operand_a] = self.pop()
        self.pc += 2

    def push(self, value):
        self.reg[SP] -= 1
        self.ram_write(self.reg[SP], value)
        print(f"PUSH reg[SP]: {self.reg[SP]}")

    def pop(self):
        value = self.ram_read(self.reg[SP])
        self.reg[SP] += 1
        print(f"POP reg[SP]: {self.reg[SP]}")
        return value

    def CMP_op(self, operand_a, operand_b):
        self.alu("CMP", operand_a, operand_b)
        self.pc += 3

    
    def JEQ_op(self, operand_a, operand_b):
        if self.flag[7] == 1:
            jump = self.ram[self.pc + 1]
            self.pc = self.reg[jump]
        else:
            self.pc += 2


    def JNE_op(self, operand_a, operand_b):
        if self.flag[7] == 0:
            jump = self.ram[self.pc + 1]
            self.pc = self.reg[jump]
        else:
            self.pc += 2

    def JMP_op(self, operand_a, operand_b):
        jump = self.ram[self.pc + 1]
        self.pc = self.reg[jump]


    def ram_read(self, mar):
        mdr = self.ram[mar]
        return mdr

    def ram_write(self, mar, value):
        self.ram[mar] = value


    def load(self):
        """Load a program into memory."""

        address = 0

        with open(sys.argv[1]) as f:
            for line in f:
                cSplit = line.split("#")
                num = cSplit[0].strip()

                if num == "":
                    continue

                instruction = int(num, 2)
                self.ram[address] = instruction
                address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.flag[7] = 1
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.flag,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while True:
            op = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if op in self.branch_table:
                self.branch_table[op](operand_a, operand_b)
            else:
                print("Unrecognized operation.")
                sys.exit(1)