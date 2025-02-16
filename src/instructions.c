#include "cpu.h"


void LDA_imm(CPU* cpu)
{
    uint8_t value = read_memory(cpu, cpu->PC++);
    cpu->A = value;

    // Set Zero or Negative Flags
    if (cpu->A == 0)
        cpu->SR |= FLAG_ZERO;
    if (cpu->A & 0x80)
        cpu->SR |= FLAG_NEGATIVE;
}