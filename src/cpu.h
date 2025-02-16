#ifndef CPU_H
#define CPU_H

#include <stdint.h>

// Total size of RAM (65536 bytes)
#define MEMORY_SIZE (1 << 16)


// Model of the NES 6502
typedef struct CPU
{
    uint8_t A;
    uint8_t X;
    uint8_t Y;
    uint16_t PC;
    uint8_t SP;
    uint8_t SR;
    uint8_t memory[MEMORY_SIZE];
} CPU;


#define FLAG_CARRY      0x01
#define FLAG_ZERO       0x02
#define FLAG_INTERRUPT  0x04
#define FLAG_DECIMAL    0x08
#define FLAG_B          0x10
#define FLAG_UNUSED     0x20
#define FLAG_OVERFLOW   0x40
#define FLAG_NEGATIVE   0x80


void init_cpu(CPU* cpu);

uint8_t read_memory(CPU* cpu, uint16_t address);
void write_memory(CPU* cpu, uint16_t address, uint8_t value);

void print_state(CPU* cpu);


#endif /* CPU_H */
