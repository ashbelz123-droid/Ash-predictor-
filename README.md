# High-Value Football Predictor Bot

⚽ A Telegram bot that predicts high-value football matches using **team form, head-to-head history, player stats, injuries, and betting odds**.  

This bot fetches global top-league fixtures, calculates **confidence scores**, and sends **filtered high-value matches** to your Telegram. Designed to work with **API-Football free tier**, legal and safe.

---

## Features

- Supports multiple leagues (Premier League, La Liga, Bundesliga by default)  
- Weighted prediction combining:
  - Team form (last 5 matches)  
  - Head-to-head history  
  - Player performance (last 5 matches per player)  
  - Injuries / suspensions  
  - Betting odds (value detection)  
- Filters only **high-confidence matches (≥ 90%)**  
- Sends rich Telegram messages including:
  - Confidence percentage  
  - Odds  
  - Key absences  
  - Top-performing players  
- Modular code for easy expansion (add leagues, stats, features)

---

## Project Structure
