"""Run from any directory: python path/to/code/experiments.py."""
from pathlib import Path
import csv, json, platform
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from model import problem, optimal_parameters, spectral_radius
from optimizers import optimize

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / 'figures'; DATA = ROOT / 'data'
FIG.mkdir(exist_ok=True); DATA.mkdir(exist_ok=True)
plt.rcParams.update({'figure.dpi': 140, 'font.size': 10, 'axes.grid': True})

def save(fig, name):
    fig.tight_layout(); fig.savefig(FIG / (name+'.png')); plt.close(fig)

def export_trace(name, result):
    np.savetxt(DATA/(name+'.csv'), np.column_stack((np.arange(len(result['loss'])),
        result['points'], result['loss'], result['relative'])), delimiter=',',
        header='iteration,x1,x2,loss,relative_loss', comments='')

def main():
    rows=[]
    fig, axes=plt.subplots(2,2,figsize=(10,7))
    for ax,kappa in zip(axes.flat,[1,10,100,1000]):
        h,x0,_=problem(kappa); ag,ah,b=optimal_parameters(1,kappa)
        for method,alpha,beta in [('GD',ag,0),('HB',ah,b)]:
            r=optimize(h,x0,alpha,beta)
            rows.append(dict(kappa=kappa,method=method,alpha=alpha,beta=beta,
                rho=spectral_radius(h,alpha,beta),iterations=r['iterations'],
                loss_increases=r['increases'],final_relative=r['relative'][-1],status=r['status']))
            ax.semilogy(np.maximum(r['relative'],1e-30),label=method)
            export_trace(f'condition_{kappa}_{method}',r)
        ax.set(title=f'Condition number = {kappa}',xlabel='Iteration',ylabel='Relative loss')
        ax.legend(); ax.axhline(1e-8,color='gray',ls=':')
    save(fig,'condition_loss')
    with (DATA/'summary.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=rows[0]); w.writeheader(); w.writerows(rows)

    h,x0,_=problem(100); ag,ah,b=optimal_parameters(1,100)
    fig,axes=plt.subplots(1,2,figsize=(10,4))
    rr=[optimize(h,x0,ag,max_iter=60,stop=False), optimize(h,x0,ah,b,max_iter=60,stop=False)]
    extent=max(np.max(np.abs(r['points'])) for r in rr)*1.1
    xx,yy=np.meshgrid(np.linspace(-extent,extent,300),np.linspace(-extent,extent,300))
    zz=.5*(h[0,0]*xx**2+2*h[0,1]*xx*yy+h[1,1]*yy**2)
    for ax,r,label in zip(axes,rr,['GD','HB']):
        ax.contour(xx,yy,zz,levels=np.geomspace(.1,zz.max(),14),linewidths=.6)
        ax.plot(*r['points'].T,'o-',ms=2,lw=.8); ax.plot(0,0,'r*',ms=10)
        ax.set(title=label+' (first 60 updates)',xlabel='x1',ylabel='x2',aspect='equal')
        export_trace('path_'+label,r)
    save(fig,'paths')

    a=np.linspace(.005,4.2,421); bs=np.linspace(0,.99,199)
    aa,bb=np.meshgrid(a,bs); radius=np.zeros_like(aa)
    for lam in [1,100]:
        t=1+bb-aa*lam/100; d=np.sqrt((t*t-4*bb).astype(complex))
        radius=np.maximum(radius,np.maximum(abs((t+d)/2),abs((t-d)/2)))
    np.savez(DATA/'stability_grid.npz',alpha_L=a,beta=bs,rho=radius)
    fig,ax=plt.subplots(figsize=(7,4))
    im=ax.pcolormesh(aa,bb,radius,shading='auto',vmin=.7,vmax=1.3,cmap='coolwarm')
    ax.plot(2*(1+bs),bs,'k--',label='alpha L = 2(1+beta)')
    ax.scatter([ah*100],[b],marker='*',s=100,color='yellow',edgecolors='k',label='Optimal HB')
    ax.set(xlabel='alpha L',ylabel='beta',title='Spectral radius, condition number = 100')
    ax.legend(); fig.colorbar(im,ax=ax,label='Spectral radius'); save(fig,'stability')

    fig,axes=plt.subplots(1,2,figsize=(10,4)); parameter_rows=[]
    for beta in [0,.5,.9,.99]:
        r=optimize(h,x0,.01,beta,max_iter=300,stop=False)
        axes[0].semilogy(np.maximum(r['relative'],1e-30),label=f'beta={beta}')
        parameter_rows.append(dict(alpha=.01,beta=beta,rho=spectral_radius(h,.01,beta),
            relative_at_300=r['relative'][-1],increases=r['increases']))
        export_trace('beta_'+str(beta),r)
    for label,alpha in [('stable',.037),('boundary',.038),('unstable',.039)]:
        r=optimize(h,x0,alpha,.9,max_iter=150,stop=False)
        axes[1].semilogy(np.maximum(r['relative'],1e-30),label=f'{label}: alpha={alpha}')
        export_trace('boundary_'+label,r)
    for ax in axes: ax.set(xlabel='Iteration',ylabel='Relative loss'); ax.legend()
    axes[0].set_title('Fixed alpha=0.01: momentum sweep')
    axes[1].set_title('Fixed beta=0.9: stability boundary')
    save(fig,'parameters')
    (DATA/'parameter_summary.json').write_text(json.dumps(parameter_rows,indent=2),encoding='utf-8')

    fig,ax=plt.subplots(figsize=(6,3))
    for label,beta in [('GD',0),('HB',.9)]:
        r=optimize(np.eye(2),np.ones(2),1,beta,max_iter=25,stop=False)
        ax.plot(r['relative'],'o-',ms=3,label=label); export_trace('counterexample_'+label,r)
    ax.set(xlabel='Iteration',ylabel='Relative loss',title='H=I, alpha=1: momentum can leave the minimizer')
    ax.legend(); save(fig,'counterexample')
    metadata=dict(python=platform.python_version(),numpy=np.__version__,matplotlib=matplotlib.__version__,
                  dtype='float64',theta='pi/6',initial_eigen_coordinates=[1,1],tol=1e-8,max_iter=10000,
                  randomness='none',loss_increase_threshold='1e-14 * initial loss')
    (DATA/'environment.json').write_text(json.dumps(metadata,indent=2),encoding='utf-8')
    print(json.dumps(rows,indent=2)); print(json.dumps(parameter_rows,indent=2))

if __name__=='__main__': main()
