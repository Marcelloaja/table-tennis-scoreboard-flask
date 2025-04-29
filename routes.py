from flask import render_template, request, redirect, url_for, jsonify, flash
from app import app, db
from models import Player, Match
import logging
import json
import os

@app.route('/')
def index():
    """Render the homepage with player name input form"""
    return render_template('index.html')

@app.route('/scoreboard', methods=['POST'])
def create_scoreboard():
    """Create a new scoreboard with the provided player names"""
    player1_name = request.form.get('player1', '').strip()
    player2_name = request.form.get('player2', '').strip()
    max_sets = int(request.form.get('max_sets', 3))
    first_server = request.form.get('first_server', 'player1')
    
    # Validate player names
    if not player1_name or not player2_name:
        flash('Both player names are required', 'danger')
        return redirect(url_for('index'))
    
    if player1_name == player2_name:
        flash('Players must have different names', 'danger')
        return redirect(url_for('index'))
    
    # Validate max_sets (should be 3 or 5)
    if max_sets not in [3, 5]:
        max_sets = 3  # Default to 3 if invalid
    
    # Check if players exist in database, create if not
    player1 = Player.query.filter_by(name=player1_name).first()
    if not player1:
        player1 = Player(name=player1_name)
        db.session.add(player1)
    
    player2 = Player.query.filter_by(name=player2_name).first()
    if not player2:
        player2 = Player(name=player2_name)
        db.session.add(player2)
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash(f'Error creating players: {str(e)}', 'danger')
        return redirect(url_for('index'))
    
    # Determine the first server
    first_server_id = player1.id if first_server == 'player1' else player2.id
    
    return render_template('scoreboard.html', 
                           player1=player1, 
                           player2=player2, 
                           max_sets=max_sets,
                           first_server_id=first_server_id)

@app.route('/leaderboard')
def leaderboard():
    """Display the leaderboard of top players"""
    top_players = Player.query.order_by(Player.wins.desc()).all()
    # Get recent matches
    recent_matches = Match.query.order_by(Match.match_date.desc()).limit(50).all()
    return render_template('leaderboard.html', top_players=top_players, recent_matches=recent_matches)

@app.route('/finish_match', methods=['POST'])
def finish_match():
    """Save the match result to the database"""
    data = request.get_json()
    
    try:
        player1_id = int(data.get('player1_id'))
        player2_id = int(data.get('player2_id'))
        player1_sets = int(data.get('player1_sets'))
        player2_sets = int(data.get('player2_sets'))
        winner_id = int(data.get('winner_id'))
        set_scores = data.get('set_scores', '[]')
        max_sets = int(data.get('max_sets', 3))
        first_server = int(data.get('first_server'))
        
        # Get player objects
        player1 = Player.query.get(player1_id)
        player2 = Player.query.get(player2_id)
        
        if not player1 or not player2:
            return jsonify({'success': False, 'message': 'Players not found'}), 404
        
        # Update player stats
        player1.matches_played += 1
        player2.matches_played += 1
        
        if winner_id == player1_id:
            player1.wins += 1
        else:
            player2.wins += 1
        
        # Create new match record
        new_match = Match(
            player1_id=player1_id,
            player2_id=player2_id,
            player1_sets=player1_sets,
            player2_sets=player2_sets,
            winner_id=winner_id,
            set_scores=set_scores,
            max_sets=max_sets,
            first_server=first_server
        )
        
        db.session.add(new_match)
        db.session.commit()
        
        # Save to JSON files
        Player.save_to_json()
        Match.save_to_json()
        
        return jsonify({'success': True, 'redirect': url_for('recent_matches')})
    
    except Exception as e:
        logging.error(f"Error in finish_match: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/recent')
def recent_matches():
    """Display recent matches with detailed set scores"""
    matches = Match.query.order_by(Match.match_date.desc()).all()
    return render_template('recent.html', matches=matches)

@app.route('/reset_data', methods=['POST'])
def reset_data():
    """Reset all data in the database"""
    try:
        # Delete all matches
        Match.query.delete()
        
        # Reset player stats or delete players
        if request.form.get('delete_players') == 'true':
            Player.query.delete()
        else:
            players = Player.query.all()
            for player in players:
                player.wins = 0
                player.matches_played = 0
        
        db.session.commit()
        
        # Delete JSON files
        if os.path.exists('players.json'):
            os.remove('players.json')
        if os.path.exists('matches.json'):
            os.remove('matches.json')
            
        flash('All data has been reset successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error resetting data: {str(e)}', 'danger')
    
    return redirect(url_for('leaderboard'))
