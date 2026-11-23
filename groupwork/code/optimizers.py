"""GD is the beta=0 specialization of the shared Heavy-ball recurrence."""
import numpy as np

def optimize(h, x0, alpha, beta=0.0, max_iter=10000, tol=1e-8, stop=True):
    x = np.array(x0, dtype=np.float64, copy=True)
    previous = x.copy()  # zero initial velocity
    points, losses = [x.copy()], [float(x @ h @ x / 2)]
    status = 'iteration_limit'
    for _ in range(max_iter):
        new = x - alpha * (h @ x) + beta * (x - previous)
        value = float(new @ h @ new / 2)
        points.append(new.copy()); losses.append(value)
        previous, x = x, new
        if not np.isfinite(value):
            status = 'nonfinite'; break
        if value / losses[0] > 1e100:
            status = 'growth_guard'; break
        if stop and value / losses[0] <= tol:
            status = 'tolerance_reached'; break
    loss = np.array(losses)
    return {'points': np.array(points), 'loss': loss, 'relative': loss/loss[0],
            'iterations': len(loss)-1, 'status': status,
            'increases': int(np.sum(np.diff(loss) > 1e-14 * loss[0]))}
