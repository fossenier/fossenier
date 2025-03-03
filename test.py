import math as m

# archimedes:
#         bne zero, a0, rec_case

#         li t0, 1
#         fmv.w.x ft0, t0         # 1
#         li t0, 3
#         fmv.w.x ft1, t0         # 3
#         fsqrt.s ft1, ft1        # sqrt(3)
#         fdiv.s fa0, ft0, ft1    # 1 / sqrt(3)

#         jalr zero, 0(ra)

# rec_case:
#         addi sp, sp, -4
#         sw ra, 0(sp)

#         addi a0, a0, -1         # Decrement
#         jal ra, archimedes      # t_(k-1) in fa0

#         li t0, 1
#         fmv.w.x ft0, t0         # 1

#         fmul.s ft1, fa0, fa0    # (t_(k-1)) ^ 2
#         fadd.s ft1, ft1, ft0
#         fsqrt.s ft1, ft1        # sqrt((t_(k-1)) ^ 2 + 1)
#         fsub.s ft1, ft1, ft0
#         fdiv.s fa0, ft1, fa0    # (sqrt((t_(k-1)) ^ 2 + 1) - 1) / t_(k-1) in fa0


def main():
    k = int(input("Enter k: "))
    tk = archimedes(k)
    n = 6 * (2**k) * tk
    print(n)


def archimedes(n):
    if n == 0:
        return 1 / m.sqrt(3)

    next = archimedes(n - 1)

    return (m.sqrt((next**2) + 1) - 1) / next


if __name__ == "__main__":
    main()
