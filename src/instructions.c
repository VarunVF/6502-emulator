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

void STA_abs(CPU* cpu)
{
    uint16_t lo_byte = read_memory(cpu, cpu->PC++);
    uint16_t hi_byte = read_memory(cpu, cpu->PC++);
    uint16_t address = (hi_byte << 8) | lo_byte;
    cpu->memory[address] = cpu->A;
}

void BRK(CPU* cpu)
{
    cpu->should_halt = true;
}
