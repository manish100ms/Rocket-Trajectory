import numpy as np
import os
import time

def planet_traj(G, M, dt, N_years, incd, t, CO):
    filename = "{:}[(x={:.3e}, y={:.3e}), (vx={:.3e}, vy={:.3e}), (dt={:.2f}), (N={:.3f} year(s))]".format(CO, incd[0][0], incd[0][1], incd[1][0], incd[1][1], dt, N_years)
    file_exists = os.path.exists(r'Data/%s.npy'%(filename))

    file_time_start = time.time()
    if file_exists == False:
        x = np.zeros(len(t))    ; x[0] = incd[0][0]
        vx = np.zeros(len(t))   ; vx[0] = incd[1][0]
        y = np.zeros(len(t))    ; y[0] = incd[0][1]
        vy = np.zeros(len(t))   ; vy[0] = incd[1][1]
        r = np.zeros(len(t))    ; r[0] = (x[0]**2+y[0]**2)**0.5
        ax = np.zeros(len(t))   ; ax[0] = G*M*x[0]/(r[0]**3)
        ay = np.zeros(len(t))   ; ay[0] = G*M*y[0]/(r[0]**3)

        file = r'Data/%s'%(filename)
        print(f'Creating new data file for {CO} as {filename}...', end=' ')
        for i in range(len(t)-1):
            # Velocity Vectors
            vx[i + 1] = vx[i] -  dt*ax[i]
            vy[i + 1] = vy[i] -  dt*ay[i]
            # Position Vectors
            x[i + 1] = x[i] + dt*vx[i + 1]
            y[i + 1] = y[i] + dt*vy[i + 1]
            # Radius
            r[i+1] = (x[i+1]**2+y[i+1]**2)**0.5
            # Acceleration
            ax[i+1] = G*M*x[i+1]/(r[i+1]**3)
            ay[i+1] = G*M*y[i+1]/(r[i+1]**3)
         
        data = np.column_stack((t, x, y, vx, vy, ax, ay))
        np.save(file, data)
        print('Done!')
        
        time.sleep(1)
        file_time_end = time.time()
        print("Time to write file =", file_time_end-file_time_start)

    else:
        print(f'File with same initial conditions for {CO} already exists. Reading data from file...', end=' ')
        file = r'Data/%s.npy'%(filename)
        data = np.load(file)
        print('Done!')
        time.sleep(1)
        file_time_end = time.time()
        print("Time to read file =", file_time_end-file_time_start)

    return(data)
