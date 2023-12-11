import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
from matplotlib.patches import Circle
import numpy as np
import time
import os
from collections import OrderedDict

alpha = np.loadtxt('Data/Alpha.txt')
print(alpha)
begin = time.time()

G = 6.674e-11
M = 1.989e30

N = 5*365*24*60*60
N_years = N/(365*24*60*60)
timestep = 60
t = np.linspace(0,N,int(N/timestep))
dt = (t[1] - t[0])
framerate = 10000

predict_trajectory = True   # Switch this to True if you want predicted trajectory for Rocket
crash_detect = False    # Switch this to True if you want to detect if the rocket will crash
life_scale = False
planets_names = OrderedDict([(0,'Mercury'), (1,'Venus'), (2,'Earth'), (3,'Mars'), (4,'Jupiter'), (5,'Saturn'), (6,'Uranus'), (7,'Neptune')])
planets_effect = [2, 3, 4, 5]
for j in planets_effect:
    if j not in planets_names:
        print("Planet(s) included in 'planets_effect' not in 'planets_names'! Following are the planets included in the simulation :-")
        for l, m in planets_names.items():
            print(l,':',m)
        print("\nPlease enter the new values for 'planets_effect'. Enter '8' to stop entering more values.")
        x = 0
        planets_effect = []
        while True:
            x = int(input())
            if x == 8:
                break
            planets_effect.append(x)

planets_radius = [2439.5e3, 6052e3, 6378e3, 3396e3, 71492e3, 60268e3, 25559e3, 24764e3]
SOI = [0.117e9, 0.616e9, 0.929e9, 0.578e9, 48.2e9, 54.5e9, 51.9e9, 86.2e9]
Mass = [0.330e24, 4.87e24, 5.97e24, 0.642e24, 1898e24, 568e24, 86.8e24, 102e24]
Dist = [57.9e9, 108.2e9, 149.6e9, 228.0e9, 778.5e9, 1432.0e9, 2867.0e9, 4515.0e9]

phi = [0, 0, 0, alpha[3], alpha[4], alpha[5], 0, 0]

Pos = [0, 0, 0, 0, 0, 0, 0, 0]
Vel = [0, 0, 0, 0, 0, 0, 0, 0]
incd = []
for i in range(8):
    Pos[i] = np.array([Dist[i]*np.cos(phi[i]), Dist[i]*np.sin(phi[i])])
    Vel_Mod = np.sqrt(G*M/np.sqrt(Pos[i].dot(Pos[i])))
    Vel[i] = np.array([np.sin(phi[i])*Vel_Mod, -np.cos(phi[i])*Vel_Mod])
    incd.append([Pos[i], Vel[i]])


#************************************ DEFINING VALUES FOR ROCKET ************************************#
# Pos_R = np.array([Pos[2][0]+7000e3, 0])
# Vel_R = np.array([0, -np.sqrt(G*M/Pos[2][0])-np.sqrt(G*Mass[2]/7000e3)-20000])
Pos_R = np.array([Pos[2][0]+0.5e9, 0])
Vel_R = np.array([0, -np.sqrt(G*M/Pos[2][0])-np.sqrt(G*Mass[2]/0.5e9)])
Add_Vel = 20000
incd_R = [Pos_R, Vel_R]
x_rocket, y_rocket = [], []
#****************************************************************************************************#

def planets(incd, t, CO, PNo):
    filename = "{:}[(x={:.3e}, y={:.3e}), (vx={:.3e}, vy={:.3e}), (dt={:.2f}), (N={:.3f} year(s))]".format(CO, incd[0][0], incd[0][1], incd[1][0], incd[1][1], dt, N_years)
    file_exists = os.path.exists(r'Data/%s.npy'%(filename))
    file_time_start = time.time()

    if file_exists:
        print(f'File with same initial conditions for {CO} already exists. Reading data from file...', end=' ')
        file = r'Data/%s.npy'%(filename)
        data = np.load(file)
        for i in range(len(t)-1):
            xP[PNo].append(data[i][1])
            yP[PNo].append(data[i][2])
        print('Done!')
        time.sleep(1)
        file_time_end = time.time()
        print("Time to read file =", file_time_end-file_time_start)
        # return(data)
    
    else:
        print("File does not exist!")


