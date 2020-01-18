import time
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.animation import FuncAnimation
from nbody import Body, System, grav


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

jupiter_mass = 1.898e27 # kg
jupiter_distance = 779e9 # m
jupiter_speed = 13.1e3 # m/s


G = -6.67430e-11 # m^3kg^-1s^-2

s = System(bodies=[
    Body(mass=sun_mass, R=10, v_x=0, c='y'),
    Body(mass=earth_mass, x=0, y=-earth_distance, v_x=earth_speed, v_y=0, R=3, c='b'),
    Body(mass=mars_mass, x=0, y=-mars_distance, v_x=mars_speed, v_y=0, R=1, c='r'),
    Body(mass=jupiter_mass, x=0, y=-jupiter_distance, v_x=jupiter_speed, R=6, c='b'),
],
           G=G)
s.set_steps(60 * 60)
print(s)

fig, ax = plt.subplots(2, 2, figsize=(12, 8), constrained_layout=True)
ax_sun = ax[0][0]
ax_grav = ax[0][1]
ax_sun_xy = ax[1][0]
ax_grav_xy = ax[1][1]

ax_sun_xy.set_title('Earth around the Sun.')
ax_grav_xy.set_title('Gravity?')
sun_T = int(365)
sun_x, sun_y = np.ones(sun_T), np.ones(sun_T)
sun_time = np.linspace(0, sun_T, sun_T)

line_sun_x, = ax_sun_xy.plot(sun_time, sun_x)
line_sun_y, = ax_sun_xy.plot(sun_time, sun_y)


x, y = s.xy()
colors = [b.c for b in s.bodies]
line_sun = ax_sun.scatter(x, y, linewidths=[b.R for b in s.bodies], c=colors)
xlim = ylim = (-jupiter_distance*1.25, jupiter_distance*1.25)

xG, yG, gG = grav(s.bodies[1:], xlim, ylim, xpts=100, ypts=100, ret_xy=True)

quad_grav = ax_grav.pcolormesh(xG, yG, gG, cmap='hsv')

vF_sun = 2
ax_sun.set_xlim(xlim)#[-vF_sun * earth_distance, vF_sun * earth_distance])
ax_sun.set_ylim(ylim)#[-vF_sun * earth_distance, vF_sun * earth_distance])

ax_sun_xy.set_ylim([-vF_sun * earth_speed, vF_sun * earth_speed])


ax_sun.axis('off')
ax_grav.axis('off')
ax_sun_xy.axis('off')
ax_grav_xy.axis('off')




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

    sun_x[1:] = sun_x[:-1]; sun_x[0] = s.bodies[1].v_x
    line_sun_x.set_data(sun_time, sun_x)
    sun_y[1:] = sun_y[:-1]; sun_y[0] = s.bodies[1].v_y
    line_sun_y.set_data(sun_time, sun_y)
    
    xG, yG, gG = grav(s.bodies[1:], xlim, ylim, xpts=100, ypts=100, ret_xy=True)
    gG = gG[:-1, :-1]
    gG = gG.ravel()
    quad_grav.set_array(gG)

    time1 = time.time()
    fps = int(1 / (time1-time0))
    fig.suptitle(f'Time: {int(s.t/60/60/24)} days: fps: {fps}')
    time0 = time.time()

    return line_sun, line_sun_x, line_sun_y, quad_grav


anim = FuncAnimation(
    fig,
    animate,  #init_func=init,
    frames=frame_N,
    interval=interval)
plt.show()

#anim.save('10_years_sun_venus_earth_moon_mars80dpi.gif', dpi=80, writer='imagemagick')
#h = anim.to_html5_video()
#HTML(h)

