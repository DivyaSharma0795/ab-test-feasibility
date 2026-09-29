"""A/B test MDD & sample-size calculator.  Run:  streamlit run app.py
Model: each treatment arm is compared with control (m = k-1 comparisons), normal approximation,
variance evaluated at the baseline. MDD = (z_alpha + z_power) * sqrt(var * (1/n_control + 1/n_treatment))."""
import numpy as np
import pandas as pd
import streamlit as st

from mdd_calc import adj_alpha, mdd, required_n, z_sum

st.set_page_config(page_title="MDD & Sample Size Calculator", layout="wide")




st.title("A/B Test MDD & Sample Size Calculator")
st.caption("Feasibility check for test design: how small a lift can k groups detect, and how big must the audience be?")

with st.sidebar:
    st.header("Inputs")
    metric = st.radio("Metric type", ["Proportion", "Continuous"], horizontal=True)
    N = st.number_input("Audience size (N)", min_value=100, value=200_000, step=1000)
    measured = st.number_input("Share of audience measured (%)", 1.0, 100.0, 100.0, help="e.g. response/observation rate")
    if metric == "Proportion":
        base = st.number_input("Baseline rate", 0.0001, 0.9999, 0.05, step=0.005, format="%.4f")
        var = base * (1 - base)
    else:
        base = st.number_input("Baseline mean", value=100.0)
        sd = st.number_input("Standard deviation", min_value=0.0001, value=50.0)
        var = sd**2
    k = st.number_input("Number of groups (incl. control)", 2, 10, 2)
    equal = st.checkbox("Equal split", value=True)
    c = 1 / k if equal else st.slider("Control share of audience", 0.05, 0.95, 0.5, 0.05)
    alpha = st.number_input("Alpha", 0.001, 0.5, 0.05, step=0.01, format="%.3f")
    power = st.number_input("Power (1 - beta)", 0.5, 0.999, 0.80, step=0.05, format="%.3f")
    tails = st.radio("Test type", ["Two-tailed", "One-tailed"], horizontal=True)
    method = st.selectbox("Multiple-comparison correction", ["Bonferroni", "Sidak", "None"])
    min_lift = st.number_input("Minimum useful relative lift (%)", 0.0, 500.0, 5.0, step=0.5) / 100

n_an = N * measured / 100
zs = z_sum(alpha, power, k - 1, tails, method)
d = mdd(n_an, k, c, var, zs)
rel = d / base
nc, nt = n_an * c, n_an * (1 - c) / (k - 1)

st.subheader("Forward mode: what can this audience detect?")
a, b, cc, e = st.columns(4)
a.metric("MDD (absolute)", f"{d:.4f}" if metric == "Proportion" else f"{d:,.3f}")
b.metric("MDD (relative to baseline)", f"{rel:.2%}")
cc.metric("Control / per-treatment n", f"{nc:,.0f} / {nt:,.0f}")
e.metric("Verdict", "Feasible" if rel <= min_lift else "Not feasible", help=f"MDD vs your minimum useful lift of {min_lift:.1%}")

st.subheader("How feasibility changes with number of groups (equal split)")
rows = []
for kk in range(2, 7):
    zk = z_sum(alpha, power, kk - 1, tails, method)
    r = mdd(n_an, kk, 1 / kk, var, zk) / base
    rows.append({"Groups": kk, "n per group": round(n_an / kk), "Alpha per comparison": adj_alpha(alpha, kk - 1, method),
                 "Relative MDD": r, "Feasible": "Yes" if r <= min_lift else "No"})
st.dataframe(pd.DataFrame(rows).style.format({"Alpha per comparison": "{:.4f}", "Relative MDD": "{:.2%}", "n per group": "{:,}"}),
             hide_index=True, use_container_width=True)

st.subheader("Relative MDD vs audience size")
grid = np.linspace(0.1, 2.0, 20) * N
chart = pd.DataFrame({f"{kk} groups": [mdd(g * measured / 100, kk, 1 / kk, var, z_sum(alpha, power, kk - 1, tails, method)) / base
                                       for g in grid] for kk in range(2, 6)}, index=grid.round(0))
chart["Min useful lift"] = min_lift
st.line_chart(chart)

st.subheader("Reverse mode: how big must the audience be?")
target = st.number_input("Target relative lift to detect (%)", 0.01, 500.0, 5.0, step=0.5) / 100
need = required_n(target * base, k, c, var, zs)
need_aud = need / (measured / 100)
r1, r2, r3 = st.columns(3)
r1.metric("Total audience required", f"{need_aud:,.0f}")
r2.metric("Control / per-treatment n", f"{need * c:,.0f} / {need * (1 - c) / (k - 1):,.0f}")
r3.metric("vs. audience available", f"{N / need_aud:.0%}", help="Above 100% means you have enough")

st.caption("Assumptions: normal approximation; variance at baseline; each arm tested against control; "
           "MDD is the smallest true effect detectable with the chosen power.")
