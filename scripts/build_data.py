"""Build data/story_data.json from the OpenAI Signals CSVs.

Usage: python scripts/build_data.py [csv_dir] [out_json]
Prints the headline figures as it goes, which is the quickest way to check a number quoted in the story.
"""
import sys, json, pathlib, pandas as pd, numpy as np, pycountry
ROOT=pathlib.Path(__file__).resolve().parent.parent
D=sys.argv[1] if len(sys.argv)>1 else str(ROOT/"data/raw/public_release_csv")
OUT=sys.argv[2] if len(sys.argv)>2 else str(ROOT/"data/story_data.json")
r=lambda n: pd.read_csv(f"{D}/{n}.csv", keep_default_na=False)
SEA=["BN","KH","LA","MY","MM","PH","SG","TH","VN"]
OVR={"KR":"South Korea","RU":"Russia","VN":"Vietnam","LA":"Laos","BN":"Brunei","TW":"Taiwan","IR":"Iran","SY":"Syria","TZ":"Tanzania","BO":"Bolivia","VE":"Venezuela","MD":"Moldova","CD":"DR Congo","CG":"Congo","CI":"Côte d'Ivoire","TR":"Türkiye","XK":"Kosovo","PS":"Palestine","HK":"Hong Kong","MO":"Macau","CZ":"Czechia","GB":"United Kingdom","US":"United States","AE":"UAE","TL":"Timor-Leste","FM":"Micronesia","KP":"North Korea","MK":"North Macedonia"}
def nm(c):
    if c in OVR: return OVR[c]
    x=pycountry.countries.get(alpha_2=c); return (getattr(x,"common_name",None) or x.name) if x else c
def rd(x,k=1): return None if pd.isna(x) else round(float(x)*100,k)
def qmean(s): return s.groupby(pd.PeriodIndex(s.index,freq="Q")).mean()
def sea_cols(p): 
    return [c for c in SEA if c in p.columns and p[c].notna().all()]
out={"notes":{}}
months=None
# ---------- work
w=r("share_of_messages_by_work_related_country_month").query("work_related==1").pivot(index="month",columns="country",values="share_of_messages")
g=r("share_of_messages_by_work_related_month").query("work_related==1").set_index("month").share_of_messages
months=list(w.index); out["months"]=[m[:7] for m in months]
qlab=[f"Q{p.quarter} {p.year}" for p in qmean(g).index]; out["quarters"]=qlab
sc=sea_cols(w); out["notes"]["sea_work"]=sc
sea=w[sc].mean(axis=1)
full=[c for c in w.columns if w[c].notna().all()]
wq=w[full].apply(qmean)
chg=(w[full].iloc[-6:].mean()-w[full].iloc[:6].mean()).sort_values(ascending=False,kind="stable")
last6=w.iloc[-6:]; l6=last6.loc[:,last6.notna().all()].mean().sort_values(ascending=False,kind="stable")
out["work"]={"id_m":[rd(v) for v in w["ID"]],"sea_m":[rd(v) for v in sea],"world_m":[rd(v) for v in g],
 "id_q":[rd(v) for v in qmean(w["ID"])],"sea_q":[rd(v) for v in qmean(sea)],"world_q":[rd(v) for v in qmean(g)],
 "countries_q":{c:[rd(v) for v in wq[c]] for c in full if c!="ID"},
 "change":[{"c":c,"n":nm(c),"d":round(float(v)*100,1)} for c,v in chg.items()],
 "world_change":round(float(g.iloc[-6:].mean()-g.iloc[:6].mean())*100,1),"sea_change":round(float(sea.iloc[-6:].mean()-sea.iloc[:6].mean())*100,1),
 "rank_now":int(list(l6.index).index("ID")+1),"rank_n":int(len(l6))}
