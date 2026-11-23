"""Independent numerical checks of analytic predictions."""
import numpy as np
from model import problem, optimal_parameters, spectral_radius
from optimizers import optimize

for kappa in [1,10,100,1000]:
    h,x,q=problem(kappa)
    np.testing.assert_allclose(np.linalg.eigvalsh(h),[1,kappa],rtol=1e-12)
    ag,ah,b=optimal_parameters(1,kappa)
    np.testing.assert_allclose(spectral_radius(h,ag),(kappa-1)/(kappa+1),atol=1e-7)
    np.testing.assert_allclose(spectral_radius(h,ah,b),(np.sqrt(kappa)-1)/(np.sqrt(kappa)+1),atol=1e-7)
    r=optimize(h,x,ag,max_iter=50,stop=False)
    assert np.all(np.diff(r['loss'])<=1e-12)
    rotated=optimize(np.diag([1.,kappa]),np.ones(2),ah,b,max_iter=50,stop=False)
    actual=optimize(h,x,ah,b,max_iter=50,stop=False)
    np.testing.assert_allclose(actual['points'],rotated['points']@q.T,atol=1e-10)
for beta in [0,.5,.9,.99]:
    h,_,_=problem(100)
    assert spectral_radius(h,2*(1+beta)/100*.999,beta)<1
    assert spectral_radius(h,2*(1+beta)/100*1.001,beta)>1
r=optimize(np.eye(2),np.ones(2),1,.9,max_iter=2,stop=False)
np.testing.assert_allclose(r['relative'],[1,0,.81])
print('PASS: spectrum, optimal rates, GD monotonicity, rotation equivalence, stability boundary, counterexample')
