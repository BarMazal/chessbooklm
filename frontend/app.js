// SVG Paths for Neoclassic Chess Pieces
const PIECE_SVGS = {
    'wP': '<svg viewBox="0 0 45 45" class="piece-svg"><path d="M 22.5,9 C 19.74,9 17.5,11.24 17.5,14 C 17.5,15.24 17.95,16.37 18.72,17.25 C 16.5,18.06 15,20.14 15,22.5 C 15,24.3 15.89,25.89 17.25,26.88 C 14.88,27.88 13.25,30.2 13,33 L 32,33 C 31.75,30.2 30.12,27.88 27.75,26.88 C 29.11,25.89 30,24.3 30,22.5 C 30,20.14 28.5,18.06 26.28,17.25 C 27.05,16.37 27.5,15.24 27.5,14 C 27.5,11.24 25.26,9 22.5,9 z" fill="#ffffff" stroke="#000000" stroke-width="1.5" stroke-linecap="round"/></svg>',
    'wN': '<svg viewBox="0 0 45 45" class="piece-svg"><path d="M 22,10 C 32.5,11 38.5,18 38,39 L 15,39 C 15,30 25,32.5 23,18" fill="#ffffff" stroke="#000000" stroke-width="1.5"/><path d="M 24,18 C 24.38,20.91 18.45,25.37 16,27 C 13,29 13.18,31.34 11,31 C 9.95,30.83 6.58,28.69 7,26 C 7.42,23.31 9.47,21.6 12,21 C 14.53,20.4 16,15 22,10 z" fill="#ffffff" stroke="#000000" stroke-width="1.5"/><circle cx="14.5" cy="18.5" r="1.5" fill="#000000"/></svg>',
    'wB': '<svg viewBox="0 0 45 45" class="piece-svg"><g fill="#ffffff" stroke="#000000" stroke-width="1.5" stroke-linecap="round"><path d="M 9,36 C 12.39,35.03 19.11,36.43 22.5,34 C 25.89,36.43 32.61,35.03 36,36 C 36,36 37.65,36.54 39,38 C 38.32,38.97 37.35,38.99 36,38.5 C 32.61,37.53 25.89,38.96 22.5,37.5 C 19.11,38.96 12.39,37.53 9,38.5 C 7.646,38.99 6.677,38.97 6,38 C 7.354,36.54 9,36 9,36 z"/><path d="M 15,32 C 17.5,34.5 27.5,34.5 30,32 C 30.5,30.5 30,28.5 28.5,27 C 27.5,25.5 26.5,24.5 26.5,22 C 26.5,19.5 27.5,17 26.5,15 C 25.5,13 23.5,11.5 22.5,11.5 C 21.5,11.5 19.5,13 18.5,15 C 17.5,17 18.5,19.5 18.5,22 C 18.5,24.5 17.5,25.5 16.5,27 C 15,28.5 14.5,30.5 15,32 z"/><circle cx="22.5" cy="8.5" r="2.5"/></g></svg>',
    'wR': '<svg viewBox="0 0 45 45" class="piece-svg"><g fill="#ffffff" stroke="#000000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M 9,39 L 36,39 L 36,36 L 9,36 z"/><path d="M 12,36 L 12,32 L 33,32 L 33,36 z"/><path d="M 11,14 L 11,9 L 15,9 L 15,11 L 20,11 L 20,9 L 25,9 L 25,11 L 30,11 L 30,9 L 34,9 L 34,14 z"/><path d="M 12,14 L 33,14 L 31,32 L 14,32 z"/></g></svg>',
    'wQ': '<svg viewBox="0 0 45 45" class="piece-svg"><g fill="#ffffff" stroke="#000000" stroke-width="1.5" stroke-linecap="round"><path d="M 9,26 C 17.5,24.5 30,24.5 36,26 C 36,33 28,34 22.5,34 C 17,34 9,33 9,26 z"/><path d="M 9,26 C 9,28 10.5,28 11.5,30 C 12.5,32 12.5,31 12,33.5 C 10.5,34.5 10.5,36 10.5,36 C 9,36 9,38 11,38.5 C 16,39.5 29,39.5 34,38.5 C 36,38 36,36 34.5,36 C 34.5,36 34.5,34.5 33,33.5 C 32.5,31 32.5,32 33.5,30 C 34.5,28 36,28 36,26"/><path d="M 9,26 L 9,15 L 15.5,20 L 22.5,10 L 29.5,20 L 36,15 L 36,26"/><circle cx="9" cy="13" r="2"/><circle cx="15.5" cy="18" r="2"/><circle cx="22.5" cy="8" r="2"/><circle cx="29.5" cy="18" r="2"/><circle cx="36" cy="13" r="2"/></g></svg>',
    'wK': '<svg viewBox="0 0 45 45" class="piece-svg"><g fill="#ffffff" stroke="#000000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M 22.5,11.63 L 22.5,6 M 19.5,8.63 L 25.5,8.63"/><path d="M 22.5,25 C 22.5,25 27,17.5 25.5,14.5 C 24,11.5 21,11.5 19.5,14.5 C 18,17.5 22.5,25 22.5,25 z"/><path d="M 11.5,37 C 17,40.5 28,40.5 33.5,37 C 37.5,30.5 31.5,28.5 22.5,28.5 C 13.5,28.5 7.5,30.5 11.5,37 z"/></g></svg>',

    'bP': '<svg viewBox="0 0 45 45" class="piece-svg"><path d="M 22.5,9 C 19.74,9 17.5,11.24 17.5,14 C 17.5,15.24 17.95,16.37 18.72,17.25 C 16.5,18.06 15,20.14 15,22.5 C 15,24.3 15.89,25.89 17.25,26.88 C 14.88,27.88 13.25,30.2 13,33 L 32,33 C 31.75,30.2 30.12,27.88 27.75,26.88 C 29.11,25.89 30,24.3 30,22.5 C 30,20.14 28.5,18.06 26.28,17.25 C 27.05,16.37 27.5,15.24 27.5,14 C 27.5,11.24 25.26,9 22.5,9 z" fill="#312e2b" stroke="#ffffff" stroke-width="1.5" stroke-linecap="round"/></svg>',
    'bN': '<svg viewBox="0 0 45 45" class="piece-svg"><path d="M 22,10 C 32.5,11 38.5,18 38,39 L 15,39 C 15,30 25,32.5 23,18" fill="#312e2b" stroke="#ffffff" stroke-width="1.5"/><path d="M 24,18 C 24.38,20.91 18.45,25.37 16,27 C 13,29 13.18,31.34 11,31 C 9.95,30.83 6.58,28.69 7,26 C 7.42,23.31 9.47,21.6 12,21 C 14.53,20.4 16,15 22,10 z" fill="#312e2b" stroke="#ffffff" stroke-width="1.5"/><circle cx="14.5" cy="18.5" r="1.5" fill="#ffffff"/></svg>',
    'bB': '<svg viewBox="0 0 45 45" class="piece-svg"><g fill="#312e2b" stroke="#ffffff" stroke-width="1.5" stroke-linecap="round"><path d="M 9,36 C 12.39,35.03 19.11,36.43 22.5,34 C 25.89,36.43 32.61,35.03 36,36 C 36,36 37.65,36.54 39,38 C 38.32,38.97 37.35,38.99 36,38.5 C 32.61,37.53 25.89,38.96 22.5,37.5 C 19.11,38.96 12.39,37.53 9,38.5 C 7.646,38.99 6.677,38.97 6,38 C 7.354,36.54 9,36 9,36 z"/><path d="M 15,32 C 17.5,34.5 27.5,34.5 30,32 C 30.5,30.5 30,28.5 28.5,27 C 27.5,25.5 26.5,24.5 26.5,22 C 26.5,19.5 27.5,17 26.5,15 C 25.5,13 23.5,11.5 22.5,11.5 C 21.5,11.5 19.5,13 18.5,15 C 17.5,17 18.5,19.5 18.5,22 C 18.5,24.5 17.5,25.5 16.5,27 C 15,28.5 14.5,30.5 15,32 z"/><circle cx="22.5" cy="8.5" r="2.5"/></g></svg>',
    'bR': '<svg viewBox="0 0 45 45" class="piece-svg"><g fill="#312e2b" stroke="#ffffff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M 9,39 L 36,39 L 36,36 L 9,36 z"/><path d="M 12,36 L 12,32 L 33,32 L 33,36 z"/><path d="M 11,14 L 11,9 L 15,9 L 15,11 L 20,11 L 20,9 L 25,9 L 25,11 L 30,11 L 30,9 L 34,9 L 34,14 z"/><path d="M 12,14 L 33,14 L 31,32 L 14,32 z"/></g></svg>',
    'bQ': '<svg viewBox="0 0 45 45" class="piece-svg"><g fill="#312e2b" stroke="#ffffff" stroke-width="1.5" stroke-linecap="round"><path d="M 9,26 C 17.5,24.5 30,24.5 36,26 C 36,33 28,34 22.5,34 C 17,34 9,33 9,26 z"/><path d="M 9,26 C 9,28 10.5,28 11.5,30 C 12.5,32 12.5,31 12,33.5 C 10.5,34.5 10.5,36 10.5,36 C 9,36 9,38 11,38.5 C 16,39.5 29,39.5 34,38.5 C 36,38 36,36 34.5,36 C 34.5,36 34.5,34.5 33,33.5 C 32.5,31 32.5,32 33.5,30 C 34.5,28 36,28 36,26"/><path d="M 9,26 L 9,15 L 15.5,20 L 22.5,10 L 29.5,20 L 36,15 L 36,26"/><circle cx="9" cy="13" r="2"/><circle cx="15.5" cy="18" r="2"/><circle cx="22.5" cy="8" r="2"/><circle cx="29.5" cy="18" r="2"/><circle cx="36" cy="13" r="2"/></g></svg>',
    'bK': '<svg viewBox="0 0 45 45" class="piece-svg"><g fill="#312e2b" stroke="#ffffff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M 22.5,11.63 L 22.5,6 M 19.5,8.63 L 25.5,8.63"/><path d="M 22.5,25 C 22.5,25 27,17.5 25.5,14.5 C 24,11.5 21,11.5 19.5,14.5 C 18,17.5 22.5,25 22.5,25 z"/><path d="M 11.5,37 C 17,40.5 28,40.5 33.5,37 C 37.5,30.5 31.5,28.5 22.5,28.5 C 13.5,28.5 7.5,30.5 11.5,37 z"/></g></svg>'
};

