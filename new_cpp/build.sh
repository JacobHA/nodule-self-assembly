#!/bin/bash

# Compile the source files
g++ -c Nodule.cpp -o Nodule.o
g++ -c NoduleField.cpp -o NoduleField.o
g++ -c main.cpp -o main.o

# Link the object files to create an executable
g++ Nodule.o NoduleField.o main.o -o program

# Run the program
./program
