from dataclasses import dataclass, field
from typing import List

import matplotlib.pyplot as plt
import numpy as np
import sympy as sp


@dataclass
class Simulation():
    t: float = 0.0
    step: float = 1.0

    def take_step(self):
        NotImplemented
s = Simulation()
s.take_step()


@dataclass
class Body(Simulation):
    x: float = 0.0
    y: float = 0.0
    R: float = 1.0
    mass: float = 1.0
    v_x: float = 0.0
    v_y: float = 0.0
    F_x: float = 0.0
    F_y: float = 0.0
    c: str = 'b'

    def take_step(self):
        self.x = self.x + self.step * self.v_x + (
            0.5 * self.F_x / self.mass) * np.power(self.step, 2)
        self.y = self.y + self.step * self.v_y + (
            0.5 * self.F_y / self.mass) * np.power(self.step, 2)
        self.v_x = (self.F_x / self.mass) * self.step + self.v_x
        self.v_y = (self.F_y / self.mass) * self.step + self.v_y
        self.t += self.step
        
    #@property
    def distance(self, other):
        return np.sqrt(np.power(self.x - other.x, 2) + np.power(self.y - other.y, 2))
    
    def unit_xy(self, other):
        x = other.x - self.x
        y = other.y - self.y
        mag = np.sqrt(np.power(x, 2) + np.power(y, 2))
        return x / mag, y / mag


@dataclass
class System(Simulation):
    bodies: List[Body] = field(default_factory=list)
    t: float = 0.0
    G: float = 1.0

    def plot(self, xlim=[None, None], ylim=[None, None]):
        fig, ax = plt.subplots(1, 1)
        ax.scatter([b.x for b in self.bodies], [b.y for b in self.bodies],
                   linewidths=[b.R for b in self.bodies])
        ax.set_xlim(xlim[0], xlim[1])
        ax.set_ylim(ylim[0], ylim[1])
        fig.show()

    def take_step(self):
        for b in self.bodies:
            F_x = 0.0
            F_y = 0.0
            for other in self.bodies:
                if other is not b:
                    ux, uy = b.unit_xy(other)
                    F = -self.G * (b.mass * other.mass) / np.power(b.distance(other), 2)
                    F_x += F * ux
                    F_y += F * uy
            b.F_x, b.F_y = F_x, F_y
        for b in self.bodies:
            b.take_step()
        self.t = self.t + self.step
    
    def set_steps(self, step=None):
        if step:
            self.step = step
        for b in self.bodies:
            b.step = self.step

    def xy(self):
        return [b.x for b in self.bodies], [b.y for b in self.bodies]

def dist(x,y):   
    return numpy.sqrt(numpy.sum((x-y)**2))

def grav1(body, xm, ym, G=6.67430e-11, c=3.0e8):
    xb, yb, m = body.x, body.y, body.mass
    r = np.sqrt(np.power(xm-xb, 2) + np.power(ym-yb, 2))
    g = (1 / c) * np.sqrt(2*G*m/r)
    return g

def grav(bodies, xlim, ylim, xpts=100, ypts=100, ret_xy=False):
    x = np.linspace(xlim[0], xlim[1], xpts)
    y = np.linspace(ylim[0], ylim[1], ypts)
    xm, ym = np.meshgrid(x, y)
    g = np.zeros_like(xm)
    for body in bodies:
        g += grav1(body, xm, ym)
    if ret_xy:
        return xm, ym, g
    return g