// Initial Chess State
let boardState = {};
let currentFen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1";
let moveHistory = []; // list of SAN strings
let moveStackUci = [];
let selectedSquare = null;
let legalMoves = [];
let isFlipped = false;
let lastMoveSquares = [];
let bestMoveArrow = null;
let currentNotebookId = "";

// DOM Elements
const chessboardEl = document.getElementById('chessboard');
const arrowsSvgEl = document.getElementById('board-arrows-svg');
const evalWhiteFillEl = document.getElementById('eval-white-fill');
const evalScoreBadgeEl = document.getElementById('eval-score-badge');
const openingNameEl = document.getElementById('opening-name');
const turnBadgeEl = document.getElementById('turn-badge');
const summaryEvalEl = document.getElementById('summary-eval');
const summaryBestMoveEl = document.getElementById('summary-best-move');
const engineLinesListEl = document.getElementById('engine-lines-list');
const moveHistoryTbodyEl = document.getElementById('move-history-tbody');
const mentorResponseAreaEl = document.getElementById('mentor-response-area');
const mentorProviderBadgeEl = document.getElementById('mentor-provider-badge');
const mentorNotebookSelectEl = document.getElementById('mentor-notebook-select');
const accountAuthTagEl = document.getElementById('account-auth-tag');
const cookiesModalEl = document.getElementById('cookies-modal');

