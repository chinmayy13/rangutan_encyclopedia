"""Draws the plot used in Thermal_Stability_Assessment.pdf.
Rates are the instrument derivative-weight signal rescaled to per cent of the 150 C mass per C
(the lab note's rate basis). Template styling: title/axis text #15295d, traces c91d1d (as made) and 277534 (post-adsorption).
Run: python3 make_plot.py [height_cm]   (default 7.0 cm, width 16.59 cm = text width). Writes plot.png next to this file.
"""
import sys, pathlib, numpy as np, openpyxl, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
HERE=pathlib.Path(__file__).resolve().parent; INP=HERE.parent/"initial_files"; H=float(sys.argv[1]) if len(sys.argv)>1 else 7.0
def lx(p):
    ws=openpyxl.load_workbook(p,data_only=True).active
    return np.array([r for r in ws.iter_rows(values_only=True) if r[0] is not None and all(isinstance(x,(int,float)) for x in r)],float)
NAVY="#15295d"; RED="#c91d1d"; GREEN="#277534"
W_IN=16.59/2.54; H_IN=H/2.54
fig,ax=plt.subplots(figsize=(W_IN,H_IN),dpi=300)
runs=[(str(INP/"CTSAgn.xlsx"),"CTSAgn as made",RED,(26,16)),(str(INP/"CTSAgn_After.xlsx"),"CTSAgn post-adsorption",GREEN,(-62,30))]
res={}
for p,label,col,off in runs:
    a=lx(p); t,w,d=a[:,1],a[:,2],a[:,5]; y=d*w[0]/w[np.argmin(abs(t-150))]   # per cent of the 150 C mass, per C
    ax.plot(t,y,color=col,lw=1.5,label=label,zorder=3)
    m=t>150; i=np.argmax(y[m]); tp,yp=t[m][i],y[m][i]; res[label]=(tp,yp)
    ax.plot(tp,yp,"o",color=col,ms=4,zorder=4)
    ax.annotate(f"{tp:.1f} °C",(tp,yp),xytext=off,textcoords="offset points",color=NAVY,fontsize=8.5,fontweight="bold",
                arrowprops=dict(arrowstyle="-",color=NAVY,lw=0.8),zorder=5)
ax.set_xlim(0,500); ax.set_ylim(0,0.35); ax.set_xticks(range(0,501,100)); ax.set_yticks(np.arange(0,0.351,0.05))
ax.set_xlabel("Sample temperature (°C)",color=NAVY,fontsize=9,fontweight="bold"); ax.set_ylabel("DTG rate (%/°C)",color=NAVY,fontsize=9,fontweight="bold")
ax.set_title("CTSAgn DTG profiles before and after phosphate adsorption",color=NAVY,fontsize=10,fontweight="bold",pad=6)
ax.tick_params(colors=NAVY,labelsize=8.5); [l.set_fontweight("bold") for l in ax.get_xticklabels()+ax.get_yticklabels()]
ax.grid(True,ls="--",lw=0.6,color="#d7d7d7",zorder=0)
for s in ax.spines.values(): s.set_color("black"); s.set_linewidth(0.8)
h,l=ax.get_legend_handles_labels(); order=[l.index("CTSAgn post-adsorption"),l.index("CTSAgn as made")]   # template order
leg=ax.legend([h[i] for i in order],[l[i] for i in order],loc="upper right",fontsize=8.5,frameon=True,edgecolor="#d7d7d7",framealpha=1)
for t_ in leg.get_texts(): t_.set_color(NAVY)
fig.tight_layout(pad=0.4); fig.savefig(HERE/"plot.png"); print("peaks",res, "fig %.2f x %.2f cm"%(W_IN*2.54,H))
