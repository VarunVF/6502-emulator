#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include "cpu.h"
#include "instructions.h"


void init_cpu(CPU* cpu)
{
    memset(cpu, 0, sizeof(CPU));

    cpu->PC = 0x8000;   // Start execution at $8000
    cpu->SP = 0xFF;     // Stack starts at $01FF
    cpu->SR = FLAG_INTERRUPT | FLAG_UNUSED;  // Default flags
}

void print_state(CPU* cpu)
{
    printf( "A:\t0x%02x\t(%i)\n", cpu->A,  cpu->A);
    printf( "X:\t0x%02x\t(%i)\n", cpu->X,  cpu->X);
    printf( "Y:\t0x%02x\t(%i)\n", cpu->Y,  cpu->Y);
    printf("PC:\t0x%04x\t(%i)\n", cpu->PC, cpu->PC);
    printf("SP:\t0x%02x\t(%i)\n", cpu->SP, cpu->SP);
    printf("SR:\t0x%02x\t(%i)\n", cpu->SR, cpu->SR);
}

uint8_t read_memory(CPU* cpu, uint16_t address)
{
    return cpu->memory[address];
}

void write_memory(CPU* cpu, uint16_t address, uint8_t value)
{
    cpu->memory[address] = value;
}

void load_program(CPU* cpu, uint8_t* program, uint16_t size, uint16_t start_address)
{
    // Ensure the program can fit in memory
    uint16_t max_program_size = (1 << 16) - start_address;
    if (size > max_program_size)
    {
        fprintf(stderr, "Error: Program is too large to fit in memory.\n");
        return;
    }
    
    memcpy(cpu->memory + start_address, program, size);
    cpu->PC = start_address;  // Set PC to start of program
}

void execute_instruction(CPU* cpu)
{
    // Fetch
    uint8_t opcode = read_memory(cpu, cpu->PC++);

    // Decode and execute
    switch (opcode)
    {
        case 0xA9:
            LDA_imm(cpu);
            break;
        case 0x8D:
            STA_abs(cpu);
            break;
        case 0x00:
            BRK(cpu);
            break;
        default:
            fprintf(stderr, "Unknown opcode: 0x%02x\n", opcode);
            print_state(cpu);
            exit(1);
    }
}

void run_cpu(CPU* cpu)
{
    while (!cpu->should_halt)
        execute_instruction(cpu);
    
    printf("Encountered BRK instruction, halting execution.\n");
}
