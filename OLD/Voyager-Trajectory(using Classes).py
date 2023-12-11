import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

#************************************** SIMULATION PARAMETERS ***************************************#
dt = 60              # Timestep in seconds
N = 100000           # Number of timesteps to be calulated. dt=86400(1 Day) and N=365(1 year) => 1 year
framerate = 1000       # Number of frames
#****************************************************************************************************#

#*********************************** DEFINING UNIVERSAL CONSTANTS ***********************************#
G = 6.674e-11                   # Gravitation Constant in SI unit (m3 kg-1 s-2)
M = 1.9885e30                    # Mass of the Sun in kg
AU = 1.496e11                   # 1 Astronomical Unit in m
#****************************************************************************************************#

#************************************* DEFINING VALUES FOR EARTH ************************************#
Mass_E = 5.97219e24                        # Mass of Earth
# Actual Parameters
# Init_Pos_E = np.array([-1.006663179017242e11, 1.076981840054020e11, -5.153697188548744e06]) # Initial position of Earth
# Init_Vel_E = np.array([-2.224907136982621e4, -2.044133575999158e4, 1.408831662804921])      # Initial velocity of Earth
# Circular Orbit Parameters
Init_Pos_E = np.array([AU, 0, 0])
Init_Vel_E = np.array([0, np.sqrt(G*M/AU), 0])
#****************************************************************************************************#

#*********************************** DEFINING VALUES FOR JUPITER ************************************#
Mass_J = 1.898e27                          # Mass of Jupiter
# Actual Parameters
# Init_Pos_J = np.array([4.830437891699320e11, -5.875968685499133e11, -8.366809258387744e9]) # Initial position of Jupiter
# Init_Vel_J = np.array([9.945908521750388e3, 8.922127867874106e3, -2.596189681368934e2])    # Initial velocity of Jupiter

'''Angle phi is calculated such that Jupiter meets the rocket at the apogee'''
phi = -1.72                                # Angle between initial position of Earth and Jupiter

# Circular Orbit Parameters
Init_Pos_J = np.array([5.2044*AU*np.cos(phi),5.2044*AU*np.sin(phi), 0])
Vel_J_Mod = np.sqrt(G*M/np.sqrt(Init_Pos_J.dot(Init_Pos_J)))
Init_Vel_J = np.array([np.cos(phi-1.5708)*Vel_J_Mod, np.sin(phi-1.5708)*Vel_J_Mod, 0])

#****************************************************************************************************#

#*********************************** DEFINING VALUES FOR SATURN ************************************#
Mass_S = 5.683e26                          # Mass of Saturn
Init_Pos_S = np.array([8.420746670179151e11,-1.233134223027472e12, -1.207455012780452e10])  # Initial position of Saturn
Init_Vel_S = np.array([7.451421688990140e3, 5.433509265952789e3, -3.914824643997095e2])     # Initial velocity of Jupiter

'''Angle phi is calculated such that Saturn meets the rocket at the apogee'''
phi1 = -2.75                               # Angle between initial position of Earth and Saturn
#****************************************************************************************************#

#************************************ DEFINING VALUES FOR ROCKET ************************************#
Mass_r = 1000
Init_Pos_r = np.array([Init_Pos_E[0]+7000e3, 0, 0])
Init_Vel_r = np.array([0, Init_Vel_E[1] + np.sqrt(G*Mass_E/7000e3), 0])
# Init_Vel_r = np.array([0, -np.sqrt(G*M*2*(5.2044*AU+(5*69911e3))/(Init_Pos_E[0]*(Init_Pos_E[0]+(5.2044*AU+(5*69911e3))))), 0])
#****************************************************************************************************#

class body:
    
    def __init__(self, name, mass, init_pos, init_vel):
        self.name = name
        self.mass = mass

        self.Pos = init_pos
        self.Pos_Array = [self.Pos]
        self.Pos_Mag_Array = []
        self.x = init_pos[0]
        self.x_Array = []
        self.y = init_pos[1]
        self.y_Array = []
        self.z = init_pos[2]
        self.z_Array = []

        self.Vel = init_vel
        self.Vel_Array = [self.Vel]
        self.Vel_Mag_Array = []

        self.Force = np.array([0, 0, 0])
        self.Force_Array = []
        self.Force_Mag = 0
        
        self.Acc = np.array([0, 0, 0])
        self.Acc_Array = []

    def force_rocket(self, m2, r2):
        r = self.Pos - r2
        r_mag = np.sqrt(r.dot(r))
        self.Pos_Mag_Array.append(r_mag)
        r_hat = r/r_mag
        self.Force = self.Force - G*self.mass*m2*r_hat/r.dot(r)
        self.Force_Array.append(self.Force)
        self.Force_Mag = np.linalg.norm(self.Force)

    def acc(self): 
        self.Acc = self.Force/self.mass
        self.Acc_Array.append(self.Acc)

    def procedure_planet(self):
        self.force_planet(M)
        self.acc()
        self.vel()
        self.pos()
    
    def procedure_rocket(self):
        self.force_planet(M)
        self.force_rocket(Mass_E, E)
        self.force_rocket(Mass_J, J)
        self.force_rocket(Mass_S, S)
        self.acc()
        self.vel()
        self.pos()
        