// Initial Setup
document.addEventListener('DOMContentLoaded', () => {
    initTabs();
    initBoard();
    parseFenToState(currentFen);
    renderBoard();
    updatePositionEvaluation();
    checkAppStatus();
    loadNotebooksList();

    // Board controls
    document.getElementById('btn-flip').addEventListener('click', toggleFlip);
    document.getElementById('btn-undo').addEventListener('click', undoMove);
    document.getElementById('btn-reset').addEventListener('click', resetBoard);
    document.getElementById('btn-bot-move').addEventListener('click', makeBotMove);

    // Mentor quick buttons
    document.getElementById('btn-explain-pos').addEventListener('click', () => requestMentorInsight("Explain the overall strategic theme, pawn structures, and piece activity for both sides in this position."));
    document.getElementById('btn-why-best').addEventListener('click', () => requestMentorInsight("Why does the engine recommend this specific move? What tactical or positional idea is behind it?"));
    document.getElementById('btn-strategic-plan').addEventListener('click', () => requestMentorInsight("What are Black and White's long term strategic goals, pawn breaks, and attack plans from our chess books?"));
    document.getElementById('btn-blunder-check').addEventListener('click', () => requestMentorInsight("Check if there are any immediate tactical blunders, undefended pieces, or king safety vulnerabilities."));
    document.getElementById('btn-ask-mentor').addEventListener('click', handleCustomMentorQuery);

    // NotebookLM Account & Select controls
    mentorNotebookSelectEl.addEventListener('change', handleSelectNotebook);
    document.getElementById('btn-refresh-notebooks').addEventListener('click', loadNotebooksList);
    document.getElementById('btn-login-fresh').addEventListener('click', handleLoginFresh);
    document.getElementById('btn-logout-notebooklm').addEventListener('click', handleLogoutNotebookLM);
    document.getElementById('btn-import-cookies').addEventListener('click', openCookiesModal);

    // Cookies modal handlers
    document.getElementById('btn-close-cookies-modal').addEventListener('click', closeCookiesModal);
    document.getElementById('btn-cancel-cookies').addEventListener('click', closeCookiesModal);
    document.getElementById('btn-submit-cookies').addEventListener('click', handleSubmitCookies);

    // Settings save
    document.getElementById('btn-save-settings').addEventListener('click', saveSettings);
});