print("work q: ID",out["work"]["id_q"],"\n SEA",out["work"]["sea_q"],"\n W",out["work"]["world_q"]); print("change ID pos",[x["c"] for x in out["work"]["change"]].index("ID")+1,"of",len(chg),"sea",out["work"]["sea_change"],"world",out["work"]["world_change"], "SEA members change", chg[sc].round(3).to_dict())
print("SEA members, work share first and last quarter",{c:[rd(qmean(w[c]).iloc[0]),rd(qmean(w[c]).iloc[-1])] for c in sc})
ws=r("share_of_messages_by_work_schoolwork_month").pivot(index="month",columns="work_schoolwork",values="share_of_messages")
print("world three-way label (log only): q3 2024",{k:rd(v) for k,v in ws.iloc[:3].mean().items()},"q3 2026",{k:rd(v) for k,v in ws.iloc[-3:].mean().items()})
# ---------- per capita
rk=r("share_of_messages_by_country_quarter_rank"); lastq=rk.quarter.max(); pc=rk[rk.quarter==lastq].sort_values("rank",kind="stable")
out["percap"]=[{"c":c,"n":nm(c),"r":int(v)} for c,v in zip(pc.country,pc["rank"])]
print("percap n",len(pc), {c:int(pc.set_index("country")["rank"].get(c,-1)) for c in ["ID"]+SEA+["TL","US","IN"]})
# ---------- topics
t=r("share_of_messages_by_topic_country_month"); tg=r("share_of_messages_by_topic_month").pivot(index="month",columns="topic",values="share_of_messages")
TOP=["Writing","Practical Guidance","Seeking information","Multimedia","Self-expression","Technical help","Other/Unknown"]
tp={}
for k in TOP:
    p=t[t.topic==k].pivot(index="month",columns="country",values="share_of_messages"); sc=sea_cols(p)
    tp[k]={"id":[rd(v) for v in qmean(p["ID"])],"sea":[rd(v) for v in qmean(p[sc].mean(axis=1))],"world":[rd(v) for v in qmean(tg[k])],"id_m":[rd(v) for v in p["ID"]]}
out["notes"]["sea_topics"]=sc
out["topics"]={"names":TOP,"series":tp}
for k in TOP: print(k,"ID",tp[k]["id"][0],tp[k]["id"][-1],"SEA",tp[k]["sea"][0],tp[k]["sea"][-1],"W",tp[k]["world"][0],tp[k]["world"][-1])
# grid (largest remainder)
def lr(vals):
    v=np.array(vals,dtype=float); v=v/v.sum()*100; f=np.floor(v).astype(int); rem=100-f.sum(); order=np.argsort(-(v-f)); 
    for i in order[:rem]: f[i]+=1
    return [int(x) for x in f]
ti=t[t.country=="ID"].pivot(index="month",columns="topic",values="share_of_messages")[TOP]
a=r("share_of_messages_by_age_group_country_month"); ag=r("share_of_messages_by_age_group_month")
y=a[a.age_group=="18-24"].pivot(index="month",columns="country",values="share_of_messages")
ge=r("share_of_messages_by_gender_country_month").query("typical_name_gender=='feminine'").pivot(index="month",columns="country",values="share_of_messages")
gg=r("global_share_of_messages_by_gender_month").query("typical_name_gender=='feminine'").set_index("month").share_of_messages
out["grid"]={"t24":lr(ti.iloc[:3].mean().values),"t26":lr(ti.iloc[-3:].mean().values),"work24":round(float(w["ID"].iloc[:3].mean()*100)),"work26":round(float(w["ID"].iloc[-3:].mean()*100)),
  "fem24":round(float(ge["ID"].iloc[:3].mean()*100)),"fem26":round(float(ge["ID"].iloc[-3:].mean()*100)),"u25_24":round(float(y["ID"].iloc[:3].mean()*100)),"u25_26":round(float(y["ID"].iloc[-3:].mean()*100))}
print("grid",out["grid"])
# ---------- ADE (work-related, last 6 months)
e=r("share_of_messages_by_work_related_ask_do_express_country_month"); e=e[e.work_related==1]
eg=r("share_of_messages_by_work_related_ask_do_express_month").query("work_related==1").pivot(index="month",columns="ask_do_express",values="share_of_messages")
P={k:e[e.ask_do_express==k].pivot(index="month",columns="country",values="share_of_messages") for k in ["asking","doing","expressing"]}
ok=[c for c in P["doing"].columns if all(P[k][c].iloc[-6:].notna().all() for k in P)]
scA=[c for c in SEA if c in ok and all(P[k][c].notna().all() for k in P)]; out["notes"]["sea_ade"]=scA
cs=[{"c":c,"n":nm(c),"a":rd(P["asking"][c].iloc[-6:].mean()),"d":rd(P["doing"][c].iloc[-6:].mean()),"e":rd(P["expressing"][c].iloc[-6:].mean())} for c in ok]
def trip(f): return {"a":rd(f("asking")),"d":rd(f("doing")),"e":rd(f("expressing"))}
out["ade"]={"countries":cs,"world":trip(lambda k: eg[k].iloc[-6:].mean()),"sea":trip(lambda k: P[k][scA].iloc[-6:].mean().mean()),
  "id_q":{k:[rd(v) for v in qmean(P[k]["ID"])] for k in P},"world_q":{k:[rd(v) for v in qmean(eg[k])] for k in P},"sea_q":{k:[rd(v) for v in qmean(P[k][scA].mean(axis=1))] for k in P}}
