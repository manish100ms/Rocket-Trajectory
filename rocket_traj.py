import numpy as np
import os
import time

def rocket_traj(G, M, dt, N_years, planets_names, planets_effect, Pos, Vel, Mass, predict_trajectory, x_rocket, y_rocket, incd, t, planets_data, CO):
    
    # A new file of Rocket is created if there is a new file for any of the planets whose effect is considered
    planet_filename = [None, None, None, None, None, None, None, None]
    planet_exists = [True, True, True, True, True, True, True, True]
    for k in planets_effect:
        planet_filename[k] = ("{:}[(x={:.3e}, y={:.3e}), (vx={:.3e}, vy={:.3e}), (dt={:.2f}), (N={:.3f} year(s))]".format(planets_names[k], Pos[k][0], Pos[k][1], Vel[k][0], Vel[k][1], dt, N_years))
        planet_exists[k] = (os.path.exists(r'Data/%s.npy'%(planet_filename[k])))
    
    p_names = ''
    for k in planets_effect: 
        p_names = p_names + planets_names[k] + ' '
    filename = "{:}[(x={:.3e}, y={:.3e}), (vx={:.3e}, vy={:.3e}), (dt={:.2f}), (N={:.3f} year(s)), (planets_effect={:})]".format(CO, incd[0][0], incd[0][1], incd[1][0], incd[1][1], dt, N_years, p_names)
    file_exists = os.path.exists(r'Data/%s.npy'%(filename))

    file_time_start = time.time()
    if (not file_exists) or (not all(planet_exists)):
        x = np.zeros(len(t))    ; x[0] = incd[0][0]
        vx = np.zeros(len(t))   ; vx[0] = incd[1][0]
        y = np.zeros(len(t))    ; y[0] = incd[0][1]
        vy = np.zeros(len(t))   ; vy[0] = incd[1][1]
        r = np.zeros(len(t))    ; r[0] = (x[0]**2+y[0]**2)**0.5
        
        ax_sun = np.zeros(len(t))   ; ax_sun[0] = G*M*x[0]/(r[0]**3)
        ay_sun = np.zeros(len(t))   ; ay_sun[0] = G*M*y[0]/(r[0]**3)
        distx = [np.zeros(len(t)), np.zeros(len(t)), np.zeros(len(t)), np.zeros(len(t)), np.zeros(len(t)), np.zeros(len(t)), np.zeros(len(t)), np.zeros(len(t))]
        disty = [np.zeros(len(t)), np.zeros(len(t)), np.zeros(len(t)), np.zeros(len(t)), np.zeros(len(t)), np.zeros(len(t)), np.zeros(len(t)), np.zeros(len(t))] 
        dist = [np.zeros(len(t)), np.zeros(len(t)), np.zeros(len(t)), np.zeros(len(t)), np.zeros(len(t)), np.zeros(len(t)), np.zeros(len(t)), np.zeros(len(t))] 
        ax_planet = [np.zeros(len(t)), np.zeros(len(t)), np.zeros(len(t)), np.zeros(len(t)), np.zeros(len(t)), np.zeros(len(t)), np.zeros(len(t)), np.zeros(len(t))]
        ay_planet = [np.zeros(len(t)), np.zeros(len(t)), np.zeros(len(t)), np.zeros(len(t)), np.zeros(len(t)), np.zeros(len(t)), np.zeros(len(t)), np.zeros(len(t))]
        ax = np.zeros(len(t))   ; ax[0] = ax_sun[0]
        ay = np.zeros(len(t))   ; ay[0] = ay_sun[0]
        for k in planets_effect:
            distx[k][0] = x[0] - planets_data[k][0][1]
            disty[k][0] = y[0] - planets_data[k][0][2]
            dist[k][0] = (distx[k][0]**2 + disty[k][0]**2)**0.5
            # if dist[k][0] < SOI[k]:
            ax_planet[k][0] =  G * Mass[k] * distx[k][0] / (dist[k][0]**3)
            ay_planet[k][0] =  G * Mass[k] * disty[k][0] / (dist[k][0]**3)
            ax[0] += ax_planet[k][0]
            ay[0] += ay_planet[k][0]

        file = r'Data/%s'%(filename)
        print(f'Creating new data file for {CO} as {filename}...', end=' ')
        for i in range(len(t)-1): 
            # Velocity Vectors
            vx[i + 1] = vx[i] - dt*ax[i]
            vy[i + 1] = vy[i] - dt*ay[i]
            # Position Vectors
            x[i + 1] = x[i] + dt*vx[i + 1]
            y[i + 1] = y[i] + dt*vy[i + 1]

            # Radius
            r[i+1] = (x[i+1]**2+y[i+1]**2)**0.5
            
            # Acceleration
            ax_sun[i+1] = G*M*x[i+1]/(r[i+1]**3)
            ay_sun[i+1] = G*M*y[i+1]/(r[i+1]**3)

            ax[i+1] += ax_sun[i+1]
            ay[i+1] += ay_sun[i+1]
            
            for k in planets_effect:
                distx[k][i+1] = x[i+1] - planets_data[k][i+1][1]
                disty[k][i+1] = y[i+1] - planets_data[k][i+1][2]
                dist[k][i+1] = (distx[k][i+1]**2+disty[k][i+1]**2)**0.5
                # if dist[k][i+1] <= SOI[k]:
                ax_planet[k][i+1] =  G * Mass[k] * distx[k][i+1] / (dist[k][i+1]**3)
                ay_planet[k][i+1] =  G * Mass[k] * disty[k][i+1] / (dist[k][i+1]**3)
                ax[i+1] += ax_planet[k][i+1]
                ay[i+1] += ay_planet[k][i+1]

        data = np.column_stack((t, x, y, vx, vy, ax, ay, dist[2], r))
        np.save(file, data)
        print('Done!')
        time.sleep(1)
        file_time_end = time.time()
        print("Time to write file =", file_time_end-file_time_start)
        if predict_trajectory: 
            for i in range(len(t)-1):
                x_rocket.append(data[i][1])
                y_rocket.append(data[i][2])
    
    else:
        print(f'File with same initial conditions for {CO} already exists. Reading data from file...', end=' ')
        file = r'Data/%s.npy'%(filename)
        data = np.load(file)
        print('Done!')
        time.sleep(1)
        file_time_end = time.time()
        print("Time to read file =", file_time_end-file_time_start)
        if predict_trajectory: 
            for i in range(len(t)-1):
                x_rocket.append(data[i][1])
                y_rocket.append(data[i][2])

    return(data)