// Game state
const gameState = {
    players: [
        { x: 1, y: 1, color: '#4deeea' }, // Player 1
        { x: 1, y: 1, color: '#f000ff' }  // Player 2 (same position)
    ],
    currentPlayer: 0,
    diceRoll: 0,
    movesLeft: 0,
    board: {
        width: 12,
        height: 10,
        tileSize: 50
    },
    // Define the path through the spaceship (non-red squares are safe)
    alienSquares: [
        { x: 3, y: 2 },
        { x: 7, y: 3 },
        { x: 5, y: 5 },
        { x: 2, y: 7 },
        { x: 8, y: 6 },
        { x: 10, y: 4 },
        { x: 4, y: 8 }
    ],
    // Define walls/obstacles in the spaceship
    walls: [
        { x: 0, y: 0, width: 12, height: 1 }, // Top wall
        { x: 0, y: 9, width: 12, height: 1 }, // Bottom wall
        { x: 0, y: 0, width: 1, height: 10 }, // Left wall
        { x: 11, y: 0, width: 1, height: 10 }, // Right wall
        { x: 3, y: 4, width: 2, height: 1 }, // Interior walls
        { x: 7, y: 5, width: 1, height: 2 },
        { x: 5, y: 3, width: 1, height: 2 }
    ],
    gameLog: []
};

// DOM elements
const canvas = document.getElementById('game-board');
const ctx = canvas.getContext('2d');
const rollDiceBtn = document.getElementById('roll-dice');
const diceResult = document.getElementById('dice-result');
const movesLeftSpan = document.getElementById('moves-left');
const moveUpBtn = document.getElementById('move-up');
const moveDownBtn = document.getElementById('move-down');
const moveLeftBtn = document.getElementById('move-left');
const moveRightBtn = document.getElementById('move-right');
const alienModal = document.getElementById('alien-modal');
const closeModal = document.querySelector('.close-modal');
const battleAlienBtn = document.getElementById('battle-alien');
const gameLog = document.getElementById('game-log');

// Load background image
const backgroundImage = new Image();
backgroundImage.src = 'images/spaceship-interior.jpg';

// Initialize game
function initGame() {
    drawBoard();
    setupEventListeners();
    addToLog("Game started! Players are in the starting position.");
}

// Draw the game board
function drawBoard() {
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Draw background image
    if (backgroundImage.complete) {
        ctx.drawImage(backgroundImage, 0, 0, canvas.width, canvas.height);
    } else {
        // Fallback background if image hasn't loaded
        ctx.fillStyle = '#1a1a3a';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
    }
    
    // Draw a semi-transparent overlay for better visibility
    ctx.fillStyle = 'rgba(26, 26, 58, 0.7)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Draw grid lines (faint for reference)
    ctx.strokeStyle = 'rgba(77, 238, 234, 0.2)';
    ctx.lineWidth = 1;
    
    for (let x = 0; x <= gameState.board.width; x++) {
        ctx.beginPath();
        ctx.moveTo(x * gameState.board.tileSize, 0);
        ctx.lineTo(x * gameState.board.tileSize, canvas.height);
        ctx.stroke();
    }
    
    for (let y = 0; y <= gameState.board.height; y++) {
        ctx.beginPath();
        ctx.moveTo(0, y * gameState.board.tileSize);
        ctx.lineTo(canvas.width, y * gameState.board.tileSize);
        ctx.stroke();
    }
    
    // Draw walls/obstacles
    gameState.walls.forEach(wall => {
        ctx.fillStyle = 'rgba(100, 100, 150, 0.7)';
        ctx.fillRect(
            wall.x * gameState.board.tileSize, 
            wall.y * gameState.board.tileSize, 
            wall.width * gameState.board.tileSize, 
            wall.height * gameState.board.tileSize
        );
        
        // Draw wall pattern
        ctx.strokeStyle = 'rgba(77, 238, 234, 0.5)';
        ctx.lineWidth = 2;
        ctx.strokeRect(
            wall.x * gameState.board.tileSize, 
            wall.y * gameState.board.tileSize, 
            wall.width * gameState.board.tileSize, 
            wall.height * gameState.board.tileSize
        );
    });
    
    // Draw alien squares (red squares)
    gameState.alienSquares.forEach(square => {
        ctx.fillStyle = 'rgba(255, 0, 0, 0.5)';
        ctx.beginPath();
        ctx.arc(
            square.x * gameState.board.tileSize + gameState.board.tileSize/2,
            square.y * gameState.board.tileSize + gameState.board.tileSize/2,
            gameState.board.tileSize/2 - 5,
            0,
            Math.PI * 2
        );
        ctx.fill();
        
        // Draw alien icon
        ctx.fillStyle = '#f000ff';
        ctx.font = '20px Arial';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('👾', 
            square.x * gameState.board.tileSize + gameState.board.tileSize/2,
            square.y * gameState.board.tileSize + gameState.board.tileSize/2
        );
    });
    
    // Draw players
    gameState.players.forEach((player, index) => {
        ctx.fillStyle = player.color;
        ctx.beginPath();
        ctx.arc(
            player.x * gameState.board.tileSize + gameState.board.tileSize/2,
            player.y * gameState.board.tileSize + gameState.board.tileSize/2,
            gameState.board.tileSize/3,
            0,
            Math.PI * 2
        );
        ctx.fill();
        
        // Player number
        ctx.fillStyle = '#000';
        ctx.font = 'bold 16px Arial';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(
            (index + 1).toString(),
            player.x * gameState.board.tileSize + gameState.board.tileSize/2,
            player.y * gameState.board.tileSize + gameState.board.tileSize/2
        );
    });
    
    // Draw starting position
    ctx.fillStyle = 'rgba(0, 255, 0, 0.3)';
    ctx.fillRect(
        gameState.players[0].x * gameState.board.tileSize,
        gameState.players[0].y * gameState.board.tileSize,
        gameState.board.tileSize,
        gameState.board.tileSize
    );
    
    ctx.fillStyle = '#0f0';
    ctx.font = '12px Arial';
    ctx.fillText('START', 10, 15);
    
    // Draw exit/objective
    ctx.fillStyle = 'rgba(0, 255, 255, 0.3)';
    ctx.fillRect(
        (gameState.board.width - 2) * gameState.board.tileSize,
        (gameState.board.height - 2) * gameState.board.tileSize,
        gameState.board.tileSize,
        gameState.board.tileSize
    );
    
    ctx.fillStyle = '#4deeea';
    ctx.font = '12px Arial';
    ctx.fillText('EXIT', canvas.width - 40, canvas.height - 10);
}

