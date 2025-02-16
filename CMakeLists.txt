cmake_minimum_required(VERSION 3.10)

project(NESemulator)

add_executable(out
    src/cpu.c
    src/instructions.c
    src/main.c
)
