    # Assume x is in x10, y is in x11, z is in x12

    beq x10, x11, if_true   # Branch to `if_true` if x == y
    # Fall-through: if x != y, continue execution here
    j end_if                # Skip the `if` block

if_true:
    add x12, x10, x11       # z = x + y
    # End of the `if` block
end_if:
    # Continue execution here




    # Registers used:
# x10 (a0): First argument and return value
# x11 (a1): Second argument
# x1  (ra): Return address

    .text
    .globl main

main: 
    # Set up arguments for the function
    li x10, 5        # Load immediate value 5 into a0 (first argument)
    li x11, 7        # Load immediate value 7 into a1 (second argument)

    # Call the add_numbers function
    jal x1, add_numbers  # Jump to add_numbers, save return address in ra (x1)

    # When add_numbers returns, the result is in x10 (a0)
    # Result of 5 + 7 = 12 will be in x10

    # End the program (exit)
    li x10, 10       # System call for exit
    ecall            # Make the system call

# Function: add_numbers
# Adds two numbers and returns the result.
# Input: a0 (x10) and a1 (x11)
# Output: a0 (x10)
add_numbers:
    add x10, x10, x11  # a0 = a0 + a1 (x10 = x10 + x11)
    ret                # Return to the caller (jumps to the address in ra)



fac:
    li t0, 1
    bgt a0, t0, notbase
    li a0, 1
    jalr zero, 0(ra)
notbase:
    addi sp, sp, -8
    sw a0, 4(sp)
    sw ra, 0(sp)
    addi a0, a0, -1
    jal ra, fac
    lw t0, 4(sp)
    mul a0, a0, t0
    lw ra, 0(sp)
    addi sp, sp, 8
    jalr zero, 0(ra)

    for "mul" need extension 'm': "ASFLAGS=-march=rv32im"