import numpy as np
import pandas as pd


def generate_player_rankings(ball_by_ball_path):
  print('Loading ball-by-ball data...')
  df = pd.read_csv(ball_by_ball_path)

  # Total runs per delivery
  df['total_runs'] = df['runs'] + df['extras1_runs'] + df['extras_2_runs']
  df = df.sort_values(
      ['match_id', 'innings', 'overid', 'over_ball_num']
  ).reset_index(drop=True)

  # Match state tracking
  df['cum_runs'] = (
      df.groupby(['match_id', 'innings'])['total_runs'].cumsum()
      - df['total_runs']
  )
  df['cum_wickets'] = (
      df.groupby(['match_id', 'innings'])['is_wicket'].cumsum()
      - df['is_wicket']
  )

  # Innings 1 totals and targets
  inn1 = (
      df[df['innings'] == 1]
      .groupby('match_id')['total_runs']
      .sum()
      .reset_index()
  )
  inn1.rename(columns={'total_runs': 'inn1_total'}, inplace=True)
  df = pd.merge(df, inn1, on='match_id', how='left')
  df['target'] = df['inn1_total'] + 1

  # Chase metrics
  df['ball_num_in_innings'] = (
      df.groupby(['match_id', 'innings']).cumcount() + 1
  )
  df['balls_remaining'] = 120 - (df['ball_num_in_innings'] - 1)
  df['runs_needed'] = df['target'] - df['cum_runs']
  df['required_run_rate'] = np.where(
      df['balls_remaining'] > 0, (df['runs_needed'] / df['balls_remaining']) * 6, 0
  )

  # --- PRESSURE DEFINITIONS ---
  df['is_death'] = df['overid'] >= 16
  df['is_collapse'] = ((df['overid'] <= 6) & (df['cum_wickets'] >= 3)) | (
      df['cum_wickets'] >= 4
  )
  df['is_high_rrr'] = (df['innings'] == 2) & (df['required_run_rate'] > 9.5)

  # Batter pressure flag
  df['batter_pressure'] = (
      df['is_death'] | df['is_collapse'] | df['is_high_rrr']
  ).astype(int)

  # Bowler pressure flag
  df['is_defending_low'] = (
      (df['innings'] == 2) & (df['inn1_total'] < 160) & (df['overid'] >= 10)
  )
  df['is_partnership_pressure'] = (
      (df['innings'] == 2) & (df['cum_wickets'] < 3) & (df['overid'] >= 8)
  )
  df['bowler_pressure'] = (
      df['is_death'] | df['is_defending_low'] | df['is_partnership_pressure']
  ).astype(int)

  # --- EVALUATE BATTERS ---
  batting_stats = []
  for batter, group in df.groupby('striker_name'):
    pressure_group = group[group['batter_pressure'] == 1]
    normal_group = group[group['batter_pressure'] == 0]

    if len(pressure_group) < 60:  # Minimum pressure sample size threshold
      continue

    sr_norm = (
        (normal_group['runs'].sum() / len(normal_group)) * 100
        if len(normal_group) > 0
        else 0
    )
    sr_pres = (
        (pressure_group['runs'].sum() / len(pressure_group)) * 100
        if len(pressure_group) > 0
        else 0
    )
    clutch_ratio = (sr_pres / sr_norm) if sr_norm > 0 else 0
    score = sr_pres * 0.55 + (clutch_ratio * 45)

    batting_stats.append({
        'Player': batter,
        'Pressure_Balls': len(pressure_group),
        'Normal_SR': round(sr_norm, 2),
        'Pressure_SR': round(sr_pres, 2),
        'Clutch_Index': round(clutch_ratio, 2),
        'Score': round(score, 2),
    })

  df_batters = (
      pd.DataFrame(batting_stats)
      .sort_values(by='Score', ascending=False)
      .head(10)
  )
  df_batters.insert(0, 'Rank', range(1, len(df_batters) + 1))

  # --- EVALUATE BOWLERS ---
  bowling_stats = []
  for bowler, group in df.groupby('bowler_name'):
    pressure_group = group[group['bowler_pressure'] == 1]
    normal_group = group[group['bowler_pressure'] == 0]

    if len(pressure_group) < 50:  # Minimum pressure sample size threshold
      continue

    econ_pres = (
        (pressure_group['total_runs'].sum() / len(pressure_group)) * 6
        if len(pressure_group) > 0
        else 99
    )
    wickets_pres = pressure_group['is_wicket'].sum()
    wicket_sr_pres = (
        (len(pressure_group) / wickets_pres) if wickets_pres > 0 else 999
    )

    score = (12 - econ_pres) * 6 + (30 / wicket_sr_pres) * 10

    bowling_stats.append({
        'Player': bowler,
        'Pressure_Balls': len(pressure_group),
        'Pressure_Econ': round(econ_pres, 2),
        'Pressure_Wicket_SR': round(wicket_sr_pres, 2),
        'Score': round(score, 2),
    })

  df_bowlers = (
      pd.DataFrame(bowling_stats)
      .sort_values(by='Score', ascending=False)
      .head(10)
  )
  df_bowlers.insert(0, 'Rank', range(1, len(df_bowlers) + 1))

  return df_batters, df_bowlers


if __name__ == '__main__':
  top_batters, top_bowlers = generate_player_rankings('ball_by_ball.csv')

  print('\n--- TOP 10 BATTERS UNDER PRESSURE ---')
  print(top_batters.to_string(index=False))

  print('\n--- TOP 10 BOWLERS UNDER PRESSURE ---')
  print(top_bowlers.to_string(index=False))