function initTabs() {
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            btn.classList.add('active');
            document.getElementById(btn.dataset.tab).classList.add('active');
        });
    });
}

function initBoard() {
    chessboardEl.innerHTML = '';
    const files = ['a','b','c','d','e','f','g','h'];
    const ranks = ['8','7','6','5','4','3','2','1'];

    const renderRanks = isFlipped ? [...ranks].reverse() : ranks;
    const renderFiles = isFlipped ? [...files].reverse() : files;

    renderRanks.forEach((r, rIdx) => {
        renderFiles.forEach((f, fIdx) => {
            const sqName = `${f}${r}`;
            const isLight = (rIdx + fIdx) % 2 === 0;
            
            const squareEl = document.createElement('div');
            squareEl.className = `square ${isLight ? 'light' : 'dark'}`;
            squareEl.dataset.square = sqName;

            if (fIdx === 0) {
                const rLabel = document.createElement('span');
                rLabel.className = 'coord-label coord-rank';
                rLabel.textContent = r;
                squareEl.appendChild(rLabel);
            }
            if (rIdx === 7) {
                const fLabel = document.createElement('span');
                fLabel.className = 'coord-label coord-file';
                fLabel.textContent = f;
                squareEl.appendChild(fLabel);
            }

            squareEl.addEventListener('click', () => handleSquareClick(sqName));
            chessboardEl.appendChild(squareEl);
        });
    });
}

function toggleFlip() {
    isFlipped = !isFlipped;
    initBoard();
    renderBoard();
}

function parseFenToState(fen) {
    if (!fen || typeof fen !== 'string') return;
    boardState = {};
    const parts = fen.split(' ');
    if (!parts[0]) return;
    const rows = parts[0].split('/');

    const files = ['a','b','c','d','e','f','g','h'];
    const ranks = ['8','7','6','5','4','3','2','1'];

    rows.forEach((row, rIdx) => {
        let fIdx = 0;
        for (let char of row) {
            if (!isNaN(char)) {
                fIdx += parseInt(char);
            } else {
                const color = char === char.toUpperCase() ? 'w' : 'b';
                const pieceType = char.toUpperCase();
                const sq = `${files[fIdx]}${ranks[rIdx]}`;
                boardState[sq] = `${color}${pieceType}`;
                fIdx++;
            }
        }
    });

    const activeTurn = parts[1] === 'w' ? 'White' : 'Black';
    turnBadgeEl.textContent = `${activeTurn} to move`;
    turnBadgeEl.className = `turn-badge ${activeTurn.toLowerCase()}`;
}

