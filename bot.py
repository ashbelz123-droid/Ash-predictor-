from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from fetcher import get_fixtures, get_team_form, get_h2h, get_players_statistics, get_injuries
from predictor import calculate_confidence, is_high_value
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
LEAGUES = [39, 140, 78]  # Premier League, La Liga, Bundesliga
SEASON = 2025

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚽ High-Value Football Predictor Bot Running!")

async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    messages = []
    for league_id in LEAGUES:
        fixtures = get_fixtures(league_id, SEASON)
        for f in fixtures:
            home_id = f['teams']['home']['id']
            away_id = f['teams']['away']['id']
            home_name = f['teams']['home']['name']
            away_name = f['teams']['away']['name']

            home_form = get_team_form(home_id)
            away_form = get_team_form(away_id)
            h2h = get_h2h(home_id, away_id)

            home_players = get_players_statistics(home_id)
            away_players = get_players_statistics(away_id)

            home_injuries = len(get_injuries(home_id))
            away_injuries = len(get_injuries(away_id))

            odds = float(f['odds'][0]['bookmakers'][0]['bets'][0]['values'][0]['odd']) if f.get('odds') else 2.0

            confidence = calculate_confidence(home_form, away_form, h2h,
                                              home_players, away_players,
                                              home_injuries, away_injuries,
                                              odds)
            if is_high_value(confidence, odds):
                top_players = sorted(home_players.items(), key=lambda x: x[1], reverse=True)[:3]
                top_str = ", ".join([f"{p[0]} {p[1]}pts" for p in top_players])
                msg = (f"🏆 {home_name} vs {away_name}\n"
                       f"💯 Confidence: {confidence*100:.1f}%\n"
                       f"💰 Odds: {odds}\n"
                       f"🩺 Absences: {', '.join(get_injuries(home_id) + get_injuries(away_id))}\n"
                       f"⭐ Top Players: {top_str}")
                messages.append(msg)

    if messages:
        await update.message.reply_text("\n\n".join(messages))
    else:
        await update.message.reply_text("No high-value matches today.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("today", today))
    app.run_polling()
