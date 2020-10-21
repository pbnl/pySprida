import mip

m = Model(sense=MAXIMIZE, solver_name=CBC)

# create variables
n = 10
numBetreuer = 5  # anzahl der betreuer
lenBetreuer = 5  # length of vector per betreuer

y = [m.add_var(var_type=BINARY) for i in range(n)]

# add constraints
m += x + y <= 10

# constraint gesamtdauer
for i in range(numBetreuer):
    m += xsum(gesamtdauer[i % lenBetreuer] * y[i] for j in range(0, numBetreuer) for i in range(j, j + lenBetreuer))

# constraint prios

# set target
m.objective = minimize(xsum(c[i] * x[i] for i in range(n)))
