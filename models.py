from extensions import db
from datetime import datetime
import json

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    wins = db.Column(db.Integer, default=0)
    matches_played = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Player {self.name}>'
    
    @staticmethod
    def save_to_json():
        players = Player.query.all()
        players_data = []
        for player in players:
            players_data.append({
                'id': player.id,
                'name': player.name,
                'wins': player.wins,
                'matches_played': player.matches_played,
                'created_at': player.created_at.isoformat()
            })
        with open('players.json', 'w') as f:
            json.dump(players_data, f, indent=4)

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player1_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    player2_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    player1_sets = db.Column(db.Integer, nullable=False)
    player2_sets = db.Column(db.Integer, nullable=False)
    winner_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    match_date = db.Column(db.DateTime, default=datetime.utcnow)
    set_scores = db.Column(db.String(255), nullable=False)
    max_sets = db.Column(db.Integer, default=3)
    first_server = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    
    player1 = db.relationship('Player', foreign_keys=[player1_id])
    player2 = db.relationship('Player', foreign_keys=[player2_id])
    winner = db.relationship('Player', foreign_keys=[winner_id])
    first_server_player = db.relationship('Player', foreign_keys=[first_server])
    
    def __repr__(self):
        return f'<Match {self.id}: {self.player1.name} vs {self.player2.name}>'
    
    def set_scores_list(self):
        try:
            return json.loads(self.set_scores)
        except:
            return []
    
    @staticmethod
    def save_to_json():
        matches = Match.query.all()
        matches_data = []
        for match in matches:
            matches_data.append({
                'id': match.id,
                'player1': match.player1.name,
                'player2': match.player2.name,
                'player1_sets': match.player1_sets,
                'player2_sets': match.player2_sets,
                'winner': match.winner.name,
                'match_date': match.match_date.isoformat(),
                'set_scores': match.set_scores_list(),
                'max_sets': match.max_sets,
                'first_server': match.first_server_player.name
            })
        with open('matches.json', 'w') as f:
            json.dump(matches_data, f, indent=4)
