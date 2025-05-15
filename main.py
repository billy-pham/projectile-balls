import numpy as np
import matplotlib.pyplot as plt

import matplotlib.patches as patches
import matplotlib.animation as animation 

#setting up the graph
max_radius = 10
fig = plt.figure(figsize=(8,5))
ax = fig.add_subplot(111,projection='3d') # 1 row, 1 column, 1 subplot 
ax.set_xlim(-max_radius, max_radius)
ax.set_ylim(-max_radius, max_radius)
ax.set_zlim(0,max_radius*2)
ax.patch.set_facecolor('black')
ax.set_facecolor('black')
ax.axis('off')

balls = 50

#balls shooting in all directions 
positions = np.zeros((balls,3))            #balls is the integer 50 (rows); 3 is for XYZ coordinates (columns)
random = np.random.default_rng()
radius = random.uniform(0,2*np.pi,balls)   #creates circle by picking random angles around vertical
vertical = np.random.uniform(-1, 1, balls) #picks random vertical position (how high)
angle = np.arccos(vertical)                #turns vertical position into angle  
speed = np.random.uniform(1, 4, balls)     #creates array for random speeds for balls between 1 and 4

#new array that copies 'positions' to hold directions and speeds for each ball
projectiles = np.zeros_like(positions)                       

# the colon ':' is balls; 0-2 are for XYZ coordinates
projectiles[:,0] = speed * np.sin(angle) * np.cos(radius)  
projectiles[:,1] = speed * np.sin(angle) * np.sin(radius)
projectiles[:,2] = speed * vertical

fading = np.ones(balls)
color = '#e2b9d0' 

#scatter is for plotting XYZ points
scatter = ax.scatter(positions[:,0], positions[:,1], positions[:,2], s=40, c=color)

gravity = 0.02
fade_rate = 0.02

def update(frame):
    global positions, balls, fading

    #decreases Z value for balls - gravity pulling ball downward
    projectiles[:,2] -= gravity

    #updates position for projectiles
    positions += projectiles

    #each ball's opacity is reduced over time and value is limited between 0 and 1
    fading[:] = np.clip(fading - fade_rate, 0, 1)

    #reset balls that fade or hit the ground 
    for i in range(balls):
        if fading[i] <=0 or positions[i,2] <=0:
            positions[i] = 0 
            radius_i = np.random.uniform(0, 2*np.pi)
            vertical_i = np.random.uniform(-1, 1)
            angle_i=np.arccos(vertical_i)
            speed_i=np.random.uniform(1,4)
            projectiles[i,0] = speed_i * np.sin(angle_i) * np.cos(radius_i)
            projectiles[i,1] = speed_i * np.sin(angle_i) * np.sin(radius_i)
            projectiles[i,2] = speed_i * vertical_i
            fading[i] = 1   

    #plot updates with new positions and opacity
    scatter._offsets3d = (positions[:,0], positions[:,1], positions[:,2])
    scatter.set_alpha(fading)
    return scatter,


animate = animation.FuncAnimation(fig, update, frames=100, interval=30, blit=False)
plt.show()