function renderBoard() {
    document.querySelectorAll('.square').forEach(sqEl => {
        const sqName = sqEl.dataset.square;
        
        sqEl.querySelectorAll('.piece-svg, .move-dot').forEach(el => el.remove());
        sqEl.classList.remove('selected', 'highlight-light', 'highlight-dark');

        if (lastMoveSquares.includes(sqName)) {
            sqEl.classList.add(sqEl.classList.contains('light') ? 'highlight-light' : 'highlight-dark');
        }

        if (selectedSquare === sqName) {
            sqEl.classList.add('selected');
        }

        const targetMove = legalMoves.find(m => m.uci.startsWith(selectedSquare) && m.uci.slice(2,4) === sqName);
        if (selectedSquare && targetMove) {
            const dotEl = document.createElement('div');
            dotEl.className = 'move-dot';
            sqEl.appendChild(dotEl);
        }

        if (boardState[sqName] && PIECE_SVGS[boardState[sqName]]) {
            const wrapper = document.createElement('div');
            wrapper.innerHTML = PIECE_SVGS[boardState[sqName]];
            sqEl.appendChild(wrapper.firstElementChild);
        }
    });

    drawBestMoveArrow();
}

function drawBestMoveArrow() {
    arrowsSvgEl.innerHTML = '';
    if (!bestMoveArrow || bestMoveArrow.length < 4) return;

    const fromSq = bestMoveArrow.slice(0, 2);
    const toSq = bestMoveArrow.slice(2, 4);

    const fromEl = document.querySelector(`.square[data-square="${fromSq}"]`);
    const toEl = document.querySelector(`.square[data-square="${toSq}"]`);
    if (!fromEl || !toEl) return;

    const boardRect = chessboardEl.getBoundingClientRect();
    const fromRect = fromEl.getBoundingClientRect();
    const toRect = toEl.getBoundingClientRect();

    const x1 = fromRect.left - boardRect.left + fromRect.width / 2;
    const y1 = fromRect.top - boardRect.top + fromRect.height / 2;
    const x2 = toRect.left - boardRect.left + toRect.width / 2;
    const y2 = toRect.top - boardRect.top + toRect.height / 2;

    const markerId = 'arrowhead-red';

    arrowsSvgEl.innerHTML = `
        <defs>
            <marker id="${markerId}" markerWidth="6" markerHeight="6" refX="4" refY="3" orient="auto">
                <polygon points="0 0, 6 3, 0 6" fill="#e74c3c" />
            </marker>
        </defs>
        <line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" 
              stroke="#e74c3c" stroke-width="6" stroke-linecap="round" 
              opacity="0.85" marker-end="url(#${markerId})" />
    `;
}

function handleSquareClick(sqName) {
    if (selectedSquare) {
        if (selectedSquare === sqName) {
            selectedSquare = null;
            renderBoard();
            return;
        }

        const matchMove = legalMoves.find(m => m.uci.startsWith(selectedSquare) && m.uci.slice(2,4) === sqName);
        if (matchMove) {
            executeMove(matchMove.san, matchMove.uci);
            selectedSquare = null;
            return;
        }
    }

    const activeColor = currentFen.split(' ')[1];
    if (boardState[sqName] && boardState[sqName].startsWith(activeColor)) {
        selectedSquare = sqName;
    } else {
        selectedSquare = null;
    }

    renderBoard();
}

async function executeMove(sanMove, uciMove) {
    moveHistory.push(sanMove);
    moveStackUci.push(uciMove);
    lastMoveSquares = [uciMove.slice(0,2), uciMove.slice(2,4)];

    await updatePositionEvaluation();
}

async function updatePositionEvaluation() {
    try {
        const resp = await fetch('/api/board/evaluate', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ fen: currentFen, moves: moveHistory })
        });
        const data = await resp.json();

        currentFen = data.fen;
        legalMoves = data.legal_moves || [];
        parseFenToState(currentFen);

        openingNameEl.textContent = data.opening || 'Custom Game';
        const scoreStr = data.eval.score;
        summaryEvalEl.textContent = scoreStr;
        evalScoreBadgeEl.textContent = scoreStr;
        summaryBestMoveEl.textContent = data.eval.best_move_san || '-';
        bestMoveArrow = data.eval.best_move;

        let whitePercentage = 50;
        if (data.eval.eval_type === 'mate') {
            whitePercentage = data.eval.eval_val > 0 ? 98 : 2;
        } else {
            const cp = data.eval.eval_val;
            whitePercentage = Math.min(98, Math.max(2, 50 + (cp * 10)));
        }
        evalWhiteFillEl.style.height = `${whitePercentage}%`;

        engineLinesListEl.innerHTML = '';
        (data.eval.top_moves || []).forEach(m => {
            const li = document.createElement('li');
            li.innerHTML = `<span class="move-san">${m.san}</span> <span class="move-score">${m.score || scoreStr}</span>`;
            engineLinesListEl.appendChild(li);
        });

        renderMoveHistoryTable();
        renderBoard();

    } catch (e) {
        console.error('Failed to update evaluation:', e);
    }
}

