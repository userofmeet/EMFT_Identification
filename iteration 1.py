import matplotlib.pyplot as plt
import numpy as np
import random

def calculate_radar_range():
    Pt = 1e6        # Transmitted power in watts
    Gt = 60         # Gain of transmitting antenna (dB)
    Gr = 60         # Gain of receiving antenna (dB)
    sigma = 1       # Radar cross-section (m^2)
    Pmin = 1e-9     # Minimum detectable power (watts)

    Gt_linear = 10 ** (Gt / 10)
    Gr_linear = 10 ** (Gr / 10)

    R = ((Pt * Gt_linear * Gr_linear * sigma) / ((4 * np.pi) ** 3 * Pmin)) ** (1 / 4)
    return R

def classify_object(reflectivity, material, geometry):
    if reflectivity > 0.8 and material == "metal":
        return "Missile"
    elif reflectivity > 0.5 and material == "composite":
        return "Drone"
    else:
        return "Unknown"

def plot_radar(friendly_jets, enemy_jets, object_results, radar_range_km, radar_position):
    fig, ax1 = plt.subplots(figsize=(10, 8))

    # Plot radar range and detected objects
    ax1.plot(*radar_position, 'bo', markersize=15, label='Radar Position')
    radar_range = plt.Circle(radar_position, radar_range_km, color='blue', fill=False, linestyle='--', linewidth=2)
    ax1.add_artist(radar_range)
    ax1.set_title(f'Radar Detection (Range {radar_range_km:.2f} km)', fontsize=16, fontweight='bold')
    ax1.set_xlim(-radar_range_km - 10, radar_range_km + 10)
    ax1.set_ylim(-radar_range_km - 10, radar_range_km + 10)
    ax1.set_aspect('equal')
    ax1.set_xlabel('X-Coordinate (km)', fontsize=12)
    ax1.set_ylabel('Y-Coordinate (km)', fontsize=12)
    ax1.grid(True, linestyle='--', color='grey', alpha=0.7)

    # Friendly jets
    for idx, jet in enumerate(friendly_jets):
        x, y = jet['position']
        distance = np.linalg.norm(np.array((x, y)) - np.array(radar_position))
        ax1.plot(x, y, 'go', markersize=8, label='Friendly Jet' if idx == 0 else "")
        ax1.text(x, y, f"Friendly Jet {idx + 1}\n{distance:.2f} km", fontsize=10, ha='right', color='green')

    # Enemy jets
    for idx, jet in enumerate(enemy_jets):
        x, y = jet['position']
        distance = np.linalg.norm(np.array((x, y)) - np.array(radar_position))
        ax1.plot(x, y, 'ro', markersize=8, label='Enemy Jet' if idx == 0 else "")
        ax1.text(x, y, f"Enemy Jet {idx + 1}\n{distance:.2f} km", fontsize=10, ha='right', color='red')

    # Drones and missiles
    drone_counter = 1
    missile_counter = 1
    for obj in object_results:
        x, y = obj['position']
        distance = np.linalg.norm(np.array((x, y)) - np.array(radar_position))
        if obj['classification'] == 'Drone':
            ax1.plot(x, y, 'ko', markersize=6, label='Drone' if drone_counter == 1 else "")
            ax1.text(x, y, f"Drone {drone_counter}\n{distance:.2f} km", fontsize=10, ha='right', color='black')
            drone_counter += 1
        elif obj['classification'] == 'Missile':
            ax1.plot(x, y, 'yo', markersize=8, label='Missile' if missile_counter == 1 else "")
            ax1.text(x, y, f"Missile {missile_counter}\n{distance:.2f} km", fontsize=10, ha='right', color='orange')
            missile_counter += 1

    # Adding a common legend outside the plot
    handles, labels = ax1.get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, 1.05), ncol=4, fontsize=12)

    plt.tight_layout()
    plt.show()

def radar_simulation():
    radar_range_km = 842.54  # Radar range is fixed at 842.54 km
    radar_position = (0, 0)

    num_friendly_jets = random.randint(1, 5)
    num_enemy_jets = random.randint(1, 5)

    friendly_jets = []
    enemy_jets = []

    # Generate friendly jets within radar range
    for _ in range(num_friendly_jets):
        angle = random.uniform(0, 2 * np.pi)
        radius = random.uniform(0, radar_range_km)
        x = radius * np.cos(angle)
        y = radius * np.sin(angle)
        friendly_jets.append({"position": (x, y)})

    # Generate enemy jets within radar range
    for _ in range(num_enemy_jets):
        angle = random.uniform(0, 2 * np.pi)
        radius = random.uniform(0, radar_range_km)
        x = radius * np.cos(angle)
        y = radius * np.sin(angle)
        enemy_jets.append({"position": (x, y)})

    num_drones = random.randint(5, 15)
    num_missiles = random.randint(5, 10)

    objects_in_range = []

    # Generate drones and missiles within radar range
    for _ in range(num_drones + num_missiles):
        angle = random.uniform(0, 2 * np.pi)
        radius = random.uniform(0, radar_range_km)
        x = radius * np.cos(angle)
        y = radius * np.sin(angle)
        reflectivity = random.uniform(0.5, 1.0)
        material = random.choice(["composite", "metal"])
        geometry = random.choice(["pointed", "large"])
        classification = classify_object(reflectivity, material, geometry)
        objects_in_range.append({"classification": classification, "position": (x, y)})

    print("\nDetected Objects in Range:")
    print(f"Friendly Jets: {len(friendly_jets)}")
    print(f"Enemy Jets: {len(enemy_jets)}")
    print(f"Drones: {sum(1 for obj in objects_in_range if obj['classification'] == 'Drone')}")
    print(f"Missiles: {sum(1 for obj in objects_in_range if obj['classification'] == 'Missile')}")

    plot_radar(friendly_jets, enemy_jets, objects_in_range, radar_range_km, radar_position)

radar_simulation()
