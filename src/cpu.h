#ifndef CPU_H
#define CPU_H

#include <stdint.h>
#include <stdbool.h>

// Total size of RAM (65536 bytes)
#define MEMORY_SIZE (1 << 16)


// Model of the NES 6502
typedef struct CPU
{
    bool should_halt;
    uint8_t A;      // Accumulator
    uint8_t X;      // X Register
    uint8_t Y;      // Y Register
    uint16_t PC;    // Program Counter
    uint8_t SP;     // Stack Pointer
    uint8_t SR;     // Status Register (Flags)
    uint8_t memory[MEMORY_SIZE];  // RAM
} CPU;


// Status Register flags
#define FLAG_CARRY      0x01
#define FLAG_ZERO       0x02
#define FLAG_INTERRUPT  0x04
#define FLAG_DECIMAL    0x08
#define FLAG_B          0x10
#define FLAG_UNUSED     0x20
#define FLAG_OVERFLOW   0x40
#define FLAG_NEGATIVE   0x80


void init_cpu(CPU* cpu);

void print_state(CPU* cpu);

uint8_t read_memory(CPU* cpu, uint16_t address);
void write_memory(CPU* cpu, uint16_t address, uint8_t value);

void load_program(CPU* cpu, uint8_t* program, uint16_t size, uint16_t start_address);
void execute_instruction(CPU* cpu);
void run_cpu(CPU* cpu);



#endif /* CPU_H */