function renderMoveHistoryTable() {
    moveHistoryTbodyEl.innerHTML = '';
    for (let i = 0; i < moveHistory.length; i += 2) {
        const row = document.createElement('tr');
        const moveNum = Math.floor(i / 2) + 1;
        const whiteMove = moveHistory[i] || '';
        const blackMove = moveHistory[i + 1] || '';

        row.innerHTML = `
            <td><strong>${moveNum}.</strong></td>
            <td>${whiteMove}</td>
            <td>${blackMove}</td>
        `;
        moveHistoryTbodyEl.appendChild(row);
    }
    const container = document.getElementById('move-history-container');
    container.scrollTop = container.scrollHeight;
}

async function undoMove() {
    if (moveHistory.length === 0) return;
    moveHistory.pop();
    moveStackUci.pop();
    currentFen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1";
    lastMoveSquares = [];
    selectedSquare = null;
    await updatePositionEvaluation();
}

async function resetBoard() {
    currentFen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1";
    moveHistory = [];
    moveStackUci = [];
    lastMoveSquares = [];
    selectedSquare = null;
    await updatePositionEvaluation();
}

async function makeBotMove() {
    if (legalMoves.length === 0) return;
    const bestMoveObj = legalMoves.find(m => m.uci === bestMoveArrow) || legalMoves[0];
    await executeMove(bestMoveObj.san, bestMoveObj.uci);
}

async function loadNotebooksList() {
    mentorNotebookSelectEl.innerHTML = '<option value="">Loading notebooks...</option>';
    try {
        const resp = await fetch('/api/notebooks');
        const data = await resp.json();

        currentNotebookId = data.active_notebook_id || "";
        mentorNotebookSelectEl.innerHTML = '';

        if (!data.notebooks || data.notebooks.length === 0) {
            const opt = document.createElement('option');
            opt.value = "";
            opt.textContent = "No notebooks found (Please log in)";
            mentorNotebookSelectEl.appendChild(opt);
            return;
        }

        data.notebooks.forEach(nb => {
            const opt = document.createElement('option');
            opt.value = nb.id;
            opt.textContent = `${nb.title} (${nb.id.slice(0, 8)}...)`;
            if (nb.id === currentNotebookId || nb.is_active) {
                opt.selected = true;
                currentNotebookId = nb.id;
            }
            mentorNotebookSelectEl.appendChild(opt);
        });

        document.getElementById('setting-notebook-id').value = currentNotebookId;

    } catch (e) {
        mentorNotebookSelectEl.innerHTML = '<option value="">Error loading notebooks</option>';
        console.error('Failed to load notebooks:', e);
    }
}

async function handleSelectNotebook() {
    const selectedId = mentorNotebookSelectEl.value;
    if (!selectedId) return;

    try {
        const resp = await fetch('/api/notebooks/select', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ notebook_id: selectedId })
        });
        const data = await resp.json();

        currentNotebookId = selectedId;
        document.getElementById('setting-notebook-id').value = selectedId;
        checkAppStatus();
    } catch (e) {
        alert('Failed to select notebook: ' + e.message);
    }
}

async function handleLoginFresh() {
    const emailVal = document.getElementById('login-email-input').value.trim();
    try {
        const resp = await fetch('/api/auth/login', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                email: emailVal || null,
                fresh: true
            })
        });
        const data = await resp.json();
        alert(data.message || 'Fresh login browser process launched! Please sign in with your Google Email & Password in the browser window.');
        setTimeout(checkAppStatus, 4000);
    } catch (e) {
        alert('Failed to trigger fresh login: ' + e.message);
    }
}

