import time
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.animation import FuncAnimation
from nbody import Body, System


earth_speed = 29.78e3 # m/s
earth_distance = 149.6e9 # m
earth_mass = 5.972e24 # kg

sun_mass = 1.989e30 # kg

moon_mass = 7.347e22 # kg
moon_distance_to_earth = 3.844e8
moon_distance = -moon_distance_to_earth + earth_distance # m
moon_speed = 1.022e3 + earth_speed # m/s

venus_mass = 4.867e24 # kg
venus_distance = 108e9 # m
venus_speed = 35.02e3 # m/s

mars_mass = 6.417e23 # kg
mars_distance = 230e9 #m
mars_speed = 24.0e3 #m/s

mercury_mass = 3.30e23 # kg
mercury_distance = 55e9 # m, big guess due to eccentricity
mercury_speed = 48e3 # m/s


G = -6.67430e-11 # m^3kg^-1s^-2

s = System(bodies=[
    Body(mass=sun_mass, R=10, v_x=0, c='y'),
    Body(mass=earth_mass, x=0, y=-earth_distance, v_x=earth_speed, v_y=0, R=3, c='b'),
    Body(mass=moon_mass, x=0, y=-moon_distance, v_x=moon_speed, v_y=0, R=1, c='gray'),
    Body(mass=venus_mass, x=0, y=-venus_distance, v_x=venus_speed, v_y=0, R=2, c='orange'),
    Body(mass=mars_mass, x=0, y=-mars_distance, v_x=mars_speed, v_y=0, R=1, c='r'),
    Body(mass=mercury_mass, x=0, y=-mercury_distance, v_x=mercury_speed, v_y=0, R=1, c='r'),
],
           G=G)
s.set_steps(60 * 60)
print(s)

fig, ax = plt.subplots(2, 2, figsize=(12, 8), constrained_layout=True)
ax_sun = ax[0][0]
ax_earth = ax[0][1]
ax_sun_xy = ax[1][0]
ax_earth_xy = ax[1][1]

ax_sun_xy.set_title('Earth around the Sun.')
ax_earth_xy.set_title('The Moon around the Earth.')
sun_T = int(365)
sun_x, sun_y = np.ones(sun_T), np.ones(sun_T)
sun_time = np.linspace(0, sun_T, sun_T)
earth_T = sun_T
earth_xP, earth_yP = np.ones(earth_T), np.ones(earth_T)
earth_time = np.linspace(0, earth_T, earth_T)

line_sun_x, = ax_sun_xy.plot(sun_time, sun_x)
line_sun_y, = ax_sun_xy.plot(sun_time, sun_y)

line_earth_x, = ax_earth_xy.plot(earth_time, earth_xP)
line_earth_y, = ax_earth_xy.plot(earth_time, earth_yP)


x, y = s.xy()
colors = [b.c for b in s.bodies]
line_sun = ax_sun.scatter(x, y, linewidths=[b.R for b in s.bodies], c=colors)

earth_x, earth_y = s.bodies[1].x, s.bodies[1].y
x_new = [xi - earth_x for xi in x]
y_new = [yi - earth_y for yi in y]
print(x_new)
print(y_new)

line_earth = ax_earth.scatter(x_new, y_new, linewidths=[b.R for b in s.bodies], c=colors)

vF_sun = 2
ax_sun.set_xlim([-vF_sun * earth_distance, vF_sun * earth_distance])
ax_sun.set_ylim([-vF_sun * earth_distance, vF_sun * earth_distance])

vF_earth = 4
ax_earth.set_xlim([-vF_earth * moon_distance_to_earth, vF_earth * moon_distance_to_earth])
ax_earth.set_ylim([-vF_earth * moon_distance_to_earth, vF_earth * moon_distance_to_earth])

ax_sun_xy.set_ylim([-vF_sun * earth_speed, vF_sun * earth_speed])
ax_earth_xy.set_ylim([-vF_earth * moon_speed, vF_earth * moon_speed])


ax_sun.axis('off')
ax_earth.axis('off')
ax_sun_xy.axis('off')
ax_earth_xy.axis('off')




interval = 1#75 / (10 / 2)  # milliseconds
T = 2000  # milliseconds
frame_N = 365*1#int(T / interval)
print(f'{frame_N} frames, {interval} interval')


fig.suptitle(f'Time: {int(s.t/60/60/24)} days: fps: ')
time0 = time.time()
def animate(i):
    global time0, time1
    for _ in range(24):
        s.take_step()
    x, y = s.xy()
    line_sun.set_offsets(np.transpose([x, y]))
    earth_x, earth_y = s.bodies[1].x, s.bodies[1].y
    x_new = [xi - earth_x for xi in x]
    y_new = [yi - earth_y for yi in y]
    line_earth.set_offsets(np.transpose([x_new, y_new]))
    
    sun_x[1:] = sun_x[:-1]; sun_x[0] = s.bodies[1].v_x
    line_sun_x.set_data(sun_time, sun_x)
    sun_y[1:] = sun_y[:-1]; sun_y[0] = s.bodies[1].v_y
    line_sun_y.set_data(sun_time, sun_y)
    
    earth_xP[1:] = earth_xP[:-1];earth_xP[0] = s.bodies[2].v_x
    line_earth_x.set_data(earth_time, earth_xP)
    earth_yP[1:] = earth_yP[:-1]; earth_yP[0] = s.bodies[2].v_y
    line_earth_y.set_data(earth_time, earth_yP)

    time1 = time.time()
    fps = int(1 / (time1-time0))
    fig.suptitle(f'Time: {int(s.t/60/60/24)} days: fps: {fps}')
    time0 = time.time()

    return line_sun, line_earth, line_sun_x, line_sun_y, line_earth_x, line_earth_y,


anim = FuncAnimation(
    fig,
    animate,  #init_func=init,
    frames=frame_N,
    interval=interval)
plt.show()

#anim.save('10_years_sun_venus_earth_moon_mars80dpi.gif', dpi=80, writer='imagemagick')
#h = anim.to_html5_video()
#HTML(h)

