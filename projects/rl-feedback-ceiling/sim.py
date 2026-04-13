"""
Canonical simulation for rl-feedback-ceiling paper.
DGP: p0=0.3, mu1-mu0=1.5, sigma=1, kappa=1.5 (unless sweeping kappa)
Selection: P(sel|X,S) = expit(beta * f_theta(X) + kappa * S)
"""

import numpy as np
from scipy.special import expit, logit
from scipy.optimize import minimize

RNG = np.random.default_rng(42)

# DGP params
P0 = 0.3
MU0, MU1 = 0.0, 1.5
SIGMA = 1.0
KAPPA = 1.5
N = 200_000  # large enough for stable estimates


def sample_population(n, rng=RNG):
    S = rng.binomial(1, P0, size=n)
    mu = np.where(S == 1, MU1, MU0)
    X = rng.normal(mu, SIGMA, size=n)
    return S, X


def bayes_optimal_theta():
    """Closed-form Bayes optimal for Gaussian class-conditionals."""
    # theta1 = (mu1 - mu0) / sigma^2
    # theta0 = log(p0/(1-p0)) - theta1 * (mu0 + mu1) / 2
    theta1 = (MU1 - MU0) / SIGMA**2
    theta0 = np.log(P0 / (1 - P0)) - theta1 * (MU0 + MU1) / 2
    return theta0, theta1


def f_theta(X, theta0, theta1):
    return expit(theta0 + theta1 * X)


def nll_population(theta, S, X):
    """NLL on the full population."""
    p = f_theta(X, theta[0], theta[1])
    p = np.clip(p, 1e-9, 1 - 1e-9)
    return -np.mean(S * np.log(p) + (1 - S) * np.log(1 - p))


def run_beta(beta, kappa=KAPPA, n=N, rng=RNG):
    S, X = sample_population(n, rng)
    theta0_opt, theta1_opt = bayes_optimal_theta()
    f = f_theta(X, theta0_opt, theta1_opt)

    # Selection probabilities
    sel_prob = expit(beta * f + kappa * S)
    sel_mask = rng.binomial(1, sel_prob).astype(bool)

    S_sel = S[sel_mask]
    X_sel = X[sel_mask]

    # Train on selected data
    def nll_sel(theta):
        p = f_theta(X_sel, theta[0], theta[1])
        p = np.clip(p, 1e-9, 1 - 1e-9)
        return -np.mean(S_sel * np.log(p) + (1 - S_sel) * np.log(1 - p))

    # Init at Bayes optimal
    res = minimize(nll_sel, [theta0_opt, theta1_opt], method='L-BFGS-B')
    theta_hat = res.x

    # Population NLL at theta_hat
    pop_nll = nll_population(theta_hat, S, X)
    # Proxy NLL (NLL on selected)
    proxy_nll = nll_sel(theta_hat)

    # IPW NLL: estimate marginal propensity (marginalizing over S)
    # P(sel|X) = p0 * expit(beta*f + kappa) + (1-p0) * expit(beta*f)
    # Use true p0 and kappa for comparison (theoretical IPW), and
    # also estimated propensity (marginalizing over S, unknown kappa -> use marginal)
    # Estimated: can only observe (X, f) — estimate propensity by logistic regression on sel ~ f
    from sklearn.linear_model import LogisticRegression
    # Fit propensity on full population (sel_mask as outcome) using model score f as feature
    lr2 = LogisticRegression(max_iter=1000)
    lr2.fit(f.reshape(-1, 1), sel_mask.astype(int))
    p_sel_est = lr2.predict_proba(f.reshape(-1, 1))[:, 1]
    p_sel_est = np.clip(p_sel_est, 1e-3, 1 - 1e-3)

    # IPW NLL on selected sample, weighted by 1/p_sel
    p_sel_sel = p_sel_est[sel_mask]
    weights = 1.0 / p_sel_sel
    weights = weights / weights.mean()  # normalize

    def nll_ipw(theta):
        p = f_theta(X_sel, theta[0], theta[1])
        p = np.clip(p, 1e-9, 1 - 1e-9)
        nll_i = -(S_sel * np.log(p) + (1 - S_sel) * np.log(1 - p))
        return np.average(nll_i, weights=weights)

    res_ipw = minimize(nll_ipw, [theta0_opt, theta1_opt], method='L-BFGS-B')
    theta_ipw = res_ipw.x
    ipw_nll = nll_population(theta_ipw, S, X)

    # Effective sample size
    ess = (weights.sum())**2 / (weights**2).sum()
    n_sel = sel_mask.sum()

    return {
        'beta': beta,
        'theta0_hat': theta_hat[0],
        'theta1_hat': theta_hat[1],
        'theta0_opt': theta0_opt,
        'theta1_opt': theta1_opt,
        'pop_nll': pop_nll,
        'proxy_nll': proxy_nll,
        'ipw_nll': ipw_nll,
        'weights_min': weights.min(),
        'weights_max': weights.max(),
        'ess': ess,
        'n_sel': n_sel,
    }


