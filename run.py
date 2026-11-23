from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

out = Path(__file__).resolve().parent
H = np.diag([1., 10.])
fig, ax = plt.subplots(2, 3, figsize=(12, 7), constrained_layout=True)
grid = np.linspace(-3, 3, 201)
X, Y = np.meshgrid(grid, grid)
rows = []
groups = [[(.08,0),(.18,0),(.20,0),(.22,0)],
          [(.18,.3),(.18,.6),(.18,.9)],
          [(.28,.5),(.30,.5),(.32,.5)]]
for j, cases in enumerate(groups):
    ax[1,j].contour(X,Y,(X**2+10*Y**2)/2,levels=[.1,1,3,8,20,40], colors="0.8")
    for a,b in cases:
        prev = x = np.array([2.,1.])
        path = [x]
        for k in range(80):
            prev,x = x,x-a*(H@x)+b*(x-prev)
            path.append(x)
        p = np.array(path)
        loss = np.sum((p@H)*p,axis=1)/2
        rho = max(abs(r) for h in H.diagonal() for r in np.roots([1,a*h-1-b,b]))
        label = f"a={a}, b={b}"
        ax[0,j].semilogy(loss,label=label)
        ax[1,j].plot(*p[:13].T,".-",label=label)
        flips = np.sum(p[1:,1]*p[:-1,1]<0)
        rows.append(f"| {a:.2f} | {b:.1f} | {rho:.4f} | {loss[-1]:.3e} | {flips} |")
    ax[0,j].set(xlabel="Iteration",ylabel="Loss",title=["GD","Fixed learning rate","Fixed momentum"][j])
    ax[0,j].legend(fontsize=8)
    ax[1,j].set(xlabel="x",ylabel="y",xlim=(-3,3),ylim=(-3,3),aspect="equal")
fig.savefig(out/"experiment.png",dpi=160)
print("\n".join(rows))
