class Armoury:
    def __init__(self):
        # Initialize attributes for Trops, Powers, and Beasts
        self.trops = {"Shinobi": 0, "Wizard": 0, "Sensei": 0}
        self.powers = {"Fire": 0, "Ice": 0, "Lightning": 0}
        self.beasts = {"Dragon": 0, "Phoenix": 0, "Tiger": 0}

def display_armoury(armoury):
    """Displays the current state of the Armoury."""
    print("Your Armoury")
    print("Trops:")
    for trop, count in armoury.trops.items():
        print(f"{trop} = {count}")
    
    print("\nPowers:")
    for power, count in armoury.powers.items():
        print(f"{power} = {count}")
    
    print("\nBeasts:")
    for beast, count in armoury.beasts.items():
        print(f"{beast} = {count}")


    # Create an instance of Armoury
    my_armoury = Armoury()
    
    # Modify some values
    my_armoury.trops["Shinobi"] = 5
    my_armoury.powers["Fire"] = 10
    my_armoury.beasts["Dragon"] = 3
    
    # Display the armoury
    display_armoury(my_armoury)
