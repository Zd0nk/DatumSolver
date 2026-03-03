"""
FPL Transfer Optimizer v5.1 — Streamlit App
============================================
Deploy on Streamlit Community Cloud via GitHub.
"""

import streamlit as st
import requests
import pandas as pd
import numpy as np
import unicodedata
import re
import json
import warnings
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed

warnings.filterwarnings("ignore")

# ══════════════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="FPL Transfer Optimizer",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Dark pitch-inspired theme */
    .stApp {
        background: #0d1117;
        color: #e6edf3;
    }

    .block-container {
        padding-top: 2rem;
        max-width: 1400px;
    }

    /* Hero header */
    .hero {
        background: linear-gradient(135deg, #1a2332 0%, #0d1117 50%, #162032 100%);
        border: 1px solid #21d07a33;
        border-radius: 12px;
        padding: 2.5rem 3rem;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    .hero::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, #21d07a15 0%, transparent 70%);
        pointer-events: none;
    }
    .hero h1 {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 3.2rem;
        letter-spacing: 3px;
        color: #21d07a;
        margin: 0 0 0.3rem 0;
        line-height: 1;
    }
    .hero p {
        color: #8b949e;
        font-size: 0.95rem;
        font-weight: 300;
        margin: 0;
    }
    .hero .badge {
        display: inline-block;
        background: #21d07a22;
        border: 1px solid #21d07a55;
        color: #21d07a;
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        padding: 3px 10px;
        border-radius: 20px;
        margin-bottom: 0.8rem;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #161b22;
        border-right: 1px solid #21262d;
    }
    [data-testid="stSidebar"] .stMarkdown h2 {
        font-family: 'Bebas Neue', sans-serif;
        letter-spacing: 2px;
        color: #21d07a;
        font-size: 1.4rem;
    }

    /* Inputs */
    .stNumberInput input, .stSelectbox select, .stSlider {
        background: #1c2128 !important;
        border: 1px solid #30363d !important;
        color: #e6edf3 !important;
        border-radius: 8px !important;
    }

    /* Run button */
    .stButton > button {
        background: linear-gradient(135deg, #21d07a, #16a05e) !important;
        color: #0d1117 !important;
        font-family: 'Bebas Neue', sans-serif !important;
        font-size: 1.1rem !important;
        letter-spacing: 2px !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 2rem !important;
        width: 100% !important;
        transition: all 0.2s !important;
    }
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 20px #21d07a44 !important;
    }

    /* Section headers */
    .section-header {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 1.5rem;
        letter-spacing: 2px;
        color: #21d07a;
        border-bottom: 1px solid #21d07a33;
        padding-bottom: 0.4rem;
        margin: 2rem 0 1rem 0;
    }

    /* Metric cards */
    .metric-card {
        background: #161b22;
        border: 1px solid #21262d;
        border-radius: 10px;
        padding: 1.2rem 1.5rem;
        text-align: center;
    }
    .metric-card .val {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 2rem;
        color: #21d07a;
        line-height: 1;
    }
    .metric-card .lbl {
        font-size: 0.72rem;
        color: #8b949e;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 4px;
    }

    /* GW plan cards */
    .gw-card {
        background: #161b22;
        border: 1px solid #21262d;
        border-radius: 10px;
        padding: 1.4rem 1.8rem;
        margin-bottom: 1rem;
        position: relative;
    }
    .gw-card.has-transfer {
        border-left: 3px solid #21d07a;
    }
    .gw-card.no-transfer {
        border-left: 3px solid #30363d;
    }
    .gw-label {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 1.3rem;
        letter-spacing: 2px;
        color: #e6edf3;
    }
    .transfer-row {
        background: #1c2128;
        border-radius: 8px;
        padding: 0.8rem 1rem;
        margin: 0.5rem 0;
        font-size: 0.85rem;
    }
    .out-badge {
        background: #da3633;
        color: white;
        font-size: 0.65rem;
        font-weight: 700;
        letter-spacing: 1px;
        padding: 2px 8px;
        border-radius: 4px;
        margin-right: 6px;
    }
    .in-badge {
        background: #21d07a;
        color: #0d1117;
        font-size: 0.65rem;
        font-weight: 700;
        letter-spacing: 1px;
        padding: 2px 8px;
        border-radius: 4px;
        margin-right: 6px;
    }
    .captain-badge {
        background: #f0b429;
        color: #0d1117;
        font-size: 0.65rem;
        font-weight: 700;
        letter-spacing: 1px;
        padding: 2px 8px;
        border-radius: 4px;
        margin-right: 6px;
    }

    /* Risk badges */
    .risk-ok    { color: #21d07a; font-weight: 600; }
    .risk-doubt { color: #f0b429; font-weight: 600; }
    .risk-bad   { color: #da3633; font-weight: 600; }

    /* Dataframe tweaks */
    .stDataFrame { border-radius: 10px; overflow: hidden; }

    /* Progress / spinner */
    .stSpinner > div { border-top-color: #21d07a !important; }

    /* Expander */
    .streamlit-expanderHeader {
        background: #161b22 !important;
        border: 1px solid #21262d !important;
        border-radius: 8px !important;
        color: #e6edf3 !important;
    }

    /* Hide Streamlit branding */
    #MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
#  CONSTANTS
# ══════════════════════════════════════════════════════════════════════

BASE              = "https://fantasy.premierleague.com/api"
MAX_TRANSFER_BANK = 5
DC_THREADS        = 20

TEAM_MAP = {
    "Manchester City":         "Man City",
    "Manchester United":       "Man Utd",
    "Tottenham":               "Spurs",
    "Nottingham Forest":       "Nott'm Forest",
    "Newcastle United":        "Newcastle",
    "Wolverhampton Wanderers": "Wolves",
    "Leicester":               "Leicester",
    "Ipswich":                 "Ipswich",
}

# ══════════════════════════════════════════════════════════════════════
#  FPL API HELPERS
# ══════════════════════════════════════════════════════════════════════

def fpl_get(endpoint):
    r = requests.get(f"{BASE}/{endpoint}", timeout=20)
    r.raise_for_status()
    return r.json()

@st.cache_data(ttl=300, show_spinner=False)
def get_bootstrap():
    return fpl_get("bootstrap-static/")

@st.cache_data(ttl=300, show_spinner=False)
def get_fixtures_data():
    return fpl_get("fixtures/")

@st.cache_data(ttl=300, show_spinner=False)
def get_my_team_data(manager_id, active_gw):
    return fpl_get(f"entry/{manager_id}/event/{active_gw}/picks/")

@st.cache_data(ttl=600, show_spinner=False)
def get_manager_history(manager_id):
    return fpl_get(f"entry/{manager_id}/history/")

def resolve_active_gw(boot):
    now    = datetime.now(timezone.utc)
    events = boot["events"]
    next_gw = None
    for event in events:
        deadline = datetime.fromisoformat(
            event["deadline_time"].replace("Z", "+00:00")
        )
        if deadline > now:
            next_gw = event["id"]
            break
    if next_gw is None:
        active_gw = events[-1]["id"]
        next_gw   = active_gw
    elif next_gw == 1:
        active_gw = 1
    else:
        active_gw = next_gw - 1
    return active_gw, next_gw

def build_fpl_table(boot):
    players = pd.DataFrame(boot["elements"]).copy()
    teams   = pd.DataFrame(boot["teams"])[["id","name","short_name"]].copy()
    teams   = teams.rename(columns={"id":"team_id","name":"team_name","short_name":"team_short"})
    players = players.rename(columns={"team":"team_ref"})
    players = players.merge(teams, left_on="team_ref", right_on="team_id", how="left")
    pos_map = {1:"GKP",2:"DEF",3:"MID",4:"FWD"}
    players["position"] = players["element_type"].map(pos_map)
    players["price"]    = players["now_cost"] / 10
    players["full_name"]= players["first_name"] + " " + players["second_name"]
    players["fpl_id"]   = players["id"]
    num_cols = [
        "total_points","form","minutes","goals_scored","assists","clean_sheets",
        "bonus","ep_next","ep_this","bps","selected_by_percent","saves",
        "penalties_saved","yellow_cards","red_cards","goals_conceded",
        "expected_goals","expected_assists","expected_goal_involvements",
        "expected_goals_conceded","threat","creativity","influence","ict_index",
        "transfers_in_event","transfers_out_event",
        "chance_of_playing_next_round","chance_of_playing_this_round",
    ]
    for c in num_cols:
        if c in players.columns:
            players[c] = pd.to_numeric(players[c], errors="coerce").fillna(0)
    keep = ["fpl_id","full_name","web_name","team_name","team_short","team_id",
            "position","price","status"] + [c for c in num_cols if c in players.columns]
    players = players.loc[:, ~players.columns.duplicated()]
    return players[[c for c in keep if c in players.columns]].reset_index(drop=True).copy()

def get_free_transfers(manager_id, active_gw):
    try:
        history    = get_manager_history(manager_id)
        gw_history = history.get("current", [])
        xfers_made = {h["event"]: h["event_transfers"] for h in gw_history}
        bank = 1
        for gw in range(1, active_gw + 1):
            bank = min(bank + 1, MAX_TRANSFER_BANK)
            bank = max(bank - xfers_made.get(gw, 0), 0)
        free_transfers = max(1, min(bank, MAX_TRANSFER_BANK))
        chips      = history.get("chips", [])
        chips_used = [c["name"] for c in chips]
        chips_avail = []
        if "wildcard" not in chips_used: chips_avail.append("Wildcard")
        if "freehit"  not in chips_used: chips_avail.append("Free Hit")
        if "bboost"   not in chips_used: chips_avail.append("Bench Boost")
        if "3xc"      not in chips_used: chips_avail.append("Triple Captain")
        return free_transfers, chips_avail
    except Exception:
        return 1, []

# ══════════════════════════════════════════════════════════════════════
#  DEFENSIVE CONTRIBUTION STATS
# ══════════════════════════════════════════════════════════════════════

@st.cache_data(ttl=600, show_spinner=False)
def fetch_dc_stats(current_gw, lookback, element_ids_and_types):
    gw_start = max(1, current_gw - lookback + 1)

    def _fetch_one(pid, pos_type):
        if pos_type == 1:
            return {"fpl_id": pid}
        try:
            data   = fpl_get(f"element-summary/{pid}/")
            recent = [
                h for h in data.get("history", [])
                if h.get("round", 0) >= gw_start and h.get("minutes", 0) > 0
            ]
            if not recent:
                return {"fpl_id": pid}
            dc_pts, total_mins, cbit_total, gw_count = 0.0, 0.0, 0.0, 0
            for gw in recent:
                total_mins += float(gw.get("minutes", 0) or 0)
                t  = float(gw.get("tackles",       gw.get("attempted_tackles", 0)) or 0)
                i  = float(gw.get("interceptions", 0) or 0)
                b  = float(gw.get("blocked_shots", gw.get("blocked", 0)) or 0)
                cl = float(gw.get("clearances",    gw.get("clearances_off_line", 0)) or 0)
                r  = float(gw.get("recoveries",    0) or 0)
                cbit = t + i + b + cl
                thresh = 10 if pos_type == 2 else 12
                total_actions = cbit if pos_type == 2 else cbit + r
                dc_pts    += 2.0 if total_actions >= thresh else 0.0
                cbit_total += cbit
                gw_count   += 1
            n90 = total_mins / 90 if total_mins > 0 else None
            return {
                "fpl_id":      pid,
                "dc_pts_p90":  dc_pts / n90 if n90 else 0.0,
                "dc_hit_rate": (dc_pts / 2.0) / gw_count if gw_count else 0.0,
                "cbit_p90":    cbit_total / n90 if n90 else 0.0,
            }
        except Exception:
            return {"fpl_id": pid}

    rows = []
    with ThreadPoolExecutor(max_workers=DC_THREADS) as ex:
        futures = {ex.submit(_fetch_one, int(pid), int(pt)): pid
                   for pid, pt in element_ids_and_types}
        for f in as_completed(futures):
            rows.append(f.result())

    dc_df = pd.DataFrame(rows).fillna(0)
    for col in ["dc_pts_p90","dc_hit_rate","cbit_p90"]:
        if col not in dc_df.columns:
            dc_df[col] = 0.0
    return dc_df.reset_index(drop=True)

# ══════════════════════════════════════════════════════════════════════
#  FIXTURE ANALYSIS & CS PROBABILITY
# ══════════════════════════════════════════════════════════════════════

def compute_fixture_difficulty(boot, fixtures, from_gw, horizon=3):
    future = [
        f for f in fixtures
        if f["event"] and from_gw < f["event"] <= from_gw + horizon
        and not f["finished_provisional"]
    ]
    team_diffs  = {t["id"]: [] for t in boot["teams"]}
    team_ngames = {t["id"]: 0  for t in boot["teams"]}
    for f in future:
        h, a = f["team_h"], f["team_a"]
        team_diffs[h].append(f["team_h_difficulty"])
        team_diffs[a].append(f["team_a_difficulty"])
        team_ngames[h] += 1
        team_ngames[a] += 1
    teams = pd.DataFrame(boot["teams"])[["id","name","short_name"]]
    rows  = []
    for tid in team_diffs:
        diffs = team_diffs[tid]
        rows.append({
            "team_id":        tid,
            "avg_difficulty": float(np.mean(diffs)) if diffs else 4.5,
            "num_fixtures":   team_ngames[tid],
            "has_dgw":        int(team_ngames[tid] > horizon),
        })
    return pd.DataFrame(rows).merge(teams, left_on="team_id", right_on="id", how="left")

def get_cs_map(boot):
    players = pd.DataFrame(boot["elements"]).copy()
    for c in ["expected_goals_conceded","minutes","clean_sheets"]:
        players[c] = pd.to_numeric(players.get(c, 0), errors="coerce").fillna(0)
    gks    = players[players["element_type"] == 1].copy()
    gk_agg = gks.groupby("team").agg(
        team_xgc=("expected_goals_conceded","sum"),
        team_cs=("clean_sheets","sum"),
        team_minutes=("minutes","sum"),
    ).reset_index().rename(columns={"team":"team_id"})
    gk_agg["games_played"] = (gk_agg["team_minutes"] / 90).replace(0, np.nan)
    gk_agg["cs_prob"]      = np.exp(-(gk_agg["team_xgc"] / gk_agg["games_played"]).fillna(1.2))
    return gk_agg.set_index("team_id")["cs_prob"].to_dict()

# ══════════════════════════════════════════════════════════════════════
#  UNDERSTAT
# ══════════════════════════════════════════════════════════════════════

@st.cache_data(ttl=3600, show_spinner=False)
def get_understat_stats():
    url     = "https://understat.com/league/EPL/2024"
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()
    except Exception:
        return pd.DataFrame()
    match = re.search(r"var\s+playersData\s*=\s*JSON\.parse\('(.+?)'\)", r.text)
    if not match:
        return pd.DataFrame()
    try:
        data = json.loads(match.group(1).encode("utf-8").decode("unicode_escape"))
    except Exception:
        return pd.DataFrame()
    rows = []
    for p in data:
        mins = float(p.get("time", 0) or 0)
        n90  = mins / 90 if mins >= 90 else np.nan
        rows.append({
            "player_name": p.get("player_name",""),
            "team_title":  p.get("team_title",""),
            "minutes_us":  mins,
            "xg_p90":    float(p.get("xG",        0) or 0) / n90 if n90 else 0,
            "xa_p90":    float(p.get("xA",        0) or 0) / n90 if n90 else 0,
            "npxg_p90":  float(p.get("npxG",      0) or 0) / n90 if n90 else 0,
            "shots_p90": float(p.get("shots",     0) or 0) / n90 if n90 else 0,
            "kp_p90":    float(p.get("key_passes",0) or 0) / n90 if n90 else 0,
        })
    df = pd.DataFrame(rows)
    return df[df["minutes_us"] >= 90].reset_index(drop=True)

# ══════════════════════════════════════════════════════════════════════
#  NAME MATCHING & RISK FLAGS
# ══════════════════════════════════════════════════════════════════════

def _norm(name):
    name = unicodedata.normalize("NFD", str(name))
    name = "".join(c for c in name if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z ]", "", name.lower().strip())

def match_understat(fpl_df, us_df, threshold=0.45):
    ext_cols = ["xg_p90","xa_p90","npxg_p90","shots_p90","kp_p90"]
    for c in ext_cols: fpl_df[c] = 0.0
    if us_df.empty: return fpl_df.reset_index(drop=True)
    us_names = [_norm(n) for n in us_df["player_name"].tolist()]
    us_teams = [_norm(TEAM_MAP.get(t,t)) for t in us_df["team_title"].tolist()]
    for idx in fpl_df.index:
        fpl_tok  = set(_norm(fpl_df.at[idx,"full_name"]).split())
        team_tok = set(_norm(fpl_df.at[idx,"team_name"]).split())
        best_s, best_i = 0.0, -1
        for i, (un, ut) in enumerate(zip(us_names, us_teams)):
            b_tok = set(un.split())
            if not b_tok: continue
            ov = len(fpl_tok & b_tok) / max(len(fpl_tok | b_tok),1)
            s  = ov + (0.08 if team_tok & set(ut.split()) else 0)
            if s > best_s: best_s, best_i = s, i
        if best_s >= threshold and best_i >= 0:
            row = us_df.iloc[best_i]
            for c in ext_cols: fpl_df.at[idx,c] = float(row.get(c,0) or 0)
    return fpl_df.reset_index(drop=True)

def add_risk_flags(df):
    df = df.reset_index(drop=True)
    mins  = df["minutes"].values.astype(float)
    pts   = df["total_points"].values.astype(float)
    games = np.where(pts > 0, np.maximum(pts / 3.0, 1.0), 1.0)
    df["minutes_per_game"] = mins / games
    risk = []
    for s, c, m in zip(df["status"].values,
                        df["chance_of_playing_next_round"].values.astype(float), mins):
        if   s == "i": risk.append("🚫 Injured")
        elif s == "s": risk.append("🚫 Suspended")
        elif c < 50:   risk.append("⚠️ Doubt")
        elif m < 500:  risk.append("⚠️ Low mins")
        else:          risk.append("✅ Ok")
    df["rotation_risk"] = risk
    return df

# ══════════════════════════════════════════════════════════════════════
#  SCORING
# ══════════════════════════════════════════════════════════════════════

def _zscore(s):
    std = s.std()
    return (s - s.mean()) / std if std > 0 else pd.Series(np.zeros(len(s)), index=s.index)

def _safe(df, col):
    if col in df.columns: return pd.to_numeric(df[col], errors="coerce").fillna(0)
    return pd.Series(np.zeros(len(df)), index=df.index)

def score_players(df):
    parts = []
    # GKP
    g = df[df["position"]=="GKP"].copy().reset_index(drop=True)
    if not g.empty:
        mins = _safe(g,"minutes").replace(0,np.nan)
        g["saves_p90"]   = _safe(g,"saves") / mins * 90
        g["cs_prob_col"] = _safe(g,"cs_prob")
        g["fix_s"]       = _safe(g,"fix_score")
        w = {"ep_next":0.34,"cs_prob_col":0.32,"saves_p90":0.22,"fix_s":0.12}
        g["fpl_value_score"] = sum(w[k]*_zscore(_safe(g,k)) for k in w).values
        parts.append(g)
    # DEF
    d = df[df["position"]=="DEF"].copy().reset_index(drop=True)
    if not d.empty:
        mins = _safe(d,"minutes").replace(0,np.nan)
        d["cs_prob_col"]    = _safe(d,"cs_prob")
        d["att_ret_p90"]    = _safe(d,"xg_p90") + _safe(d,"xa_p90")
        d["yellow_rate"]    = _safe(d,"yellow_cards") / mins * 90
        d["fix_s"]          = _safe(d,"fix_score")
        d["dc_hit_rate_col"]= _safe(d,"dc_hit_rate")
        w = {"ep_next":0.20,"cs_prob_col":0.25,"dc_hit_rate_col":0.22,
             "att_ret_p90":0.15,"fix_s":0.12,"xg_p90":0.08,"yellow_rate":-0.04}
        d["fpl_value_score"] = sum(w[k]*_zscore(_safe(d,k)) for k in w).values
        parts.append(d)
    # MID
    m = df[df["position"]=="MID"].copy().reset_index(drop=True)
    if not m.empty:
        mins = _safe(m,"minutes").replace(0,np.nan)
        m["cs_prob_col"]    = _safe(m,"cs_prob")
        m["bonus_p90"]      = _safe(m,"bonus") / mins * 90
        m["yellow_rate"]    = _safe(m,"yellow_cards") / mins * 90
        m["fix_s"]          = _safe(m,"fix_score")
        m["dc_hit_rate_col"]= _safe(m,"dc_hit_rate")
        w = {"ep_next":0.22,"xg_p90":0.17,"xa_p90":0.14,"kp_p90":0.10,
             "shots_p90":0.08,"dc_hit_rate_col":0.10,"fix_s":0.09,
             "cs_prob_col":0.05,"bonus_p90":0.05,"yellow_rate":-0.04}
        m["fpl_value_score"] = sum(w[k]*_zscore(_safe(m,k)) for k in w).values
        parts.append(m)
    # FWD
    f = df[df["position"]=="FWD"].copy().reset_index(drop=True)
    if not f.empty:
        mins = _safe(f,"minutes").replace(0,np.nan)
        f["bonus_p90"] = _safe(f,"bonus") / mins * 90
        f["fix_s"]     = _safe(f,"fix_score")
        w = {"ep_next":0.28,"xg_p90":0.22,"npxg_p90":0.15,
             "shots_p90":0.13,"xa_p90":0.10,"fix_s":0.08,"bonus_p90":0.04}
        f["fpl_value_score"] = sum(w[k]*_zscore(_safe(f,k)) for k in w).values
        parts.append(f)
    return pd.concat([p for p in parts if not p.empty], ignore_index=True)

def apply_risk_appetite(df, appetite):
    own = pd.to_numeric(df["selected_by_percent"], errors="coerce").fillna(0)
    df["ownership"] = own
    z = _zscore(own)
    if   appetite == "safe":         df["fpl_value_score"] += 0.30 * z
    elif appetite == "differential": df["fpl_value_score"] -= 0.30 * z
    return df

def rescore_for_gw(players_base, boot, fixtures, target_gw, cs_map):
    df      = players_base.copy()
    fix_df  = compute_fixture_difficulty(boot, fixtures, target_gw - 1, horizon=3)
    fix_map = fix_df.set_index("team_id")[["avg_difficulty","num_fixtures","has_dgw"]].to_dict("index")
    df["avg_fix_diff"] = df["team_id"].map(lambda t: fix_map.get(t,{}).get("avg_difficulty",3.0))
    df["num_fixtures"] = df["team_id"].map(lambda t: fix_map.get(t,{}).get("num_fixtures",3))
    df["has_dgw"]      = df["team_id"].map(lambda t: fix_map.get(t,{}).get("has_dgw",0))
    df["fix_score"]    = (6 - df["avg_fix_diff"]) * (df["num_fixtures"] / 3)
    df["cs_prob"]      = df["team_id"].map(cs_map).fillna(0.25)
    df = score_players(df)
    df = apply_risk_appetite(df, st.session_state.get("risk_appetite","safe"))
    return df

# ══════════════════════════════════════════════════════════════════════
#  CAPTAIN PROJECTION
# ══════════════════════════════════════════════════════════════════════

def compute_gw_projected_pts(squad_df, target_gw, fixtures):
    df = squad_df.copy().reset_index(drop=True)
    gw_fixtures = [f for f in fixtures
                   if f["event"] == target_gw and not f["finished_provisional"]]
    team_gw_diff, teams_playing = {}, set()
    for f in gw_fixtures:
        team_gw_diff[f["team_h"]] = f["team_h_difficulty"]
        team_gw_diff[f["team_a"]] = f["team_a_difficulty"]
        teams_playing.update([f["team_h"], f["team_a"]])
    df["gw_diff"]        = df["team_id"].map(team_gw_diff).fillna(3.0)
    df["fix_multiplier"] = 1.0 + (3.0 - df["gw_diff"]) * 0.10
    df["has_fixture"]    = df["team_id"].isin(teams_playing)
    max_mins = df["minutes"].max()
    df["mins_factor"] = (df["minutes"] / max_mins).clip(0.5, 1.0) if max_mins > 0 else 1.0
    proj_pts = []
    for _, p in df.iterrows():
        if not p["has_fixture"]:
            proj_pts.append(0.0)
            continue
        pos, fm, mf = p.get("position",""), float(p["fix_multiplier"]), float(p["mins_factor"])
        cs  = float(p.get("cs_prob",    0.25))
        xg  = float(p.get("xg_p90",    0.0))
        xa  = float(p.get("xa_p90",    0.0))
        dc  = float(p.get("dc_hit_rate",0.0))
        sv  = float(p.get("saves",     0.0))
        sm  = max(float(p.get("minutes",90.0)),1.0)
        saves_p90 = sv / sm * 90.0
        if   pos == "GKP": base = (cs*6) + (saves_p90/3) + 2
        elif pos == "DEF": base = (cs*6) + (xg*6) + (xa*3) + (dc*2) + 2
        elif pos == "MID": base = (cs*1) + (xg*5) + (xa*3) + (dc*2) + 2
        else:              base = (xg*4) + (xa*3) + 2
        proj_pts.append(base * fm * mf)
    df["gw_proj_pts"] = proj_pts
    return df

# ══════════════════════════════════════════════════════════════════════
#  TRANSFER ENGINE
# ══════════════════════════════════════════════════════════════════════

def suggest_transfers_for_gw(squad_ids, scored_players, my_team_df, itb,
                              num_transfers=2, budget_padding=0.0):
    available   = scored_players[
        (~scored_players["fpl_id"].isin(squad_ids)) &
        (scored_players["status"].isin(["a","d"]))
    ].copy()
    team_counts = my_team_df["team_id"].value_counts().to_dict()
    results = []
    for _, out_p in my_team_df.iterrows():
        sell, pos = float(out_p["price"]), out_p["position"]
        bdgt      = sell + itb + budget_padding
        s_out     = float(out_p.get("fpl_value_score",0))
        out_team  = int(out_p["team_id"])
        counts_ao = dict(team_counts)
        counts_ao[out_team] = counts_ao.get(out_team,0) - 1
        def wtl(cid, _c=counts_ao): return _c.get(int(cid),0) < 3
        cands = available[
            (available["position"]==pos) &
            (available["price"]<=bdgt) &
            (available["team_id"].apply(wtl))
        ].sort_values("fpl_value_score",ascending=False).head(5)
        for _, cand in cands.iterrows():
            gain = float(cand["fpl_value_score"]) - s_out
            if gain > 0.05:
                results.append({
                    "OUT":out_p["web_name"],"OUT_pos":pos,"OUT_£":sell,
                    "OUT_score":round(s_out,3),"OUT_ep_next":float(out_p.get("ep_next",0)),
                    "OUT_dc_hit_rate":round(float(out_p.get("dc_hit_rate",0)),2),
                    "OUT_fix_diff":round(float(out_p.get("avg_fix_diff",0)),2),
                    "OUT_risk":out_p.get("rotation_risk","?"),
                    "IN":cand["web_name"],"IN_team":cand["team_short"],
                    "IN_team_id":int(cand["team_id"]),"IN_pos":pos,
                    "IN_£":float(cand["price"]),"IN_score":round(float(cand["fpl_value_score"]),3),
                    "IN_ep_next":float(cand.get("ep_next",0)),
                    "IN_xg_p90":round(float(cand.get("xg_p90",0)),3),
                    "IN_xa_p90":round(float(cand.get("xa_p90",0)),3),
                    "IN_dc_hit_rate":round(float(cand.get("dc_hit_rate",0)),2),
                    "IN_fix_diff":round(float(cand.get("avg_fix_diff",0)),2),
                    "IN_cs_prob":round(float(cand.get("cs_prob",0)),2),
                    "IN_own%":float(cand.get("ownership",0)),
                    "IN_risk":cand.get("rotation_risk","?"),
                    "score_gain":round(gain,3),
                    "price_diff":round(float(cand["price"])-sell,1),
                    "_out_fpl_id":int(out_p["fpl_id"]),
                    "_out_team_id":out_team,
                })
    if not results:
        return [], my_team_df.copy(), squad_ids.copy()
    results_df = pd.DataFrame(results).sort_values("score_gain",ascending=False).reset_index(drop=True)
    selected, updated_squad, updated_ids = [], my_team_df.copy(), set(squad_ids)
    for _ in range(num_transfers):
        best = None
        for _, row in results_df.iterrows():
            if row["OUT"] not in updated_squad["web_name"].values: continue
            if any(row["IN"]==p["IN"] for p in selected): continue
            sim = dict(team_counts)
            for p in selected:
                sim[p["_out_team_id"]] = sim.get(p["_out_team_id"],0) - 1
                sim[p["IN_team_id"]]   = sim.get(p["IN_team_id"],0)   + 1
            sim[int(row["_out_team_id"])] = sim.get(int(row["_out_team_id"]),0) - 1
            if sim.get(int(row["IN_team_id"]),0) + 1 > 3: continue
            best = row
            break
        if best is None: break
        selected.append(best.to_dict())
        out_id = int(updated_squad.loc[updated_squad["web_name"]==best["OUT"],"fpl_id"].values[0])
        in_row = scored_players[scored_players["web_name"]==best["IN"]]
        if not in_row.empty:
            updated_squad = updated_squad[updated_squad["fpl_id"]!=out_id]
            updated_squad = pd.concat([updated_squad,in_row.iloc[[0]]],ignore_index=True)
            updated_ids.discard(out_id)
            updated_ids.add(int(in_row.iloc[0]["fpl_id"]))
        results_df = results_df[results_df["OUT"]!=best["OUT"]].reset_index(drop=True)
    return selected, updated_squad, updated_ids

# ══════════════════════════════════════════════════════════════════════
#  MAIN APP
# ══════════════════════════════════════════════════════════════════════

def main():
    # ── Hero ────────────────────────────────────────────────────────
    st.markdown("""
    <div class="hero">
        <div class="badge">v5.1 · 2025/26</div>
        <h1>FPL Transfer Optimizer</h1>
        <p>Rolling 6-GW transfer planner · GW-specific captain projections · DC model per official 2025/26 rules</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Sidebar — FPL ID input is the FIRST thing the user sees ────
    with st.sidebar:
        st.markdown("## ⚽ Your FPL Details")
        st.markdown("---")

        fpl_id = st.number_input(
            "🔑 Enter your FPL Manager ID",
            min_value=1,
            max_value=99_999_999,
            value=None,
            placeholder="e.g. 210697",
            help="Find your ID in the FPL website URL: fantasy.premierleague.com/entry/**YOUR_ID**/history",
        )

        if fpl_id:
            st.success(f"Manager ID: **{int(fpl_id)}**")
        else:
            st.info("👆 Enter your FPL Manager ID above to get started.")
            st.markdown("""
            **How to find your ID:**
            1. Log in at [fantasy.premierleague.com](https://fantasy.premierleague.com)
            2. Go to **Points** or **Pick Team**
            3. Your ID is the number in the URL:\n`/entry/**12345**/`
            """)

        st.markdown("---")
        st.markdown("## ⚙️ Settings")

        horizon = st.slider("Gameweeks to plan ahead", 1, 8, 6)
        risk    = st.selectbox("Risk appetite", ["safe","balanced","differential"],
                               help="Safe = favour high-ownership · Differential = favour low-ownership")
        lookback = st.slider("DC stat lookback (GWs)", 3, 12, 8,
                             help="How many recent gameweeks to average defensive contribution stats over")
        budget_pad = st.number_input("Extra budget padding (£m)", 0.0, 5.0, 0.0, 0.1)

        st.session_state["risk_appetite"] = risk

        st.markdown("---")
        run = st.button("▶  RUN ANALYSIS", disabled=(not fpl_id))

        st.markdown("---")
        st.markdown("""
        <div style='font-size:0.72rem;color:#8b949e;line-height:1.6'>
        <b>Data sources</b><br>
        FPL API · Understat<br><br>
        <b>DC rules (2025/26)</b><br>
        DEF: 2pts if ≥10 CBIT<br>
        MID: 2pts if ≥12 CBIRT<br>
        GKP: not applicable<br><br>
        <b>Transfer bank cap:</b> 5
        </div>
        """, unsafe_allow_html=True)

    # ── Guard — wait for ID + button ────────────────────────────────
    if not fpl_id:
        st.markdown("""
        <div style='text-align:center;padding:5rem 2rem;color:#8b949e'>
            <div style='font-size:4rem;margin-bottom:1rem'>⚽</div>
            <div style='font-family:Bebas Neue,sans-serif;font-size:2rem;
                        letter-spacing:3px;color:#21d07a;margin-bottom:0.5rem'>
                Enter your FPL Manager ID
            </div>
            <div style='font-size:0.95rem'>
                Type your manager ID in the sidebar on the left to get started.
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    if not run:
        st.markdown("""
        <div style='text-align:center;padding:4rem 2rem;color:#8b949e'>
            <div style='font-size:0.95rem'>
                Settings configured — click <b style='color:#21d07a'>▶ RUN ANALYSIS</b>
                in the sidebar to generate your transfer plan.
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    fpl_id = int(fpl_id)

    # ── Load data ────────────────────────────────────────────────────
    progress = st.progress(0, text="Loading FPL data…")

    try:
        boot     = get_bootstrap()
        fixtures = get_fixtures_data()
        progress.progress(15, text="Resolving gameweek…")

        active_gw, next_gw = resolve_active_gw(boot)
        players             = build_fpl_table(boot)
        cs_map              = get_cs_map(boot)

        progress.progress(25, text="Fetching your squad…")
        picks_raw = get_my_team_data(fpl_id, active_gw)
        picks     = pd.DataFrame(picks_raw["picks"])
        itb       = picks_raw["entry_history"]["bank"]  / 10
        tv        = picks_raw["entry_history"]["value"] / 10

        free_transfers, chips_avail = get_free_transfers(fpl_id, active_gw)

        progress.progress(35, text="Fetching defensive contribution stats…")
        elements = pd.DataFrame(boot["elements"])
        targets  = elements[elements["element_type"].isin([2,3,4])][
            ["id","element_type"]
        ].values.tolist()
        dc_df = fetch_dc_stats(active_gw, lookback, tuple(map(tuple, targets)))

        progress.progress(60, text="Fetching Understat xG/xA data…")
        us_df = get_understat_stats()

        progress.progress(75, text="Scoring players…")

        # Initial fixture scores
        fix_df  = compute_fixture_difficulty(boot, fixtures, active_gw, horizon)
        fix_map = fix_df.set_index("team_id")[["avg_difficulty","num_fixtures","has_dgw"]].to_dict("index")
        players["avg_fix_diff"] = players["team_id"].map(lambda t: fix_map.get(t,{}).get("avg_difficulty",3.0))
        players["num_fixtures"] = players["team_id"].map(lambda t: fix_map.get(t,{}).get("num_fixtures",horizon))
        players["has_dgw"]      = players["team_id"].map(lambda t: fix_map.get(t,{}).get("has_dgw",0))
        players["fix_score"]    = (6 - players["avg_fix_diff"]) * (players["num_fixtures"] / horizon)
        players["cs_prob"]      = players["team_id"].map(cs_map).fillna(0.25)

        players = players.merge(dc_df, on="fpl_id", how="left")
        for col in ["dc_pts_p90","dc_hit_rate","cbit_p90"]:
            players[col] = players[col].fillna(0) if col in players.columns else 0.0

        players = match_understat(players, us_df)
        players = add_risk_flags(players)
        players = score_players(players)
        players = apply_risk_appetite(players, risk)

        my_ids     = set(int(x) for x in picks["element"].tolist())
        my_team_df = players[players["fpl_id"].isin(my_ids)].copy().reset_index(drop=True)

        progress.progress(100, text="Done!")
        progress.empty()

    except Exception as e:
        progress.empty()
        st.error(f"❌ Failed to load data: {e}\n\nPlease check your FPL Manager ID and try again.")
        return

    # ── Manager summary cards ────────────────────────────────────────
    st.markdown('<div class="section-header">📊 Manager Overview</div>', unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns(5)
    for col, val, lbl in [
        (c1, f"GW{active_gw}", "Active GW"),
        (c2, f"GW{next_gw}", "Planning For"),
        (c3, f"£{tv:.1f}m", "Team Value"),
        (c4, f"£{itb:.1f}m", "In the Bank"),
        (c5, str(free_transfers), f"Free Transfers (cap {MAX_TRANSFER_BANK})"),
    ]:
        col.markdown(f"""
        <div class="metric-card">
            <div class="val">{val}</div>
            <div class="lbl">{lbl}</div>
        </div>""", unsafe_allow_html=True)

    if chips_avail:
        st.markdown(
            f"<div style='margin-top:0.8rem;font-size:0.82rem;color:#8b949e'>"
            f"🃏 Chips available: <b style='color:#f0b429'>"
            f"{' · '.join(chips_avail)}</b></div>",
            unsafe_allow_html=True
        )

    # ── Current squad ────────────────────────────────────────────────
    st.markdown('<div class="section-header">👥 Your Current Squad</div>', unsafe_allow_html=True)
    squad_cols = ["web_name","team_short","position","price","ep_next",
                  "xg_p90","xa_p90","dc_hit_rate","cs_prob","avg_fix_diff","rotation_risk"]
    squad_cols = [c for c in squad_cols if c in my_team_df.columns]

    for pos in ["GKP","DEF","MID","FWD"]:
        sub = my_team_df[my_team_df["position"]==pos][squad_cols]
        if sub.empty: continue
        with st.expander(f"**{pos}** ({len(sub)} players)", expanded=True):
            st.dataframe(
                sub.rename(columns={
                    "web_name":"Player","team_short":"Team","position":"Pos",
                    "price":"£","ep_next":"EP Next","xg_p90":"xG/90",
                    "xa_p90":"xA/90","dc_hit_rate":"DC Hit Rate",
                    "cs_prob":"CS Prob","avg_fix_diff":"Fix Diff","rotation_risk":"Risk"
                }).reset_index(drop=True),
                use_container_width=True, hide_index=True,
            )

    # ── Rolling transfer plan ────────────────────────────────────────
    st.markdown(
        f'<div class="section-header">📋 Rolling {horizon}-GW Transfer Plan</div>',
        unsafe_allow_html=True
    )

    current_squad    = my_team_df.copy()
    current_ids      = set(my_ids)
    current_itb      = itb
    banked_transfers = free_transfers

    for gw_offset in range(horizon):
        target_gw     = next_gw + gw_offset
        num_available = min(banked_transfers, MAX_TRANSFER_BANK)

        scored       = rescore_for_gw(players, boot, fixtures, target_gw, cs_map)
        scored_squad = scored[scored["fpl_id"].isin(current_ids)].copy()

        transfers, updated_squad, updated_ids = suggest_transfers_for_gw(
            current_ids, scored, scored_squad, current_itb,
            num_transfers=min(num_available, 2),
            budget_padding=budget_pad,
        )
        transfers_made = len(transfers)

        # Captain
        cap_pool = scored[scored["fpl_id"].isin(updated_ids)].copy()
        cap_pool = compute_gw_projected_pts(cap_pool, target_gw, fixtures)
        cap_pool = cap_pool[cap_pool["has_fixture"]]
        top3_cap = cap_pool.sort_values("gw_proj_pts",ascending=False).head(3) if not cap_pool.empty else pd.DataFrame()

        card_class = "has-transfer" if transfers else "no-transfer"
        gw_html = f"""
        <div class="gw-card {card_class}">
            <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:0.8rem'>
                <span class="gw-label">GW {target_gw}</span>
                <span style='font-size:0.8rem;color:#8b949e'>
                    {num_available} free transfer{'s' if num_available!=1 else ''} · £{current_itb:.1f}m ITB
                </span>
            </div>
        """

        if not transfers:
            gw_html += "<div style='color:#8b949e;font-size:0.85rem'>✅ No beneficial transfers — hold this week.</div>"
        else:
            for i, t in enumerate(transfers, 1):
                gw_html += f"""
                <div class="transfer-row">
                    <div><span class="out-badge">OUT</span>
                    <b>{t['OUT']}</b> [{t['OUT_pos']}] &nbsp;
                    £{t['OUT_£']:.1f}m &nbsp; ep:{t['OUT_ep_next']:.2f} &nbsp;
                    fix:{t['OUT_fix_diff']:.1f} &nbsp;
                    <span style='color:#8b949e'>{t['OUT_risk']}</span>
                    </div>
                    <div style='margin-top:6px'>
                    <span class="in-badge">IN</span>
                    <b>{t['IN']}</b> ({t['IN_team']}) &nbsp;
                    £{t['IN_£']:.1f}m &nbsp; ep:{t['IN_ep_next']:.2f} &nbsp;
                    xG:{t['IN_xg_p90']:.3f} &nbsp; xA:{t['IN_xa_p90']:.3f} &nbsp;
                    DC:{t['IN_dc_hit_rate']:.0%} &nbsp; CS:{t['IN_cs_prob']:.0%} &nbsp;
                    fix:{t['IN_fix_diff']:.1f} &nbsp; own:{t['IN_own%']:.1f}% &nbsp;
                    <span style='color:#8b949e'>{t['IN_risk']}</span>
                    </div>
                    <div style='margin-top:6px;font-size:0.78rem;color:#8b949e'>
                    Score gain: <b style='color:#21d07a'>{t['score_gain']:+.3f}</b> &nbsp;
                    Price diff: <b>{t['price_diff']:+.1f}m</b>
                    </div>
                </div>
                """

        if not top3_cap.empty:
            cap = top3_cap.iloc[0]
            gw_html += f"""
            <div style='margin-top:0.8rem;font-size:0.82rem'>
                <span class="captain-badge">★ CAPTAIN</span>
                <b>{cap['web_name']}</b> ({cap.get('team_short','?')}) &nbsp;
                proj pts: <b style='color:#f0b429'>{cap['gw_proj_pts']:.2f}</b> &nbsp;
                fix diff: {cap.get('gw_diff',3.0):.1f} &nbsp;
                xG/90: {cap.get('xg_p90',0):.3f} &nbsp;
                CS: {cap.get('cs_prob',0):.0%}
            </div>
            """
            if len(top3_cap) > 1:
                others = " &nbsp;|&nbsp; ".join(
                    f"{r['web_name']} ({r['gw_proj_pts']:.2f})"
                    for _, r in top3_cap.iloc[1:].iterrows()
                )
                gw_html += f"<div style='font-size:0.75rem;color:#8b949e;margin-top:4px'>Also consider: {others}</div>"

        gw_html += "</div>"
        st.markdown(gw_html, unsafe_allow_html=True)

        # Update state
        current_squad    = updated_squad
        current_ids      = updated_ids
        banked_transfers = max(min(banked_transfers - transfers_made + 1, MAX_TRANSFER_BANK), 0)
        for t in transfers:
            current_itb = current_itb + t["OUT_£"] - t["IN_£"]

    st.markdown("---")
    st.markdown(
        "<div style='text-align:center;font-size:0.75rem;color:#8b949e'>"
        "FPL Transfer Optimizer v5.1 · Data: FPL API + Understat · "
        "DC rules per official 2025/26 FPL scoring"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
