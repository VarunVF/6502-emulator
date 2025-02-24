#ifndef INSTRUCTIONS_H
#define INSTRUCTIONS_H

#include "cpu.h"


uint16_t cpu_get_abs_addr(CPU* cpu);

void LDA_set_flags(CPU* cpu);

void LDA_imm(CPU* cpu);
void LDA_zpg(CPU* cpu);
void LDA_zpg_x(CPU* cpu);
void LDA_abs(CPU* cpu);
void LDA_abs_x(CPU* cpu);
void LDA_abs_y(CPU* cpu);
void LDA_ind_x(CPU* cpu);
void LDA_ind_y(CPU* cpu);

void STA_abs(CPU* cpu);

void BRK(CPU* cpu);

#endif /* INSTRUCTIONS_H */