// Set up event listeners
function setupEventListeners() {
    rollDiceBtn.addEventListener('click', rollDice);
    moveUpBtn.addEventListener('click', () => movePlayer(0, -1));
    moveDownBtn.addEventListener('click', () => movePlayer(0, 1));
    moveLeftBtn.addEventListener('click', () => movePlayer(-1, 0));
    moveRightBtn.addEventListener('click', () => movePlayer(1, 0));
    closeModal.addEventListener('click', () => alienModal.style.display = 'none');
    battleAlienBtn.addEventListener('click', battleAlien);
    
    // Close modal when clicking outside
    window.addEventListener('click', (event) => {
        if (event.target === alienModal) {
            alienModal.style.display = 'none';
        }
    });
}

// Check if a position is blocked by a wall
function isPositionBlocked(x, y) {
    for (const wall of gameState.walls) {
        if (x >= wall.x && x < wall.x + wall.width &&
            y >= wall.y && y < wall.y + wall.height) {
            return true;
        }
    }
    return false;
}

// Roll dice function
function rollDice() {
    gameState.diceRoll = Math.floor(Math.random() * 6) + 1;
    gameState.movesLeft = gameState.diceRoll;
    
    diceResult.textContent = gameState.diceRoll;
    movesLeftSpan.textContent = gameState.movesLeft;
    
    // Enable movement buttons
    moveUpBtn.disabled = false;
    moveDownBtn.disabled = false;
    moveLeftBtn.disabled = false;
    moveRightBtn.disabled = false;
    
    // Disable roll dice button until moves are used
    rollDiceBtn.disabled = true;
    
    addToLog(`Dice rolled: ${gameState.diceRoll}. You have ${gameState.movesLeft} moves.`);
}

// Move player function
function movePlayer(dx, dy) {
    if (gameState.movesLeft <= 0) return;
    
    const newX = gameState.players[0].x + dx;
    const newY = gameState.players[0].y + dy;
    
    // Check if move is valid (within board boundaries and not blocked)
    if (newX >= 0 && newX < gameState.board.width && 
        newY >= 0 && newY < gameState.board.height &&
        !isPositionBlocked(newX, newY)) {
        
        // Update both players' positions (they move together)
        gameState.players[0].x = newX;
        gameState.players[0].y = newY;
        gameState.players[1].x = newX;
        gameState.players[1].y = newY;
        
        gameState.movesLeft--;
        movesLeftSpan.textContent = gameState.movesLeft;
        
        addToLog(`Moved to position (${newX}, ${newY}). Moves left: ${gameState.movesLeft}`);
        
        // Redraw board with new positions
        drawBoard();
        
        // Check if landed on alien square
        checkAlienEncounter();
        
        // Check if reached the exit
        if (newX === gameState.board.width - 2 && newY === gameState.board.height - 2) {
            addToLog("Congratulations! You've reached the exit and completed your mission!");
            // You could add a victory modal here
        }
        
        // If no moves left, enable roll dice button
        if (gameState.movesLeft === 0) {
            moveUpBtn.disabled = true;
            moveDownBtn.disabled = true;
            moveLeftBtn.disabled = true;
            moveRightBtn.disabled = true;
            rollDiceBtn.disabled = false;
            addToLog("All moves used. Roll the dice again!");
        }
    } else {
        addToLog("Invalid move! Can't move there.");
    }
}

// Check if players landed on an alien square
function checkAlienEncounter() {
    const currentPos = { x: gameState.players[0].x, y: gameState.players[0].y };
    
    for (const square of gameState.alienSquares) {
        if (square.x === currentPos.x && square.y === currentPos.y) {
            // Found an alien square
            alienModal.style.display = 'flex';
            addToLog("Alien encounter! Prepare for battle.");
            return;
        }
    }
}

// Battle alien function
function battleAlien() {
    // Simple battle logic - 80% chance of success
    const battleSuccess = Math.random() < 0.8;
    
    if (battleSuccess) {
        addToLog("You defeated the alien! Well done team!");
    } else {
        addToLog("The alien got away! Be careful next time.");
    }
    
    alienModal.style.display = 'none';
}

// Add message to game log
function addToLog(message) {
    const logEntry = document.createElement('div');
    logEntry.className = 'log-entry';
    logEntry.textContent = message;
    gameLog.appendChild(logEntry);
    gameLog.scrollTop = gameLog.scrollHeight;
}

// Initialize the game when page loads
window.onload = initGame;
