import matplotlib.pyplot as plt
import numpy as np
import random

def encrypt_message(message, shift):    # Encrypt the msg using CAESER CIPHER algorithm
    encrypted_message = ""
    for char in message:
        if char.isalpha():
            shift_base = 65 if char.isupper() else 97
            encrypted_message += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
            encrypted_message += char
    return encrypted_message

def decrypt_message(encrypted_message, shift):      # Decrypt msg using CAESER CIPHER 
    decrypted_message = ""
    for char in encrypted_message:
        if char.isalpha():
            shift_base = 65 if char.isupper() else 97
            decrypted_message += chr((ord(char) - shift_base - shift) % 26 + shift_base)
        else:
            decrypted_message += char
    return decrypted_message

def identify_jet_or_drone(decrypted_message, correct_message):      # Friendly Jet / Enemy Jet
    return "Friendly" if decrypted_message == correct_message else "Enemy"

def classify_object(reflectivity, material, geometry):
    if reflectivity < 0.2 and material == "composite" and geometry == "small":
        return "Drone"
    elif 0.2 <= reflectivity < 0.8 and material == "metal" and geometry == "large":
        return "Fighter Jet"
    elif reflectivity >= 0.8 and material == "metal" and geometry == "pointed":
        return "Missile"
    else:
        return "Unknown Object"

def plot_radar(friendly_jets, enemy_jets, object_results, radar_range_km, radar_position):
    fig, ax = plt.subplots(figsize=(12, 12))

    ax.plot(*radar_position, 'bo', markersize=15)

    radar_range = plt.Circle(radar_position, radar_range_km, color='blue', fill=False, linestyle='--', linewidth=2)
    ax.add_artist(radar_range)

    for idx, jet in enumerate(friendly_jets):
        x, y = jet['position']
        label = f"Friendly Jet {idx + 1}"
        ax.plot(x, y, 'go', markersize=8)  
        ax.text(x, y, label, fontsize=10, ha='right', color='green')

    for idx, jet in enumerate(enemy_jets):
        x, y = jet['position']
        label = f"Enemy Jet {idx + 1}"
        ax.plot(x, y, 'ro', markersize=8) 
        ax.text(x, y, label, fontsize=10, ha='right', color='red')

    for idx, obj in enumerate(object_results):
        x, y = obj['position']
        if obj['classification'] == 'Drone':
            ax.plot(x, y, 'ko', markersize=6)  
            ax.text(x, y, f"Drone {idx + 1}", fontsize=10, ha='right', color='black')
        elif obj['classification'] == 'Missile':
            ax.plot(x, y, 'yo', markersize=8)  
            ax.text(x, y, f"Missile {idx + 1}", fontsize=10, ha='right', color='orange')

    ax.set_title(f'Radar Detection (Range {radar_range_km} km)', fontsize=16, fontweight='bold')
    ax.set_xlim(-radar_range_km - 10, radar_range_km + 10)
    ax.set_ylim(-radar_range_km - 10, radar_range_km + 10)
    ax.set_aspect('equal')
    ax.set_xlabel('X-Coordinate (km)', fontsize=12)
    ax.set_ylabel('Y-Coordinate (km)', fontsize=12)
    plt.grid(True, linestyle='--', color='grey', alpha=0.7)

    legend_labels = {
        'Friendly Jet': 'go',
        'Enemy Jet': 'ro',
        'Drone': 'ko',
        'Missile': 'yo'
    }
    handles = [plt.Line2D([0], [0], marker=marker, color='w', markerfacecolor=color, markersize=8, linestyle='') for label, (color, marker) in legend_labels.items()]
    labels = list(legend_labels.keys())
    legend = ax.legend(handles, labels, loc='upper left', fontsize=12, title='Legend', bbox_to_anchor=(1, 1))
    legend.get_frame().set_facecolor('white')
    legend.get_frame().set_edgecolor('black')

    plt.show()

