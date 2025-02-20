#include <stdio.h>

#include "cpu.h"


int main(int argc, char* argv[])
{
    CPU cpu;
    init_cpu(&cpu);

    // LDA #255, STA $1200, BRK
    uint8_t program[] = {
        0xA9, 0xFF, 0x8D, 0x00, 0x12, 0x00
    };

    load_program(&cpu, program, sizeof(program), 0x8000);
    run_cpu(&cpu);

    print_state(&cpu);
    uint8_t valA = read_memory(&cpu, 0x1200);
    printf("Value at $1200: %i", valA);
    
    return 0;
}
