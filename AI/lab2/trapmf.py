import skfuzzy as fuzz
from skfuzzy import control as ctrl
import numpy as np
import matplotlib.pyplot as plt
import time

my = ctrl.Antecedent(np.arange(0, 1.01, 0.01), "my")
mx = ctrl.Antecedent(np.arange(0, 1.01, 0.01), "mx")
mf = ctrl.Consequent(np.arange(0.8, 1.9, 0.01), "mf")


mx["mx1"] = fuzz.trapmf(mx.universe, [-0.2, 0, 0.1,  0.2])
mx["mx2"] = fuzz.trapmf(mx.universe, [0, 0.2, 0.3,  0.4])
mx["mx3"] = fuzz.trapmf(mx.universe, [0.2, 0.4, 0.5,  0.6])
mx["mx4"] = fuzz.trapmf(mx.universe, [0.4, 0.6,0.7, 0.8])
mx["mx5"] = fuzz.trapmf(mx.universe, [0.6, 0.8,0.9, 1.0])
mx["mx6"] = fuzz.trapmf(mx.universe, [0.8, 1.0,1.1, 1.2])

my["my1"] = fuzz.trapmf(my.universe, [-0.2, 0, 0.1,  0.2])
my["my2"] = fuzz.trapmf(my.universe, [0, 0.2, 0.3,  0.4])
my["my3"] = fuzz.trapmf(my.universe, [0.2, 0.4, 0.5,  0.6])
my["my4"] = fuzz.trapmf(my.universe, [0.4, 0.6,0.7, 0.8])
my["my5"] = fuzz.trapmf(my.universe, [0.6, 0.8,0.9, 1.0])
my["my6"] = fuzz.trapmf(my.universe, [0.8, 1.0,1.1, 1.2])

for i in range(9):
    mf[f"mf{i+1}"] = fuzz.trapmf(mf.universe, [0.9 + (0.11 * (i-1)), 0.9 + 0.11 * (i-0.2), 0.9 + 0.11 * (i+0.2), 0.9 + (0.11 * (i+1))])

rule_mf1 = ctrl.Rule(antecedent=(mx["mx1"] & my["my5"] |
                                 mx["mx1"] & my["my6"]),
                                 consequent=mf["mf1"], label = 'rule mf1')
rule_mf2 = ctrl.Rule(antecedent=(mx["mx1"] & my["my1"]|
                                 mx["mx1"] & my["my2"]|
                                 mx["mx1"] & my["my3"]|
                                 mx["mx1"] & my["my4"]),
                     consequent=mf["mf2"], label= "rule mf2")

rule_mf3 = ctrl.Rule(antecedent=(mx["mx2"] & my["my4"]|
                                 mx["mx2"] & my["my5"]|
                                 mx["mx2"] & my["my6"]),
                     consequent = mf["mf3"], label = "rule mf3")

rule_mf4 = ctrl.Rule(antecedent=(mx["mx3"] & my["my6"] |
                                 mx["mx2"] & my["my1"] |
                                 mx["mx2"] & my["my2"] |
                                 mx["mx2"] & my["my3"]),
                     consequent=mf["mf4"], label="rule mf4")

rule_mf5 = ctrl.Rule(antecedent=(mx["mx3"] & my["my1"] |
                                 mx["mx3"] & my["my2"] |
                                 mx["mx3"] & my["my3"] |
                                 mx["mx3"] & my["my4"] |
                                 mx["mx3"] & my["my5"]),
                     consequent=mf["mf5"], label= "rule mf5")

rule_mf6 = ctrl.Rule(antecedent=(mx["mx4"] & my["my5"] |
                                 mx["mx4"] & my["my6"]),
                     consequent=mf["mf6"], label= "rule mf6")

rule_mf7 = ctrl.Rule(antecedent=(mx["mx4"] & my["my1"] |
                                 mx["mx4"] & my["my2"] |
                                 mx["mx4"] & my["my3"] |
                                 mx["mx4"] & my["my4"] |
                                 mx["mx5"] & my["my6"]),
                     consequent=mf["mf7"], label= "rule mf7")

rule_mf8 = ctrl.Rule(antecedent=(mx["mx5"] & my["my1"] |
                                 mx["mx5"] & my["my2"] |
                                 mx["mx5"] & my["my3"] |
                                 mx["mx5"] & my["my4"] |
                                 mx["mx5"] & my["my5"] |
                                 mx["mx6"] & my["my6"]),
                     consequent=mf["mf8"], label= "rule mf8")

rule_mf9 = ctrl.Rule(antecedent=(mx["mx6"] & my["my1"] |
                                 mx["mx6"] & my["my2"] |
                                 mx["mx6"] & my["my3"] |
                                 mx["mx6"] & my["my4"] |
                                 mx["mx6"] & my["my5"]),
                     consequent=mf["mf9"], label= "rule mf9")

system = ctrl.ControlSystem(rules=[rule_mf1,rule_mf2,rule_mf3,rule_mf4,rule_mf5, rule_mf6, rule_mf7, rule_mf8, rule_mf9])

my.view()
time.sleep(5)
mx.view()
time.sleep(5)
mf.view()
time.sleep(5)
plt.show()

sim = ctrl.ControlSystemSimulation(system)
upsampled = [0, 0.2, 0.4, 0.6, 0.8, 1]

x, y = np.meshgrid(upsampled, upsampled)
z = np.zeros_like(x)


for i in range(len(upsampled)):
    for j in range(len(upsampled)):
        # print(x[i, j], y[i, j], end=' ')
        sim.input['mx'] = x[i, j]
        sim.input['my'] = y[i, j]
        sim.compute()
        z[i, j] = sim.output['mf']
        # print(z[i, j])


fig = plt.figure(figsize=(9, 9))
ax = fig.add_subplot(111, projection='3d')

surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap='viridis', linewidth=0.4, antialiased=True)

cset = ax.contourf(x, y, z, zdir='z', offset=-2.5, cmap='viridis', alpha=0.5)
cset = ax.contourf(x, y, z, zdir='x', offset=3, cmap='viridis', alpha=0.5)
cset = ax.contourf(x, y, z, zdir='y', offset=3, cmap='viridis', alpha=0.5)

ax.view_init(30, 200)


plt.show()
x_y = np.arange(0, 1.2, 0.2)
z_2d = np.zeros_like(x_y)
x_g = np.arange(0, 1, 0.05)

z_r = np.sin(x_y) + np.cos(x_y / 2)
z_g = np.sin(x_g) + np.cos(x_g / 2)

for i in range(len(x_y)):
    sim.input['mx'] = x_y[i]
    sim.input['my'] = x_y[i]
    sim.compute()
    z_2d[i] = sim.output['mf']


e = abs(z_r - z) / z_r
print(f"Error = {round(np.mean(e) * 100, 3)} %")

plt.plot(x_y, z_2d)
plt.plot(x_g, z_g)
plt.title("Порівняння моделі побудованою за доп. trapmf та оригінальної")
plt.xlabel(f"Error = {round(np.mean(e) * 100, 3)} %")
plt.ylabel("mf")
plt.show()
