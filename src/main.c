#include <stdio.h>

#include "cpu.h"


int main(int argc, char* argv[])
{
    CPU cpu;
    init_cpu(&cpu);
    
    uint16_t address = (uint16_t)1;
    uint8_t value = read_memory(&cpu, address);
    
    printf("Memory read at address %i: %i\n", address, value);
    print_state(&cpu);

    return 0;
}
