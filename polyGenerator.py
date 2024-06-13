coeffs = [0, 2, 11, 21, 23, 32]

sol = []
for i in range(33):
    if i in coeffs:
        sol.append('1')
    else:
        sol.append('0')

sol = sol[::-1]
print("".join(sol))

