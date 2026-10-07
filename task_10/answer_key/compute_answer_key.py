"""Recompute every graded value for the CTSAgn task from the input files.

Run from the repo root:  python3 -I task_10/answer_key/compute_answer_key.py
Reads the input files in task_10/initial_files.
"""
import csv, os, json, numpy as np, openpyxl

IN = "task_10/initial_files"
def p(name): return os.path.join(IN, name)

def load_txt(path):
    rows = []
    for line in open(path, "rb").read().decode("utf-16").splitlines():
        s = line.split("\t")
        if len(s) == 6:
            try: rows.append([float(x) for x in s])
            except ValueError: pass
    return np.array(rows)

def load_xlsx(path):
    ws = openpyxl.load_workbook(path, data_only=True).active
    return np.array([r for r in ws.iter_rows(values_only=True)
                     if r[0] is not None and all(isinstance(x, (int, float)) for x in r)], float)

RUNS = {
    "Chitosan precursor": load_txt(p("CTS.txt")),
    "Alginate precursor": load_txt(p("Agn.txt")),
    "CTSAgn as made": load_xlsx(p("CTSAgn.xlsx")),
    "CTSAgn post-adsorption": load_xlsx(p("CTSAgn_After.xlsx")),
}
# columns: time(min), T(C), weight(mg), balance purge, sample purge, deriv weight (%/C of initial mass)

out = {"thermal": {}, "cost": {}}
for name, a in RUNS.items():
    t, w, d = a[:, 1], a[:, 2], a[:, 5]
    m0 = w[0]; m150 = w[np.argmin(abs(t - 150))]
    sel = t > 150
    i = np.argmax(d[sel]); Tp, raw = t[sel][i], d[sel][i]
    dry = raw * m0 / m150                      # per cent of the 150 C mass, per C
    idx = np.where((t > 150) & (w <= 0.95 * m150))[0][0]
    out["thermal"][name] = dict(m0_mg=m0, m150_mg=m150, peak_T=Tp, peak_rate_raw=raw, peak_rate_dry=dry, T_5pct_loss_since_150=t[idx])

T = out["thermal"]; r = lambda k: T[k]["peak_rate_dry"]
C, A, M, P = "Chitosan precursor", "Alginate precursor", "CTSAgn as made", "CTSAgn post-adsorption"
out["thermal"]["_derived"] = dict(
    asmade_vs_chitosan=r(C)/r(M), asmade_vs_alginate=r(A)/r(M),
    post_vs_chitosan=r(C)/r(P), post_vs_alginate=r(A)/r(P),
    post_over_asmade_dry=r(P)/r(M), post_over_asmade_raw=T[P]["peak_rate_raw"]/T[M]["peak_rate_raw"],
    shift_C=T[P]["peak_T"] - T[M]["peak_T"],
    asmade_below_alginate_C=T[A]["peak_T"] - T[M]["peak_T"], asmade_below_chitosan_C=T[C]["peak_T"] - T[M]["peak_T"],
    ceiling_C=T[P]["T_5pct_loss_since_150"], ceiling_margin_over_175=T[P]["T_5pct_loss_since_150"] - 175,
    ceiling_below_peak_C=T[P]["peak_T"] - T[P]["T_5pct_loss_since_150"])

rows = list(csv.reader(open(p("CTSAgn_batch_economics.csv"), encoding="utf-8")))
hdr = rows[1]; ix = {h: i for i, h in enumerate(hdr)}
batches = rows[2:9]
cost_cols = ["Chitosan_Cost_$", "Alginate_Cost_$", "CaCl2_Cost_$", "Acetic_Acid_Cost_$", "Water_Utilities_$",
             "Energy_$", "Labor_$", "Equipment_Depreciation_$", "Overhead_$"]   # excludes the stated Total and Cost_per_kg columns
cash = lambda b: sum(float(b[ix[c]]) for c in cost_cols if c != "Equipment_Depreciation_$")
tot = lambda b: sum(float(b[ix[c]]) for c in cost_cols)
for b in batches:
    assert abs(sum(float(b[ix[c]]) for c in cost_cols) - float(b[ix["Total_Production_Cost_$"]])) < 1e-9, b[0]
rel = [b for b in batches if b[ix["Batch_Disposition"]] == "Released"]
rej = [b for b in batches if b[ix["Batch_Disposition"]] != "Released"]
kg = sum(float(b[ix["Adsorbent_Produced_kg"]]) for b in rel)
cap = sum(float(b[ix["Adsorbent_Produced_kg"]]) * float(b[ix["Adsorption_Capacity_mg_per_g"]]) for b in rel) / kg
def metrics(cost_total):
    perkg = cost_total / kg; perg = perkg / 1000
    return dict(cost_usd_per_kg=perkg, cost_usd_per_g=perg, capacity_mg_per_g=cap, cost_per_mg=perg / cap, efficiency_mg_per_usd=cap / perg)
bench = {"Biochar": (10, 30), "Chitosan": (200, 100), "Activated Carbon": (150, 60), "Iron Oxide": (80, 50)}
out["cost"]["benchmarks"] = {n: dict(cost_usd_per_kg=k, cost_usd_per_g=k/1000, capacity=c, cost_per_mg=k/1000/c, efficiency=c/(k/1000)) for n, (k, c) in bench.items()}
rel_cash, rej_cash = sum(cash(b) for b in rel), sum(cash(b) for b in rej)
out["cost"]["released_cash"] = dict(total=rel_cash, kg=kg, **metrics(rel_cash))
out["cost"]["rejected_cash"] = rej_cash
out["cost"]["loss_case"] = dict(total=rel_cash + rej_cash, **metrics(rel_cash + rej_cash))
closest = min(out["cost"]["benchmarks"].items(), key=lambda kv: abs(kv[1]["efficiency"] - out["cost"]["released_cash"]["efficiency_mg_per_usd"]))
beff = closest[1]["efficiency"]
be_total = cap / beff * 1000 * kg
out["cost"]["closest_benchmark"] = closest[0]
out["cost"]["efficiency_vs_closest_released"] = out["cost"]["released_cash"]["efficiency_mg_per_usd"] / beff - 1
out["cost"]["efficiency_vs_closest_loss"] = out["cost"]["loss_case"]["efficiency_mg_per_usd"] / beff - 1
out["cost"]["break_even"] = dict(max_total_for_parity=be_total, headroom=be_total - rel_cash, rejected_cash=rej_cash,
                                 headroom_share_of_rejected=(be_total - rel_cash) / rej_cash, shortfall=rej_cash - (be_total - rel_cash))
# traps the agent can fall into (kept for rubric sanity checks)
out["cost"]["trap_total_incl_depreciation"] = dict(released=sum(tot(b) for b in rel), rejected=sum(tot(b) for b in rej))
print(json.dumps(out, indent=2, default=float))
