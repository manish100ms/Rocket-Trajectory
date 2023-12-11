def func(x,y):
    return x + y**2

x = []
y = []
x.append(0)
y.append(1)
h = 0.1

n = 0

while(x[n] < 0.2):
    k1 = h * func(x[n], y[n])
    k2 = h * func(x[n] + (h/2), y[n] + (k1/2))
    k3 = h * func(x[n] + (h/2), y[n] + (k2/2))
    k4 = h * func(x[n] + h, y[n] + k3)

    k = (k1 + 2*k2 + 2*k3 + k4)/6
    y.append(y[n] + k)

    x.append(x[n] + h)
    n += 1

print(x)
print(y)
