import numpy as np
import matplotlib.pyplot as plt

import os
os.makedirs("figures", exist_ok=True)

L = 1.0
N = 50
alpha = 1e-6 # thermal diffusivity(m^2/s),typical order for rock
r = 0.4 # a safe value from the stability condition(factor 0.4 < 0.5)
dx = L/N
dt = r*dx**2/alpha
n_steps = 12000

print("stability number r = ",r,"(must be<=0.5)")
print(f"each step is {dt:.0f} 秒，total simulated time is {n_steps*dt/86400:.1f} days")
# :.0f 不保留小数 ; :.1f 保留一位小数

x = np.linspace(0,L,N+1)
T = np.zeros(N+1)
T[0] = 100.0
T[-1] = 0.0

snapshots = {0.0: T.copy()} # 创建字典;T.copy()会创建一个独立副本，保留当时的温度状态
snapshots_steps = [200,600,1500,4000,n_steps-1]

for step in range(n_steps):
    T_new = T.copy()
    T_new[1:-1] = T[1:-1] + r*(T[2:]-2*T[1:-1]+T[:-2])
    T = T_new
    T[0] = 100.0
    T[-1] = 0.0
    if step in snapshots_steps:
        time_days = (step+1) * dt/86400
        snapshots[time_days] = T.copy()

plt.figure(figsize=(12,8))
for time_days,T_snap in snapshots.items(): # .items() 每次循环取出一个键值对
    plt.plot(x,T_snap,label=f"t= {time_days:.1f} days")
plt.xlabel("Position along core (m)")
plt.ylabel("Temperature (°C)")
plt.title("1D heat conduction: explicit finite difference")
plt.legend()
plt.savefig("figures/heat_conduction.png", dpi=200)
plt.show()

T_steady_analytical = 100 * (1 - x / L)

plt.figure(figsize=(12,8))
plt.plot(x, T, "o-", label="Numerical (final step)", markersize=3)
plt.plot(x, T_steady_analytical, "--", label="Analytical steady state")

plt.xlabel("Position (m)")
plt.ylabel("Temperature (°C)")
plt.legend()
plt.savefig("figures/verification.png", dpi=200)
plt.show()

max_error = np.max(np.abs(T - T_steady_analytical)) # abs 绝对值
print("最大偏差:", max_error, "°C")

# 故意违反稳定性条件
r2 = 0.6
dt_unstable = r2*dx**2/alpha

T2 = np.zeros(N+1)
T2[0] = 100.0
T2[-1] = 0.0

for step in range(200):
    T2_new = T2.copy()
    T2_new[1:-1] = T2[1:-1] + r2 * (T2[2:]-2*T2[1:-1]+T2[:-2])
    T2 = T2_new
    T2[0] = 100.0
    T2[-1] = 0.0

print("最大绝对值:", np.max(np.abs(T2)), "（物理上应该在 0 到 100 之间）")
plt.plot(x, T2)
plt.title(f"Unstable result (r = {r2:.2f} > 0.5)")
plt.xlabel("Position (m)")
plt.ylabel("Temperature")
plt.savefig("figures/instability.png", dpi=200)
plt.show()