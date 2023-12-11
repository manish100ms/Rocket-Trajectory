from collections import OrderedDict
from tkinter import *
from tkinter.ttk import Separator

def gui():
    root = Tk()
    Section1 = Frame(root)
    Section1.grid(row=0, column=0, columnspan=2, sticky='EW')

    Label(Section1, text="Simulation Parameters :-").grid(row=0,column=0, sticky='W')

    predict_trajectory= BooleanVar()   # Switch this to True if you want predicted trajectory for Rocket
    crash_detect = BooleanVar()    # Switch this to True if you want to detect if the rocket will crash
    closest_approach = BooleanVar() # Switch this to True if you want to calculate distance of closest approach to target planet
    to_scale = BooleanVar()
    Checkbutton(Section1, text="Predicted Trajectory", variable=predict_trajectory).grid(row=1,column=0, sticky='W')
    Checkbutton(Section1, text="Crash Detect", variable=crash_detect).grid(row=2,column=0, sticky='W')
    Checkbutton(Section1, text="Closest Approach to Target Planet", variable=closest_approach).grid(row=3,column=0, sticky='W')
    Checkbutton(Section1, text="Planets to be 'to-scale'", variable=to_scale).grid(row=4,column=0, sticky='W')


    N_years = DoubleVar()
    timestep = DoubleVar()
    framerate = IntVar()
    Label(Section1, text="Simulation time(in years): ").grid(row=5, column=0, sticky='W')
    Label(Section1, text="Timestep(in seconds): ").grid(row=6, column=0, sticky='W')
    Label(Section1, text="Number of frames(Higher=Slower): ").grid(row=7, column=0, sticky='W')
    Entry(Section1, textvariable=N_years).grid(row=5, column=1, sticky='W')
    Entry(Section1, textvariable=timestep).grid(row=6, column=1, sticky='W')
    Entry(Section1, textvariable=framerate).grid(row=7, column=1, sticky='W')

    Separator(Section1, orient='horizontal').grid(row=8, column=0, columnspan=3, sticky='EW', pady=5, padx=5)

    time_date = IntVar()
    time_month = IntVar()
    time_year = IntVar()
    Label(Section1, text="Date to start simulation :- ").grid(row=9, column=0, sticky='W')
    Label(Section1, text="Date: ").grid(row=10, column=0, sticky='W')
    Label(Section1, text="Month: ").grid(row=11, column=0, sticky='W')
    Label(Section1, text="Year: ").grid(row=12, column=0, sticky='W')
    Entry(Section1, textvariable=time_date).grid(row=10, column=0)
    Entry(Section1, textvariable=time_month).grid(row=11, column=0)
    Entry(Section1, textvariable=time_year).grid(row=12, column=0)

    Separator(root, orient='horizontal').grid(row=1, column=0, columnspan=3, sticky='EW', pady=5, padx=5)

    Section2 = Frame(root)
    Section2.grid(row=2, column=0, columnspan=3, sticky='EW')

    Label(Section2, text="Planets to be included in Simulation :-").grid(row=0, column=0)
    mercury_sim = BooleanVar()
    venus_sim = BooleanVar()
    earth_sim = BooleanVar()
    mars_sim = BooleanVar()
    jupiter_sim = BooleanVar()
    saturn_sim = BooleanVar()
    uranus_sim = BooleanVar()
    neptune_sim = BooleanVar()
    Checkbutton(Section2, text='Mercury', variable=mercury_sim).grid(row=1, column=0, sticky='W')
    Checkbutton(Section2, text='Venus', variable=venus_sim).grid(row=2, column=0, sticky='W')
    Checkbutton(Section2, text='Earth', variable=earth_sim).grid(row=3, column=0, sticky='W')
    Checkbutton(Section2, text='Mars', variable=mars_sim).grid(row=4, column=0, sticky='W')
    Checkbutton(Section2, text='Jupiter', variable=jupiter_sim).grid(row=5, column=0, sticky='W')
    Checkbutton(Section2, text='Saturn', variable=saturn_sim).grid(row=6, column=0, sticky='W')
    Checkbutton(Section2, text='Uranus', variable=uranus_sim).grid(row=7, column=0, sticky='W')
    Checkbutton(Section2, text='Neptune', variable=neptune_sim).grid(row=8, column=0, sticky='W')

    Separator(Section2, orient='vertical').grid(row=0, column=1, rowspan=9, sticky='NS', padx=5)

    Label(Section2, text="Planets whose gravity effect will be accounted:-").grid(row=0, column=2)
    mercury_eff = BooleanVar()
    venus_eff = BooleanVar()
    earth_eff = BooleanVar()
    mars_eff = BooleanVar()
    jupiter_eff = BooleanVar()
    saturn_eff = BooleanVar()
    uranus_eff = BooleanVar()
    neptune_eff = BooleanVar()
    def check():
        if mercury_eff.get(): mercury_sim.set(True)
        if venus_eff.get(): venus_sim.set(True)
        if earth_eff.get(): earth_sim.set(True)
        if mars_eff.get(): mars_sim.set(True)
        if jupiter_eff.get(): jupiter_sim.set(True)
        if saturn_eff.get(): saturn_sim.set(True)
        if uranus_eff.get(): uranus_sim.set(True)
        if neptune_eff.get(): neptune_sim.set(True)
    Checkbutton(Section2, text='Mercury', variable=mercury_eff, command=check).grid(row=1, column=2, sticky='W')
    Checkbutton(Section2, text='Venus', variable=venus_eff, command=check).grid(row=2, column=2, sticky='W')
    Checkbutton(Section2, text='Earth', variable=earth_eff, command=check).grid(row=3, column=2, sticky='W')
    Checkbutton(Section2, text='Mars', variable=mars_eff, command=check).grid(row=4, column=2, sticky='W')
    Checkbutton(Section2, text='Jupiter', variable=jupiter_eff, command=check).grid(row=5, column=2, sticky='W')
    Checkbutton(Section2, text='Saturn', variable=saturn_eff, command=check).grid(row=6, column=2, sticky='W')
    Checkbutton(Section2, text='Uranus', variable=uranus_eff, command=check).grid(row=7, column=2, sticky='W')
    Checkbutton(Section2, text='Neptune', variable=neptune_eff, command=check).grid(row=8, column=2, sticky='W')

    Separator(root, orient='horizontal').grid(row=3, column=0, columnspan=4, sticky='EW', pady=5, padx=5)

    Label(root, text="Select the target planet:-").grid(row=4, column=0, sticky='W')
    Section3 = Frame(root)
    Section3.grid(row=5, column=0, columnspan=4, sticky='EW')
    target = IntVar()
    Radiobutton(Section3, text='Mercury', variable=target, value=0).grid(row=0, column=0, sticky='W')
    Radiobutton(Section3, text='Venus', variable=target, value=1).grid(row=0, column=1, sticky='W')
    Radiobutton(Section3, text='Earth', variable=target, value=2).grid(row=0, column=2, sticky='W')
    Radiobutton(Section3, text='Mars', variable=target, value=3).grid(row=0, column=3, sticky='W')
    Radiobutton(Section3, text='Jupiter', variable=target, value=4).grid(row=1, column=0, sticky='W')
    Radiobutton(Section3, text='Saturn', variable=target, value=5).grid(row=1, column=1, sticky='W')
    Radiobutton(Section3, text='Uranus', variable=target, value=6).grid(row=1, column=2, sticky='W')
    Radiobutton(Section3, text='Neptune', variable=target, value=7).grid(row=1, column=3, sticky='W')

    # Default values
    predict_trajectory.set(True)
    crash_detect.set(False)
    closest_approach.set(True)
    N_years.set(4)
    timestep.set(60)
    framerate.set(1000)
    time_date.set(6)
    time_month.set(9)
    time_year.set(1977)
    mercury_sim.set(False)
    venus_sim.set(False)
    earth_sim.set(True)
    mars_sim.set(False)
    jupiter_sim.set(True)
    saturn_sim.set(False)
    uranus_sim.set(False)
    neptune_sim.set(False)
    mercury_eff.set(False)
    venus_eff.set(False)
    earth_eff.set(True)
    mars_eff.set(False)
    jupiter_eff.set(True)
    saturn_eff.set(False)
    uranus_eff.set(False)
    neptune_eff.set(False)
    target.set(4)

    Button(root, text="Simulate", command=root.destroy).grid(row=6, column=0)

    root.mainloop()

    planets_sim = [mercury_sim.get(), venus_sim.get(), earth_sim.get(), mars_sim.get(), jupiter_sim.get(), saturn_sim.get(), uranus_sim.get(), neptune_sim.get()]
    planets_names = OrderedDict([(0,'Mercury'), (1,'Venus'), (2,'Earth'), (3,'Mars'), (4,'Jupiter'), (5,'Saturn'), (6,'Uranus'), (7,'Neptune')])
    for i,j in enumerate(planets_sim):
        if j == False:
            planets_names.pop(i)
    
    planets_eff = [mercury_eff.get(), venus_eff.get(), earth_eff.get(), mars_eff.get(), jupiter_eff.get(), saturn_eff.get(), uranus_eff.get(), neptune_eff.get()]
    planets_effect = []
    for i,j in enumerate(planets_eff):
        if j == True:
            planets_effect.append(i)
    
    time = (time_date.get(), time_month.get(), time_year.get())

    return (predict_trajectory.get(), crash_detect.get(), closest_approach.get(), to_scale.get(), N_years.get(), timestep.get(), framerate.get(), time, planets_names, planets_effect, target.get())
