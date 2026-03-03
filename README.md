# ⚽ FPL Transfer Optimizer v5.1

A rolling 6-gameweek Fantasy Premier League transfer planner built with Streamlit.

## Features

- **Rolling GW-by-GW plan** — suggests the best 1–2 transfers for each of the next 6 gameweeks, updating the squad after each recommendation so suggestions are always coherent
- **GW-specific captain projections** — projects points using actual fixture difficulty for each specific GW rather than a static `ep_next` value, so the captain recommendation changes each week
- **Corrected DC model** — defensive contributions modelled per official 2025/26 rules: DEF needs ≥10 CBIT, MID needs ≥12 CBIRT, capped at 2pts/match; GKPs excluded
- **Auto-detects free transfers** — reads your full transfer history to compute exactly how many free transfers you have banked (cap: 5 per 2025/26 rules)
- **Deadline-aware** — automatically plans for the next GW once the current deadline has passed
- **3-per-team rule enforced** — all transfer suggestions respect the maximum 3 players per club rule

## Data Sources

- [FPL API](https://fantasy.premierleague.com/api) — squad, prices, form, expected points, GW history, DC stats
- [Understat](https://understat.com) — xG, xA, npxG, shots, key passes per player

## How to Use

1. Go to the app URL
2. Enter your **FPL Manager ID** in the sidebar (find it in the URL on the FPL website: `fantasy.premierleague.com/entry/YOUR_ID/history`)
3. Adjust settings (horizon, risk appetite, DC lookback)
4. Click **▶ RUN ANALYSIS**

## Deploy Your Own Copy

### 1. Fork this repo
Click **Fork** at the top right of this page.

### 2. Deploy on Streamlit Community Cloud (free)
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click **New app**
4. Select your forked repo, set the main file as `app.py`
5. Click **Deploy**

Your app will be live at `https://your-username-fpl-optimizer.streamlit.app` within a few minutes.

### 3. Updates
Any `git push` to your repo automatically redeploys the app.

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## DC Scoring Rules (2025/26)

| Position | Actions counted | Threshold | Points |
|----------|----------------|-----------|--------|
| GKP | N/A | N/A | N/A |
| DEF | Clearances + Blocks + Interceptions + Tackles (CBIT) | ≥ 10 | 2 pts |
| MID/FWD | CBIT + Ball Recoveries (CBIRT) | ≥ 12 | 2 pts |

Points are capped at 2 per match regardless of total actions.

## Captain Projection Model

Points are projected per-GW using:
- **GKP**: `cs_prob × 6 + saves_p90 / 3 + 2`
- **DEF**: `cs_prob × 6 + xg_p90 × 6 + xa_p90 × 3 + dc_hit_rate × 2 + 2`
- **MID**: `cs_prob × 1 + xg_p90 × 5 + xa_p90 × 3 + dc_hit_rate × 2 + 2`
- **FWD**: `xg_p90 × 4 + xa_p90 × 3 + 2`

Each is multiplied by a fixture difficulty factor: difficulty 3 = 1.0×, easier = up to 1.2×, harder = down to 0.8×.

## License

MIT
