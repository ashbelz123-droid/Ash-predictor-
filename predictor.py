def calculate_confidence(home_form, away_form, h2h_score,
                         home_players_score, away_players_score,
                         injuries_home=0, injuries_away=0,
                         odds=2.0):
    form_score = sum(home_form)/len(home_form) - sum(away_form)/len(away_form)
    player_score = (sum(home_players_score.values()) - sum(away_players_score.values())) / 10
    injury_score = (injuries_away - injuries_home)/5
    odds_prob = 1 / odds
    confidence = 0.3*form_score + 0.25*h2h_score + 0.25*player_score + 0.1*injury_score + 0.1*(1-odds_prob)
    return max(0, min(confidence,1))

def is_high_value(confidence, odds, threshold=0.9):
    implied_prob = 1 / odds
    value_score = confidence - implied_prob
    return confidence >= threshold and value_score > 0
