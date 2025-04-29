document.addEventListener('DOMContentLoaded', function() {
    // Get match settings from hidden elements
    const maxSetsValue = parseInt(document.getElementById('max-sets').value) || 3;
    const firstServerId = document.getElementById('first-server-id').value;
    
    // Game state
    const state = {
        currentSet: 1,
        maxSets: maxSetsValue,
        setScores: [], // Store set scores history
        totalPoints: 0, // Track total points for serve switching
        currentServer: firstServerId,
        scores: {
            player1: {
                currentSet: 0,
                sets: 0
            },
            player2: {
                currentSet: 0,
                sets: 0
            }
        },
        gameOver: false
    };

    // DOM elements
    const player1ScoreElement = document.getElementById('player1-score');
    const player2ScoreElement = document.getElementById('player2-score');
    const player1SetsElement = document.getElementById('player1-sets');
    const player2SetsElement = document.getElementById('player2-sets');
    const currentSetElement = document.getElementById('current-set');
    const player1AddButton = document.getElementById('player1-add');
    const player2AddButton = document.getElementById('player2-add');
    const gameStatusElement = document.getElementById('game-status');
    const finishMatchButton = document.getElementById('finish-match');
    const restartButton = document.getElementById('restart-match');
    const totalPointsElement = document.getElementById('total-points');
    const player1ServerIndicator = document.getElementById('player1-server-indicator');
    const player2ServerIndicator = document.getElementById('player2-server-indicator');
    
    // Player info
    const player1Id = document.getElementById('player1-id').value;
    const player2Id = document.getElementById('player2-id').value;
    const player1Name = document.getElementById('player1-name').textContent;
    const player2Name = document.getElementById('player2-name').textContent;

    // Update the server indicators
    function updateServerIndicator() {
        // Hide both indicators first
        player1ServerIndicator.classList.add('d-none');
        player2ServerIndicator.classList.add('d-none');
        
        // Show the current server indicator
        if (state.currentServer == player1Id) {
            player1ServerIndicator.classList.remove('d-none');
        } else {
            player2ServerIndicator.classList.remove('d-none');
        }
    }
    
    // Handle server switching
    function switchServer() {
        // Calculate if server should switch (every 2 points)
        // After 20-20, service switches after each point
        const p1Score = state.scores.player1.currentSet;
        const p2Score = state.scores.player2.currentSet;
        
        if ((p1Score >= 10 && p2Score >= 10) || (state.totalPoints % 2 === 0)) {
            // Switch server
            state.currentServer = state.currentServer == player1Id ? player2Id : player1Id;
            updateServerIndicator();
        }
    }
    
    // Update display
    function updateDisplay() {
        player1ScoreElement.textContent = state.scores.player1.currentSet;
        player2ScoreElement.textContent = state.scores.player2.currentSet;
        player1SetsElement.textContent = state.scores.player1.sets;
        player2SetsElement.textContent = state.scores.player2.sets;
        currentSetElement.textContent = `Set ${state.currentSet}`;
        totalPointsElement.textContent = state.totalPoints;
        
        // Update server indicator
        updateServerIndicator();
        
        // Disable buttons if game is over
        if (state.gameOver) {
            player1AddButton.disabled = true;
            player2AddButton.disabled = true;
            finishMatchButton.classList.remove('d-none');
        }
    }

    // Check if a player has won the current set
    function checkSetWinner() {
        const p1Score = state.scores.player1.currentSet;
        const p2Score = state.scores.player2.currentSet;
        
        // A player needs at least 11 points and a 2-point lead to win
        if ((p1Score >= 11 && p1Score - p2Score >= 2) || (p2Score >= 11 && p2Score - p1Score >= 2)) {
            // Save the set scores before resetting
            state.setScores.push({
                player1_score: p1Score,
                player2_score: p2Score
            });
            
            // Determine set winner
            if (p1Score > p2Score) {
                state.scores.player1.sets++;
                gameStatusElement.textContent = `${player1Name} wins set ${state.currentSet}!`;
            } else {
                state.scores.player2.sets++;
                gameStatusElement.textContent = `${player2Name} wins set ${state.currentSet}!`;
            }
            
            // Calculate sets needed to win based on match format (best of 3 or best of 5)
            const setsToWin = Math.ceil(state.maxSets / 2);
            
            // Check if match is over
            if (state.scores.player1.sets >= setsToWin || state.scores.player2.sets >= setsToWin) {
                endMatch();
            } else {
                // Move to next set
                state.currentSet++;
                state.scores.player1.currentSet = 0;
                state.scores.player2.currentSet = 0;
                state.totalPoints = 0;
                
                // Service alternates between players at the start of each set
                state.currentServer = (state.currentSet % 2 === 1) ? 
                    firstServerId : 
                    (firstServerId == player1Id ? player2Id : player1Id);
                
                // Give users time to see the set winner message
                setTimeout(() => {
                    gameStatusElement.textContent = `Starting set ${state.currentSet}`;
                    updateDisplay();
                }, 2000);
            }
            
            updateDisplay();
            return true;
        }
        
        return false;
    }

    // End the match
    function endMatch() {
        state.gameOver = true;
        
        if (state.scores.player1.sets > state.scores.player2.sets) {
            gameStatusElement.textContent = `Match over! ${player1Name} wins the match!`;
        } else {
            gameStatusElement.textContent = `Match over! ${player2Name} wins the match!`;
        }
        
        updateDisplay();
    }

    // Event listeners for score buttons
    player1AddButton.addEventListener('click', function() {
        if (state.gameOver) return;
        
        state.scores.player1.currentSet++;
        state.totalPoints++;
        
        // Check server switching
        switchServer();
        updateDisplay();
        
        if (!checkSetWinner()) {
            gameStatusElement.textContent = `Playing set ${state.currentSet}`;
        }
    });

    player2AddButton.addEventListener('click', function() {
        if (state.gameOver) return;
        
        state.scores.player2.currentSet++;
        state.totalPoints++;
        
        // Check server switching
        switchServer();
        updateDisplay();
        
        if (!checkSetWinner()) {
            gameStatusElement.textContent = `Playing set ${state.currentSet}`;
        }
    });

    // Finish match button - save results to database
    finishMatchButton.addEventListener('click', function() {
        if (!state.gameOver) return;
        
        const winnerId = state.scores.player1.sets > state.scores.player2.sets ? 
            player1Id : player2Id;
        
        const matchData = {
            player1_id: player1Id,
            player2_id: player2Id,
            player1_sets: state.scores.player1.sets,
            player2_sets: state.scores.player2.sets,
            winner_id: winnerId,
            set_scores: JSON.stringify(state.setScores),
            max_sets: state.maxSets,
            first_server: firstServerId
        };
        
        // Send data to server using fetch
        fetch('/finish_match', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(matchData),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = data.redirect;
            } else {
                alert('Error saving match: ' + data.message);
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            alert('An error occurred while saving the match.');
        });
    });

    // Restart match button
    restartButton.addEventListener('click', function() {
        // Reset game state
        state.currentSet = 1;
        state.scores.player1.currentSet = 0;
        state.scores.player1.sets = 0;
        state.scores.player2.currentSet = 0;
        state.scores.player2.sets = 0;
        state.gameOver = false;
        state.setScores = [];
        state.totalPoints = 0;
        state.currentServer = firstServerId;
        
        // Enable score buttons
        player1AddButton.disabled = false;
        player2AddButton.disabled = false;
        finishMatchButton.classList.add('d-none');
        
        gameStatusElement.textContent = 'Starting new match';
        updateDisplay();
    });

    // Initialize the display
    updateDisplay();
    gameStatusElement.textContent = 'Match started! First to win 2 sets.';
});