def radar_simulation():
    """
    Simulate the radar system and plot detection results.
    """
    radar_range_km = 40  # Radar's detection range (PRACTICAL SCENARIO TAKEN with radius as 40km)
    message = "THIS IS THE INDIAN SKIES, IDENTIFY YOURSELF OR WE WILL SHOT YOU DOWN RIGHT NOW"
    shift_key = 4  
    encrypted_message = encrypt_message(message, shift_key)
    print(f"Radar: Encrypted message sent -> {encrypted_message}\n")
    
    radar_position = (0, 0) 

    num_friendly_jets = random.randint(1, 5) 
    num_enemy_jets = random.randint(1, 5)

    friendly_jets = []
    enemy_jets = []

    for i in range(num_friendly_jets):
        shift = random.choice([4, 7, 9])  
        x, y = np.random.uniform(-radar_range_km, radar_range_km, 2)
        friendly_jets.append({"jet_id": i + 1, "shift_key": shift, "position": (x, y)})

    for i in range(num_enemy_jets):
        shift = random.choice([4, 7, 9])
        x, y = np.random.uniform(-radar_range_km, radar_range_km, 2)
        enemy_jets.append({"jet_id": i + 1, "shift_key": shift, "position": (x, y)})

    correct_message = message
    detected_friendly_jets = []
    detected_enemy_jets = []

    print("Jet Decryption Results:")
    for jet in friendly_jets + enemy_jets:
        decrypted_message = decrypt_message(encrypted_message, jet["shift_key"])
        status = identify_jet_or_drone(decrypted_message, correct_message)
        if np.linalg.norm(np.array(jet["position"]) - np.array(radar_position)) <= radar_range_km:
            if status == "Friendly":
                detected_friendly_jets.append({"jet_id": len(detected_friendly_jets) + 1, "position": jet["position"]})
            else:
                detected_enemy_jets.append({"jet_id": len(detected_enemy_jets) + 1, "position": jet["position"]})
        print(f"Jet {jet['jet_id']} decryption -> {decrypted_message}: {status}")

    num_drones = random.randint(1, 5)  
    num_missiles = random.randint(1, 5)  
    num_objects = num_drones + num_missiles

    objects_in_range = []
    has_drone = False
    has_missile = False

    for i in range(num_drones):
        x, y = np.random.uniform(-radar_range_km, radar_range_km, 2)
        reflectivity = np.random.uniform(0.1, 0.3)
        material = random.choice(["composite", "metal"])
        geometry = random.choice(["small", "large"])
        classification = classify_object(reflectivity, material, geometry)
        if classification == "Drone":
            has_drone = True
        if np.linalg.norm(np.array((x, y)) - np.array(radar_position)) <= radar_range_km:
            objects_in_range.append({"classification": "Drone", "position": (x, y)})

    for i in range(num_missiles):
        x, y = np.random.uniform(-radar_range_km, radar_range_km, 2)
        reflectivity = np.random.uniform(0.7, 1.0)
        material = random.choice(["composite", "metal"])
        geometry = random.choice(["small", "large", "pointed"])
        classification = classify_object(reflectivity, material, geometry)
        if classification == "Missile":
            has_missile = True
        if np.linalg.norm(np.array((x, y)) - np.array(radar_position)) <= radar_range_km:
            objects_in_range.append({"classification": "Missile", "position": (x, y)})

    if not has_drone:
        x, y = np.random.uniform(-radar_range_km, radar_range_km, 2)
        objects_in_range.append({"classification": "Drone", "position": (x, y)})
    if not has_missile:
        x, y = np.random.uniform(-radar_range_km, radar_range_km, 2)
        objects_in_range.append({"classification": "Missile", "position": (x, y)})

    print("\nDetected Objects in Range:")
    print(f"Friendly Jets: {len(detected_friendly_jets)}")
    print(f"Enemy Jets: {len(detected_enemy_jets)}")
    print(f"Drones: {sum(1 for obj in objects_in_range if obj['classification'] == 'Drone')}")
    print(f"Missiles: {sum(1 for obj in objects_in_range if obj['classification'] == 'Missile')}")

    plot_radar(detected_friendly_jets, detected_enemy_jets, objects_in_range, radar_range_km, radar_position)

radar_simulation()