Earth_Class = body('Earth', Mass_E, Init_Pos_E, Init_Vel_E)
Jupiter_Class = body('Jupiter', Mass_J, Init_Pos_J, Init_Vel_J)
Saturn_Class = body('Saturn', Mass_S, Init_Pos_S, Init_Vel_S)
Rocket_Class = body('Rocket', Mass_r, Init_Pos_r, Init_Vel_r)

aphelion = 0
perihelion = 99999999999
t = 0
while t < N:
    Earth_Class.procedure_planet()
    if aphelion < np.linalg.norm(Earth_Class.Pos): aphelion = np.linalg.norm(Earth_Class.Pos) 
    Jupiter_Class.procedure_planet()
    Saturn_Class.procedure_planet()
    E = Earth_Class.Pos
    J = Jupiter_Class.Pos
    S = Saturn_Class.Pos
    Rocket_Class.procedure_rocket()
    if t == 4000 : Rocket_Class.add_vel()
    if t == 5000 : dt = 10000
    # print(Rocket_Class.Pos)
    t = t + 1

print("Aphelion =", aphelion)

fig = plt.figure()
ax = plt.axes(projection ='3d')
range = 10*AU
ax.set_xlim([-range, range])
ax.set_ylim([-range, range])
ax.set_zlim([-range, range])
ax.plot([-range, range], [0,0], lw=0.5)
ax.plot([0,0], [-range, range], lw=0.5)

Earth_Graph, = plt.plot(Earth_Class.Pos_Array[0][0], Earth_Class.Pos_Array[0][1], Earth_Class.Pos_Array[0][2], lw=2, marker='o', label='Earth', color='blue')
Jupiter_Graph, = plt.plot(Jupiter_Class.Pos_Array[0][0], Jupiter_Class.Pos_Array[0][1], Jupiter_Class.Pos_Array[0][2], lw=2, marker='o', label='Jupiter', color='orange')
Saturn_Graph, = plt.plot(Saturn_Class.Pos_Array[0][0], Saturn_Class.Pos_Array[0][1], Saturn_Class.Pos_Array[0][2], lw=2, marker='o', label='Saturn', color='brown')
Rocket_Graph, = plt.plot(Rocket_Class.Pos_Array[0][0], Rocket_Class.Pos_Array[0][1], Rocket_Class.Pos_Array[0][2], lw=2, marker='o', label='Rocket', color='red')

def animate(i):
    j = int(N * i / framerate)

    Earth_Graph.set_data(Earth_Class.x_Array[j], Earth_Class.y_Array[j])
    Earth_Graph.set_3d_properties(Earth_Class.z_Array[j])

    Jupiter_Graph.set_data(Jupiter_Class.x_Array[j], Jupiter_Class.y_Array[j])
    Jupiter_Graph.set_3d_properties(Jupiter_Class.z_Array[j])

    Saturn_Graph.set_data(Saturn_Class.x_Array[j], Saturn_Class.y_Array[j])
    Saturn_Graph.set_3d_properties(Saturn_Class.z_Array[j])

    Rocket_Graph.set_data(Rocket_Class.x_Array[j], Rocket_Class.y_Array[j])
    Rocket_Graph.set_3d_properties(Rocket_Class.z_Array[j])

    '''
    # Earth's Prespective
    x, y, z = Earth_Class.Pos_Array[j]
    ax.set_xlim([x-10e7, x+10e7])
    ax.set_ylim([y-10e7, y+10e7])
    ax.set_zlim([z-10e7, z+10e7])
    '''

    return Earth_Graph, Jupiter_Graph, Saturn_Graph, # Rocket_Graph,

anim = FuncAnimation(fig, animate, frames = framerate, interval = 1, blit = False)

plt.plot(Earth_Class.x_Array, Earth_Class.y_Array, Earth_Class.z_Array, lw=0.5, color='grey')
plt.plot(Jupiter_Class.x_Array, Jupiter_Class.y_Array, Jupiter_Class.z_Array, lw=0.5, color='grey')
plt.plot(Saturn_Class.x_Array, Saturn_Class.y_Array, Saturn_Class.z_Array, lw=0.5, color='grey')
plt.plot(Rocket_Class.x_Array, Rocket_Class.y_Array, Rocket_Class.z_Array, lw=0.5, color='grey')

plt.show()