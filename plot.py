import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle

def plot(framerate, t, Dist, planets_names, planets_data, planets_radius, to_scale, target_planet, data_R, x_rocket, y_rocket, closest_approach):

    if closest_approach:
        closest_approach_dist = 1e20
        for i in range(len(t)):
            x = data_R[i][1]
            y = data_R[i][2]
            distx = x - planets_data[target_planet][i][1]
            disty = y - planets_data[target_planet][i][2]
            dist = int((distx**2+disty**2)**0.5/1000)
            if dist < closest_approach_dist:
                closest_approach_dist = dist

    fig = plt.figure()
    ax = plt.subplot2grid((1,2), (0, 0))
    fig.set_size_inches(12, 6)
    Distance_From_Earth = ax.text(1.03, 0.97, "", transform = ax.transAxes)
    Velocity_Of_Rocket = ax.text(1.03, 0.93, "", transform = ax.transAxes)
    Time_Months = ax.text(1.03, 0.89, "", transform = ax.transAxes)
    Distance_From_Target = ax.text(1.03, 0.85, "", transform = ax.transAxes)
    if closest_approach:
        Distance_Of_Closest_Approach = ax.text(1.03, 0.81, "Distance of closest approach to " + planets_names[target_planet] + ": " + str(closest_approach_dist) + " km", transform = ax.transAxes)

    temp = 0
    for k in planets_names: 
        if temp <= k+1: temp = k+1

    plot_range = max(Dist[0:temp])
    plot_range += 0.1*plot_range
    plt.xlim([-plot_range, plot_range])
    plt.ylim([-plot_range, plot_range])
    ax.plot([-plot_range, plot_range], [0,0], lw=0.5)

    x1 = [[],[],[],[],[],[],[],[]]
    y1 = [[],[],[],[],[],[],[],[]]
    planet_graph = [0,0,0,0,0,0,0,0]
    planet_orbit_graph = [0,0,0,0,0,0,0,0]
    graph_colors = ['indianred', 'coral', 'blue', 'firebrick', 'orange', 'goldenrod', 'cyan', 'navy']

    if to_scale:
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

    xR, yR = [], []

    ax2 = plt.subplot2grid((1,2), (0,1))
    ax2.axis('off')

    def animate(i):
        # time.sleep(2)
        j = int(len(t) * i / framerate)

        for k, planet in planets_names.items():
            x = planets_data[k][j][1]
            y = planets_data[k][j][2]
            x1[k].append(x)
            y1[k].append(y)
            if to_scale:
                planet_graph[k].set(center = (x, y))    
            else:
                planet_graph[k].set_data(x, y)
            planet_orbit_graph[k].set_data(x1[k], y1[k])

        x = data_R[j][1]
        y = data_R[j][2]
        vx = data_R[j][3]
        vy = data_R[j][4]
        distx = x - planets_data[target_planet][j][1]
        disty = y - planets_data[target_planet][j][2]
        dist = int((distx**2+disty**2)**0.5/1000)
        Distance_From_Earth.set_text("Distance from Earth: " +str(int(data_R[j][7]/1000)) + " km")
        temp = int(((vx**2)+(vy**2))**(0.5)/1000)
        Velocity_Of_Rocket.set_text("Velocity: " +str(temp) + " km/s")
        Time_Months.set_text("Time: " + str(int(data_R[j][0]/(60*60*24*30))) + " months")
        Distance_From_Target.set_text("Distance from " + planets_names[target_planet] + ": " + str(dist) + " km")

        xR.append(x)
        yR.append(y)
        if to_scale:
            Rocket.set(center = (x, y))
        else:
            Rocket.set_data(x, y)
        RocketOrbit.set_data(xR, yR)

        # rangex = data_R[j][1]
        # rangey = data_R[j][2]
        # plt.xlim([rangex+20000e5, rangex-20000e5])
        # plt.ylim([rangey+20000e5, rangey-20000e5])

        # if data_R[j][7] < SOI[1] : time.sleep(0.4)

        arr = [Rocket, RocketOrbit]
        for k in planets_names:
            arr.append(planet_graph[k])
            arr.append(planet_orbit_graph[k])
        return arr

    anim = FuncAnimation(fig, animate, frames = framerate, interval = 1, blit = False)
    ax.plot(x_rocket, y_rocket, lw=0.5, color='lightgray')
    # plt.legend()
    plt.show()