# SupeRR Selector Season 2: Identifying the Most Reliable Players Under Pressure
**Rajasthan Royals Data-Driven Analytics Submission**

---

## 1. Executive Summary
In high-stakes T20 cricket, success is rarely determined by average performances in routine situations; rather, matches are won or lost in moments of acute pressure. Traditional metrics often fail to isolate how players adapt when the game is on the line. 

This project establishes a rigorous, data-driven evaluation pipeline using historical IPL and T20 International (T20I) ball-by-ball data (2022 onwards). By quantitatively defining pressure across multiple tactical dimensions—such as death-over acceleration, batting collapses, steep required run rates, and defensive squeeze phases—we isolate true "clutch" performers from those who merely accumulate numbers against weaker game states. 

Our dual-tier rating system combines volume-weighted pressure output with a **Clutch Index** (measuring performance scaling from baseline to pressure), filtering out sample-size noise to deliver definitive Top 10 rankings for both batters and bowlers.

---

## 2. Defining "Pressure" (The Tactical Framework)
Rather than relying on subjective intuition, pressure is defined across objective, situational match states derived directly from delivery-level records.

### For Batters:
1. **Death Overs Phase ($\text{overid} \ge 16$):** Extreme scoreboard velocity and execution required under maximum bowling pressure.
2. **Batting Collapse / Rescue Situations:** 
   * Top-order collapse: $\text{overid} \le 6$ and $\text{cum\_wickets} \ge 3$.
   * General middle-order collapse: $\text{cum\_wickets} \ge 4$.
3. **High Required Run Rate (RRR) Pressure:** Chases in Innings 2 where $\text{required\_run\_rate} > 9.5$.

### For Bowlers:
1. **Death Overs Phase ($\text{overid} \ge 16$):** Restricting free-scoring batters when boundaries are at a premium.
2. **Defending Low Totals:** Innings 2 bowling when $\text{inn1\_total} < 160$ and $\text{overid} \ge 10$.
3. **Partnership Pressure:** Innings 2 bowling when opposition wickets in hand are high ($\text{cum\_wickets} < 3$ at $\text{overid} \ge 8$), putting maximum onus on the bowler to break the stand.

---

## 3. Performance Measurement & Rating Logic

To ensure fairness, players are evaluated not just on raw output under pressure, but on their **Clutch Factor**—how significantly their performance scales when transitioning from normal situations to pressure situations.

### A. Batters Rating Logic
* **Baseline Strike Rate ($SR_{\text{normal}}$):** Runs scored per 100 balls in normal/low-pressure deliveries.
* **Pressure Strike Rate ($SR_{\text{pressure}}$):** Runs scored per 100 balls in high-pressure deliveries.
* **Clutch Index ($C$):** 
  $$C = \frac{SR_{\text{pressure}}}{SR_{\text{normal}}}$$
* **Composite Score:** 
  $$\text{Score} = (SR_{\text{pressure}} \times 0.55) + (C \times 45)$$
* **Eligibility Threshold:** Minimum requirement of **$\ge 60$ pressure balls faced** to eliminate part-time anomalies.

### B. Bowlers Rating Logic
* **Pressure Economy Rate ($Econ_{\text{pressure}}$):** Runs conceded per 6 balls under pressure.
* **Pressure Wicket Strike Rate ($WSR_{\text{pressure}}$):** Balls bowled per wicket taken under pressure.
* **Composite Score:** 
  $$\text{Score} = (12 - Econ_{\text{pressure}}) \times 6 + \left(\frac{30}{WSR_{\text{pressure}}}\right) \times 10$$
* **Eligibility Threshold:** Minimum requirement of **$\ge 50$ pressure balls bowled**.

---

## 4. Final Rankings & Results

### Top 10 Batters Under Pressure
| Rank | Player Name | Pressure Balls | Normal SR | Pressure SR | Clutch Index | Composite Score |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **1** | Daniel Sams | 75 | 14.29 | 118.67 | 8.31 | 439.07 |
| **2** | Dwaine Pretorius | 76 | 40.00 | 172.37 | 4.31 | 288.72 |
| **3** | Odean Smith | 140 | 33.33 | 125.00 | 3.75 | 237.50 |
| **4** | Ijaz Ahmadzai | 102 | 41.67 | 143.14 | 3.44 | 233.31 |
| **5** | Nurul Hasan | 234 | 36.36 | 128.63 | 3.54 | 229.93 |
| **6** | Kieron Pollard | 195 | 37.14 | 118.97 | 3.20 | 209.58 |
| **7** | Mitchell Owen | 117 | 54.55 | 147.86 | 2.71 | 203.31 |
| **8** | Dinesh Karthik | 676 | 71.43 | 157.40 | 2.20 | 185.73 |
| **9** | Shashank Singh | 540 | 81.25 | 160.37 | 1.97 | 177.02 |
| **10**| Ramandeep Singh | 290 | 75.00 | 150.34 | 2.00 | 172.90 |

### Top 10 Bowlers Under Pressure
| Rank | Player Name | Pressure Balls | Pressure Economy | Pressure Wicket SR | Composite Score |
| :---: | :--- | :---: | :---: | :---: | :---: |
| **1** | Kane Richardson | 88 | 7.43 | 7.33 | 68.32 |
| **2** | Matthew Humphreys | 95 | 6.69 | 9.50 | 63.41 |
| **3** | Dushan Hemantha | 85 | 7.41 | 8.50 | 62.82 |
| **4** | Ben Dwarshuis | 94 | 9.38 | 6.71 | 60.38 |
| **5** | Graham Hume | 62 | 8.42 | 7.75 | 60.19 |
| **6** | Ripon Mondol | 108 | 8.56 | 7.71 | 59.56 |
| **7** | Pramod Madushan | 81 | 7.70 | 9.00 | 59.11 |
| **8** | Mark Wood | 95 | 8.53 | 7.92 | 58.74 |
| **9** | Mehidy Hasan Miraz | 77 | 6.16 | 12.83 | 58.44 |
| **10**| Glenn Phillips | 66 | 6.91 | 11.00 | 57.82 |

---

## 5. Reliability, Consistency & Limitations

1. **Sample Size Controls:** By enforcing strict minimum ball thresholds, we prevented skewed statistics from players who faced only a handful of deliveries in high-leverage moments.
2. **Contextual Variance:** T20I matches feature different international bowling attacks compared to domestic IPL franchises. Our model treats competitions holistically while maintaining uniform situational definitions.
3. **Future Enhancements:** Future iterations of this pipeline will incorporate venue-specific par scores and pitch degradation indices to further refine pressure weighting.