print("ADE n",len(cs),"world",out["ade"]["world"],"sea",out["ade"]["sea"],"ID",[x for x in cs if x["c"]=="ID"], "JP",[x for x in cs if x["c"]=="JP"])
# ---------- IWA
iw=r("share_of_work_related_messages_by_onet_iwa_country_quarter"); qs=sorted(iw.quarter.unique())
lw=iw[iw.quarter.isin(qs[-4:])].groupby(["country","iwa_cleaned"]).share_of_messages.mean().unstack()
scI=[c for c in SEA if c in lw.index and (iw[iw.country==c].quarter.nunique()==len(qs))]; out["notes"]["sea_iwa"]=scI
ACTS=[("4.A.2.b.2.I23","Developing research plans or methods"),("4.A.3.b.6.I03","Presenting research or technical information"),("4.A.2.a.1.I08","Evaluating scholarly work"),("4.A.2.a.4.I04","Analyzing scientific data with math"),("4.A.3.b.6.I12","Preparing informational or teaching materials"),("4.A.2.b.2.I15","Developing educational programs or plans"),("4.A.4.b.3.I02","Teaching academic or vocational subjects"),("4.A.2.b.1.I07","Editing written materials"),("4.A.1.a.1.I07","Getting information about goods or services"),("4.A.4.b.6.I08","Advising on legal or regulatory matters")]
acts=[]
for code,lab in ACTS:
    s=lw[code].dropna(); srt=s.sort_values(ascending=False,kind="stable")
    acts.append({"code":code,"label":lab,"id":rd(s["ID"],2),"sea":rd(s[scI].mean(),2),"med":rd(s.median(),2),"rank":int(list(srt.index).index("ID")+1),"n":int(len(s)),"vals":[[c,rd(v,2)] for c,v in s.items() if c!="ID"]})
    print(lab,"ID",acts[-1]["id"],"SEA",acts[-1]["sea"],"med",acts[-1]["med"],"rank",acts[-1]["rank"],"/",acts[-1]["n"])
cl=lw[[c for c,_ in ACTS[:7]]].sum(axis=1); 
out["iwa"]={"acts":acts,"cluster":{"id":rd(cl["ID"]),"sea":rd(cl[scI].mean()),"med":rd(cl.median()),"rank":int(list(cl.sort_values(ascending=False,kind="stable").index).index("ID")+1),"n":int(len(cl))}}
print("cluster",out["iwa"]["cluster"], cl[scI].round(3).to_dict())
ii=iw.pivot_table(index="quarter",columns=["country","iwa_cleaned"],values="share_of_messages")
def ser(code):
    p=iw[iw.iwa_cleaned==code].pivot(index="quarter",columns="country",values="share_of_messages")
    return {"id":[rd(v,2) for v in p["ID"]],"sea":[rd(v,2) for v in p[scI].mean(axis=1)],"med":[rd(v,2) for v in p.median(axis=1)]}
out["pics"]={"quarters":[f"Q{pd.Period(q,'Q').quarter} {pd.Period(q,'Q').year}" for q in qs],"design":ser("4.A.2.b.2.I18"),"prog":ser("4.A.3.b.1.I01"),"edit":ser("4.A.2.b.1.I07")}
print("pics",out["pics"])
# ---------- age
AG=["18-24","25-34","35-44","45-54","55-64","65+"]
scG=None; mix={"id":[],"sea":[],"world":[]}
agp=ag.pivot(index="month",columns="age_group",values="share_of_messages")
series={}
for k in AG:
    p=a[a.age_group==k].pivot(index="month",columns="country",values="share_of_messages"); sc=sea_cols(p); scG=sc
    mix["id"].append(rd(p["ID"].iloc[-3:].mean())); mix["sea"].append(rd(p[sc].iloc[-3:].mean().mean())); mix["world"].append(rd(agp[k].iloc[-3:].mean()))
    series[k]={"id_q":[rd(v) for v in qmean(p["ID"])],"id_m":[rd(v) for v in p["ID"]]}
    if k=="18-24": u={"id_m":[rd(v) for v in p["ID"]],"sea_m":[rd(v) for v in p[sc].mean(axis=1)],"world_m":[rd(v) for v in agp[k]],"id_q":[rd(v) for v in qmean(p["ID"])],"sea_q":[rd(v) for v in qmean(p[sc].mean(axis=1))],"world_q":[rd(v) for v in qmean(agp[k])]}
