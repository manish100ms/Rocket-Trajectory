import numpy as np
import time
from astropy.time import Time
from astroquery.jplhorizons import Horizons

from gui import gui
from planets_effect_check import planets_effect_check
from planets_traj import planet_traj
from rocket_traj import rocket_traj
from plot import plot

begin = time.time()

#*********************************** DEFINING UNIVERSAL CONSTANTS ***********************************#
G           = 6.674e-11
M           = 1.989e30
AU          = 149597870691
AU_perDay   = 1731460       # Converts velocity from AU per day to m/s
#****************************************************************************************************#

#******************************* SIMULATION PARAMETERS FROM GUI MODULE ******************************#
temp                = gui()             # Stores return value of GUI module to a temporary variable
predict_trajectory  = temp[0]           # Predicted trajectory for Rocket
crash_detect        = temp[1]           # To detect if the rocket will crash
closest_approach    = temp[2]           # To calculate distance of closest approach to target planet
to_scale            = temp[3]           # Planets are 'to-scale'
N_years             = temp[4]           # Total simulation time in years
N                   = temp[4]*365*24*60*60      # Total simulations time in seconds
dt                  = temp[5]           # Timestep. Since we are using Leapfrog, this becomes half the actual timestep.
t                   = np.linspace(0,N,int(N/dt))  # Create a linear space of different times at equal timestep
framerate           = temp[6]           # Ratio of points to be animated. (Total points)/(No. of points to be skipped)
sim_time            = Time(str(str(temp[7][2]) + '-' + str(temp[7][1]) + '-' + str(temp[7][0]) + ' 00:00')) # Simulation start date and time
planets_names       = temp[8]           # Names of planets included in the simulation
planets_effect      = temp[9]           # Names of planets whose gravity is considered
target_planet       = temp[10]          # Target planet of rocket
#****************************************************************************************************#

# This function checks whether the planets whose gravity is considered are included in the simulation or not
planets_effect = planets_effect_check(planets_names, planets_effect)    

planets_radius = [2439.5e3, 6052e3, 6378e3, 3396e3, 71492e3, 60268e3, 25559e3, 24764e3] # Radius of planets for planets 'to-scale' and for crash detect
# SOI = [0.117e9, 0.616e9, 0.929e9, 0.578e9, 48.2e9, 54.5e9, 51.9e9, 86.2e9]              
Mass = [0.330e24, 4.87e24, 5.97e24, 0.642e24, 1898e24, 568e24, 86.8e24, 102e24]         # Mass of planets
Dist = [57.9e9, 108.2e9, 149.6e9, 228.0e9, 778.5e9, 1432.0e9, 2867.0e9, 4515.0e9]       # Orbital radii of planets

# Following are the IDs for JPL Horizon data
# [id: 10]   Sun [Sol]
# [id:199]   Mercury
# [id:299]   Venus
# [id:399]   Earth
# [id:499]   Mars
# [id:599]   Jupiter
# [id:699]   Saturn
# [id:799]   Uranus
# [id:899]   Neptune
id = ['199', '299', '399', '499', '599', '699', '799', '899']
Pos = [0, 0, 0, 0, 0, 0, 0, 0]      # This array stores initial positions of all the planets
Vel = [0, 0, 0, 0, 0, 0, 0, 0]      # This array stores initial velocities of all the planets
incd = [0, 0, 0, 0, 0, 0, 0, 0]     # This array stores the initial conditions i.e. the initial positions and velocities of all the planets
horizon_data = [0, 0, 0, 0, 0, 0, 0, 0] # This array stores the JPL Horizon data for all the planets
for i, j in zip(id, range(8)):
    horizon_data[j] = Horizons(i, location='500@0', epochs=sim_time.tdb.jd)
    horizon_data[j] = horizon_data[j].vectors()
    Pos[j] = np.array([horizon_data[j]['x'][0]*AU, horizon_data[j]['y'][0]*AU])
    Vel[j] = np.array([horizon_data[j]['vx'][0]*AU_perDay, horizon_data[j]['vy'][0]*AU_perDay])
    incd[j] = [Pos[j], Vel[j]]

# Pos[2] = np.array([1.447732376809139E+11, -4.248306893639585E+10])
# Vel[2] = np.array([7.800855426390862E+03, 2.848755079035207E+04])
# incd[2] = [Pos[2], Vel[2]]
#************************************ DEFINING VALUES FOR ROCKET ************************************#
# Pos_R = np.array([Pos[2][0]+7000e3, 0])
# Vel_R = np.array([0, -np.sqrt(G*M/Pos[2][0])-np.sqrt(G*Mass[2]/7000e3)])
Pos_R = np.array([1.451559148454779e11, -4.285835857828943e10])
Vel_R = np.array([1.158587716438512e4, 3.813754724695271e4])
incd_R = [Pos_R, Vel_R]

# These arrays store all the positions of the rocket at all time points to plot the predicted trajectory
x_rocket, y_rocket = [], [] 
#****************************************************************************************************#

planets_data = [0,0,0,0,0,0,0,0]
for i, planet in planets_names.items():
    planets_data[i] = planet_traj(G, M, dt, N_years, incd[i], t, planet)

data_R = rocket_traj(G, M, dt, N_years, planets_names, planets_effect, Pos, Vel, Mass, predict_trajectory, x_rocket, y_rocket, incd_R, t, planets_data, 'Rocket')

if crash_detect:
    for k, planet in planets_names.items():   
        for i in range(len(t)-1): 
            if ((data_R[i][1]-planets_data[k][i][1])**2 + (data_R[i][2]-planets_data[k][i][2])**2) <= planets_radius[k]**2:
                print('Crash with', planet)
                break

time.sleep(1)
end = time.time()
print("Total time =", end-begin)

plot(framerate, t, Dist, planets_names, planets_data, planets_radius, to_scale, target_planet, data_R, x_rocket, y_rocket, closest_approach)