async function handleLogoutNotebookLM() {
    if (!confirm('Are you sure you want to log out of your Google NotebookLM account?')) return;
    try {
        const resp = await fetch('/api/auth/logout', { method: 'POST' });
        const data = await resp.json();
        alert(data.message || 'Logged out.');
        checkAppStatus();
        loadNotebooksList();
    } catch (e) {
        alert('Logout failed: ' + e.message);
    }
}

function openCookiesModal() {
    cookiesModalEl.classList.remove('hidden');
}

function closeCookiesModal() {
    cookiesModalEl.classList.add('hidden');
}

async function handleSubmitCookies() {
    const inputVal = document.getElementById('cookies-json-input').value.trim();
    if (!inputVal) {
        alert('Please paste valid cookies JSON.');
        return;
    }

    try {
        const resp = await fetch('/api/auth/import-cookies', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ cookies_json: inputVal })
        });
        const data = await resp.json();
        if (data.success) {
            alert(data.message);
            closeCookiesModal();
            checkAppStatus();
            loadNotebooksList();
        } else {
            alert(data.message);
        }
    } catch (e) {
        alert('Error importing cookies: ' + e.message);
    }
}

async function requestMentorInsight(customQuestion = null) {
    const selectedMode = document.querySelector('input[name="translator-mode"]:checked').value;
    mentorResponseAreaEl.innerHTML = '<p class="placeholder-text">Consulting NotebookLM & Chess Engine...</p>';

    try {
        const resp = await fetch('/api/mentor/explain', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                fen: currentFen,
                moves: moveHistory,
                mode: selectedMode,
                question: customQuestion,
                notebook_id: currentNotebookId
            })
        });
        const data = await resp.json();

        mentorProviderBadgeEl.textContent = data.provider || "Mentor";
        mentorResponseAreaEl.innerHTML = formatMarkdownToHtml(data.response || "");

    } catch (e) {
        mentorResponseAreaEl.innerHTML = `<p style="color:#e74c3c;">Failed to get AI mentor explanation: ${e.message}</p>`;
    }
}

function handleCustomMentorQuery() {
    const qEl = document.getElementById('mentor-custom-question');
    const question = qEl.value.trim();
    if (!question) return;
    requestMentorInsight(question);
}

function formatMarkdownToHtml(md) {
    if (!md || typeof md !== 'string') return '<p class="placeholder-text">No explanation content returned.</p>';
    let html = md
        .replace(/^### (.*$)/gim, '<h3>$1</h3>')
        .replace(/^## (.*$)/gim, '<h2>$1</h2>')
        .replace(/^\* (.*$)/gim, '<li>$1</li>')
        .replace(/^\- (.*$)/gim, '<li>$1</li>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/\n\n/g, '<br><br>');
    return html;
}

async function checkAppStatus() {
    try {
        const resp = await fetch('/api/status');
        const data = await resp.json();

        if (data.stockfish.has_local_binary) {
            document.getElementById('engine-status-text').textContent = 'Local Stockfish Ready';
        } else {
            document.getElementById('engine-status-text').textContent = 'Lichess Cloud Ready';
        }

        if (data.notebooklm.is_logged_in) {
            accountAuthTagEl.textContent = `Authenticated (${data.notebooklm.profile})`;
            accountAuthTagEl.className = 'account-auth-tag green';
            
            document.getElementById('notebook-status-text').textContent = `NotebookLM: ${data.notebooklm.notebook_id.slice(0, 8)}...`;
            document.getElementById('notebook-status-badge').querySelector('.status-dot').className = 'status-dot green';
        } else {
            accountAuthTagEl.textContent = 'Not Logged In';
            accountAuthTagEl.className = 'account-auth-tag red';

            document.getElementById('notebook-status-text').textContent = 'NotebookLM Standby';
            document.getElementById('notebook-status-badge').querySelector('.status-dot').className = 'status-dot orange';
        }
    } catch (e) {
        console.error('Status check failed:', e);
    }
}

async function saveSettings() {
    const nbId = document.getElementById('setting-notebook-id').value.trim();
    const sfPath = document.getElementById('setting-stockfish-path').value.trim();

    try {
        const resp = await fetch('/api/config', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                notebook_id: nbId,
                stockfish_path: sfPath
            })
        });
        const data = await resp.json();
        alert('Settings saved successfully!');
        checkAppStatus();
        loadNotebooksList();
    } catch (e) {
        alert('Failed to save settings: ' + e.message);
    }
}
