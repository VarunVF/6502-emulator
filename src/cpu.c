#include <stdio.h>
#include <string.h>

#include "cpu.h"


void init_cpu(CPU *cpu)
{
    memset(cpu, 0, sizeof(CPU));
}

void print_state(CPU *cpu)
{
    printf( "A:\t0x%02x\t(%i)\n", cpu->A,  cpu->A);
    printf( "X:\t0x%02x\t(%i)\n", cpu->X,  cpu->X);
    printf( "Y:\t0x%02x\t(%i)\n", cpu->Y,  cpu->Y);
    printf("PC:\t0x%04x\t(%i)\n", cpu->PC, cpu->PC);
    printf("SP:\t0x%02x\t(%i)\n", cpu->SP, cpu->SP);
    printf("SR:\t0x%02x\t(%i)\n", cpu->SR, cpu->SR);
}

uint8_t read_memory(CPU *cpu, uint16_t address)
{
    // TODO: bounds check
    return cpu->memory[address];
}

void write_memory(CPU *cpu, uint16_t address, uint8_t value)
{
    // TODO: bounds check
    cpu->memory[address] = value;
}
