def planets_effect_check(planets_names, planets_effect):
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
    
    return planets_effect
