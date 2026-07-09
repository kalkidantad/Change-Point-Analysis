"""Run change point analysis and export results."""

import json
import sys
from pathlib import Path

import arviz as az
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.change_point_model import (
    associate_change_point_with_events,
    fit_change_point_model,
    price_level_impact,
)
from src.data_loader import load_brent_prices, load_events, compute_log_returns

OUTPUT_DIR = PROJECT_ROOT / "outputs"
FIGURES_DIR = PROJECT_ROOT / "figures"


def plot_tau_posterior(result, title: str, filename: str) -> None:
    tau_samples = result.trace.posterior["tau"].values.flatten()
    tau_dates = result.dates[tau_samples.astype(int)]

    fig, axes = plt.subplots(1, 2, figsize=(14, 4))

    axes[0].hist(tau_samples, bins=50, color="#3498db", edgecolor="white")
    axes[0].axvline(result.tau_summary["tau_median_index"], color="red", linestyle="--", label="Median")
    axes[0].set_title("Posterior: Switch Point Index (τ)")
    axes[0].set_xlabel("Index")
    axes[0].legend()

    axes[1].hist(tau_dates, bins=50, color="#2ecc71", edgecolor="white")
    axes[1].axvline(pd.Timestamp(result.tau_summary["tau_median_date"]), color="red", linestyle="--", label="Median date")
    axes[1].set_title("Posterior: Switch Point Date")
    axes[1].xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    axes[1].tick_params(axis="x", rotation=45)
    axes[1].legend()

    fig.suptitle(title, fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / filename, dpi=150)
    plt.close()


def plot_parameter_posteriors(result, title: str, filename: str) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    params = ["mu_1", "mu_2", "sigma"]
    colors = ["#3498db", "#e74c3c", "#95a5a6"]

    for ax, param, color in zip(axes, params, colors):
        samples = result.trace.posterior[param].values.flatten()
        ax.hist(samples, bins=40, color=color, edgecolor="white", alpha=0.85)
        ax.axvline(np.mean(samples), color="black", linestyle="--", linewidth=1)
        ax.set_title(f"Posterior: {param}")

    fig.suptitle(title, fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / filename, dpi=150)
    plt.close()


def plot_trace(result, filename: str) -> None:
    """Plot MCMC trace diagnostics using matplotlib."""
    fig, axes = plt.subplots(4, 2, figsize=(12, 10))
    params = ["tau", "mu_1", "mu_2", "sigma"]
    n_chains = int(result.trace.posterior.sizes.get("chain", 1))

    for row, param in enumerate(params):
        samples = result.trace.posterior[param].values
        for chain_idx in range(n_chains):
            chain = samples[chain_idx].flatten()
            axes[row, 0].plot(chain, alpha=0.6, linewidth=0.5)
        axes[row, 0].set_ylabel(param)
        if row == 0:
            axes[row, 0].set_title("Trace")
        if row == 3:
            axes[row, 0].set_xlabel("Draw")

        combined = samples.flatten()
        axes[row, 1].hist(combined, bins=40, color="#3498db", edgecolor="white", alpha=0.85)
        if row == 0:
            axes[row, 1].set_title("Posterior")
        if row == 3:
            axes[row, 1].set_xlabel("Value")

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / filename, dpi=120, bbox_inches="tight")
    plt.close()


def run_analysis(
    name: str,
    returns: pd.Series,
    prices: pd.DataFrame,
    events: pd.DataFrame,
    draws: int = 1500,
    tune: int = 1000,
) -> dict:
    print(f"\n=== Running: {name} ({len(returns)} obs) ===")
    result = fit_change_point_model(returns, draws=draws, tune=tune, chains=2)

    print(result.summary)
    print(f"Change point (median): {result.tau_summary['tau_median_date']}")
    print(f"94% HDI: {result.tau_summary['tau_hdi_lower_date']} – {result.tau_summary['tau_hdi_upper_date']}")
    print(f"P(μ₂ > μ₁): {result.impact_summary['prob_mu2_greater_mu1']:.3f}")

    associations = associate_change_point_with_events(result, events)
    price_impact = price_level_impact(prices, result)

    plot_tau_posterior(result, f"Change Point Posterior — {name}", f"cp_tau_{name}.png")
    plot_parameter_posteriors(result, f"Parameter Posteriors — {name}", f"cp_params_{name}.png")
    plot_trace(result, f"cp_trace_{name}.png")

    return {
        "name": name,
        "n_observations": len(returns),
        "start_date": str(returns.index.min().date()),
        "end_date": str(returns.index.max().date()),
        "convergence": result.summary[["r_hat", "ess_bulk"]].to_dict(),
        "tau_summary": result.tau_summary,
        "impact_summary": result.impact_summary,
        "price_impact": price_impact,
        "top_event_associations": associations.head(5).to_dict(orient="records"),
    }


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    FIGURES_DIR.mkdir(exist_ok=True)

    prices = load_brent_prices()
    events = load_events()
    returns = compute_log_returns(prices)

    # Period-focused analyses with windows aligned to known regime shifts
    analyses = [
        ("covid_2020", returns["2020-01-01":"2020-12-31"], prices["2020-01-01":"2020-12-31"], 2000, 1500),
        ("opec_price_war", returns["2014-06-01":"2016-06-30"], prices["2014-06-01":"2016-06-30"], 2000, 1500),
        ("financial_crisis", returns["2008-01-01":"2009-06-30"], prices["2008-01-01":"2009-06-30"], 2000, 1500),
        ("ukraine_war", returns["2022-01-01":"2022-09-30"], prices["2022-01-01":"2022-09-30"], 2000, 1500),
        ("gulf_war_era", returns["1990-06-01":"1991-03-31"], prices["1990-06-01":"1991-03-31"], 2000, 1500),
    ]

    all_results = []
    for name, ret, pr, draws, tune in analyses:
        if len(ret) < 100:
            continue
        all_results.append(run_analysis(name, ret, pr, events, draws=draws, tune=tune))

    # Export for dashboard
    results_path = OUTPUT_DIR / "change_point_results.json"
    with open(results_path, "w") as f:
        json.dump(all_results, f, indent=2, default=str)

    # Flat association table
    rows = []
    for r in all_results:
        for ev in r["top_event_associations"]:
            rows.append({"analysis": r["name"], **ev})
    pd.DataFrame(rows).to_csv(OUTPUT_DIR / "event_associations.csv", index=False)

    print(f"\nResults saved to {results_path}")


if __name__ == "__main__":
    main()
