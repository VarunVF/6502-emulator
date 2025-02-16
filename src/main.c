#include <stdio.h>

#include "cpu.h"


int main(int argc, char* argv[])
{
    CPU cpu;
    init_cpu(&cpu);

    // LDA #255, BRK
    uint8_t program[] = {
        0xA9, 0xFF, 0x00
    };

    load_program(&cpu, program, sizeof(program), 0x8000);
    run_cpu(&cpu);

    print_state(&cpu);
    return 0;
}
