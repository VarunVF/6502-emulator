#include <stdio.h>

#include "cpu.h"


int main(int argc, char* argv[])
{
    if (argc != 2) {
        fprintf(stderr, "Usage: %s program_file\n", argv[0]);
        fprintf(stderr, "Argument input_file is required\n");
        return 1;
    }

    CPU cpu;
    init_cpu(&cpu);
    
    load_program_file(&cpu, argv[1], 0x8000);
    run_cpu(&cpu);
    
    print_state(&cpu);
    
    return 0;
}