out["notes"]["sea_age"]=scG
out["age"]={"groups":AG,"u25":u,"mix":mix,"id_groups":series}
# Age mix by country for the last three months: countries with all six groups in each month, ordered by the 18-24 share.
# The page draws Indonesia, the region, and the world beside a fixed set of large countries (PICK).
PICK=["IN","NG","MX","BR","JP","DE","US","KR"]
xa=a[a.month.isin(sorted(a.month.unique())[-3:])]; cnt=xa.groupby("country").share_of_messages.count()
mxa=xa.groupby(["country","age_group"]).share_of_messages.mean().unstack()[AG].loc[[c for c in cnt.index if cnt[c]==3*len(AG)]].sort_values("18-24",ascending=False,kind="stable")
out["age"]["pick"]=[{"c":c,"n":nm(c),"m":[rd(v) for v in mxa.loc[c]]} for c in PICK]
out["age"]["u25_rank"]=int(list(mxa.index).index("ID")+1); out["age"]["u25_n"]=int(len(mxa))
# Ages 45 and over as one group, for the phone layout, summed before rounding.
OLD=AG[3:]
out["age"]["mix45"]={"id":rd(mxa.loc["ID"][OLD].sum()),"sea":rd(mxa.loc[scG][OLD].sum(axis=1).mean()),"world":rd(sum(agp[k].iloc[-3:].mean() for k in OLD))}
for d in out["age"]["pick"]: d["o"]=rd(mxa.loc[d["c"]][OLD].sum())
print("age 45 and over, last 3 months:",out["age"]["mix45"],{d["n"]:d["o"] for d in out["age"]["pick"]})
print("age by country, last 3 months: ID ranks",out["age"]["u25_rank"],"of",out["age"]["u25_n"],"by 18-24 share;",{d["n"]:d["m"] for d in out["age"]["pick"]})
print("age mix",mix); print("u25 q id",u["id_q"],"sea",u["sea_q"],"world",u["world_q"])
# ---------- gender
sc=sea_cols(ge); out["notes"]["sea_gender"]=sc
gt=r("share_of_messages_by_gender_topic_country_month").query("typical_name_gender=='feminine'"); ggt=r("share_of_messages_by_gender_topic_month").query("typical_name_gender=='feminine'").pivot(index="month",columns="topic",values="share_of_messages")
gtop={"id":[],"sea":[],"world":[]}; 
for k in TOP:
    p=gt[gt.topic==k].pivot(index="month",columns="country",values="share_of_messages"); s2=sea_cols(p)
    gtop["id"].append(rd(p["ID"].iloc[-3:].mean())); gtop["sea"].append(None); gtop["world"].append(rd(ggt[k].iloc[-3:].mean()))
out["notes"]["sea_gender_topic"]=s2
out["gender"]={"id_m":[rd(v) for v in ge["ID"]],"sea_m":[rd(v) for v in ge[sc].mean(axis=1)],"world_m":[rd(v) for v in gg],"id_q":[rd(v) for v in qmean(ge["ID"])],"sea_q":[rd(v) for v in qmean(ge[sc].mean(axis=1))],"world_q":[rd(v) for v in qmean(gg)],"topic":gtop}
print("gender q id",out["gender"]["id_q"],"sea",out["gender"]["sea_q"],"world",out["gender"]["world_q"]); print("gtopic",gtop); print("SEA fem last3",ge[sc].iloc[-3:].mean().round(3).to_dict())
print(out["notes"])
with open(OUT,"w",encoding="utf-8",newline="\n") as f: json.dump(out,f,separators=(",",":"),ensure_ascii=False)
import os
try: shown=pathlib.Path(OUT).resolve().relative_to(ROOT).as_posix()
except ValueError: shown=OUT
print("wrote",shown,os.path.getsize(OUT),"bytes")