def rocket(incd, t, planets_data, CO):
    p_names = ''
    for k in planets_effect: 
        p_names = p_names + planets_names[k] + ' '
    filename = "{:}[(x={:.3e}, y={:.3e}), (vx={:.3e}, vy={:.3e}), (dt={:.2f}), (N={:.3f} year(s)), (planets_effect={:})]".format(CO, incd[0][0], incd[0][1], incd[1][0], incd[1][1], dt, N_years, p_names)
    file_exists = os.path.exists(r'Data/%s.npy'%(filename))
    file_time_start = time.time()

    if file_exists:
        print(f'File with same initial conditions for {CO} already exists. Reading data from file...', end=' ')
        file = r'Data/%s.npy'%(filename)
        data = np.load(file)
        print('Done!')
        time.sleep(1)
        file_time_end = time.time()
        print("Time to read file =", file_time_end-file_time_start) 
        for i in range(len(t)-1):
            xR.append(data[i][1])
            yR.append(data[i][2])
            x_rocket.append(data[i][1])
            y_rocket.append(data[i][2])
        # return(data)
    
    else:
        print("File does not exist!")

xP = [[],[],[],[],[],[],[],[]]
yP = [[],[],[],[],[],[],[],[]]
xR, yR = [], []
planets_data = [0,0,0,0,0,0,0,0]
for i, planet in planets_names.items():
    planets(incd[i], t, planet, i)

rocket(incd_R, t, planets_data, 'Rocket')
data_R = []


time.sleep(1)
end = time.time()
print("Total time =", end-begin)

fig, ax = plt.subplots()
fig.set_size_inches(6, 6)
temp = 0
for k in planets_names: 
    if temp <= k+1: temp = k+1

range = max(Dist[0:temp])
range += 0.1*range
# range = 5000e9
plt.xlim([-range, range])
plt.ylim([-range, range])
ax.plot([-range, range], [0,0], lw=0.5)

x1 = [[],[],[],[],[],[],[],[]]
y1 = [[],[],[],[],[],[],[],[]]
x2, y2 = [], []
planet_graph = [0,0,0,0,0,0,0,0]
planet_orbit_graph = [0,0,0,0,0,0,0,0]
graph_colors = ['indianred', 'coral', 'blue', 'firebrick', 'orange', 'goldenrod', 'cyan', 'navy']

# to_scale = int(input(("\nDo you want the planets' size to be 'to-scale'? (1-Yes | 0-No): ")))
to_scale = 0
if to_scale == 1:
    for i, planet in planets_names.items():
        planet_graph[i] = Circle((0,0), planets_radius[i], label=str(planet), color=graph_colors[i])
        ax.add_artist(planet_graph[i])
        planet_orbit_graph[i], = ax.plot([], [], lw=0.5, color=graph_colors[i])

    Rocket = Circle((0,0), 50, label='Rocket', color='red')
    ax.add_artist(Rocket)
    RocketOrbit, = ax.plot([], [], lw=0.5, color='red')

else:
    for i, planet in planets_names.items():
        planet_graph[i], = ax.plot([], [], marker='o', label=str(planet), color=graph_colors[i])
        planet_orbit_graph[i], = ax.plot([], [], lw=0.5, color=graph_colors[i])
    Rocket, = ax.plot([], [], marker='o', label='Rocket', color='red')
    RocketOrbit, = ax.plot([], [], lw=0.5, color='red')

def animate(i):
    j = int(len(t) * i / framerate)
    for k, planet in planets_names.items():
        x = xP[k][j]
        y = yP[k][j]
        x1[k].append(x)
        y1[k].append(y)
        if to_scale == 1:
            planet_graph[k].set(center = (x, y))    
        else:
            planet_graph[k].set_data(x, y)
        planet_orbit_graph[k].set_data(x1[k], y1[k])

    x = xR[j]
    y = yR[j]
    x2.append(x)
    y2.append(y)
    if to_scale == 1:
        Rocket.set(center = (x, y))
    else:
        Rocket.set_data(x, y)
    RocketOrbit.set_data(x2, y2)

    # rangex = xP[2][j]
    # rangey = yP[2][j]
    # rangex = xR[j]
    # rangey = yR[j]
    # plt.xlim([rangex-6e9, rangex+6e9])
    # plt.ylim([rangey-6e9, rangey+6e9])

    # if data_R[j][7] < SOI[1] : time.sleep(0.4)

    arr = [Rocket, RocketOrbit]
    for k in planets_names:
        arr.append(planet_graph[k])
        arr.append(planet_orbit_graph[k])
    return arr

anim = FuncAnimation(fig, animate, frames = framerate, interval = 1, blit = True)
plt.plot(x_rocket, y_rocket, lw=0.5, color='lightgray')

# plt.legend()
plt.show()