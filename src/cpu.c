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
    printf("CPU State:\n");
    printf("\t A:\t0x%02x\t(%i)\n", cpu->A,  cpu->A);
    printf("\t X:\t0x%02x\t(%i)\n", cpu->X,  cpu->X);
    printf("\t Y:\t0x%02x\t(%i)\n", cpu->Y,  cpu->Y);
    printf("\tPC:\t0x%04x\t(%i) -> 0x%02x\n", cpu->PC, cpu->PC, cpu->memory[cpu->PC]);
    printf("\tSP:\t0x%02x\t(%i)\n", cpu->SP, cpu->SP);
    
    printf("\tSR:\t0x%02x\t(0b", cpu->SR);
    for (int i = 0; i < 8; i++) {
        if (cpu->SR & (1 << i))
            printf("1");
        else
            printf("0");
    }
    printf(")\n");
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

void load_program_file(CPU* cpu, char* filename, uint16_t start_address)
{
    // Open file for reading, binary mode
    FILE* fd = fopen(filename, "rb");
    if (fd == NULL) {
        fprintf(stderr, "Error loading program file!\n");
        exit(1);
    }

    // Find program size
    fseek(fd, 0, SEEK_END);
    long filesize = ftell(fd);
    rewind(fd);
    
    // Ensure program can fit in memory
    uint8_t* dstbuf = &cpu->memory[start_address];
    uint16_t max_program_size = (1 << 16) - start_address;
    if (filesize > max_program_size) {
        fprintf(stderr, "Error: Program is too large to fit in memory.\n");
        exit(1);
    }

    // Copy program into memory
    fread(dstbuf, 1, filesize, fd);

    // Close the file
    fclose(fd);

    // Set PC to start of program
    cpu->PC = start_address;
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
        case 0xEA:
            // NOP (no operation)
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