def bayes_opt_pop_nll(n=N, rng=RNG):
    """Population NLL at the analytic Bayes-optimal theta (kappa=0 baseline)."""
    S, X = sample_population(n, rng)
    theta0_opt, theta1_opt = bayes_optimal_theta()
    return nll_population([theta0_opt, theta1_opt], S, X)


if __name__ == '__main__':
    theta0_opt, theta1_opt = bayes_optimal_theta()
    print(f"Bayes-optimal theta: theta0={theta0_opt:.4f}, theta1={theta1_opt:.4f}")

    bayes_nll = bayes_opt_pop_nll()
    print(f"Population NLL at Bayes-optimal theta: {bayes_nll:.4f}")
    print()

    betas = [0.0, 1.0, 2.0, 4.0]
    results = []
    for b in betas:
        r = run_beta(b)
        results.append(r)
        drift = r['pop_nll'] - bayes_nll
        print(f"beta={b:.1f}: theta1_hat={r['theta1_hat']:.4f}, "
              f"pop_nll={r['pop_nll']:.4f}, proxy_nll={r['proxy_nll']:.4f}, "
              f"ipw_nll={r['ipw_nll']:.4f}, drift={drift:+.4f}, "
              f"ess={r['ess']:.0f}/{r['n_sel']} w=[{r['weights_min']:.3f},{r['weights_max']:.3f}]")

    print()
    print("Table (for paper):")
    print(f"| beta | theta1_hat | theta0_hat | Pop NLL | Proxy NLL | IPW NLL | Drift |")
    print(f"|------|-----------|-----------|---------|-----------|---------|-------|")
    # beta=0 row: analytic baseline
    print(f"| 0.0  | {theta1_opt:.2f} (opt) | {theta0_opt:.2f} (opt) | {bayes_nll:.3f} | — | — | 0.000 |")
    for r in results[1:]:  # skip beta=0 sim, use analytic for that row
        drift = r['pop_nll'] - bayes_nll
        print(f"| {r['beta']:.1f}  | {r['theta1_hat']:.2f} | {r['theta0_hat']:.2f} | {r['pop_nll']:.3f} | {r['proxy_nll']:.3f} | {r['ipw_nll']:.3f} | {drift:+.4f} |")

    print()
    print("Kappa sweep (beta=2.0 fixed):")
    kappas = [0.0, 0.5, 1.0, 1.5, 2.0, 3.0]
    bayes_nll_ref = bayes_nll
    print(f"| kappa | theta1_hat | Pop NLL | Residual gap |")
    print(f"|-------|-----------|---------|--------------|")
    for k in kappas:
        r = run_beta(2.0, kappa=k)
        gap = r['pop_nll'] - bayes_nll_ref
        print(f"| {k:.1f}   | {r['theta1_hat']:.2f} | {r['pop_nll']:.3f} | {gap:+.4f} |")
