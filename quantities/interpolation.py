from sklearn.datasets import make_friedman2
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import DotProduct, WhiteKernel
# X, y = make_friedman2(n_samples=500, noise=0, random_state=0)
import numpy as np
X = np.array([1,2,3]).reshape(-1, 1)
y = np.array([3,5,7])
kernel = DotProduct() + WhiteKernel()
gpr = GaussianProcessRegressor(kernel=kernel, random_state=0).fit(X, y)
gpr.score(X, y)
X0 = np.array([1.2,2.3,3.4,4.5]).reshape(-1, 1)
gpr.predict(X0, return_std=True)

