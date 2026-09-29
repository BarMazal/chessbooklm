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
let startFen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1";
let currentFen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1";
let moveHistory = []; // list of SAN strings
let moveStackUci = [];
let selectedSquare = null;
let legalMoves = [];
let isFlipped = false;
let lastMoveSquares = [];
let bestMoveArrow = null;
let currentNotebookId = "";
let autoMoveTimer = null;
let isAutoPaused = true;
let overrideShowHintForCurrentMove = false;
let isEditBoardMode = false;
let selectedPalettePiece = null;
let hasDeclaredGameOver = false;
let latestEvalData = null;

const DEFAULT_TURN_GUIDELINES = [
    {
        id: 'loose_piece_check',
        icon: '🛡️',
        title: 'The "Loose Piece Alert" Check',
        text: 'Before finalizing any move, ask: "Is any piece left unguarded?" If you see an unprotected piece (like the knight on c8), verify that it isn\'t under threat before moving another piece away.',
        citations: '[1, 5]',
        category: 'Tactics'
    },
    {
        id: 'luft_rule',
        icon: '👑',
        title: 'The "Luft" (Escape Square) Rule for Kings',
        text: 'Never march your king into enemy territory if pawns and rooks cut off all retreating squares. Always ensure your king has at least one clear, safe escape square ("luft") before advancing.',
        citations: '[2, 4]',
        category: 'King Safety'
    },
    {
        id: 'simplify_material',
        icon: '🎯',
        title: 'Simplify When Ahead in Material',
        text: 'When you are up a full piece (as you were on move 39), your primary goal should be to trade off enemy active pieces (especially rooks) and keep your own position completely safe and defended.',
        citations: '[3, 5]',
        category: 'Strategy'
    }
];

let gameSettings = {
    p1Type: 'human',
    p1Difficulty: 10,
    p2Type: 'bot',
    p2Difficulty: 10,
    colorAssignment: 'random',
    showScoreBar: true,
    whiteArrows: true,
    blackArrows: true,
    showTurnGuidelines: true,
    showPracticeSubject: true,
    enableAutoLLMAnalysis: true,
    activePracticeSubject: 'auto',
    whitePlayerMode: 'manual',
    blackPlayerMode: 'manual',
    whiteDifficulty: 10,
    blackDifficulty: 10,
    autoAdjustDifficulty: false,
    autoAdjustBias: 'medium',
    enableClocks: false,
    flagAutomatedLoss: true,
    whiteClockPreset: 'blitz_5_0',
    whiteClockMins: 5,
    whiteClockInc: 0,
    blackClockPreset: 'blitz_5_0',
    blackClockMins: 5,
    blackClockInc: 0,
    alertOverride: true,
    alertRemove: true,
    alertCheck: true,
    alertMate: true,
    alertTie: true
};



// DOM Elements
const chessboardEl = document.getElementById('chessboard');
const arrowsSvgEl = document.getElementById('board-arrows-svg');
const evalBarContainerEl = document.querySelector('.eval-bar-container');
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
const gameSettingsModalEl = document.getElementById('game-settings-modal');

// Initial Setup
document.addEventListener('DOMContentLoaded', async () => {
    isAutoPaused = true;
    updatePauseResumeButtonUI();

    initTabs();
    loadGameSettings();
    checkAppStatus();
    loadNotebooksList();
    initUserProfileModule();
    initChessClockModule();
    initAdvancedMentorCapabilities();
    initStrategicDisplaysModule();
    initNewGameModalModule();

    // Board controls
    const btnQuick = document.getElementById('btn-quick-new-game');
    if (btnQuick) {
        btnQuick.addEventListener('click', () => startNewGame());
    }

    document.getElementById('btn-game-settings').addEventListener('click', openGameSettingsModal);
    document.getElementById('btn-edit-board').addEventListener('click', toggleEditBoardMode);
    document.getElementById('btn-show-hint').addEventListener('click', handleShowHintClick);
    document.getElementById('btn-pause-resume').addEventListener('click', togglePauseResume);
    document.getElementById('btn-flip').addEventListener('click', toggleFlip);
    document.getElementById('btn-undo').addEventListener('click', undoMove);
    document.getElementById('btn-resign')?.addEventListener('click', handleResign);
    document.getElementById('btn-reset').addEventListener('click', resetBoard);
    document.getElementById('btn-bot-move').addEventListener('click', makeBotMove);

    document.getElementById('select-overlay-side-filter')?.addEventListener('change', () => {
        renderBoardOverlays(latestEvalData ? latestEvalData.overlays : null);
    });
    document.getElementById('select-overlay-motif-filter')?.addEventListener('change', () => {
        renderBoardOverlays(latestEvalData ? latestEvalData.overlays : null);
    });

    initPalettePieces();

    document.querySelectorAll('input[name="edit-active-turn"]').forEach(radio => {
        radio.addEventListener('change', () => {
            if (isEditBoardMode) triggerLiveEditBoardEval();
        });
    });


    // Game Settings Modal controls
    document.getElementById('btn-close-game-settings').addEventListener('click', closeGameSettingsModal);
    document.getElementById('btn-cancel-game-settings')?.addEventListener('click', closeGameSettingsModal);
    document.getElementById('btn-apply-game-settings').addEventListener('click', applyGameSettingsFromModal);

    document.querySelectorAll('input[name="white-player-mode"]').forEach(radio => {
        radio.addEventListener('change', updateDifficultyUIControls);
    });
    document.querySelectorAll('input[name="black-player-mode"]').forEach(radio => {
        radio.addEventListener('change', updateDifficultyUIControls);
    });

    const whiteSlider = document.getElementById('slider-white-difficulty');
    if (whiteSlider) {
        whiteSlider.addEventListener('input', () => {
            const label = document.getElementById('white-difficulty-label');
            if (label) label.textContent = getDifficultyLabel(whiteSlider.value);
        });
    }
    const blackSlider = document.getElementById('slider-black-difficulty');
    if (blackSlider) {
        blackSlider.addEventListener('input', () => {
            const label = document.getElementById('black-difficulty-label');
            if (label) label.textContent = getDifficultyLabel(blackSlider.value);
        });
    }


    // Mentor quick prompt chip buttons (trigger live chat query)
    document.getElementById('btn-explain-pos')?.addEventListener('click', () => triggerQuickPromptChip("Explain the overall strategic theme, pawn structures, and piece activity for both sides in this position."));
    document.getElementById('btn-why-best')?.addEventListener('click', () => triggerQuickPromptChip("Why is the top engine move recommended in this position? What tactical or positional ideas support it?"));
    document.getElementById('btn-strategic-plan')?.addEventListener('click', () => triggerQuickPromptChip("What are the long-term strategic plans and key target squares for White and Black in this setup?"));
    document.getElementById('btn-blunder-check')?.addEventListener('click', () => triggerQuickPromptChip("Check for potential blunders, threats, and tactics. What forcing moves should I watch out for?"));
    document.getElementById('btn-ask-mentor')?.addEventListener('click', handleCustomMentorQuery);

    initAccountCardToggle();
    initSidebarResizer();
    initMentorChatModule();

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

    // Game & FEN/PGN Manager controls
    document.getElementById('btn-open-game-manager').addEventListener('click', openGameManagerModal);
    document.getElementById('btn-close-game-manager').addEventListener('click', closeGameManagerModal);
    document.getElementById('btn-save-current-game').addEventListener('click', saveCurrentGame);
    document.getElementById('btn-copy-fen').addEventListener('click', copyFenToClipboard);
    document.getElementById('btn-load-fen').addEventListener('click', loadFenFromInput);
    document.getElementById('btn-generate-pgn').addEventListener('click', generateCurrentPgnText);
    document.getElementById('btn-copy-pgn').addEventListener('click', copyPgnToClipboard);
    document.getElementById('btn-download-pgn').addEventListener('click', downloadPgnFile);
    document.getElementById('btn-load-pgn').addEventListener('click', loadPgnFromInput);
    document.getElementById('pgn-file-input').addEventListener('change', handlePgnFileUpload);

    // Profile Modal controls
    const headerProfileBadge = document.getElementById('header-profile-badge');
    if (headerProfileBadge) headerProfileBadge.addEventListener('click', openProfileModal);
    const closeProfileBtn = document.getElementById('btn-close-profile-modal');
    if (closeProfileBtn) closeProfileBtn.addEventListener('click', closeProfileModal);
    const createProfileBtn = document.getElementById('btn-create-profile');
    if (createProfileBtn) createProfileBtn.addEventListener('click', handleCreateProfile);

    const toggleAutoAdjust = document.getElementById('toggle-auto-adjust-difficulty');
    if (toggleAutoAdjust) toggleAutoAdjust.addEventListener('change', updateDifficultyUIControls);
    const selectAutoBias = document.getElementById('select-auto-adjust-bias');
    if (selectAutoBias) selectAutoBias.addEventListener('change', updateDifficultyUIControls);

    const btnForceMove = document.getElementById('btn-force-move');
    if (btnForceMove) btnForceMove.addEventListener('click', handleForceBotMove);

    const toggleEnableClocks = document.getElementById('toggle-enable-clocks');
    if (toggleEnableClocks) toggleEnableClocks.addEventListener('change', updateClockSettingsUIControls);
    const selectWhiteClock = document.getElementById('select-white-clock-preset');
    if (selectWhiteClock) selectWhiteClock.addEventListener('change', updateClockSettingsUIControls);
    const selectBlackClock = document.getElementById('select-black-clock-preset');
    if (selectBlackClock) selectBlackClock.addEventListener('change', updateClockSettingsUIControls);

    initManagerSubtabs();
    initProfileSubtabs();
    initUserProfileModule();
    initPlacementTestModule();
    initChessClockModule();

    // Strictly run Quick New Game on app startup to apply persistent new game settings immediately!
    await startNewGame();
});


function initTabs() {
    document.querySelectorAll('.sidebar-section').forEach(sidebar => {
        const tabBtns = sidebar.querySelectorAll('.tab-btn');
        const tabContents = sidebar.querySelectorAll('.tab-content');
        tabBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                tabBtns.forEach(b => b.classList.remove('active'));
                tabContents.forEach(c => c.classList.remove('active'));
                btn.classList.add('active');
                const targetId = btn.dataset.tab;
                const targetContent = sidebar.querySelector('#' + targetId);
                if (targetContent) {
                    targetContent.classList.add('active');
                }
            });
        });
    });
}

function initBoard() {
    chessboardEl.innerHTML = '';
    const files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'];
    const ranks = ['8', '7', '6', '5', '4', '3', '2', '1'];

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
    updateClockPositionsUI();
}

function parseFenToState(fen) {
    if (!fen || typeof fen !== 'string') return;
    boardState = {};
    const parts = fen.split(' ');
    if (!parts[0]) return;
    const rows = parts[0].split('/');

    const files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'];
    const ranks = ['8', '7', '6', '5', '4', '3', '2', '1'];

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

        const targetMove = legalMoves.find(m => m.uci.startsWith(selectedSquare) && m.uci.slice(2, 4) === sqName);
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

    updateCheckStateUI(latestEvalData);
    drawBestMoveArrow();
    renderBoardOverlays(latestEvalData ? latestEvalData.overlays : null);
}

function renderBoardOverlays(overlays) {
    document.querySelectorAll('.square-overlay-layer, .square-badge-container').forEach(el => el.remove());
    hideOverlayTooltip();

    if (!overlays || !Array.isArray(overlays) || overlays.length === 0) return;

    const sideFilter = document.getElementById('select-overlay-side-filter')?.value || 'all';
    const motifFilter = document.getElementById('select-overlay-motif-filter')?.value || 'all';

    if (sideFilter === 'off') return;

    const activeOverlays = overlays.filter(o => {
        if (sideFilter === 'white' && o.side !== 'white') return false;
        if (sideFilter === 'black' && o.side !== 'black') return false;

        if (motifFilter === 'good' && !['outpost', 'open_file', 'battery'].includes(o.type)) return false;
        if (motifFilter === 'weak' && !['weak_hole', 'loose_target'].includes(o.type)) return false;

        return true;
    });

    if (activeOverlays.length === 0) return;

    const squareOverlaysMap = {};
    activeOverlays.forEach(o => {
        if (!squareOverlaysMap[o.square]) squareOverlaysMap[o.square] = [];
        squareOverlaysMap[o.square].push(o);
    });

    const hexToRgba = (hex, alpha = 0.4) => {
        if (!hex) return `rgba(59, 130, 246, ${alpha})`;
        hex = hex.replace('#', '');
        if (hex.length === 3) hex = hex.split('').map(c => c + c).join('');
        const r = parseInt(hex.substring(0, 2), 16) || 0;
        const g = parseInt(hex.substring(2, 4), 16) || 0;
        const b = parseInt(hex.substring(4, 6), 16) || 0;
        return `rgba(${r}, ${g}, ${b}, ${alpha})`;
    };

    const colorWhiteOverlay = gameSettings.colorWhiteOverlay || document.getElementById('setting-color-white-overlay')?.value || '#3b82f6';
    const colorWhiteGood = gameSettings.colorWhiteGood || document.getElementById('setting-color-white-good')?.value || '#10b981';
    const colorBlackOverlay = gameSettings.colorBlackOverlay || document.getElementById('setting-color-black-overlay')?.value || '#ef4444';
    const colorBlackGood = gameSettings.colorBlackGood || document.getElementById('setting-color-black-good')?.value || '#8b5cf6';

    const getOverlayColor = (o) => {
        if (o.side === 'white') {
            return o.type === 'outpost' ? colorWhiteGood : colorWhiteOverlay;
        } else {
            return o.type === 'outpost' ? colorBlackGood : colorBlackOverlay;
        }
    };

    Object.keys(squareOverlaysMap).forEach(sqName => {
        const sqEl = document.querySelector(`.square[data-square="${sqName}"]`);
        if (!sqEl) return;

        const sqOverlays = squareOverlaysMap[sqName];
        const whiteOverlays = sqOverlays.filter(o => o.side === 'white');
        const blackOverlays = sqOverlays.filter(o => o.side === 'black');

        const overlayLayer = document.createElement('div');
        overlayLayer.className = 'square-overlay-layer';

        if (whiteOverlays.length > 0 && blackOverlays.length > 0) {
            const cW = hexToRgba(getOverlayColor(whiteOverlays[0]), 0.45);
            const cB = hexToRgba(getOverlayColor(blackOverlays[0]), 0.45);
            overlayLayer.classList.add('hatched-dual');
            overlayLayer.style.background = `repeating-linear-gradient(45deg, ${cW}, ${cW} 5px, ${cB} 5px, ${cB} 10px)`;
        } else if (whiteOverlays.length > 0) {
            overlayLayer.style.backgroundColor = hexToRgba(getOverlayColor(whiteOverlays[0]), 0.35);
        } else if (blackOverlays.length > 0) {
            overlayLayer.style.backgroundColor = hexToRgba(getOverlayColor(blackOverlays[0]), 0.35);
        }

        sqEl.appendChild(overlayLayer);

        let tooltipLines = [];
        if (whiteOverlays.length > 0) {
            tooltipLines.push(`⚪ White: ` + whiteOverlays.map(o => o.tooltip).join(' • '));
        }
        if (blackOverlays.length > 0) {
            tooltipLines.push(`⚫ Black: ` + blackOverlays.map(o => o.tooltip).join(' • '));
        }
        tooltipLines.push('💡 Click badge to view explanation in Mentor Feed');
        const fullTooltipText = tooltipLines.join('\n\n');

        const badgeContainer = document.createElement('div');
        badgeContainer.className = 'square-badge-container';

        const seenBadges = new Set();
        sqOverlays.forEach(o => {
            if (seenBadges.has(o.badge)) return;
            seenBadges.add(o.badge);

            const badgeEl = document.createElement('span');
            badgeEl.className = 'square-badge';
            badgeEl.textContent = o.badge;
            badgeEl.style.cursor = 'pointer';
            badgeEl.addEventListener('mouseenter', (e) => showOverlayTooltip(e, fullTooltipText));
            badgeEl.addEventListener('mousemove', (e) => moveOverlayTooltip(e));
            badgeEl.addEventListener('mouseleave', () => hideOverlayTooltip());
            badgeEl.addEventListener('click', (e) => {
                e.stopPropagation();
                scrollToSquareCommentary(sqName);
            });

            badgeContainer.appendChild(badgeEl);
        });

        sqEl.appendChild(badgeContainer);
    });
}

function showOverlayTooltip(e, text) {
    let tooltipEl = document.getElementById('board-overlay-tooltip');
    if (!tooltipEl) {
        tooltipEl = document.createElement('div');
        tooltipEl.id = 'board-overlay-tooltip';
        document.body.appendChild(tooltipEl);
    }
    tooltipEl.textContent = text;
    tooltipEl.classList.add('visible');
    moveOverlayTooltip(e);
}

function moveOverlayTooltip(e) {
    const tooltipEl = document.getElementById('board-overlay-tooltip');
    if (!tooltipEl) return;
    const x = e.clientX + 12;
    const y = e.clientY + 12;
    tooltipEl.style.left = `${Math.min(x, window.innerWidth - 310)}px`;
    tooltipEl.style.top = `${Math.min(y, window.innerHeight - 100)}px`;
}

function hideOverlayTooltip() {
    const tooltipEl = document.getElementById('board-overlay-tooltip');
    if (tooltipEl) {
        tooltipEl.classList.remove('visible');
    }
}

function updateCheckStateUI(data = null) {
    document.querySelectorAll('.square.king-in-check').forEach(sq => sq.classList.remove('king-in-check'));

    const topBanner = document.getElementById('check-banner-top');
    const bottomBanner = document.getElementById('check-banner-bottom');
    const middleBanner = document.getElementById('check-banner-middle');

    if (topBanner) topBanner.classList.add('hidden');
    if (bottomBanner) bottomBanner.classList.add('hidden');
    if (middleBanner) middleBanner.classList.add('hidden');

    let whiteInCheck = false;
    let blackInCheck = false;
    let isMate = false;
    let isStalemate = false;

    if (data) {
        whiteInCheck = !!data.white_in_check || (data.checked_sides && data.checked_sides.includes('White'));
        blackInCheck = !!data.black_in_check || (data.checked_sides && data.checked_sides.includes('Black'));
        if (!whiteInCheck && !blackInCheck && data.is_check) {
            const activeColor = currentFen.split(' ')[1] || 'w';
            if (activeColor === 'w') whiteInCheck = true;
            else blackInCheck = true;
        }

        const isCheck = whiteInCheck || blackInCheck || data.is_check;
        const noLegalMoves = !data.legal_moves || data.legal_moves.length === 0;

        if (noLegalMoves && isCheck) {
            isMate = true;
        } else if (noLegalMoves && !isCheck) {
            isStalemate = true;
        }
    }

    if (whiteInCheck) {
        for (let sq in boardState) {
            if (boardState[sq] === 'wK') {
                const sqEl = document.querySelector(`.square[data-square="${sq}"]`);
                if (sqEl) sqEl.classList.add('king-in-check');
                break;
            }
        }
    }

    if (blackInCheck) {
        for (let sq in boardState) {
            if (boardState[sq] === 'bK') {
                const sqEl = document.querySelector(`.square[data-square="${sq}"]`);
                if (sqEl) sqEl.classList.add('king-in-check');
                break;
            }
        }
    }

    const whiteSide = isFlipped ? 'top' : 'bottom';
    const blackSide = isFlipped ? 'bottom' : 'top';

    const bannerText = isMate ? '👑 MATE!' : '⚠️ CHECK!';

    if (whiteInCheck) {
        const targetBanner = (whiteSide === 'top') ? topBanner : bottomBanner;
        if (targetBanner) {
            targetBanner.textContent = bannerText;
            targetBanner.classList.remove('hidden');
        }
    }

    if (blackInCheck) {
        const targetBanner = (blackSide === 'top') ? topBanner : bottomBanner;
        if (targetBanner) {
            targetBanner.textContent = bannerText;
            targetBanner.classList.remove('hidden');
        }
    }

    if (isStalemate && middleBanner) {
        middleBanner.textContent = '🤝 STALEMATE!';
        middleBanner.classList.remove('hidden');
    }
}

function drawBestMoveArrow() {
    arrowsSvgEl.innerHTML = '';
    if (!bestMoveArrow || bestMoveArrow.length < 4) return;

    const activeColor = currentFen.split(' ')[1]; // 'w' or 'b'
    const arrowsEnabled = (activeColor === 'w' && gameSettings.whiteArrows) ||
        (activeColor === 'b' && gameSettings.blackArrows);

    if (!arrowsEnabled && !overrideShowHintForCurrentMove) return;

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
    if (isEditBoardMode) {
        handleEditModeSquareClick(sqName);
        return;
    }

    const activeTurnColor = currentFen.split(' ')[1]; // 'w' or 'b'
    const isWhiteAuto = (activeTurnColor === 'w' && gameSettings.whitePlayerMode === 'auto');
    const isBlackAuto = (activeTurnColor === 'b' && gameSettings.blackPlayerMode === 'auto');
    if (isWhiteAuto || isBlackAuto) return;

    if (selectedSquare) {
        if (selectedSquare === sqName) {
            selectedSquare = null;
            renderBoard();
            return;
        }

        const matchingMoves = legalMoves.filter(m => m.uci.startsWith(selectedSquare) && m.uci.slice(2, 4) === sqName);
        if (matchingMoves.length > 0) {
            const isPromotion = matchingMoves.some(m => m.uci.length === 5);
            if (isPromotion) {
                openPromotionModal(matchingMoves, activeTurnColor);
                return;
            } else {
                executeMove(matchingMoves[0].san, matchingMoves[0].uci);
                selectedSquare = null;
                return;
            }
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

function openPromotionModal(matchingMoves, activeTurnColor) {
    const modal = document.getElementById('pawn-promotion-modal');
    const grid = document.getElementById('promotion-piece-grid');
    if (!modal || !grid) return;

    const pieceColor = activeTurnColor || 'w';
    const pieces = [
        { code: 'q', name: 'Queen', key: pieceColor + 'Q' },
        { code: 'r', name: 'Rook', key: pieceColor + 'R' },
        { code: 'b', name: 'Bishop', key: pieceColor + 'B' },
        { code: 'n', name: 'Knight', key: pieceColor + 'N' }
    ];

    grid.innerHTML = '';
    pieces.forEach(p => {
        const moveObj = matchingMoves.find(m => m.uci.endsWith(p.code)) || matchingMoves[0];
        const btn = document.createElement('div');
        btn.className = 'promotion-option-box';
        btn.style.cssText = 'width:64px; height:64px; background:#161512; border:2px solid var(--card-border); border-radius:8px; display:flex; flex-direction:column; align-items:center; justify-content:center; cursor:pointer; transition:all 0.2s ease;';
        btn.innerHTML = `
            <div style="width:38px; height:38px; display:flex; align-items:center; justify-content:center;">${PIECE_SVGS[p.key] || ''}</div>
            <span style="font-size:10px; color:#8b8987; margin-top:2px; font-weight:600;">${p.name}</span>
        `;

        btn.addEventListener('mouseenter', () => {
            btn.style.borderColor = 'var(--accent-color)';
            btn.style.background = '#1e1c18';
        });
        btn.addEventListener('mouseleave', () => {
            btn.style.borderColor = 'var(--card-border)';
            btn.style.background = '#161512';
        });

        btn.addEventListener('click', () => {
            modal.classList.add('hidden');
            selectedSquare = null;
            executeMove(moveObj.san, moveObj.uci);
        });

        grid.appendChild(btn);
    });

    const cancelBtn = document.getElementById('btn-cancel-promotion');
    if (cancelBtn) {
        cancelBtn.onclick = () => {
            modal.classList.add('hidden');
            selectedSquare = null;
            renderBoard();
        };
    }

    modal.classList.remove('hidden');
}

async function executeMove(sanMove, uciMove) {
    overrideShowHintForCurrentMove = false;
    hasDeclaredGameOver = false;
    selectedHistoryMoveIndex = -1;
    const bannerEl = document.getElementById('move-replay-banner');
    if (bannerEl) bannerEl.classList.add('hidden');

    const previousTurnColor = currentFen.split(' ')[1] || 'w';
    moveHistory.push(sanMove);
    moveStackUci.push(uciMove);
    lastMoveSquares = [uciMove.slice(0, 2), uciMove.slice(2, 4)];

    if (isAutoPaused) {
        isAutoPaused = false;
        updatePauseResumeButtonUI();
    }

    await updatePositionEvaluation();
    onMoveExecutedClockTick(previousTurnColor);
}

async function updatePositionEvaluation(evalFen, evalMoves) {
    const targetFen = (evalFen !== undefined) ? evalFen : (isEditBoardMode ? currentFen : startFen);
    const targetMoves = (evalMoves !== undefined) ? evalMoves : (isEditBoardMode ? [] : moveHistory);
    try {
        const resp = await fetch('/api/board/evaluate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ fen: targetFen, moves: targetMoves })
        });
        const data = await resp.json();
        latestEvalData = data;

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
        updateUndoButtonState();
        renderTurnGuidelines(boardState, currentFen, data);
        renderPracticeSubjectInstruction(boardState, currentFen, data);
        triggerAutoLiveCoaching(moveHistory.length);

        const isGameOver = data.is_game_over || legalMoves.length === 0;
        if (isGameOver) {
            stopClockTimer();
            if (!isAutoPaused) {
                isAutoPaused = true;
                updatePauseResumeButtonUI();
                if (autoMoveTimer) {
                    clearTimeout(autoMoveTimer);
                    autoMoveTimer = null;
                }
            }

            if (!hasDeclaredGameOver && moveHistory.length > 0) {
                hasDeclaredGameOver = true;
                const activeTurnColor = data.turn || (currentFen.split(' ')[1] === 'w' ? 'white' : 'black');
                const isCheck = data.is_check || data.white_in_check || data.black_in_check;

                const isWhiteManual = (gameSettings.whitePlayerMode === 'manual');
                const isBlackManual = (gameSettings.blackPlayerMode === 'manual');

                let oppElo = 1500;
                if (isWhiteManual && !isBlackManual) {
                    oppElo = getOpponentEloForGame('b');
                } else if (!isWhiteManual && isBlackManual) {
                    oppElo = getOpponentEloForGame('w');
                }

                if (isCheck || (data.eval && data.eval.eval_type === 'mate')) {
                    const winnerColor = (activeTurnColor === 'white') ? 'black' : 'white';
                    const winner = (activeTurnColor === 'white') ? 'Black' : 'White';

                    if (turnBadgeEl) {
                        turnBadgeEl.textContent = `🏆 Checkmate - ${winner} Wins!`;
                        turnBadgeEl.className = `turn-badge ${winner.toLowerCase()}`;
                    }

                    let outcome = 'draw';
                    if (isWhiteManual && !isBlackManual) {
                        outcome = (winnerColor === 'white') ? 'win' : 'loss';
                    } else if (!isWhiteManual && isBlackManual) {
                        outcome = (winnerColor === 'black') ? 'win' : 'loss';
                    } else {
                        outcome = (winnerColor === 'white') ? 'win' : 'loss';
                    }

                    recordGameResult(outcome, oppElo);
                } else {
                    if (turnBadgeEl) {
                        turnBadgeEl.textContent = `🤝 Stalemate - Draw!`;
                        turnBadgeEl.className = 'turn-badge';
                    }
                    recordGameResult('draw', oppElo);
                }
            }
        } else {
            checkAndTriggerAutoMove();
        }

    } catch (e) {
        console.error('Failed to update evaluation:', e);
    }
}

let selectedHistoryMoveIndex = -1;
let editingGuidelineId = null;

function renderMoveHistoryTable() {
    if (!moveHistoryTbodyEl) return;
    moveHistoryTbodyEl.innerHTML = '';
    for (let i = 0; i < moveHistory.length; i += 2) {
        const row = document.createElement('tr');
        const moveNum = Math.floor(i / 2) + 1;
        const whiteMoveIndex = i;
        const blackMoveIndex = i + 1;
        const whiteMove = moveHistory[whiteMoveIndex] || '';
        const blackMove = (moveHistory.length > blackMoveIndex) ? moveHistory[blackMoveIndex] : '';

        const whiteActive = selectedHistoryMoveIndex === whiteMoveIndex ? 'active-move-cell' : '';
        const blackActive = selectedHistoryMoveIndex === blackMoveIndex ? 'active-move-cell' : '';

        row.innerHTML = `
            <td><strong>${moveNum}.</strong></td>
            <td class="clickable-move-cell ${whiteActive}" data-move-index="${whiteMoveIndex}">${whiteMove}</td>
            <td class="clickable-move-cell ${blackActive}" data-move-index="${blackMoveIndex}">${blackMove}</td>
        `;

        row.querySelectorAll('td.clickable-move-cell').forEach(td => {
            const idx = parseInt(td.dataset.moveIndex, 10);
            if (!isNaN(idx) && idx < moveHistory.length) {
                td.addEventListener('click', () => viewHistoricalMove(idx));
            }
        });

        moveHistoryTbodyEl.appendChild(row);
    }
    const container = document.getElementById('move-history-container');
    if (container && selectedHistoryMoveIndex === -1) {
        container.scrollTop = container.scrollHeight;
    }
}

async function viewHistoricalMove(moveIndex) {
    if (moveIndex < 0 || moveIndex >= moveHistory.length) return;

    if (!isAutoPaused) {
        isAutoPaused = true;
        updatePauseResumeButtonUI();
        if (autoMoveTimer) {
            clearTimeout(autoMoveTimer);
            autoMoveTimer = null;
        }
    }

    selectedHistoryMoveIndex = moveIndex;

    const bannerEl = document.getElementById('move-replay-banner');
    const textEl = document.getElementById('replay-banner-text');
    const moveNum = Math.floor(moveIndex / 2) + 1;
    const isWhite = (moveIndex % 2 === 0);
    const moveSan = moveHistory[moveIndex];
    const sidePrefix = isWhite ? `${moveNum}.` : `${moveNum}...`;

    if (bannerEl) bannerEl.classList.remove('hidden');
    if (textEl) textEl.textContent = `📜 Viewing Past Move #${moveNum} (${sidePrefix} ${moveSan})`;

    const historicalMoves = moveHistory.slice(0, moveIndex + 1);

    try {
        const resp = await fetch('/api/board/evaluate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ fen: startFen, moves: historicalMoves })
        });
        const data = await resp.json();

        currentFen = data.fen;
        parseFenToState(currentFen);

        const scoreStr = data.eval ? data.eval.score : '+0.0';
        if (summaryEvalEl) summaryEvalEl.textContent = scoreStr;
        if (evalScoreBadgeEl) evalScoreBadgeEl.textContent = scoreStr;
        if (summaryBestMoveEl) summaryBestMoveEl.textContent = data.eval ? data.eval.best_move_san || '-' : '-';

        let whitePercentage = 50;
        if (data.eval && data.eval.eval_type === 'mate') {
            whitePercentage = data.eval.eval_val > 0 ? 98 : 2;
        } else if (data.eval) {
            const cp = data.eval.eval_val;
            whitePercentage = Math.min(98, Math.max(2, 50 + (cp * 10)));
        }
        if (evalWhiteFillEl) evalWhiteFillEl.style.height = `${whitePercentage}%`;

        renderMoveHistoryTable();
        renderBoard();
    } catch (e) {
        console.error('Failed to evaluate historical move:', e);
    }
}

async function returnToLiveGame() {
    selectedHistoryMoveIndex = -1;
    const bannerEl = document.getElementById('move-replay-banner');
    if (bannerEl) bannerEl.classList.add('hidden');
    await updatePositionEvaluation();
}

function updateUndoButtonState() {
    const btnUndo = document.getElementById('btn-undo');
    if (!btnUndo) return;

    const whiteIsManual = (gameSettings.whitePlayerMode === 'manual');
    const blackIsManual = (gameSettings.blackPlayerMode === 'manual');
    const atLeastOneManual = whiteIsManual || blackIsManual;

    if (!atLeastOneManual) {
        btnUndo.disabled = true;
        btnUndo.title = "Undo is disabled during Computer vs Computer mode";
    } else if (moveHistory.length === 0) {
        btnUndo.disabled = true;
        btnUndo.title = "No moves to undo";
    } else {
        btnUndo.disabled = false;
        btnUndo.title = "Undo Move";
    }
}

async function undoMove() {
    overrideShowHintForCurrentMove = false;
    if (autoMoveTimer) {
        clearTimeout(autoMoveTimer);
        autoMoveTimer = null;
    }

    if (moveHistory.length === 0) return;

    const whiteIsManual = (gameSettings.whitePlayerMode === 'manual');
    const blackIsManual = (gameSettings.blackPlayerMode === 'manual');

    // Enabled only if at least one of the players is "Player" (Manual)
    if (!whiteIsManual && !blackIsManual) return;

    let movesToUndo = 1;

    if (whiteIsManual && blackIsManual) {
        // Both are Human -> undo last move (1 move)
        movesToUndo = 1;
    } else {
        // One is Human and one is Computer
        const lastMoveIndex = moveHistory.length - 1;
        const lastMoveWasWhite = (lastMoveIndex % 2 === 0);
        const lastMoveColor = lastMoveWasWhite ? 'w' : 'b';
        const lastMovePlayerMode = (lastMoveColor === 'w') ? gameSettings.whitePlayerMode : gameSettings.blackPlayerMode;

        if (lastMovePlayerMode === 'manual') {
            // Last move was by Human -> undo 1 move
            movesToUndo = 1;
        } else {
            // Last move was by Computer -> undo 2 moves (Computer response + Human move)
            movesToUndo = Math.min(2, moveHistory.length);
        }
    }

    for (let i = 0; i < movesToUndo; i++) {
        if (moveHistory.length > 0) {
            moveHistory.pop();
            moveStackUci.pop();
        }
    }

    currentFen = startFen;
    lastMoveSquares = [];
    selectedSquare = null;
    hasDeclaredGameOver = false;
    await updatePositionEvaluation();
}

async function resetBoardState() {
    overrideShowHintForCurrentMove = false;
    hasDeclaredGameOver = false;
    if (autoMoveTimer) {
        clearTimeout(autoMoveTimer);
        autoMoveTimer = null;
    }
    isAutoPaused = false;
    updatePauseResumeButtonUI();
    startFen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1";
    currentFen = startFen;
    moveHistory = [];
    moveStackUci = [];
    lastMoveSquares = [];
    selectedSquare = null;

    initBoard();
    resetChessClocks();
    updateClockPositionsUI();

    await updatePositionEvaluation();
}

function rollRandomPlayerColor() {
    if (window.crypto && window.crypto.getRandomValues) {
        const array = new Uint8Array(1);
        window.crypto.getRandomValues(array);
        return (array[0] % 2) === 0;
    }
    return Math.random() < 0.5;
}

function showGameToast(message, durationMs = 3500) {
    let container = document.getElementById('game-toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'game-toast-container';
        container.className = 'game-toast-container';
        document.body.appendChild(container);
    }
    const toast = document.createElement('div');
    toast.className = 'game-toast';
    toast.innerHTML = message;
    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transition = 'opacity 0.4s ease-out';
        setTimeout(() => toast.remove(), 400);
    }, durationMs);
}

async function startNewGame(customConfig = null) {
    if (customConfig) {
        if (customConfig.p1Type !== undefined) gameSettings.p1Type = customConfig.p1Type;
        if (customConfig.p1Difficulty !== undefined) gameSettings.p1Difficulty = parseInt(customConfig.p1Difficulty, 10);
        if (customConfig.p2Type !== undefined) gameSettings.p2Type = customConfig.p2Type;
        if (customConfig.p2Difficulty !== undefined) gameSettings.p2Difficulty = parseInt(customConfig.p2Difficulty, 10);
        if (customConfig.colorAssignment !== undefined) gameSettings.colorAssignment = customConfig.colorAssignment;
        if (customConfig.autoAdjustDifficulty !== undefined) gameSettings.autoAdjustDifficulty = customConfig.autoAdjustDifficulty;
        if (customConfig.autoAdjustBias !== undefined) gameSettings.autoAdjustBias = customConfig.autoAdjustBias;
        saveGameSettingsToStorage();
    }

    let p1IsWhite = true;
    if (gameSettings.colorAssignment === 'random') {
        p1IsWhite = rollRandomPlayerColor();
    } else if (gameSettings.colorAssignment === 'black') {
        p1IsWhite = false;
    } else {
        p1IsWhite = true;
    }

    if (p1IsWhite) {
        gameSettings.whitePlayerMode = (gameSettings.p1Type === 'bot') ? 'auto' : 'manual';
        gameSettings.whiteDifficulty = gameSettings.p1Difficulty ?? 10;

        gameSettings.blackPlayerMode = (gameSettings.p2Type === 'bot') ? 'auto' : 'manual';
        gameSettings.blackDifficulty = gameSettings.p2Difficulty ?? 10;
    } else {
        gameSettings.whitePlayerMode = (gameSettings.p2Type === 'bot') ? 'auto' : 'manual';
        gameSettings.whiteDifficulty = gameSettings.p2Difficulty ?? 10;

        gameSettings.blackPlayerMode = (gameSettings.p1Type === 'bot') ? 'auto' : 'manual';
        gameSettings.blackDifficulty = gameSettings.p1Difficulty ?? 10;
    }

    // Auto Board Flip: ONLY flip if it is Computer vs Human and the Human plays Black!
    const isHumanVsBot = (gameSettings.p1Type === 'human' && gameSettings.p2Type === 'bot');
    const isBotVsHuman = (gameSettings.p1Type === 'bot' && gameSettings.p2Type === 'human');

    let humanIsBlack = false;
    let humanIsWhite = false;

    if (isHumanVsBot) {
        humanIsBlack = !p1IsWhite;
        humanIsWhite = p1IsWhite;
        isFlipped = humanIsBlack;
    } else if (isBotVsHuman) {
        humanIsBlack = p1IsWhite;
        humanIsWhite = !p1IsWhite;
        isFlipped = humanIsBlack;
    } else {
        // Human vs Human OR Bot vs Bot: DO NOT FLIP! (Standard White at bottom)
        isFlipped = false;
    }

    if (gameSettings.colorAssignment === 'random') {
        let assignedName = p1IsWhite ? '⚪ White' : '⚫ Black';
        if (isHumanVsBot || isBotVsHuman) {
            assignedName = humanIsWhite ? '⚪ White' : '⚫ Black';
        }
        showGameToast(`🎲 <strong>Random Side Assignment:</strong> You play as <strong>${assignedName}</strong>!`);
    }

    saveGameSettingsToStorage();
    await resetBoardState();
}

async function resetBoard() {
    await startNewGame();
}

function initNewGameModalModule() {
    const modalEl = document.getElementById('new-game-modal');
    const btnTrigger = document.getElementById('btn-new-game-modal-trigger');
    const btnClose = document.getElementById('btn-close-new-game-modal');
    const btnCancel = document.getElementById('btn-cancel-new-game');
    const btnSubmit = document.getElementById('btn-submit-new-game');

    const p1Slider = document.getElementById('ng-p1-difficulty-slider');
    const p1Label = document.getElementById('ng-p1-difficulty-label');
    const p2Slider = document.getElementById('ng-p2-difficulty-slider');
    const p2Label = document.getElementById('ng-p2-difficulty-label');

    const toggleAutoAdjust = document.getElementById('ng-toggle-auto-adjust-difficulty');
    const selectAutoBias = document.getElementById('ng-select-auto-adjust-bias');
    const biasContainer = document.getElementById('ng-auto-adjust-bias-container');
    const profileEloText = document.getElementById('ng-auto-adjust-profile-elo-text');

    const updateAutoAdjustUI = () => {
        const isAuto = toggleAutoAdjust ? toggleAutoAdjust.checked : false;
        if (biasContainer) biasContainer.classList.toggle('hidden', !isAuto);

        const activeProf = (typeof getActiveProfile === 'function') ? getActiveProfile() : { elo: 1500, name: 'Player' };
        const userElo = activeProf.elo || 1500;
        if (profileEloText) profileEloText.textContent = `${userElo} ELO`;

        const autoBias = selectAutoBias ? selectAutoBias.value : 'medium';
        let targetAutoElo = userElo;
        if (autoBias === 'easy') targetAutoElo = Math.max(800, userElo - 150);
        else if (autoBias === 'hard') targetAutoElo = userElo + 150;
        else if (autoBias === 'nightmare') targetAutoElo = userElo + 350;

        const p1Val = document.querySelector('input[name="ng-p1-type"]:checked')?.value || 'human';
        const p1Box = document.getElementById('ng-p1-bot-controls');
        if (p1Box) p1Box.classList.toggle('hidden', p1Val !== 'bot');
        if (p1Label && p1Slider) {
            if (isAuto && p1Val === 'bot') {
                p1Label.textContent = `🤖 Auto-Adjusted (~${targetAutoElo} ELO)`;
            } else {
                p1Label.textContent = getDifficultyLabel(p1Slider.value);
            }
        }

        const p2Val = document.querySelector('input[name="ng-p2-type"]:checked')?.value || 'bot';
        const p2Box = document.getElementById('ng-p2-bot-controls');
        if (p2Box) p2Box.classList.toggle('hidden', p2Val !== 'bot');
        if (p2Label && p2Slider) {
            if (isAuto && p2Val === 'bot') {
                p2Label.textContent = `🤖 Auto-Adjusted (~${targetAutoElo} ELO)`;
            } else {
                p2Label.textContent = getDifficultyLabel(p2Slider.value);
            }
        }
    };

    document.querySelectorAll('input[name="ng-p1-type"]').forEach(r => r.addEventListener('change', updateAutoAdjustUI));
    document.querySelectorAll('input[name="ng-p2-type"]').forEach(r => r.addEventListener('change', updateAutoAdjustUI));
    if (toggleAutoAdjust) toggleAutoAdjust.addEventListener('change', updateAutoAdjustUI);
    if (selectAutoBias) selectAutoBias.addEventListener('change', updateAutoAdjustUI);

    if (p1Slider) p1Slider.addEventListener('input', updateAutoAdjustUI);
    if (p2Slider) p2Slider.addEventListener('input', updateAutoAdjustUI);

    // Segmented color buttons
    document.querySelectorAll('.color-select-btn').forEach(lbl => {
        lbl.addEventListener('click', () => {
            document.querySelectorAll('.color-select-btn').forEach(l => l.classList.remove('active'));
            lbl.classList.add('active');
            const radio = lbl.querySelector('input[type="radio"]');
            if (radio) radio.checked = true;
        });
    });

    const openModal = () => {
        if (!modalEl) return;
        const p1Type = gameSettings.p1Type || 'human';
        const p2Type = gameSettings.p2Type || 'bot';
        const colAssign = gameSettings.colorAssignment || 'random';
        const autoAdjust = gameSettings.autoAdjustDifficulty ?? false;
        const autoBias = gameSettings.autoAdjustBias || 'medium';

        const p1Radio = document.querySelector(`input[name="ng-p1-type"][value="${p1Type}"]`);
        if (p1Radio) p1Radio.checked = true;

        const p2Radio = document.querySelector(`input[name="ng-p2-type"][value="${p2Type}"]`);
        if (p2Radio) p2Radio.checked = true;

        if (p1Slider) p1Slider.value = gameSettings.p1Difficulty ?? 10;
        if (p2Slider) p2Slider.value = gameSettings.p2Difficulty ?? 10;

        if (toggleAutoAdjust) toggleAutoAdjust.checked = autoAdjust;
        if (selectAutoBias) selectAutoBias.value = autoBias;

        document.querySelectorAll('.color-select-btn').forEach(lbl => {
            const r = lbl.querySelector('input[type="radio"]');
            if (r && r.value === colAssign) {
                lbl.classList.add('active');
                r.checked = true;
            } else {
                lbl.classList.remove('active');
            }
        });

        updateAutoAdjustUI();
        modalEl.classList.remove('hidden');
    };

    const closeModal = () => {
        if (modalEl) modalEl.classList.add('hidden');
    };

    if (btnTrigger) btnTrigger.addEventListener('click', openModal);
    if (btnClose) btnClose.addEventListener('click', closeModal);
    if (btnCancel) btnCancel.addEventListener('click', closeModal);

    if (btnSubmit) {
        btnSubmit.addEventListener('click', () => {
            const p1Type = document.querySelector('input[name="ng-p1-type"]:checked')?.value || 'human';
            const p2Type = document.querySelector('input[name="ng-p2-type"]:checked')?.value || 'bot';
            const p1Diff = p1Slider ? parseInt(p1Slider.value, 10) : 10;
            const p2Diff = p2Slider ? parseInt(p2Slider.value, 10) : 10;
            const colorAss = document.querySelector('input[name="ng-color-assignment"]:checked')?.value || 'random';
            const autoAdjust = toggleAutoAdjust ? toggleAutoAdjust.checked : false;
            const autoBias = selectAutoBias ? selectAutoBias.value : 'medium';

            closeModal();
            startNewGame({
                p1Type,
                p1Difficulty: p1Diff,
                p2Type,
                p2Difficulty: p2Diff,
                colorAssignment: colorAss,
                autoAdjustDifficulty: autoAdjust,
                autoAdjustBias: autoBias
            });
        });
    }
}

const BOT_ELO_LEVELS = [
    { level: 0, elo: 400, label: 'Absolute Beginner (~400 ELO)' },
    { level: 1, elo: 600, label: 'Beginner (~600 ELO)' },
    { level: 2, elo: 800, label: 'Beginner (~800 ELO)' },
    { level: 3, elo: 1000, label: 'Casual (~1000 ELO)' },
    { level: 4, elo: 1200, label: 'Casual (~1200 ELO)' },
    { level: 5, elo: 1350, label: 'Novice (~1350 ELO)' },
    { level: 6, elo: 1500, label: 'Intermediate (~1500 ELO)' },
    { level: 7, elo: 1600, label: 'Intermediate (~1600 ELO)' },
    { level: 8, elo: 1700, label: 'Intermediate (~1700 ELO)' },
    { level: 9, elo: 1800, label: 'Advanced (~1800 ELO)' },
    { level: 10, elo: 1900, label: 'Advanced (~1900 ELO)' },
    { level: 11, elo: 2000, label: 'Advanced (~2000 ELO)' },
    { level: 12, elo: 2150, label: 'Expert (~2150 ELO)' },
    { level: 13, elo: 2300, label: 'Master (~2300 ELO)' },
    { level: 14, elo: 2450, label: 'Master (~2450 ELO)' },
    { level: 15, elo: 2600, label: 'Grandmaster (~2600 ELO)' },
    { level: 16, elo: 2700, label: 'Grandmaster (~2700 ELO)' },
    { level: 17, elo: 2800, label: 'Super GM (~2800 ELO)' },
    { level: 18, elo: 2900, label: 'Super GM (~2900 ELO)' },
    { level: 19, elo: 3000, label: 'Super GM (~3000 ELO)' },
    { level: 20, elo: 3100, label: 'Max Stockfish (~3100 ELO)' }
];

function getBotEloEstimate(lvl) {
    const idx = Math.min(20, Math.max(0, parseInt(lvl, 10)));
    return BOT_ELO_LEVELS[idx] ? BOT_ELO_LEVELS[idx].elo : 1500;
}

function getDifficultyLabel(val) {
    const idx = Math.min(20, Math.max(0, parseInt(val, 10)));
    return BOT_ELO_LEVELS[idx] ? BOT_ELO_LEVELS[idx].label : `Level ${val}`;
}

function eloToSkillLevel(targetElo) {
    let closestLevel = 0;
    let minDiff = Infinity;
    for (let i = 0; i < BOT_ELO_LEVELS.length; i++) {
        const diff = Math.abs(BOT_ELO_LEVELS[i].elo - targetElo);
        if (diff < minDiff) {
            minDiff = diff;
            closestLevel = i;
        }
    }
    return closestLevel;
}

function updateDifficultyUIControls() {
    const whiteContainer = document.getElementById('white-difficulty-container');
    const blackContainer = document.getElementById('black-difficulty-container');
    const whiteSlider = document.getElementById('slider-white-difficulty');
    const blackSlider = document.getElementById('slider-black-difficulty');
    const whiteLabel = document.getElementById('white-difficulty-label');
    const blackLabel = document.getElementById('black-difficulty-label');

    const selectedWhite = document.querySelector('input[name="white-player-mode"]:checked');
    const selectedBlack = document.querySelector('input[name="black-player-mode"]:checked');
    const tAuto = document.getElementById('toggle-auto-adjust-difficulty');
    const biasSelect = document.getElementById('select-auto-adjust-bias');
    const biasContainer = document.getElementById('auto-adjust-bias-container');

    const isAutoSettings = tAuto ? tAuto.checked : (gameSettings.autoAdjustDifficulty ?? false);
    const bias = biasSelect ? biasSelect.value : (gameSettings.autoAdjustBias || 'medium');

    const isWhiteManual = selectedWhite ? (selectedWhite.value === 'manual') : (gameSettings.whitePlayerMode === 'manual');
    const isBlackManual = selectedBlack ? (selectedBlack.value === 'manual') : (gameSettings.blackPlayerMode === 'manual');

    // Auto-adjust applies ONLY when there is a Human player facing a Bot
    const isBotVsBot = !isWhiteManual && !isBlackManual;
    const isAutoActive = isAutoSettings && !isBotVsBot;

    if (biasContainer) {
        biasContainer.classList.toggle('hidden', !isAutoSettings);
    }

    const activeProf = (typeof getActiveProfile === 'function') ? getActiveProfile() : { elo: 1500 };
    const profElo = activeProf.elo || 1500;

    let targetElo = profElo;
    if (bias === 'easy') targetElo = Math.max(800, profElo - 150);
    else if (bias === 'hard') targetElo = profElo + 150;
    else if (bias === 'nightmare') targetElo = profElo + 350;

    const autoSkillLevel = eloToSkillLevel(targetElo);

    const autoTextEl = document.getElementById('auto-adjust-profile-elo-text');
    if (autoTextEl) autoTextEl.textContent = `${profElo} ELO (${bias.toUpperCase()} -> ~${targetElo} ELO)`;

    if (selectedWhite) {
        if (whiteSlider) {
            whiteSlider.disabled = isWhiteManual || isAutoActive;
            if (isAutoActive && !isWhiteManual) whiteSlider.value = autoSkillLevel;
        }
        if (whiteContainer) {
            whiteContainer.classList.toggle('disabled', isWhiteManual);
        }
    }

    if (selectedBlack) {
        if (blackSlider) {
            blackSlider.disabled = isBlackManual || isAutoActive;
            if (isAutoActive && !isBlackManual) blackSlider.value = autoSkillLevel;
        }
        if (blackContainer) {
            blackContainer.classList.toggle('disabled', isBlackManual);
        }
    }

    if (whiteSlider && whiteLabel) {
        whiteLabel.textContent = (isAutoActive && !isWhiteManual) ? `🤖 Auto (${bias.toUpperCase()} ~${targetElo} ELO)` : getDifficultyLabel(whiteSlider.value);
    }
    if (blackSlider && blackLabel) {
        blackLabel.textContent = (isAutoActive && !isBlackManual) ? `🤖 Auto (${bias.toUpperCase()} ~${targetElo} ELO)` : getDifficultyLabel(blackSlider.value);
    }

    updateClockPlayerTypesUI();
}


async function makeBotMove() {
    if (legalMoves.length === 0) return;

    const activeTurnColor = currentFen.split(' ')[1]; // 'w' or 'b'
    const isWhiteAuto = (gameSettings.whitePlayerMode === 'auto');
    const isBlackAuto = (gameSettings.blackPlayerMode === 'auto');

    let skillLevel = (activeTurnColor === 'w') ? (gameSettings.whiteDifficulty ?? 10) : (gameSettings.blackDifficulty ?? 10);
    let targetElo = getBotEloEstimate(skillLevel);

    if (gameSettings.autoAdjustDifficulty && (isWhiteAuto !== isBlackAuto)) {
        const activeProf = (typeof getActiveProfile === 'function') ? getActiveProfile() : { elo: 1500 };
        const profElo = activeProf.elo || 1500;
        const bias = gameSettings.autoAdjustBias || 'medium';

        targetElo = profElo;
        if (bias === 'easy') targetElo = Math.max(800, profElo - 150);
        else if (bias === 'hard') targetElo = profElo + 150;
        else if (bias === 'nightmare') targetElo = profElo + 350;

        skillLevel = eloToSkillLevel(targetElo);
    }

    try {
        const resp = await fetch('/api/board/bot-move', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                fen: startFen,
                moves: moveHistory,
                skill_level: skillLevel,
                target_elo: targetElo
            })
        });
        const data = await resp.json();
        if (data.move_uci && data.move_san) {
            await executeMove(data.move_san, data.move_uci);
            return;
        }
    } catch (e) {
        console.error('Failed to fetch bot move:', e);
    }

    const bestMoveObj = legalMoves.find(m => m.uci === bestMoveArrow) || legalMoves[0];
    await executeMove(bestMoveObj.san, bestMoveObj.uci);
}

// Game Settings & Action Handlers
function applyGameSettingsVisuals() {
    updateDifficultyUIControls();
    updateClockPlayerTypesUI();

    const evalBar = document.getElementById('eval-bar-container') || document.querySelector('.eval-bar');
    if (evalBar) {
        evalBar.style.display = (gameSettings.showScoreBar ?? true) ? '' : 'none';
    }

    const guidelinesBox = document.getElementById('turn-guidelines-box');
    if (guidelinesBox) {
        guidelinesBox.style.display = (gameSettings.showTurnGuidelines ?? true) ? '' : 'none';
    }

    const practiceBox = document.getElementById('practice-subject-box');
    if (practiceBox) {
        practiceBox.style.display = (gameSettings.showPracticeSubject ?? true) ? '' : 'none';
    }
}

function loadGameSettings() {
    const saved = localStorage.getItem('chess_game_settings');
    if (saved) {
        try {
            gameSettings = Object.assign({}, gameSettings, JSON.parse(saved));
        } catch (e) { }
    }
    applyGameSettingsVisuals();
}

function saveGameSettingsToStorage() {
    localStorage.setItem('chess_game_settings', JSON.stringify(gameSettings));
}

function openGameSettingsModal() {
    if (!isAutoPaused) {
        isAutoPaused = true;
        updatePauseResumeButtonUI();
        if (autoMoveTimer) {
            clearTimeout(autoMoveTimer);
            autoMoveTimer = null;
        }
    }

    document.getElementById('toggle-score-bar').checked = gameSettings.showScoreBar;
    document.getElementById('toggle-arrow-white').checked = gameSettings.whiteArrows;
    document.getElementById('toggle-arrow-black').checked = gameSettings.blackArrows;

    const wRadios = document.querySelectorAll('input[name="white-player-mode"]');
    wRadios.forEach(r => r.checked = (r.value === gameSettings.whitePlayerMode));

    const bRadios = document.querySelectorAll('input[name="black-player-mode"]');
    bRadios.forEach(r => r.checked = (r.value === gameSettings.blackPlayerMode));

    const tAuto = document.getElementById('toggle-auto-adjust-difficulty');
    if (tAuto) tAuto.checked = gameSettings.autoAdjustDifficulty ?? false;

    const selectBias = document.getElementById('select-auto-adjust-bias');
    if (selectBias) selectBias.value = gameSettings.autoAdjustBias || 'medium';

    const whiteSlider = document.getElementById('slider-white-difficulty');
    if (whiteSlider) whiteSlider.value = gameSettings.whiteDifficulty ?? 10;

    const blackSlider = document.getElementById('slider-black-difficulty');
    if (blackSlider) blackSlider.value = gameSettings.blackDifficulty ?? 10;

    const tClocks = document.getElementById('toggle-enable-clocks');
    if (tClocks) tClocks.checked = gameSettings.enableClocks ?? false;

    const tFlagLoss = document.getElementById('toggle-flag-automated-loss');
    if (tFlagLoss) tFlagLoss.checked = gameSettings.flagAutomatedLoss ?? true;

    const selectWClock = document.getElementById('select-white-clock-preset');
    if (selectWClock) selectWClock.value = gameSettings.whiteClockPreset || 'blitz_5_0';

    const inputWMins = document.getElementById('input-white-clock-mins');
    if (inputWMins) inputWMins.value = gameSettings.whiteClockMins ?? 5;

    const inputWInc = document.getElementById('input-white-clock-inc');
    if (inputWInc) inputWInc.value = gameSettings.whiteClockInc ?? 0;

    const selectBClock = document.getElementById('select-black-clock-preset');
    if (selectBClock) selectBClock.value = gameSettings.blackClockPreset || 'blitz_5_0';

    const inputBMins = document.getElementById('input-black-clock-mins');
    if (inputBMins) inputBMins.value = gameSettings.blackClockMins ?? 5;

    const inputBInc = document.getElementById('input-black-clock-inc');
    if (inputBInc) inputBInc.value = gameSettings.blackClockInc ?? 0;

    const tOverride = document.getElementById('toggle-alert-override');
    if (tOverride) tOverride.checked = gameSettings.alertOverride ?? true;
    const tRemove = document.getElementById('toggle-alert-remove');
    if (tRemove) tRemove.checked = gameSettings.alertRemove ?? true;
    const tCheck = document.getElementById('toggle-alert-check');
    if (tCheck) tCheck.checked = gameSettings.alertCheck ?? true;
    const tMate = document.getElementById('toggle-alert-mate');
    if (tMate) tMate.checked = gameSettings.alertMate ?? true;
    const tTie = document.getElementById('toggle-alert-tie');
    if (tTie) tTie.checked = gameSettings.alertTie ?? true;

    const tShowGuide = document.getElementById('toggle-show-turn-guidelines');
    if (tShowGuide) tShowGuide.checked = gameSettings.showTurnGuidelines ?? true;

    const tShowPractice = document.getElementById('toggle-show-practice-subject');
    if (tShowPractice) tShowPractice.checked = gameSettings.showPracticeSubject ?? true;

    const tAutoLLM = document.getElementById('setting-enable-auto-llm-analysis');
    if (tAutoLLM) tAutoLLM.checked = gameSettings.enableAutoLLMAnalysis ?? true;

    const selectDefSubject = document.getElementById('setting-default-practice-subject');
    if (selectDefSubject) selectDefSubject.value = gameSettings.activePracticeSubject || 'auto';

    const colorWO = document.getElementById('setting-color-white-overlay');
    if (colorWO) colorWO.value = gameSettings.colorWhiteOverlay || '#3b82f6';
    const colorWG = document.getElementById('setting-color-white-good');
    if (colorWG) colorWG.value = gameSettings.colorWhiteGood || '#10b981';
    const colorBO = document.getElementById('setting-color-black-overlay');
    if (colorBO) colorBO.value = gameSettings.colorBlackOverlay || '#ef4444';
    const colorBG = document.getElementById('setting-color-black-good');
    if (colorBG) colorBG.value = gameSettings.colorBlackGood || '#8b5cf6';

    updateDifficultyUIControls();
    updateClockSettingsUIControls();

    gameSettingsModalEl.classList.remove('hidden');
}


function closeGameSettingsModal() {
    gameSettingsModalEl.classList.add('hidden');
}

function applyGameSettingsFromModal() {
    gameSettings.showScoreBar = document.getElementById('toggle-score-bar').checked;
    gameSettings.whiteArrows = document.getElementById('toggle-arrow-white').checked;
    gameSettings.blackArrows = document.getElementById('toggle-arrow-black').checked;

    const colorWO = document.getElementById('setting-color-white-overlay');
    if (colorWO) gameSettings.colorWhiteOverlay = colorWO.value;
    const colorWG = document.getElementById('setting-color-white-good');
    if (colorWG) gameSettings.colorWhiteGood = colorWG.value;
    const colorBO = document.getElementById('setting-color-black-overlay');
    if (colorBO) gameSettings.colorBlackOverlay = colorBO.value;
    const colorBG = document.getElementById('setting-color-black-good');
    if (colorBG) gameSettings.colorBlackGood = colorBG.value;

    const tShowGuide = document.getElementById('toggle-show-turn-guidelines');
    if (tShowGuide) gameSettings.showTurnGuidelines = tShowGuide.checked;

    const tShowPractice = document.getElementById('toggle-show-practice-subject');
    if (tShowPractice) gameSettings.showPracticeSubject = tShowPractice.checked;

    const tAutoLLM = document.getElementById('setting-enable-auto-llm-analysis');
    if (tAutoLLM) {
        gameSettings.enableAutoLLMAnalysis = tAutoLLM.checked;
        const feedChk = document.getElementById('chk-auto-llm-analysis');
        if (feedChk) feedChk.checked = tAutoLLM.checked;
        if (typeof renderLiveCoachLogFeed === 'function') renderLiveCoachLogFeed();
    }

    const selectDefSubject = document.getElementById('setting-default-practice-subject');
    if (selectDefSubject) {
        gameSettings.activePracticeSubject = selectDefSubject.value;
        const mainSelect = document.getElementById('practice-subject-select');
        if (mainSelect) mainSelect.value = selectDefSubject.value;
    }

    const selectedWhite = document.querySelector('input[name="white-player-mode"]:checked');
    if (selectedWhite) gameSettings.whitePlayerMode = selectedWhite.value;

    const selectedBlack = document.querySelector('input[name="black-player-mode"]:checked');
    if (selectedBlack) gameSettings.blackPlayerMode = selectedBlack.value;

    const tAuto = document.getElementById('toggle-auto-adjust-difficulty');
    if (tAuto) gameSettings.autoAdjustDifficulty = tAuto.checked;

    const selectBias = document.getElementById('select-auto-adjust-bias');
    if (selectBias) gameSettings.autoAdjustBias = selectBias.value;

    const tClocks = document.getElementById('toggle-enable-clocks');
    if (tClocks) gameSettings.enableClocks = tClocks.checked;

    const tFlagLoss = document.getElementById('toggle-flag-automated-loss');
    if (tFlagLoss) gameSettings.flagAutomatedLoss = tFlagLoss.checked;

    const selectWClock = document.getElementById('select-white-clock-preset');
    if (selectWClock) gameSettings.whiteClockPreset = selectWClock.value;

    const inputWMins = document.getElementById('input-white-clock-mins');
    if (inputWMins) gameSettings.whiteClockMins = parseInt(inputWMins.value, 10) || 5;

    const inputWInc = document.getElementById('input-white-clock-inc');
    if (inputWInc) gameSettings.whiteClockInc = parseInt(inputWInc.value, 10) || 0;

    const selectBClock = document.getElementById('select-black-clock-preset');
    if (selectBClock) gameSettings.blackClockPreset = selectBClock.value;

    const inputBMins = document.getElementById('input-black-clock-mins');
    if (inputBMins) gameSettings.blackClockMins = parseInt(inputBMins.value, 10) || 5;

    const inputBInc = document.getElementById('input-black-clock-inc');
    if (inputBInc) gameSettings.blackClockInc = parseInt(inputBInc.value, 10) || 0;

    const whiteSlider = document.getElementById('slider-white-difficulty');
    if (whiteSlider) gameSettings.whiteDifficulty = parseInt(whiteSlider.value, 10);

    const blackSlider = document.getElementById('slider-black-difficulty');
    if (blackSlider) gameSettings.blackDifficulty = parseInt(blackSlider.value, 10);

    resetChessClocks();

    const tOverride = document.getElementById('toggle-alert-override');
    if (tOverride) gameSettings.alertOverride = tOverride.checked;
    const tRemove = document.getElementById('toggle-alert-remove');
    if (tRemove) gameSettings.alertRemove = tRemove.checked;
    const tCheck = document.getElementById('toggle-alert-check');
    if (tCheck) gameSettings.alertCheck = tCheck.checked;
    const tMate = document.getElementById('toggle-alert-mate');
    if (tMate) gameSettings.alertMate = tMate.checked;
    const tTie = document.getElementById('toggle-alert-tie');
    if (tTie) gameSettings.alertTie = tTie.checked;

    // Sync p1 / p2 settings so opening New Game Modal reflects Game Settings Dialog changes:
    if (gameSettings.whitePlayerMode === 'manual' && gameSettings.blackPlayerMode === 'auto') {
        gameSettings.p1Type = 'human';
        gameSettings.p2Type = 'bot';
        gameSettings.p2Difficulty = gameSettings.blackDifficulty;
        isFlipped = false;
    } else if (gameSettings.whitePlayerMode === 'auto' && gameSettings.blackPlayerMode === 'manual') {
        gameSettings.p1Type = 'human';
        gameSettings.p2Type = 'bot';
        gameSettings.p2Difficulty = gameSettings.whiteDifficulty;
        isFlipped = true;
    } else if (gameSettings.whitePlayerMode === 'auto' && gameSettings.blackPlayerMode === 'auto') {
        gameSettings.p1Type = 'bot';
        gameSettings.p2Type = 'bot';
        gameSettings.p1Difficulty = gameSettings.whiteDifficulty;
        gameSettings.p2Difficulty = gameSettings.blackDifficulty;
        isFlipped = false;
    } else if (gameSettings.whitePlayerMode === 'manual' && gameSettings.blackPlayerMode === 'manual') {
        gameSettings.p1Type = 'human';
        gameSettings.p2Type = 'human';
        isFlipped = false;
    }

    initBoard();
    updateClockPositionsUI();

    saveGameSettingsToStorage();
    applyGameSettingsVisuals();
    closeGameSettingsModal();
    checkAndTriggerAutoMove();
}

// ==========================================
// ✏️ BOARD EDITING & PALETTE LOGIC
// ==========================================
function buildFenFromBoardState(bState, activeColor = 'w') {
    const files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'];
    const ranks = ['8', '7', '6', '5', '4', '3', '2', '1'];

    let rows = [];
    for (let r of ranks) {
        let rowStr = '';
        let emptyCount = 0;
        for (let f of files) {
            const sq = `${f}${r}`;
            const piece = bState[sq];
            if (piece) {
                if (emptyCount > 0) {
                    rowStr += emptyCount;
                    emptyCount = 0;
                }
                const color = piece[0];
                const type = piece[1];
                rowStr += (color === 'w') ? type : type.toLowerCase();
            } else {
                emptyCount++;
            }
        }
        if (emptyCount > 0) {
            rowStr += emptyCount;
        }
        rows.push(rowStr);
    }
    const piecePlacement = rows.join('/');

    let castling = '';
    if (bState['e1'] === 'wK' && bState['h1'] === 'wR') castling += 'K';
    if (bState['e1'] === 'wK' && bState['a1'] === 'wR') castling += 'Q';
    if (bState['e8'] === 'bK' && bState['h8'] === 'bR') castling += 'k';
    if (bState['e8'] === 'bK' && bState['a8'] === 'bR') castling += 'q';
    if (!castling) castling = '-';

    return `${piecePlacement} ${activeColor} ${castling} - 0 1`;
}

function initPalettePieces() {
    document.querySelectorAll('#piece-palette-bar .piece-option').forEach(el => {
        const piece = el.dataset.piece;
        if (piece && PIECE_SVGS[piece]) {
            el.innerHTML = PIECE_SVGS[piece];
        }
        el.addEventListener('click', () => handleSelectPalettePiece(piece));
    });

    const trashBtn = document.getElementById('btn-palette-trash');
    if (trashBtn) {
        trashBtn.addEventListener('click', () => handleSelectPalettePiece('trash'));
    }

    const clearBtn = document.getElementById('btn-clear-board');
    if (clearBtn) {
        clearBtn.addEventListener('click', handleClearBoard);
    }

    const resetPaletteBtn = document.getElementById('btn-reset-initial-board');
    if (resetPaletteBtn) {
        resetPaletteBtn.addEventListener('click', handleResetInitialBoard);
    }
}

function handleSelectPalettePiece(piece) {
    if (selectedPalettePiece === piece) {
        selectedPalettePiece = null;
    } else {
        selectedPalettePiece = piece;
    }
    selectedSquare = null;
    updatePaletteSelectionUI();
    renderBoard();
}

function updatePaletteSelectionUI() {
    document.querySelectorAll('#piece-palette-bar .piece-option, #piece-palette-bar .palette-btn').forEach(el => {
        el.classList.remove('selected');
    });
    if (selectedPalettePiece) {
        if (selectedPalettePiece === 'trash') {
            const trashBtn = document.getElementById('btn-palette-trash');
            if (trashBtn) trashBtn.classList.add('selected');
        } else {
            const pieceEl = document.querySelector(`#piece-palette-bar .piece-option[data-piece="${selectedPalettePiece}"]`);
            if (pieceEl) pieceEl.classList.add('selected');
        }
    }
}

function handleClearBoard() {
    if (gameSettings.alertRemove) {
        if (!confirm('Are you sure you want to clear all pieces from the board?')) return;
    }
    boardState = {};
    selectedSquare = null;
    renderBoard();
}

function handleResetInitialBoard() {
    currentFen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1";
    parseFenToState(currentFen);
    selectedSquare = null;
    renderBoard();
}

async function toggleEditBoardMode() {
    if (!isEditBoardMode) {
        // Enter Edit Mode
        if (!isAutoPaused) {
            isAutoPaused = true;
            updatePauseResumeButtonUI();
            if (autoMoveTimer) {
                clearTimeout(autoMoveTimer);
                autoMoveTimer = null;
            }
        }
        isEditBoardMode = true;
        selectedPalettePiece = null;
        selectedSquare = null;

        const activeTurnColor = currentFen.split(' ')[1] || 'w';
        const radio = document.querySelector(`input[name="edit-active-turn"][value="${activeTurnColor}"]`);
        if (radio) radio.checked = true;

        const btnEdit = document.getElementById('btn-edit-board');
        if (btnEdit) {
            btnEdit.textContent = '✅ Done';
            btnEdit.classList.add('btn-accent');
            btnEdit.classList.remove('btn-secondary');
        }

        const paletteBar = document.getElementById('piece-palette-bar');
        if (paletteBar) paletteBar.classList.remove('hidden');

        chessboardEl.classList.add('edit-mode');
        updatePaletteSelectionUI();
        renderBoard();
    } else {
        // Finish Edit Mode
        await finishEditBoardMode();
    }
}

async function finishEditBoardMode() {
    let wKingCount = 0;
    let bKingCount = 0;
    for (let sq in boardState) {
        if (boardState[sq] === 'wK') wKingCount++;
        if (boardState[sq] === 'bK') bKingCount++;
    }

    if (wKingCount !== 1 || bKingCount !== 1) {
        alert(`Invalid Board Setup:\nA valid chess position must contain exactly 1 White King and 1 Black King.\n\nCurrent setup has ${wKingCount} White King(s) and ${bKingCount} Black King(s).`);
        return;
    }

    const activeTurnRadio = document.querySelector('input[name="edit-active-turn"]:checked');
    const activeTurn = activeTurnRadio ? activeTurnRadio.value : 'w';

    const editedFen = buildFenFromBoardState(boardState, activeTurn);

    try {
        const resp = await fetch('/api/board/evaluate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ fen: editedFen })
        });
        const data = await resp.json();

        const turnName = activeTurn === 'w' ? 'White' : 'Black';
        const isCheck = data.is_check || data.white_in_check || data.black_in_check;
        const isGameOver = data.is_game_over;
        const isMate = data.eval && data.eval.eval_type === 'mate';
        const noLegalMoves = !data.legal_moves || data.legal_moves.length === 0;

        const checkedSideText = (data.checked_sides && data.checked_sides.length > 0)
            ? data.checked_sides.join(' & ')
            : (data.black_in_check ? 'Black' : (data.white_in_check ? 'White' : turnName));

        if ((isMate || noLegalMoves) && isCheck) {
            if (gameSettings.alertMate) {
                if (!confirm(`⚠️ Position Warning:\nThis position is CHECKMATE (${turnName} has no legal moves and is in check).\n\nApply this position anyway?`)) {
                    return;
                }
            }
        } else if ((isGameOver || noLegalMoves) && !isCheck) {
            if (gameSettings.alertTie) {
                if (!confirm(`⚠️ Position Warning:\nThis position is STALEMATE / DRAW (${turnName} has no legal moves).\n\nApply this position anyway?`)) {
                    return;
                }
            }
        } else if (isCheck) {
            if (gameSettings.alertCheck) {
                if (!confirm(`⚠️ Position Warning:\nThis position puts ${checkedSideText} King in CHECK.\n\nApply this position anyway?`)) {
                    return;
                }
            }
        }

        startFen = data.fen;
        currentFen = data.fen;
        legalMoves = data.legal_moves || [];
        parseFenToState(currentFen);

        openingNameEl.textContent = data.opening || 'Custom Position';
        const scoreStr = data.eval ? data.eval.score : '+0.0';
        summaryEvalEl.textContent = scoreStr;
        evalScoreBadgeEl.textContent = scoreStr;
        summaryBestMoveEl.textContent = data.eval ? data.eval.best_move_san || '-' : '-';
        bestMoveArrow = data.eval ? data.eval.best_move : null;

        let whitePercentage = 50;
        if (data.eval && data.eval.eval_type === 'mate') {
            whitePercentage = data.eval.eval_val > 0 ? 98 : 2;
        } else if (data.eval) {
            const cp = data.eval.eval_val;
            whitePercentage = Math.min(98, Math.max(2, 50 + (cp * 10)));
        }
        evalWhiteFillEl.style.height = `${whitePercentage}%`;

        engineLinesListEl.innerHTML = '';
        if (data.eval && data.eval.top_moves) {
            data.eval.top_moves.forEach(m => {
                const li = document.createElement('li');
                li.innerHTML = `<span class="move-san">${m.san}</span> <span class="move-score">${m.score || scoreStr}</span>`;
                engineLinesListEl.appendChild(li);
            });
        }

        moveHistory = [];
        moveStackUci = [];
        lastMoveSquares = [];
        selectedSquare = null;
        selectedPalettePiece = null;
        isEditBoardMode = false;

        const btnEdit = document.getElementById('btn-edit-board');
        if (btnEdit) {
            btnEdit.textContent = '✏️ Edit Board';
            btnEdit.classList.remove('btn-accent');
            btnEdit.classList.add('btn-secondary');
        }

        const paletteBar = document.getElementById('piece-palette-bar');
        if (paletteBar) paletteBar.classList.add('hidden');

        chessboardEl.classList.remove('edit-mode');

        renderMoveHistoryTable();
        renderBoard();
        updateUndoButtonState();
        checkAndTriggerAutoMove();

    } catch (e) {
        alert('Failed to evaluate edited board position: ' + e.message);
    }
}

function handleEditModeSquareClick(sqName) {
    hasDeclaredGameOver = false;

    if (selectedPalettePiece) {
        if (selectedPalettePiece === 'trash') {
            if (boardState[sqName]) {
                delete boardState[sqName];
                triggerLiveEditBoardEval();
            }
        } else {
            if (boardState[sqName] && boardState[sqName] !== selectedPalettePiece) {
                if (gameSettings.alertOverride) {
                    const oldPiece = boardState[sqName];
                    if (!confirm(`Square ${sqName} currently contains ${oldPiece}. Replace it with ${selectedPalettePiece}?`)) return;
                }
            }
            boardState[sqName] = selectedPalettePiece;
            triggerLiveEditBoardEval();
        }
    } else {
        if (selectedSquare) {
            if (selectedSquare === sqName) {
                selectedSquare = null;
                renderBoard();
                return;
            }

            if (boardState[sqName] && boardState[sqName] !== boardState[selectedSquare]) {
                if (gameSettings.alertOverride) {
                    const oldPiece = boardState[sqName];
                    if (!confirm(`Square ${sqName} contains ${oldPiece}. Override with ${boardState[selectedSquare]}?`)) return;
                }
            }

            boardState[sqName] = boardState[selectedSquare];
            delete boardState[selectedSquare];
            selectedSquare = null;
            triggerLiveEditBoardEval();
        } else {
            if (boardState[sqName]) {
                selectedSquare = sqName;
                renderBoard();
            }
        }
    }
}

function triggerLiveEditBoardEval() {
    const activeTurnRadio = document.querySelector('input[name="edit-active-turn"]:checked');
    const activeTurn = activeTurnRadio ? activeTurnRadio.value : 'w';
    currentFen = buildFenFromBoardState(boardState, activeTurn);
    renderBoard();
    updatePositionEvaluation();
}



function applyGameSettingsVisuals() {
    if (evalBarContainerEl) {
        evalBarContainerEl.style.display = gameSettings.showScoreBar ? 'flex' : 'none';
    }
    renderBoard();
    updateUndoButtonState();
}

function checkAndTriggerAutoMove() {
    if (autoMoveTimer) {
        clearTimeout(autoMoveTimer);
        autoMoveTimer = null;
    }

    if (!currentFen || legalMoves.length === 0) return;
    if (isAutoPaused) return;

    const activeColor = currentFen.split(' ')[1]; // 'w' or 'b'
    const isWhiteAuto = (activeColor === 'w' && gameSettings.whitePlayerMode === 'auto');
    const isBlackAuto = (activeColor === 'b' && gameSettings.blackPlayerMode === 'auto');

    if (isWhiteAuto || isBlackAuto) {
        autoMoveTimer = setTimeout(async () => {
            await makeBotMove();
        }, 500);
    }
}

function handleShowHintClick() {
    overrideShowHintForCurrentMove = true;
    renderBoard();
}

function togglePauseResume() {
    isAutoPaused = !isAutoPaused;
    updatePauseResumeButtonUI();
    if (isAutoPaused) {
        if (autoMoveTimer) {
            clearTimeout(autoMoveTimer);
            autoMoveTimer = null;
        }
    } else {
        checkAndTriggerAutoMove();
    }
}

function updatePauseResumeButtonUI() {
    const btn = document.getElementById('btn-pause-resume');
    if (!btn) return;
    if (isAutoPaused) {
        btn.textContent = '▶️ Resume';
        btn.classList.add('btn-accent');
        btn.classList.remove('btn-secondary');
        btn.title = 'Resume Computer Auto-Play';
    } else {
        btn.textContent = '⏸️ Pause';
        btn.classList.add('btn-secondary');
        btn.classList.remove('btn-accent');
        btn.title = 'Pause Computer Auto-Play';
    }
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

        if (!currentNotebookId && mentorNotebookSelectEl.value) {
            currentNotebookId = mentorNotebookSelectEl.value;
        }

        document.getElementById('setting-notebook-id').value = currentNotebookId || "";

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
            headers: { 'Content-Type': 'application/json' },
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
    try {
        const resp = await fetch('/api/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                fresh: true
            })
        });
        const data = await resp.json();
        alert('🌐 Fresh Google Sign-In Window Launched!\n\nSteps to log in:\n1. Enter your Google Email in the browser window and click Next.\n2. Enter your Google Password on the next screen.\n3. Once signed in, return here and click 🔄 Refresh to load your notebooks!');
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
            headers: { 'Content-Type': 'application/json' },
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

let mentorChatFontSizePx = parseInt(localStorage.getItem('chess_mentor_chat_font_px')) || 14;

function bindBubbleDeleteAction(bubble) {
    if (!bubble) return;
    const deleteBtn = bubble.querySelector('.btn-delete-bubble');
    if (deleteBtn && !deleteBtn.dataset.bound) {
        deleteBtn.dataset.bound = 'true';
        deleteBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            bubble.remove();
        });
    }
}

function initMentorChatModule() {
    const btnInc = document.getElementById('btn-font-inc');
    const btnDec = document.getElementById('btn-font-dec');
    const btnFeedInc = document.getElementById('btn-feed-font-inc');
    const btnFeedDec = document.getElementById('btn-feed-font-dec');
    const btnClear = document.getElementById('btn-clear-chat');

    const handleFontInc = (e) => {
        if (e) e.preventDefault();
        setMentorChatFontSize(mentorChatFontSizePx + 2);
    };

    const handleFontDec = (e) => {
        if (e) e.preventDefault();
        setMentorChatFontSize(Math.max(8, mentorChatFontSizePx - 2));
    };

    if (btnInc) btnInc.addEventListener('click', handleFontInc);
    if (btnFeedInc) btnFeedInc.addEventListener('click', handleFontInc);
    if (btnDec) btnDec.addEventListener('click', handleFontDec);
    if (btnFeedDec) btnFeedDec.addEventListener('click', handleFontDec);

    if (btnClear) {
        btnClear.addEventListener('click', () => {
            if (confirm('Clear chat history?')) {
                clearMentorChatHistory();
            }
        });
    }

    // Bind delete actions to any initial bubbles
    document.querySelectorAll('#mentor-chat-messages .chat-bubble').forEach(b => bindBubbleDeleteAction(b));

    setMentorChatFontSize(mentorChatFontSizePx);

    const inputArea = document.getElementById('mentor-custom-question');
    if (inputArea) {
        inputArea.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleCustomMentorQuery();
            }
        });
    }
}

function setMentorChatFontSize(sizePx) {
    let px = parseInt(sizePx);
    if (isNaN(px) || px < 6) px = 14;
    mentorChatFontSizePx = px;

    const chatBox = document.getElementById('mentor-chat-messages');
    const feedList = document.getElementById('live-coach-log-list');
    const labelEl = document.getElementById('font-size-label');
    const feedLabelEl = document.getElementById('feed-font-size-label');

    if (chatBox) {
        chatBox.style.setProperty('--mentor-font-size', `${px}px`);
    }
    if (feedList) {
        feedList.style.setProperty('--mentor-font-size', `${px}px`);
    }

    const pixelVal = `${px}px`;
    if (labelEl) labelEl.textContent = pixelVal;
    if (feedLabelEl) feedLabelEl.textContent = pixelVal;

    localStorage.setItem('chess_mentor_chat_font_px', px.toString());
}

function clearMentorChatHistory() {
    const chatBox = document.getElementById('mentor-chat-messages');
    if (!chatBox) return;

    chatBox.innerHTML = `
        <div class="chat-bubble mentor-bubble">
            <div class="bubble-header">
                <span class="bubble-avatar">🎓</span>
                <span class="bubble-author">AI Mentor</span>
                <span class="bubble-tag">NotebookLM Standby</span>
                <button class="btn-delete-bubble" title="Clear this comment block">✖</button>
            </div>
            <div class="bubble-content">
                <p>Hello! I am your AI Chess Mentor connected to your NotebookLM chess library. Ask me any question about the position, long-term plans, or tactical motifs, or click one of the quick prompt chips above! ♟️</p>
            </div>
        </div>
    `;
    const newBubble = chatBox.querySelector('.chat-bubble');
    if (newBubble) bindBubbleDeleteAction(newBubble);
}

function appendUserChatBubble(text) {
    const chatBox = document.getElementById('mentor-chat-messages');
    if (!chatBox) return;

    const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const activeProf = (typeof getActiveProfile === 'function') ? getActiveProfile() : { name: 'Player' };
    const userName = activeProf.name || 'You';

    const bubble = document.createElement('div');
    bubble.className = 'chat-bubble user-bubble';
    bubble.innerHTML = `
        <div class="bubble-header">
            <span class="bubble-avatar">👤</span>
            <span class="bubble-author">${userName}</span>
            <span class="bubble-time">${timeStr}</span>
            <button class="btn-delete-bubble" title="Clear this comment block">✖</button>
        </div>
        <div class="bubble-content"><p>${escapeHtmlText(text)}</p></div>
    `;
    bindBubbleDeleteAction(bubble);
    chatBox.appendChild(bubble);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function appendMentorThinkingBubble() {
    const chatBox = document.getElementById('mentor-chat-messages');
    if (!chatBox) return null;

    const bubble = document.createElement('div');
    bubble.className = 'chat-bubble mentor-bubble thinking';
    bubble.innerHTML = `
        <div class="bubble-header">
            <span class="bubble-avatar">🎓</span>
            <span class="bubble-author">AI Mentor</span>
            <span class="bubble-tag">Consulting NotebookLM...</span>
            <button class="btn-delete-bubble" title="Clear this comment block">✖</button>
        </div>
        <div class="bubble-content">
            <div class="typing-dots">
                <span></span><span></span><span></span>
            </div>
        </div>
    `;
    bindBubbleDeleteAction(bubble);
    chatBox.appendChild(bubble);
    chatBox.scrollTop = chatBox.scrollHeight;
    return bubble;
}

function extractTurnRuleTextSnippet(text) {
    if (!text) return 'Maintain Strategic Connectivity';

    // 1. Check for explicit GENERALIZED TURN RULE section from structured prompt
    const ruleMatch = text.match(/(?:💡\s*)?(?:GENERALIZED\s+)?TURN\s+RULE:\s*([^\n]+)/i) ||
                      text.match(/(?:🎓\s*)?(?:GENERALIZED\s+)?RULE:\s*([^\n]+)/i);
    if (ruleMatch && ruleMatch[1]) {
        let rule = ruleMatch[1].replace(/[`*~_]/g, '').trim();
        rule = rule.replace(/^[?:,.\s]+|[?:,.\s]+$/g, '').trim();
        if (rule.length > 5) {
            if (rule.length > 55) return rule.slice(0, 52) + '...';
            return rule;
        }
    }

    // 2. Parse lines for general strategic principles, excluding specific move notation (like 7...Na5)
    let cleaned = text.replace(/<[^>]*>/g, '')
                      .replace(/#+\s+/g, '')
                      .replace(/[🎓🛡️♟️⚔️🎯⚠️🏰👑📍📌💡]/g, '')
                      .trim();

    const lines = cleaned.split('\n').map(l => l.trim()).filter(l => l.length > 0);
    let targetPhrase = '';

    for (const l of lines) {
        if (/(?:rule|takeaway|remember|key focus|principle|priority):/i.test(l)) {
            targetPhrase = l.replace(/^(?:rule|takeaway|remember|key focus|principle|priority):\s*/i, '');
            break;
        } else if (/(?:when|always|never|prioritize|maintain|exploit|target|avoid|ensure)/i.test(l) && !/\b\d+\.\.\.|\b[a-h][1-8]\b/i.test(l)) {
            targetPhrase = l;
            break;
        }
    }

    if (!targetPhrase) {
        for (const l of lines) {
            if (l.length > 15 && !/\b\d+\.\.\.|\b[a-h][1-8]\b/i.test(l) && !/welcome to/i.test(l) && !/position overview/i.test(l)) {
                targetPhrase = l;
                break;
            }
        }
    }

    if (!targetPhrase && lines.length > 0) {
        targetPhrase = lines[0].replace(/\b\d+\.\.\.[\w\d\s.]+/g, 'the variation').trim();
    }

    targetPhrase = targetPhrase.replace(/^[?:,.\s]+|[?:,.\s]+$/g, '').trim();

    if (targetPhrase.length > 55) {
        return targetPhrase.slice(0, 52) + '...';
    }
    return targetPhrase || 'Maintain Strategic Connectivity';
}

function updateMentorBubbleWithResponse(bubbleEl, responseText, provider) {
    if (!bubbleEl) return;

    const tagEl = bubbleEl.querySelector('.bubble-tag');
    if (tagEl) {
        tagEl.textContent = provider || 'NotebookLM';
    }

    const contentEl = bubbleEl.querySelector('.bubble-content');
    if (contentEl) {
        contentEl.innerHTML = formatMarkdownToHtml(responseText);
        
        const ruleSnippet = extractTurnRuleTextSnippet(responseText);
        const fullCleanText = responseText.replace(/<[^>]*>?/gm, '').trim();

        const actionRow = document.createElement('div');
        actionRow.style.cssText = 'display:flex; justify-content:flex-end; margin-top:8px;';
        actionRow.innerHTML = `<button class="btn btn-xs btn-secondary save-as-rule-btn" style="font-size:0.88em; padding:4px 12px; max-width:100%; white-space:normal; text-align:left; word-break:break-word;" title="Click to review and save '${escapeHtmlText(ruleSnippet)}' as a turn rule">➕ Save "${escapeHtmlText(ruleSnippet)}" as Turn Rule</button>`;
        actionRow.querySelector('.save-as-rule-btn').addEventListener('click', () => {
            openGuidelineModal({
                title: ruleSnippet || 'Mentor Takeaway Rule',
                category: 'Strategy',
                text: fullCleanText || responseText.slice(0, 180),
                citations: '[AI Mentor Chat Recommendation]'
            });
        });
        contentEl.appendChild(actionRow);
    }

    bubbleEl.classList.remove('thinking');

    const chatBox = document.getElementById('mentor-chat-messages');
    if (chatBox) chatBox.scrollTop = chatBox.scrollHeight;
}

function escapeHtmlText(str) {
    if (!str) return '';
    return str.replace(/&/g, "&amp;")
              .replace(/</g, "&lt;")
              .replace(/>/g, "&gt;")
              .replace(/"/g, "&quot;")
              .replace(/'/g, "&#039;");
}

async function requestMentorInsight(customQuestion = null) {
    const questionText = customQuestion || "Explain the overall strategic theme in this position.";
    appendUserChatBubble(questionText);

    const thinkingBubble = appendMentorThinkingBubble();
    const modeRadio = document.querySelector('input[name="translator-mode"]:checked');
    const selectedMode = modeRadio ? modeRadio.value : 'human';

    try {
        const subjectSelect = document.getElementById('practice-subject-select');
        const activeSubject = subjectSelect ? subjectSelect.value : (gameSettings.activePracticeSubject || 'auto');
        const currentRules = typeof getGlobalTurnGuidelines === 'function' ? getGlobalTurnGuidelines() : [];

        const activeProfile = typeof getActiveProfile === 'function' ? getActiveProfile() : null;

        const isWhiteManual = (gameSettings.whitePlayerMode === 'manual');
        const isBlackManual = (gameSettings.blackPlayerMode === 'manual');
        let studentColor = 'white';
        if (!isWhiteManual && isBlackManual) {
            studentColor = 'black';
        } else if (isWhiteManual && !isBlackManual) {
            studentColor = 'white';
        } else if (isFlipped) {
            studentColor = 'black';
        }

        const resp = await fetch('/api/mentor/explain', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                fen: currentFen || startFen,
                moves: moveHistory,
                mode: selectedMode,
                question: customQuestion,
                student_color: studentColor,
                practice_subject: activeSubject,
                turn_guidelines: currentRules,
                user_profile: activeProfile,
                notebook_id: currentNotebookId
            })
        });
        const data = await resp.json();

        const provider = data.provider || "NotebookLM / Local";
        if (mentorProviderBadgeEl) mentorProviderBadgeEl.textContent = provider;
        updateMentorBubbleWithResponse(thinkingBubble, data.response || "No explanation content returned.", provider);

    } catch (e) {
        updateMentorBubbleWithResponse(thinkingBubble, `Failed to get AI mentor explanation: ${e.message}`, "Error");
    }
}

function handleCustomMentorQuery() {
    const qEl = document.getElementById('mentor-custom-question');
    if (!qEl) return;
    const question = qEl.value.trim();
    if (!question) return;
    qEl.value = '';
    requestMentorInsight(question);
}

function triggerQuickPromptChip(promptText) {
    requestMentorInsight(promptText);
}

function formatMarkdownToHtml(md) {
    if (!md || typeof md !== 'string') return '<p class="placeholder-text">No explanation content returned.</p>';
    let html = md
        .replace(/^---$/gim, '<hr class="section-divider">')
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
            headers: { 'Content-Type': 'application/json' },
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

function appendPromptTemplate(templateText) {
    const qEl = document.getElementById('mentor-custom-question');
    if (!qEl) return;
    const curVal = qEl.value.trim();
    if (!curVal) {
        qEl.value = templateText;
    } else {
        qEl.value = curVal + "\n\n" + templateText;
    }
    qEl.focus();
}

function initAccountCardToggle() {
    const card = document.getElementById('account-card');
    const header = document.getElementById('account-card-header');
    if (!card || !header) return;

    header.addEventListener('click', (e) => {
        if (e.target.tagName === 'BUTTON' && e.target.id !== 'btn-toggle-account') return;
        card.classList.toggle('collapsed');
    });
}

function initSidebarResizer() {
    const resizer = document.getElementById('sidebar-resizer');
    const sidebar = document.querySelector('.sidebar-section');
    if (!resizer || !sidebar) return;

    let isDragging = false;
    let startX = 0;
    let startWidth = 0;

    resizer.addEventListener('mousedown', (e) => {
        isDragging = true;
        startX = e.clientX;
        startWidth = sidebar.offsetWidth;
        resizer.classList.add('dragging');
        document.body.style.cursor = 'col-resize';
        document.body.style.userSelect = 'none';
    });

    document.addEventListener('mousemove', (e) => {
        if (!isDragging) return;
        const deltaX = startX - e.clientX;
        const newWidth = Math.max(320, Math.min(window.innerWidth * 0.75, startWidth + deltaX));
        sidebar.style.width = `${newWidth}px`;
    });

    document.addEventListener('mouseup', () => {
        if (isDragging) {
            isDragging = false;
            resizer.classList.remove('dragging');
            document.body.style.cursor = '';
            document.body.style.userSelect = '';
        }
    });
}

// ==========================================
// 💾 GAME & FEN/PGN MANAGER LOGIC
// ==========================================
let savedGames = [];

function loadSavedGamesFromStorage() {
    const saved = localStorage.getItem('chess_saved_games');
    if (saved) {
        try {
            savedGames = JSON.parse(saved);
        } catch (e) {
            savedGames = [];
        }
    }
}

function saveSavedGamesToStorage() {
    localStorage.setItem('chess_saved_games', JSON.stringify(savedGames));
}

function openGameManagerModal() {
    const modal = document.getElementById('game-manager-modal');
    if (!modal) return;

    if (!isAutoPaused) {
        isAutoPaused = true;
        updatePauseResumeButtonUI();
        if (autoMoveTimer) {
            clearTimeout(autoMoveTimer);
            autoMoveTimer = null;
        }
    }

    loadSavedGamesFromStorage();
    renderSavedGamesList();

    const fenText = document.getElementById('fen-input-text');
    if (fenText) fenText.value = currentFen;

    generateCurrentPgnText();

    modal.classList.remove('hidden');
}

function closeGameManagerModal() {
    const modal = document.getElementById('game-manager-modal');
    if (modal) modal.classList.add('hidden');
}

function initManagerSubtabs() {
    document.querySelectorAll('.subtab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.subtab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.subtab-content').forEach(c => c.classList.remove('active'));
            btn.classList.add('active');
            const target = document.getElementById(btn.dataset.subtab);
            if (target) target.classList.add('active');
        });
    });
}

function saveCurrentGame() {
    const titleInput = document.getElementById('save-game-title');
    const notesInput = document.getElementById('save-game-notes');
    const title = (titleInput && titleInput.value.trim()) || `Game - ${new Date().toLocaleDateString()} ${new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`;
    const notes = notesInput ? notesInput.value.trim() : '';

    const newGame = {
        id: 'game_' + Date.now(),
        title: title,
        date: new Date().toLocaleString(),
        fen: currentFen,
        moves: [...moveHistory],
        notes: notes
    };

    savedGames.unshift(newGame);
    saveSavedGamesToStorage();
    renderSavedGamesList();

    if (titleInput) titleInput.value = '';
    if (notesInput) notesInput.value = '';
    alert('Game saved to library successfully!');
}

function renderSavedGamesList() {
    const listEl = document.getElementById('saved-games-list');
    if (!listEl) return;
    listEl.innerHTML = '';

    if (savedGames.length === 0) {
        listEl.innerHTML = '<p class="placeholder-text">No saved games yet. Save your current game above!</p>';
        return;
    }

    savedGames.forEach(g => {
        const card = document.createElement('div');
        card.className = 'saved-game-card';
        card.innerHTML = `
            <div class="saved-game-info">
                <span class="saved-game-title">${g.title}</span>
                <span class="saved-game-meta">📅 ${g.date} | ♟️ ${g.moves ? g.moves.length : 0} moves ${g.notes ? '| 📝 ' + g.notes : ''}</span>
            </div>
            <div class="saved-game-actions">
                <button class="btn btn-secondary btn-sm" data-action="load" data-id="${g.id}">▶️ Load</button>
                <button class="btn btn-secondary btn-sm" data-action="export" data-id="${g.id}">📥 PGN</button>
                <button class="btn btn-secondary btn-sm" data-action="delete" data-id="${g.id}">🗑️</button>
            </div>
        `;

        card.querySelector('[data-action="load"]').addEventListener('click', () => loadSavedGame(g.id));
        card.querySelector('[data-action="export"]').addEventListener('click', () => exportSavedGamePgn(g.id));
        card.querySelector('[data-action="delete"]').addEventListener('click', () => deleteSavedGame(g.id));

        listEl.appendChild(card);
    });
}

async function loadSavedGame(gameId) {
    const game = savedGames.find(g => g.id === gameId);
    if (!game) return;

    if (game.moves && game.moves.length > 0) {
        moveHistory = [];
        moveStackUci = [];
        currentFen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1";
        parseFenToState(currentFen);

        for (let m of game.moves) {
            moveHistory.push(m);
        }
        await updatePositionEvaluation();
    } else if (game.fen) {
        currentFen = game.fen;
        moveHistory = [];
        moveStackUci = [];
        await updatePositionEvaluation();
    }
    closeGameManagerModal();
    alert(`Loaded game: "${game.title}"`);
}

async function exportSavedGamePgn(gameId) {
    const game = savedGames.find(g => g.id === gameId);
    if (!game) return;

    try {
        const resp = await fetch('/api/pgn/export', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                moves: game.moves || [],
                fen: game.fen || null,
                headers: {
                    Event: game.title,
                    Site: "Chess AI Mentor Library"
                }
            })
        });
        const data = await resp.json();
        if (data.pgn) {
            const blob = new Blob([data.pgn], { type: 'text/plain;charset=utf-8' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${game.title.replace(/[^a-z0-9]/gi, '_')}.pgn`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }
    } catch (e) {
        alert('Failed to export PGN: ' + e.message);
    }
}

function deleteSavedGame(gameId) {
    if (!confirm('Are you sure you want to delete this saved game?')) return;
    savedGames = savedGames.filter(g => g.id !== gameId);
    saveSavedGamesToStorage();
    renderSavedGamesList();
}

function copyFenToClipboard() {
    const fenText = document.getElementById('fen-input-text').value;
    navigator.clipboard.writeText(fenText).then(() => {
        alert('FEN copied to clipboard!');
    }).catch(() => {
        alert('Copied FEN text.');
    });
}

async function loadFenFromInput() {
    const fenVal = document.getElementById('fen-input-text').value.trim();
    if (!fenVal) {
        alert('Please enter a valid FEN string.');
        return;
    }
    try {
        const resp = await fetch('/api/board/evaluate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ fen: fenVal })
        });
        const data = await resp.json();

        startFen = data.fen;
        currentFen = data.fen;
        legalMoves = data.legal_moves || [];
        parseFenToState(currentFen);
        moveHistory = [];
        moveStackUci = [];
        lastMoveSquares = [];
        selectedSquare = null;

        renderMoveHistoryTable();
        renderBoard();
        updateUndoButtonState();
        closeGameManagerModal();
        alert('FEN loaded onto board successfully!');
    } catch (e) {
        alert('Invalid FEN string: ' + e.message);
    }
}

async function generateCurrentPgnText() {
    const pgnArea = document.getElementById('pgn-input-text');
    if (!pgnArea) return;

    const activeProf = (typeof getActiveProfile === 'function') ? getActiveProfile() : { name: 'Player' };
    const profileName = activeProf.name || 'Human Player';

    const wIsAuto = (gameSettings.whitePlayerMode === 'auto');
    const bIsAuto = (gameSettings.blackPlayerMode === 'auto');

    let whiteHeader = wIsAuto ? `Stockfish Level ${gameSettings.whiteDifficulty}` : profileName;
    let blackHeader = bIsAuto ? `Stockfish Level ${gameSettings.blackDifficulty}` : (!wIsAuto ? 'Black' : profileName);

    try {
        const resp = await fetch('/api/pgn/export', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                moves: moveHistory,
                headers: {
                    White: whiteHeader,
                    Black: blackHeader
                }
            })
        });
        const data = await resp.json();
        if (data.pgn) {
            pgnArea.value = data.pgn;
        }
    } catch (e) {
        console.error('Failed to generate PGN:', e);
    }
}

function copyPgnToClipboard() {
    const pgnText = document.getElementById('pgn-input-text').value;
    if (!pgnText) return;
    navigator.clipboard.writeText(pgnText).then(() => {
        alert('PGN copied to clipboard!');
    }).catch(() => {
        alert('Copied PGN text.');
    });
}

function downloadPgnFile() {
    const pgnText = document.getElementById('pgn-input-text').value;
    if (!pgnText) {
        alert('No PGN text available to download.');
        return;
    }
    const blob = new Blob([pgnText], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `chess_game_${Date.now()}.pgn`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

async function loadPgnFromInput() {
    const pgnVal = document.getElementById('pgn-input-text').value.trim();
    if (!pgnVal) {
        alert('Please enter or upload valid PGN text.');
        return;
    }
    try {
        const resp = await fetch('/api/pgn/parse', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ pgn: pgnVal })
        });
        const data = await resp.json();

        if (data.san_moves && data.san_moves.length > 0) {
            moveHistory = [...data.san_moves];
            moveStackUci = [...data.uci_moves];
            currentFen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1";
            parseFenToState(currentFen);
            await updatePositionEvaluation();
            closeGameManagerModal();
            alert(`PGN game loaded successfully (${data.san_moves.length} moves).`);
        } else if (data.final_fen) {
            currentFen = data.final_fen;
            moveHistory = [];
            moveStackUci = [];
            await updatePositionEvaluation();
            closeGameManagerModal();
            alert('Loaded initial PGN position onto board.');
        } else {
            alert('No moves found in PGN.');
        }
    } catch (e) {
        alert('Failed to parse PGN: ' + e.message);
    }
}

function handlePgnFileUpload(e) {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (evt) => {
        const content = evt.target.result;
        const pgnArea = document.getElementById('pgn-input-text');
        if (pgnArea) pgnArea.value = content;
        loadPgnFromInput();
    };
    reader.readAsText(file);
}

// ==========================================
// 👤 USER PROFILES & CONCEPT SKILL MATRIX MODULE
// ==========================================

const DEFAULT_PROFILES = [
    {
        id: 'prof_default',
        name: 'Player',
        elo: 1500,
        gamesPlayed: 0,
        wins: 0,
        draws: 0,
        losses: 0,
        concepts: {
            offensive: { name: 'Offensive Strategy', rating: 1500, icon: '⚔️' },
            defensive: { name: 'Defensive Maneuvers', rating: 1450, icon: '🛡️' },
            tactics: { name: 'Tactics & Forks', rating: 1520, icon: '⚡' },
            batteries: { name: 'Battery Attacks', rating: 1480, icon: '🔋' },
            pins: { name: 'Pins & Skewers', rating: 1510, icon: '🎯' },
            endgame: { name: 'Endgame & Gambits', rating: 1460, icon: '♟️' }
        }
    }
];

let userProfiles = [];
let activeProfileId = 'prof_default';

function initUserProfileModule() {
    loadUserProfilesFromStorage();
    updateHeaderProfileUI();
    updateClockPlayerTypesUI();

    const headerBadge = document.getElementById('header-profile-badge');
    if (headerBadge) headerBadge.addEventListener('click', openProfileModal);

    document.querySelectorAll('.clock-card').forEach(card => {
        card.style.cursor = 'pointer';
        card.title = 'Click to open User Profiles & Skill Matrix';
        card.addEventListener('click', (e) => {
            openProfileModal();
        });
    });
}

function loadUserProfilesFromStorage() {
    const savedProfiles = localStorage.getItem('chess_user_profiles');
    const savedActiveId = localStorage.getItem('chess_active_profile_id');

    if (savedProfiles) {
        try {
            userProfiles = JSON.parse(savedProfiles);
        } catch (e) {
            userProfiles = DEFAULT_PROFILES;
        }
    } else {
        userProfiles = DEFAULT_PROFILES;
        saveUserProfilesToStorage();
    }

    if (savedActiveId && userProfiles.some(p => p.id === savedActiveId)) {
        activeProfileId = savedActiveId;
    } else if (userProfiles.length > 0) {
        activeProfileId = userProfiles[0].id;
    }
}

function saveUserProfilesToStorage() {
    localStorage.setItem('chess_user_profiles', JSON.stringify(userProfiles));
    localStorage.setItem('chess_active_profile_id', activeProfileId);
}

function getActiveProfile() {
    return userProfiles.find(p => p.id === activeProfileId) || userProfiles[0] || DEFAULT_PROFILES[0];
}

function updateHeaderProfileUI() {
    const prof = getActiveProfile();
    const nameEl = document.getElementById('header-profile-name');
    const eloEl = document.getElementById('header-profile-elo');

    if (nameEl) nameEl.textContent = prof.name;
    if (eloEl) eloEl.textContent = `${prof.elo} ELO`;
}

function openProfileModal() {
    const modal = document.getElementById('user-profile-modal');
    if (!modal) return;

    if (!isAutoPaused) {
        isAutoPaused = true;
        updatePauseResumeButtonUI();
        if (autoMoveTimer) {
            clearTimeout(autoMoveTimer);
            autoMoveTimer = null;
        }
    }

    renderProfileSummaryCard();
    renderSkillBreakdownTab();
    renderConversionsTab();
    renderProfilesListTab();

    modal.classList.remove('hidden');
}

function closeProfileModal() {
    const modal = document.getElementById('user-profile-modal');
    if (modal) modal.classList.add('hidden');
}

function initProfileSubtabs() {
    document.querySelectorAll('[data-profile-tab]').forEach(btn => {
        btn.addEventListener('click', () => {
            const modal = document.getElementById('user-profile-modal');
            if (!modal) return;
            modal.querySelectorAll('[data-profile-tab]').forEach(b => b.classList.remove('active'));
            modal.querySelectorAll('.profile-tab-content').forEach(c => c.classList.remove('active'));

            btn.classList.add('active');
            const target = document.getElementById(btn.dataset.profileTab);
            if (target) target.classList.add('active');
        });
    });
}

function getSkillTierName(elo) {
    if (elo < 1200) return 'Novice / Beginner';
    if (elo < 1400) return 'Casual Player';
    if (elo < 1600) return 'Intermediate Player';
    if (elo < 1800) return 'Advanced Club Player';
    if (elo < 2000) return 'Expert / Candidate Master';
    return 'Master Level';
}

function renderProfileSummaryCard() {
    const prof = getActiveProfile();
    const nameEl = document.getElementById('profile-card-name');
    const tierEl = document.getElementById('profile-card-tier');
    const eloEl = document.getElementById('profile-card-elo');
    const gamesEl = document.getElementById('profile-card-games');
    const recordEl = document.getElementById('profile-card-record');
    const winrateEl = document.getElementById('profile-card-winrate');

    if (nameEl) nameEl.textContent = prof.name;
    if (tierEl) tierEl.textContent = `${getSkillTierName(prof.elo)} (~${prof.elo})`;
    if (eloEl) eloEl.textContent = prof.elo;

    const wins = prof.wins || 0;
    const draws = prof.draws || 0;
    const losses = prof.losses || 0;
    const total = prof.gamesPlayed || (wins + draws + losses);

    if (gamesEl) gamesEl.textContent = total;
    if (recordEl) recordEl.textContent = `${wins}W - ${draws}D - ${losses}L`;

    const wr = total > 0 ? Math.round((wins / total) * 100) : 0;
    if (winrateEl) winrateEl.textContent = total > 0 ? `${wr}%` : '0% (No Games)';
}

function renderSkillBreakdownTab() {
    const grid = document.getElementById('profile-skills-grid');
    if (!grid) return;

    const prof = getActiveProfile();
    const concepts = prof.concepts || DEFAULT_PROFILES[0].concepts;

    grid.innerHTML = '';

    Object.keys(concepts).forEach(key => {
        const item = concepts[key];
        const rating = item.rating || prof.elo;
        const progressPct = Math.min(100, Math.max(10, Math.round(((rating - 800) / 1600) * 100)));

        const card = document.createElement('div');
        card.className = 'skill-card';
        card.innerHTML = `
            <div class="skill-header">
                <span class="skill-title">${item.icon} ${item.name}</span>
                <span class="skill-rating-val">${rating} ELO</span>
            </div>
            <div class="skill-progress-track">
                <div class="skill-progress-fill" style="width: ${progressPct}%"></div>
            </div>
        `;
        grid.appendChild(card);
    });
}

function renderConversionsTab() {
    const grid = document.getElementById('profile-conversions-grid');
    if (!grid) return;

    const prof = getActiveProfile();
    const baseElo = prof.elo;

    const conversions = [
        { system: 'FIDE Rating', score: Math.round(baseElo * 0.97 - 20) },
        { system: 'USCF Rating', score: Math.round(baseElo * 1.03 + 30) },
        { system: 'Chess.com Blitz', score: Math.round(baseElo * 1.05) },
        { system: 'Lichess Classical', score: Math.round(baseElo * 1.15 + 100) },
        { system: 'ECF Rating', score: Math.round((baseElo - 600) / 8) }
    ];

    grid.innerHTML = '';
    conversions.forEach(c => {
        const card = document.createElement('div');
        card.className = 'conversion-card';
        card.innerHTML = `
            <span class="conversion-system-title">${c.system}</span>
            <span class="conversion-score">~${c.score}</span>
        `;
        grid.appendChild(card);
    });
}

function renderProfilesListTab() {
    const list = document.getElementById('profiles-list');
    if (!list) return;

    list.innerHTML = '';

    userProfiles.forEach(p => {
        const isActive = p.id === activeProfileId;
        const wins = p.wins || 0;
        const draws = p.draws || 0;
        const losses = p.losses || 0;
        const total = p.gamesPlayed || (wins + draws + losses);
        const wr = total > 0 ? Math.round((wins / total) * 100) : 0;

        const card = document.createElement('div');
        card.className = `profile-item-card ${isActive ? 'active-profile' : ''}`;
        card.style.cursor = 'pointer';
        card.innerHTML = `
            <div class="profile-item-info">
                <span class="profile-item-name">${p.name} ${isActive ? '⭐ (Active)' : ''}</span>
                <span class="profile-item-elo">${p.elo} ELO • ${wins}W / ${draws}D / ${losses}L (${wr}% Win Rate)</span>
            </div>
            <div class="saved-game-actions">
                ${!isActive ? `<button class="btn btn-secondary btn-sm" data-action="switch-prof" data-id="${p.id}">▶️ Switch</button>` : ''}
                ${userProfiles.length > 1 ? `<button class="btn btn-secondary btn-sm" data-action="delete-prof" data-id="${p.id}">🗑️</button>` : ''}
            </div>
        `;

        card.addEventListener('click', (e) => {
            if (e.target.closest('[data-action="delete-prof"]')) return;
            if (!isActive) switchActiveProfile(p.id);
        });

        const delBtn = card.querySelector('[data-action="delete-prof"]');
        if (delBtn) delBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            deleteUserProfile(p.id);
        });

        list.appendChild(card);
    });
}

function handleCreateProfile() {
    const nameInput = document.getElementById('new-profile-name');
    const eloSelect = document.getElementById('new-profile-starting-elo');

    const name = nameInput ? nameInput.value.trim() : '';
    if (!name) {
        alert('Please enter a profile name.');
        return;
    }

    const startingElo = parseInt(eloSelect ? eloSelect.value : '1500', 10);
    const newProf = {
        id: 'prof_' + Date.now(),
        name: name,
        elo: startingElo,
        gamesPlayed: 0,
        wins: 0,
        draws: 0,
        losses: 0,
        concepts: {
            offensive: { name: 'Offensive Strategy', rating: startingElo, icon: '⚔️' },
            defensive: { name: 'Defensive Maneuvers', rating: Math.max(800, startingElo - 50), icon: '🛡️' },
            tactics: { name: 'Tactics & Forks', rating: startingElo + 20, icon: '⚡' },
            batteries: { name: 'Battery Attacks', rating: startingElo - 20, icon: '🔋' },
            pins: { name: 'Pins & Skewers', rating: startingElo + 10, icon: '🎯' },
            endgame: { name: 'Endgame & Gambits', rating: Math.max(800, startingElo - 40), icon: '♟️' }
        }
    };

    userProfiles.push(newProf);
    activeProfileId = newProf.id;
    saveUserProfilesToStorage();
    updateHeaderProfileUI();
    updateClockPlayerTypesUI();

    if (nameInput) nameInput.value = '';
    renderProfileSummaryCard();
    renderSkillBreakdownTab();
    renderConversionsTab();
    renderProfilesListTab();

    alert(`Created and activated profile "${name}" (${startingElo} ELO).`);
}

function switchActiveProfile(profId) {
    if (!userProfiles.some(p => p.id === profId)) return;
    activeProfileId = profId;
    saveUserProfilesToStorage();
    updateHeaderProfileUI();
    updateClockPlayerTypesUI();
    updateDifficultyUIControls();

    renderProfileSummaryCard();
    renderSkillBreakdownTab();
    renderConversionsTab();
    renderProfilesListTab();
}

function deleteUserProfile(profId) {
    if (userProfiles.length <= 1) {
        alert('You must keep at least one profile.');
        return;
    }

    const target = userProfiles.find(p => p.id === profId);
    if (!target) return;

    if (!confirm(`Are you sure you want to delete profile "${target.name}"?`)) return;

    userProfiles = userProfiles.filter(p => p.id !== profId);
    if (activeProfileId === profId) {
        activeProfileId = userProfiles[0].id;
    }

    saveUserProfilesToStorage();
    updateHeaderProfileUI();

    renderProfileSummaryCard();
    renderSkillBreakdownTab();
    renderConversionsTab();
    renderProfilesListTab();
}

// ==========================================
// 🎯 AI MENTOR PLACEMENT TEST MODULE
// ==========================================

// Backup & Restore Main Board State during Diagnostic Quizzes
let savedMainBoardFen = null;
let savedMainBoardState = null;
let savedMainMoveHistory = null;
let savedMainMoveStackUci = null;
let isQuizActive = false;

function backupMainBoardState() {
    if (isQuizActive) return;
    savedMainBoardFen = currentFen;
    savedMainBoardState = JSON.parse(JSON.stringify(boardState));
    savedMainMoveHistory = [...moveHistory];
    savedMainMoveStackUci = [...moveStackUci];
    isQuizActive = true;
}

function restoreMainBoardState() {
    if (!isQuizActive || !savedMainBoardFen) return;
    currentFen = savedMainBoardFen;
    boardState = savedMainBoardState ? JSON.parse(JSON.stringify(savedMainBoardState)) : {};
    moveHistory = savedMainMoveHistory ? [...savedMainMoveHistory] : [];
    moveStackUci = savedMainMoveStackUci ? [...savedMainMoveStackUci] : [];
    isQuizActive = false;
    parseFenToState(currentFen);
    renderBoard();
    updatePositionEvaluation();
}

const QUESTION_BANK = {
    tactics: [
        {
            elo: 1100,
            concept: 'tactics',
            title: "⚡ Tactical Awareness — Knight Fork (1100 ELO)",
            desc: "Look at the main board: White's Knight on e5 can jump to c7, checking Black's King and threatening the undefended Rook on a8. What is your strategic move?",
            fen: "r1bqkb1r/pppp1ppp/5n2/4N3/4P3/8/PPPP1PPP/RNBQKB1R w KQkq - 1 4",
            options: [
                { text: "⚡ Play Nc7+ (Fork King & Rook to win material)", isCorrect: true, eloBonus: 250 },
                { text: "🛡️ Retreat Bishop to d3 defensively", isCorrect: false, eloBonus: 50 },
                { text: "♟️ Push h3 pawn to create an escape square", isCorrect: false, eloBonus: 20 }
            ]
        },
        {
            elo: 1500,
            concept: 'tactics',
            title: "⚡ Discovered Attack & Queen Trap (1500 ELO)",
            desc: "Look at the main board: White's Bishop on c4 blocks a line of sight from White's Queen to Black's Queen on d5. Moving the Bishop gives check!",
            fen: "r1b1k2r/pppp1ppp/8/3q4/2B1n3/5N2/PPPP1PPP/RNBQK2R w KQkq - 0 7",
            options: [
                { text: "⚡ Play Bxf7+ (Discovered attack capturing Black's Queen)", isCorrect: true, eloBonus: 250 },
                { text: "🛡️ Castle King-side O-O", isCorrect: false, eloBonus: 80 },
                { text: "♟️ Play d3 pawn push", isCorrect: false, eloBonus: 50 }
            ]
        },
        {
            elo: 1900,
            concept: 'tactics',
            title: "⚡ Smothered Mate Sequence (1900 ELO)",
            desc: "Look at the main board: Black's King is boxed in on h8. How can White force a Smothered Mate sequence?",
            fen: "6rk/5Npp/8/8/8/8/5PPP/6K1 w - - 0 1",
            options: [
                { text: "⚡ Play Nh6+ double check forcing Smothered Mate", isCorrect: true, eloBonus: 250 },
                { text: "🛡️ Trade Rooks on the back rank", isCorrect: false, eloBonus: 50 },
                { text: "♟️ Retreat Knight to e5", isCorrect: false, eloBonus: 30 }
            ]
        }
    ],
    defensive: [
        {
            elo: 1200,
            concept: 'defensive',
            title: "🛡️ Defensive Setup — King Safety (1200 ELO)",
            desc: "Look at the main board: Black is preparing a central pawn break while White's King remains in the center. What is your defensive priority?",
            fen: "r1bqk2r/pppp1ppp/2n2n2/2b1p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4",
            options: [
                { text: "🛡️ Play O-O (Castle immediately for King safety)", isCorrect: true, eloBonus: 250 },
                { text: "⚔️ Push d4 opening central files", isCorrect: false, eloBonus: 100 },
                { text: "♟️ Push h3 pawn", isCorrect: false, eloBonus: 50 }
            ]
        },
        {
            elo: 1600,
            concept: 'defensive',
            title: "🛡️ Defensive Fortification against Pawn Storm (1600 ELO)",
            desc: "Look at the main board: Black is launching a dangerous King-side pawn storm. What defensive anchor move do you choose?",
            fen: "r1bq1rk1/ppp2ppp/2n5/3qp3/3P4/2PB1N2/PP3PPP/R2Q1RK1 w - - 0 10",
            options: [
                { text: "🛡️ Anchor Knight on f3 to defend key King-side squares", isCorrect: true, eloBonus: 250 },
                { text: "⚔️ Counter-attack aggressively on the Queen-side", isCorrect: false, eloBonus: 120 },
                { text: "🏃 Push King-side pawns forward into Black's storm", isCorrect: false, eloBonus: 40 }
            ]
        },
        {
            elo: 2000,
            concept: 'defensive',
            title: "🛡️ Prophylaxis — Preventing Sacrifices (2000 ELO)",
            desc: "Look at the main board: Black is aiming for a Greek Gift sacrifice (Bxh2+). How do you neutralize the threat before it starts?",
            fen: "r1bq1rk1/ppp2p1p/2n2np1/3pp3/3PP3/2PB1N2/PP3PPP/RN1QR1K1 w - - 0 10",
            options: [
                { text: "🛡️ Play h3 or Re1 (Prophylactic moves suppressing the sacrifice)", isCorrect: true, eloBonus: 250 },
                { text: "⚔️ Push e5 immediately opening central lines", isCorrect: false, eloBonus: 80 },
                { text: "♟️ Step King to h1 in the corner", isCorrect: false, eloBonus: 50 }
            ]
        },
        {
            elo: 1400,
            concept: 'defensive',
            title: "🛡️ Solidifying Pawn Structure (1400 ELO)",
            desc: "Look at the main board: Black is attacking your central e4 pawn with Knight and Pawn. What is the most solid defensive consolidation?",
            fen: "r1bqkb1r/pp3ppp/2n5/2ppP3/3P4/5N2/PP3PPP/R1BQKB1R w KQkq c6 0 8",
            options: [
                { text: "🛡️ Play c3 (Reinforce d4 pawn center and defend control)", isCorrect: true, eloBonus: 250 },
                { text: "⚔️ Trade pawns on c5 immediately", isCorrect: false, eloBonus: 90 },
                { text: "♟️ Push a3 to prevent Bb4", isCorrect: false, eloBonus: 60 }
            ]
        }
    ],
    offensive: [
        {
            elo: 1100,
            concept: 'offensive',
            title: "⚔️ Offensive Strategy — Opening Central Files (1100 ELO)",
            desc: "Look at the main board: White is preparing a central pawn thrust. Which move opens lines of attack towards Black's uncastled King?",
            fen: "r1bqk2r/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 0 5",
            options: [
                { text: "⚔️ Push d4! (Open central d-file and e-file lines)", isCorrect: true, eloBonus: 250 },
                { text: "🛡️ Retreat Bishop to e2", isCorrect: false, eloBonus: 70 },
                { text: "♟️ Push c3 pawn chain", isCorrect: false, eloBonus: 100 }
            ]
        },
        {
            elo: 1800,
            concept: 'offensive',
            title: "⚔️ Breakthrough Attack on King (1800 ELO)",
            desc: "Look at the main board: White has Queen on h5 and Bishop on d3 targeting h7. How do you remove Black's defensive Knight on f6?",
            fen: "r1b2rk1/ppp2ppp/5n2/7Q/4p3/2PB4/PPP2PPP/R1B1R1K1 w - - 0 12",
            options: [
                { text: "⚔️ Play Bg5 or Rxe4 (Deflect/eliminate f6 Knight defender)", isCorrect: true, eloBonus: 250 },
                { text: "🛡️ Retreat Queen to d1", isCorrect: false, eloBonus: 60 },
                { text: "♟️ Push b3 to develop c1 Bishop", isCorrect: false, eloBonus: 80 }
            ]
        },
        {
            elo: 1550,
            concept: 'offensive',
            title: "⚔️ King-side Outpost Invasion (1550 ELO)",
            desc: "Look at the main board: White's Knight can occupy an aggressive outpost on d5. How do you exploit Black's passive setup?",
            fen: "r1b1qr1k/ppp3pp/2n5/4pp2/2P5/2N1PN2/PP1QBPPP/R4RK1 w - - 0 13",
            options: [
                { text: "⚔️ Play Nd5! (Establish powerful central/offensive outpost)", isCorrect: true, eloBonus: 250 },
                { text: "🛡️ Step King to h1 passively", isCorrect: false, eloBonus: 70 },
                { text: "♟️ Trade Knights on f3", isCorrect: false, eloBonus: 50 }
            ]
        }
    ],
    batteries: [
        {
            elo: 1300,
            concept: 'batteries',
            title: "🔋 Battery Attack — Queen & Bishop Alignment (1300 ELO)",
            desc: "Look at the main board: White has Queen on d3 and Bishop on c2 forming a battery aimed at h7. How do you press the threat?",
            fen: "r1bq1rk1/ppp2ppp/2n2n2/3p4/8/2QBP3/PPB2PPP/R1B1K2R w KQ - 0 10",
            options: [
                { text: "🔋 Play Bxh7+ / Qd3 battery attack on h7", isCorrect: true, eloBonus: 250 },
                { text: "🛡️ Trade Knights on d5", isCorrect: false, eloBonus: 80 },
                { text: "♟️ Push a3 pawn", isCorrect: false, eloBonus: 40 }
            ]
        },
        {
            elo: 1750,
            concept: 'batteries',
            title: "🔋 Doubled Rooks Battery on Open File (1750 ELO)",
            desc: "Look at the main board: White has doubled Rooks on the open d-file facing Black's 7th rank. What is the optimal invasion?",
            fen: "2r3k1/1p3ppp/8/3R4/8/8/1R3PPP/6K1 w - - 0 25",
            options: [
                { text: "🔋 Play Rd7 (Infiltrate 7th rank with doubled Rooks battery)", isCorrect: true, eloBonus: 250 },
                { text: "🛡️ Play h3 luft space for King", isCorrect: false, eloBonus: 100 },
                { text: "🔄 Trade Rooks on c8", isCorrect: false, eloBonus: 60 }
            ]
        },
        {
            elo: 1450,
            concept: 'batteries',
            title: "🔋 Heavy File Battery (1450 ELO)",
            desc: "Look at the main board: White has Rook on e1 aligned with Black's central King file. How do you maximize battery pressure?",
            fen: "r3r1k1/pp3ppp/2p5/4n3/4P3/6P1/PPP2PBP/R3R1K1 w - - 0 18",
            options: [
                { text: "🔋 Play Rad1 (Double heavy pieces on central open files)", isCorrect: true, eloBonus: 250 },
                { text: "🛡️ Move King to f1", isCorrect: false, eloBonus: 60 },
                { text: "♟️ Push h4 pawn", isCorrect: false, eloBonus: 50 }
            ]
        }
    ],
    pins: [
        {
            elo: 1250,
            concept: 'pins',
            title: "🎯 Pins & Skewers — Pinned Knight Exploitation (1250 ELO)",
            desc: "Look at the main board: Black's Knight on f6 is pinned to the King by White's Bishop on g5. How do you pile pressure on the pinned piece?",
            fen: "r1bqk2r/pppp1ppp/2n2n2/4p1B1/2B1P3/5N2/PPPP1PPP/RN1QK2R w KQkq - 4 5",
            options: [
                { text: "🎯 Play Nd5 (Increase attack pressure on the pinned f6 Knight)", isCorrect: true, eloBonus: 250 },
                { text: "🛡️ Retreat Bishop to e3", isCorrect: false, eloBonus: 60 },
                { text: "♟️ Push h3 pawn", isCorrect: false, eloBonus: 50 }
            ]
        },
        {
            elo: 1850,
            concept: 'pins',
            title: "🎯 Diagonal Skewer Win (1850 ELO)",
            desc: "Look at the main board: Black's Queen on d6 and King on b8 are on the same diagonal. How does White win heavy material?",
            fen: "1k1r3r/ppp2ppp/3q4/8/8/8/PPP2PPP/R1B2RK1 w - - 0 15",
            options: [
                { text: "🎯 Play Bf4 (Diagonal Skewer attacking Queen and King behind it)", isCorrect: true, eloBonus: 250 },
                { text: "🛡️ Play Re1 controlling open file", isCorrect: false, eloBonus: 90 },
                { text: "♟️ Push c3 pawn", isCorrect: false, eloBonus: 50 }
            ]
        }
    ],
    endgame: [
        {
            elo: 1350,
            concept: 'endgame',
            title: "♟️ Endgame Technique — Passed Pawn & Opposition (1350 ELO)",
            desc: "Look at the main board: In a King & Pawn endgame, how do you position your King relative to the passed pawn?",
            fen: "8/8/4k3/8/4P3/8/4K3/8 w - - 0 1",
            options: [
                { text: "♟️ Advance King in FRONT of the passed pawn (Ke3/Ke4 opposition)", isCorrect: true, eloBonus: 250 },
                { text: "🏃 Push pawn immediately without King support (e5)", isCorrect: false, eloBonus: 80 },
                { text: "🛡️ Retreat King to e1 back rank", isCorrect: false, eloBonus: 40 }
            ]
        },
        {
            elo: 2100,
            concept: 'endgame',
            title: "♟️ Lucena Position Promotion Bridge (2100 ELO)",
            desc: "Look at the main board: White has a passed pawn on e7 and Rook on b8. What master technique shields the King to force promotion?",
            fen: "1R6/4k3/8/8/8/4K3/4P3/r7 w - - 0 1",
            options: [
                { text: "♟️ Build the Bridge (Lucena 4th rank Rook placement)", isCorrect: true, eloBonus: 250 },
                { text: "🛡️ Check Black's King continuously from behind", isCorrect: false, eloBonus: 100 },
                { text: "🏃 Move King to e8 blocking own pawn", isCorrect: false, eloBonus: 60 }
            ]
        },
        {
            elo: 1650,
            concept: 'endgame',
            title: "♟️ Rook Endgame Skewer & Cutting King (1650 ELO)",
            desc: "Look at the main board: White has Rook on b2 giving check to Black's King on b6. How do you cut off the enemy King?",
            fen: "8/8/1k6/8/8/8/1R6/1K6 w - - 0 1",
            options: [
                { text: "♟️ Check and cut off King along the file (Rb2+ / Rb5)", isCorrect: true, eloBonus: 250 },
                { text: "🛡️ Move King away to a1", isCorrect: false, eloBonus: 50 },
                { text: "♟️ Offer Rook trade", isCorrect: false, eloBonus: 40 }
            ]
        }
    ]
};

function shuffleArray(array) {
    const arr = [...array];
    for (let i = arr.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
}

let activePlacementQuestions = [];
let placementCurrentStep = 0;
let quizDesiredCount = 10;
let quizFontSize = localStorage.getItem('chess_quiz_font_size') || 'font-large';
let placementScores = {
    tactics: 1200,
    defensive: 1200,
    offensive: 1200,
    batteries: 1200,
    pins: 1200,
    endgame: 1200
};
let placementTotalBonus = 0;

function initPlacementTestModule() {
    const startBtn = document.getElementById('btn-start-placement-test');
    if (startBtn) startBtn.addEventListener('click', openPlacementTestModal);

    const closeBtn = document.getElementById('btn-close-placement-modal');
    if (closeBtn) closeBtn.addEventListener('click', closePlacementTestModal);

    const fontSelect = document.getElementById('select-quiz-font-size');
    if (fontSelect) {
        fontSelect.value = quizFontSize;
        fontSelect.addEventListener('change', () => {
            quizFontSize = fontSelect.value;
            localStorage.setItem('chess_quiz_font_size', quizFontSize);
            const container = document.getElementById('placement-question-container');
            if (container) {
                container.className = `placement-question-box ${quizFontSize}`;
            }
        });
    }
}

function closeAllOtherModals() {
    closeProfileModal();
    const modalsToClose = [
        'user-profile-modal',
        'game-settings-modal',
        'game-manager-modal',
        'cookies-modal',
        'modal-analysis-report',
        'modal-opening-explorer'
    ];
    modalsToClose.forEach(id => {
        const el = document.getElementById(id);
        if (el) el.classList.add('hidden');
    });
}

function openPlacementTestModal() {
    closeAllOtherModals();
    backupMainBoardState();

    placementCurrentStep = 0;
    placementTotalBonus = 0;

    const modal = document.getElementById('placement-test-modal');
    if (!modal) return;

    modal.classList.add('quiz-floating-mode');
    const boardWrapper = document.querySelector('.board-wrapper');
    if (boardWrapper) boardWrapper.classList.add('quiz-board-highlight');

    renderQuizSetupScreen();
    modal.classList.remove('hidden');
}

function renderQuizSetupScreen() {
    const container = document.getElementById('placement-question-container');
    const stepEl = document.getElementById('placement-question-step');
    const fillEl = document.getElementById('placement-progress-fill');

    if (!container) return;
    if (stepEl) stepEl.textContent = 'Diagnostic Setup';
    if (fillEl) fillEl.style.width = '0%';

    container.className = `placement-question-box ${quizFontSize}`;
    container.innerHTML = `
        <div class="quiz-setup-container">
            <div class="quiz-setup-title">🎯 AI Mentor Diagnostic Profile Analysis</div>
            <div class="quiz-setup-desc">Select how many diagnostic questions you want to solve to analyze your skill matrix and assign your initial ELO:</div>
            <div class="quiz-count-grid">
                <div class="quiz-count-card ${quizDesiredCount === 5 ? 'active' : ''}" data-count="5">
                    <span class="count-badge">⚡ Quick</span>
                    <span class="count-number">5 Questions</span>
                    <span class="count-desc">Fast 2-minute check</span>
                </div>
                <div class="quiz-count-card ${quizDesiredCount === 10 ? 'active' : ''}" data-count="10">
                    <span class="count-badge recommended">⭐ Recommended</span>
                    <span class="count-number">10 Questions</span>
                    <span class="count-desc">Balanced 5-minute analysis</span>
                </div>
                <div class="quiz-count-card ${quizDesiredCount === 15 ? 'active' : ''}" data-count="15">
                    <span class="count-badge">🔍 Detailed</span>
                    <span class="count-number">15 Questions</span>
                    <span class="count-desc">Full category & skill evaluation</span>
                </div>
                <div class="quiz-count-card ${quizDesiredCount === 20 ? 'active' : ''}" data-count="20">
                    <span class="count-badge">🎓 Deep</span>
                    <span class="count-number">20 Questions</span>
                    <span class="count-desc">Comprehensive master breakdown</span>
                </div>
            </div>
            <button class="btn btn-accent btn-lg" id="btn-begin-quiz" style="width:100%; font-size:16px; padding:12px;">🚀 Begin Profile Analysis</button>
        </div>
    `;

    container.querySelectorAll('.quiz-count-card').forEach(card => {
        card.addEventListener('click', () => {
            container.querySelectorAll('.quiz-count-card').forEach(c => c.classList.remove('active'));
            card.classList.add('active');
            quizDesiredCount = parseInt(card.dataset.count, 10);
        });
    });

    const beginBtn = document.getElementById('btn-begin-quiz');
    if (beginBtn) {
        beginBtn.addEventListener('click', startQuizQuestions);
    }
}

function startQuizQuestions() {
    placementCurrentStep = 0;
    placementTotalBonus = 0;
    placementScores = {
        tactics: 1200,
        defensive: 1200,
        offensive: 1200,
        batteries: 1200,
        pins: 1200,
        endgame: 1200
    };

    let allPool = [];
    Object.keys(QUESTION_BANK).forEach(cat => {
        allPool.push(...QUESTION_BANK[cat]);
    });

    allPool = shuffleArray(allPool);

    activePlacementQuestions = allPool.slice(0, Math.min(quizDesiredCount, allPool.length));

    renderPlacementQuestionStep();
}

function closePlacementTestModal() {
    const modal = document.getElementById('placement-test-modal');
    if (modal) {
        modal.classList.remove('quiz-floating-mode');
        modal.classList.add('hidden');
    }
    const boardWrapper = document.querySelector('.board-wrapper');
    if (boardWrapper) boardWrapper.classList.remove('quiz-board-highlight');
    restoreMainBoardState();
}

function renderPlacementQuestionStep() {
    const stepEl = document.getElementById('placement-question-step');
    const fillEl = document.getElementById('placement-progress-fill');
    const container = document.getElementById('placement-question-container');

    if (!container) return;

    const totalQ = activePlacementQuestions.length;
    if (placementCurrentStep >= totalQ) {
        renderPlacementResultScreen(container);
        return;
    }

    const q = activePlacementQuestions[placementCurrentStep];
    const progressPct = Math.round(((placementCurrentStep + 1) / totalQ) * 100);

    if (stepEl) stepEl.textContent = `Question ${placementCurrentStep + 1} of ${totalQ}`;
    if (fillEl) fillEl.style.width = `${progressPct}%`;

    // Render Question FEN directly onto the MAIN CHESSBOARD
    startFen = q.fen;
    currentFen = q.fen;
    moveHistory = [];
    moveStackUci = [];
    parseFenToState(q.fen);
    renderBoard();

    arrowsSvgEl.innerHTML = '';
    bestMoveArrow = null;

    const turnColor = q.fen.split(' ')[1] || 'w';
    if (turnBadgeEl) {
        turnBadgeEl.textContent = turnColor === 'w' ? '⚪ White to Move (Quiz)' : '⚫ Black to Move (Quiz)';
        turnBadgeEl.className = `turn-badge ${turnColor === 'w' ? 'white' : 'black'}`;
    }

    container.className = `placement-question-box ${quizFontSize}`;
    container.innerHTML = `
        <div class="placement-question-title">${q.title}</div>
        <div class="placement-question-desc">${q.desc}</div>
        <div class="placement-options-list">
            ${q.options.map((opt, idx) => `
                <button class="placement-option-btn" data-idx="${idx}">${opt.text}</button>
            `).join('')}
        </div>
    `;

    container.querySelectorAll('.placement-option-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const idx = parseInt(btn.dataset.idx, 10);
            const selectedOpt = q.options[idx];
            if (selectedOpt.isCorrect) {
                placementTotalBonus += selectedOpt.eloBonus || 250;
                if (placementScores[q.concept] !== undefined) {
                    placementScores[q.concept] = Math.round((placementScores[q.concept] + q.elo) / 2 + 150);
                }
            } else {
                if (placementScores[q.concept] !== undefined) {
                    placementScores[q.concept] = Math.max(800, placementScores[q.concept] - 100);
                }
            }

            placementCurrentStep++;
            renderPlacementQuestionStep();
        });
    });
}

function renderPlacementResultScreen(container) {
    const calculatedElo = Math.min(2400, Math.max(900, 1000 + Math.round(placementTotalBonus * 0.8)));
    const tierName = getSkillTierName(calculatedElo);

    container.innerHTML = `
        <div class="placement-result-card">
            <div class="placement-result-title">🎯 AI Mentor Diagnostic Complete!</div>
            <p style="color:#b0b0b0; font-size:13px; margin:4px 0;">Based on your tactical, defensive, and positional decisions across all concept fields, your estimated skill level is:</p>
            <h3 style="color:var(--accent-color); font-size:24px; margin:8px 0;">${calculatedElo} ELO — ${tierName}</h3>
            
            <div style="display:flex; flex-direction:column; gap:8px; text-align:left; margin-top:12px;">
                <label style="font-size:12px; font-weight:600; color:#8b8987;">Enter Profile Name to Save & Activate:</label>
                <input type="text" id="placement-profile-name" placeholder="e.g. Master Candidate, Alex" style="background:#161512; border:1px solid var(--card-border); padding:8px 12px; color:#fff; border-radius:6px; font-size:13px;">
                <button class="btn btn-accent" id="btn-save-placement-profile" style="margin-top:6px;">💾 Save & Activate Profile (${calculatedElo} ELO)</button>
            </div>
        </div>
    `;

    const saveBtn = document.getElementById('btn-save-placement-profile');
    if (saveBtn) {
        saveBtn.addEventListener('click', () => {
            const nameInput = document.getElementById('placement-profile-name');
            const name = (nameInput && nameInput.value.trim()) || `Profile ${userProfiles.length + 1}`;

            const newProf = {
                id: 'prof_' + Date.now(),
                name: name,
                elo: calculatedElo,
                gamesPlayed: 0,
                wins: 0,
                draws: 0,
                losses: 0,
                concepts: {
                    offensive: { name: 'Offensive Strategy', rating: placementScores.offensive || calculatedElo, icon: '⚔️' },
                    defensive: { name: 'Defensive Maneuvers', rating: placementScores.defensive || calculatedElo, icon: '🛡️' },
                    tactics: { name: 'Tactics & Forks', rating: placementScores.tactics || calculatedElo, icon: '⚡' },
                    batteries: { name: 'Battery Attacks', rating: placementScores.batteries || calculatedElo, icon: '🔋' },
                    pins: { name: 'Pins & Skewers', rating: placementScores.pins || calculatedElo, icon: '🎯' },
                    endgame: { name: 'Endgame & Gambits', rating: placementScores.endgame || calculatedElo, icon: '♟️' }
                }
            };

            userProfiles.push(newProf);
            activeProfileId = newProf.id;
            saveUserProfilesToStorage();
            updateHeaderProfileUI();

            closePlacementTestModal();
            openProfileModal();
            alert(`Profile "${name}" created with estimated ${calculatedElo} ELO (${tierName})!`);
        });
    }
}

// ==========================================
// ⚡ FORCE BOT MOVE HANDLER
// ==========================================
async function handleForceBotMove() {
    if (legalMoves.length === 0) {
        alert('No legal moves available.');
        return;
    }

    if (autoMoveTimer) {
        clearTimeout(autoMoveTimer);
        autoMoveTimer = null;
    }

    await makeBotMove();
}


// ==========================================
// ⏱️ CHESS CLOCKS & TIME CONTROL MODULE
// ==========================================

const TIME_CONTROL_PRESETS = {
    'untimed': { name: '♾️ Untimed', minutes: 0, increment: 0, untimed: true },
    'blitz_3_2': { name: '⚡ 3+2 Blitz', minutes: 3, increment: 2 },
    'blitz_5_0': { name: '⚡ 5+0 Blitz', minutes: 5, increment: 0 },
    'rapid_10_0': { name: '⏱️ 10+0 Rapid', minutes: 10, increment: 0 },
    'rapid_15_10': { name: '⏱️ 15+10 Rapid', minutes: 15, increment: 10 },
    'classical_30_0': { name: '⏳ 30+0 Classical', minutes: 30, increment: 0 }
};

let whiteTimeMs = 300000;
let blackTimeMs = 300000;
let clockInterval = null;
let isClockRunning = false;
let isClockFlagged = false;

function initChessClockModule() {
    updateClockSettingsUIControls();
    resetChessClocks();
}

function updateClockSettingsUIControls() {
    const tClocks = document.getElementById('toggle-enable-clocks');
    const isEnabled = tClocks ? tClocks.checked : (gameSettings.enableClocks ?? false);

    const optionsContainer = document.getElementById('time-control-options-container');
    if (optionsContainer) optionsContainer.classList.toggle('hidden', !isEnabled);

    const selectW = document.getElementById('select-white-clock-preset');
    const presetW = selectW ? selectW.value : (gameSettings.whiteClockPreset || 'blitz_5_0');

    const customWContainer = document.getElementById('custom-white-clock-container');
    if (customWContainer) customWContainer.classList.toggle('hidden', !isEnabled || presetW !== 'custom');

    const selectB = document.getElementById('select-black-clock-preset');
    const presetB = selectB ? selectB.value : (gameSettings.blackClockPreset || 'blitz_5_0');

    const customBContainer = document.getElementById('custom-black-clock-container');
    if (customBContainer) customBContainer.classList.toggle('hidden', !isEnabled || presetB !== 'custom');

    updateClockPositionsUI();
}

function updateClockPositionsUI() {
    const topBar = document.getElementById('top-clock-bar');
    const bottomBar = document.getElementById('bottom-clock-bar');
    const clockStore = document.getElementById('clock-elements-store');
    const cardBlack = document.getElementById('clock-card-black');
    const cardWhite = document.getElementById('clock-card-white');

    if (!topBar || !bottomBar || !cardBlack || !cardWhite) return;

    if (!gameSettings.enableClocks) {
        topBar.classList.add('hidden');
        bottomBar.classList.add('hidden');
        if (clockStore) {
            if (!clockStore.contains(cardBlack)) clockStore.appendChild(cardBlack);
            if (!clockStore.contains(cardWhite)) clockStore.appendChild(cardWhite);
        }
        return;
    }

    topBar.classList.remove('hidden');
    bottomBar.classList.remove('hidden');

    if (!isFlipped) {
        // Standard: Black on Top, White on Bottom
        if (!topBar.contains(cardBlack)) topBar.appendChild(cardBlack);
        if (!bottomBar.contains(cardWhite)) bottomBar.appendChild(cardWhite);
    } else {
        // Flipped: White on Top, Black on Bottom
        if (!topBar.contains(cardWhite)) topBar.appendChild(cardWhite);
        if (!bottomBar.contains(cardBlack)) bottomBar.appendChild(cardBlack);
    }
}

function getPlayerTimeControlConfig(color) {
    const presetKey = (color === 'w') ? (gameSettings.whiteClockPreset || 'blitz_5_0') : (gameSettings.blackClockPreset || 'blitz_5_0');
    if (presetKey === 'untimed') {
        return { name: '♾️ Untimed', minutes: 0, increment: 0, untimed: true };
    }
    if (presetKey === 'custom') {
        const mins = (color === 'w') ? (gameSettings.whiteClockMins || 5) : (gameSettings.blackClockMins || 5);
        const inc = (color === 'w') ? (gameSettings.whiteClockInc || 0) : (gameSettings.blackClockInc || 0);
        return { name: `⚙️ ${mins}+${inc}`, minutes: mins, increment: inc, untimed: false };
    }
    return TIME_CONTROL_PRESETS[presetKey] || TIME_CONTROL_PRESETS['blitz_5_0'];
}

function resetChessClocks() {
    stopClockTimer();
    isClockFlagged = false;

    const configW = getPlayerTimeControlConfig('w');
    const configB = getPlayerTimeControlConfig('b');

    whiteTimeMs = configW.untimed ? Infinity : (configW.minutes * 60 * 1000);
    blackTimeMs = configB.untimed ? Infinity : (configB.minutes * 60 * 1000);

    const tcNameEl = document.getElementById('clock-time-control-name');
    if (tcNameEl) {
        if (configW.name === configB.name) {
            tcNameEl.textContent = configW.name;
        } else {
            tcNameEl.textContent = `⚪ ${configW.name} | ⚫ ${configB.name}`;
        }
    }

    const whiteCard = document.getElementById('clock-card-white');
    const blackCard = document.getElementById('clock-card-black');
    if (whiteCard) whiteCard.classList.remove('flagged-clock');
    if (blackCard) blackCard.classList.remove('flagged-clock');

    updateClockPlayerTypesUI();
    updateClockDisplaysUI();
    updateClockActiveTurnHighlight();
}

function updateClockPlayerTypesUI() {
    const wTypeEl = document.getElementById('clock-white-type');
    const bTypeEl = document.getElementById('clock-black-type');
    const wNameEl = document.getElementById('clock-white-name') || document.querySelector('#clock-card-white .player-name-text');
    const bNameEl = document.getElementById('clock-black-name') || document.querySelector('#clock-card-black .player-name-text');

    const activeProf = (typeof getActiveProfile === 'function') ? getActiveProfile() : { elo: 1500, name: 'Player' };
    const userElo = activeProf.elo || 1500;
    const profileName = activeProf.name || 'Player';

    const wIsAuto = (gameSettings.whitePlayerMode === 'auto');
    const bIsAuto = (gameSettings.blackPlayerMode === 'auto');

    const isAutoActive = gameSettings.autoAdjustDifficulty && (wIsAuto !== bIsAuto);
    const bias = gameSettings.autoAdjustBias || 'medium';

    let targetAutoElo = userElo;
    if (bias === 'easy') targetAutoElo = Math.max(800, userElo - 150);
    else if (bias === 'hard') targetAutoElo = userElo + 150;
    else if (bias === 'nightmare') targetAutoElo = userElo + 350;

    let wElo = userElo;
    if (wIsAuto) {
        if (isAutoActive) {
            wElo = targetAutoElo;
        } else {
            const lvl = gameSettings.whiteDifficulty ?? 10;
            wElo = getBotEloEstimate(lvl);
        }
    }

    let bElo = userElo;
    if (bIsAuto) {
        if (isAutoActive) {
            bElo = targetAutoElo;
        } else {
            const lvl = gameSettings.blackDifficulty ?? 10;
            bElo = getBotEloEstimate(lvl);
        }
    }

    if (wTypeEl) wTypeEl.textContent = wIsAuto ? `🤖 Bot (~${wElo} ELO)` : `🧑 Player (${wElo} ELO)`;
    if (bTypeEl) bTypeEl.textContent = bIsAuto ? `🤖 Bot (~${bElo} ELO)` : `🧑 Player (${bElo} ELO)`;

    if (!wIsAuto && bIsAuto) {
        if (wNameEl) wNameEl.textContent = profileName;
        if (bNameEl) bNameEl.textContent = 'Stockfish';
    } else if (wIsAuto && !bIsAuto) {
        if (wNameEl) wNameEl.textContent = 'Stockfish';
        if (bNameEl) bNameEl.textContent = profileName;
    } else if (!wIsAuto && !bIsAuto) {
        if (wNameEl) wNameEl.textContent = profileName;
        if (bNameEl) bNameEl.textContent = 'Black';
    } else {
        if (wNameEl) wNameEl.textContent = 'Stockfish 1';
        if (bNameEl) bNameEl.textContent = 'Stockfish 2';
    }
}

function formatClockTimeMs(ms) {
    if (ms === Infinity) return "♾️ Unlimited";
    if (ms <= 0) return "00:00";
    const totalSeconds = Math.floor(ms / 1000);
    const mins = Math.floor(totalSeconds / 60);
    const secs = totalSeconds % 60;

    if (mins === 0 && secs < 10) {
        const tenths = Math.floor((ms % 1000) / 100);
        return `${String(secs).padStart(2, '0')}.${tenths}`;
    }

    return `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
}

function updateClockDisplaysUI() {
    const wDisplay = document.getElementById('clock-display-white');
    const bDisplay = document.getElementById('clock-display-black');

    if (wDisplay) wDisplay.textContent = formatClockTimeMs(whiteTimeMs);
    if (bDisplay) bDisplay.textContent = formatClockTimeMs(blackTimeMs);
}

function updateClockActiveTurnHighlight() {
    const whiteCard = document.getElementById('clock-card-white');
    const blackCard = document.getElementById('clock-card-black');
    const activeColor = currentFen.split(' ')[1] || 'w';

    if (whiteCard) whiteCard.classList.toggle('active-turn', activeColor === 'w');
    if (blackCard) blackCard.classList.toggle('active-turn', activeColor === 'b');
}

function startClockTimer() {
    if (!gameSettings.enableClocks || isClockRunning || isClockFlagged || isAutoPaused || isEditBoardMode) return;
    if (moveHistory.length === 0) return;

    isClockRunning = true;
    clockInterval = setInterval(clockTickHandler, 100);
}

function stopClockTimer() {
    isClockRunning = false;
    if (clockInterval) {
        clearInterval(clockInterval);
        clockInterval = null;
    }
}

function clockTickHandler() {
    if (!gameSettings.enableClocks || isAutoPaused || isEditBoardMode || isClockFlagged) {
        stopClockTimer();
        return;
    }

    const activeColor = currentFen.split(' ')[1] || 'w';

    if (activeColor === 'w') {
        if (whiteTimeMs !== Infinity) {
            whiteTimeMs -= 100;
            if (whiteTimeMs <= 0) {
                whiteTimeMs = 0;
                updateClockDisplaysUI();
                handleTimeFlagged('w');
                return;
            }
        }
    } else {
        if (blackTimeMs !== Infinity) {
            blackTimeMs -= 100;
            if (blackTimeMs <= 0) {
                blackTimeMs = 0;
                updateClockDisplaysUI();
                handleTimeFlagged('b');
                return;
            }
        }
    }

    updateClockDisplaysUI();
}

function onMoveExecutedClockTick(previousTurnColor) {
    if (!gameSettings.enableClocks) return;

    const config = getPlayerTimeControlConfig(previousTurnColor);
    const incMs = (config.increment || 0) * 1000;

    if (incMs > 0 && moveHistory.length > 1) {
        if (previousTurnColor === 'w' && whiteTimeMs !== Infinity) {
            whiteTimeMs += incMs;
        } else if (previousTurnColor === 'b' && blackTimeMs !== Infinity) {
            blackTimeMs += incMs;
        }
    }

    updateClockDisplaysUI();
    updateClockActiveTurnHighlight();

    if (!isClockRunning && !isAutoPaused && !isEditBoardMode && !isClockFlagged) {
        startClockTimer();
    }
}

function getOpponentEloForGame(botColor = 'b') {
    const activeProf = (typeof getActiveProfile === 'function') ? getActiveProfile() : { elo: 1500 };
    const userElo = activeProf.elo || 1500;

    const isWhiteAuto = (gameSettings.whitePlayerMode === 'auto');
    const isBlackAuto = (gameSettings.blackPlayerMode === 'auto');

    if (gameSettings.autoAdjustDifficulty && (isWhiteAuto !== isBlackAuto)) {
        const bias = gameSettings.autoAdjustBias || 'medium';
        if (bias === 'easy') return Math.max(800, userElo - 150);
        if (bias === 'hard') return userElo + 150;
        if (bias === 'nightmare') return userElo + 350;
        return userElo;
    }

    const lvl = (botColor === 'w') ? (gameSettings.whiteDifficulty ?? 10) : (gameSettings.blackDifficulty ?? 10);
    return getBotEloEstimate(lvl);
}

function recordGameResult(outcome, opponentElo = 1500) {
    const prof = getActiveProfile();
    if (!prof) return;

    const oldElo = prof.elo || 1500;
    const oppElo = opponentElo || 1500;

    const expectedScore = 1 / (1 + Math.pow(10, (oppElo - oldElo) / 400));

    let actualScore = 0.5;
    if (outcome === 'win') actualScore = 1.0;
    else if (outcome === 'loss') actualScore = 0.0;

    const kFactor = 32;
    const rawChange = kFactor * (actualScore - expectedScore);

    let eloChange = 0;
    if (outcome === 'win') {
        // Guarantee at least +1 ELO increase on a win (ceil raw fractional gain)
        eloChange = Math.max(1, Math.ceil(rawChange));
    } else if (outcome === 'loss') {
        eloChange = Math.min(-1, Math.floor(rawChange));
    } else {
        eloChange = Math.round(rawChange);
    }

    const newElo = Math.max(800, oldElo + eloChange);

    prof.elo = newElo;
    prof.gamesPlayed = (prof.gamesPlayed || 0) + 1;
    if (outcome === 'win') prof.wins = (prof.wins || 0) + 1;
    else if (outcome === 'loss') prof.losses = (prof.losses || 0) + 1;
    else if (outcome === 'draw') prof.draws = (prof.draws || 0) + 1;

    if (prof.concepts) {
        Object.keys(prof.concepts).forEach(key => {
            const currentRating = prof.concepts[key].rating || oldElo;
            const skillChange = outcome === 'win' ? Math.max(1, Math.ceil(eloChange * 0.5 + 5)) : outcome === 'loss' ? Math.min(-1, Math.floor(eloChange * 0.5 - 2)) : 0;
            prof.concepts[key].rating = Math.max(800, currentRating + skillChange);
        });
    }

    saveUserProfilesToStorage();
    updateHeaderProfileUI();
    updateClockPlayerTypesUI();
    renderProfileSummaryCard();
    renderProfilesListTab();

    const sign = eloChange >= 0 ? `+${eloChange}` : `${eloChange}`;
    const total = prof.gamesPlayed;
    const wins = prof.wins || 0;
    const wr = Math.round((wins / total) * 100);

    let messageTitle = '';
    if (outcome === 'win') messageTitle = `🏆 VICTORY! (${sign} ELO: ${oldElo} ➔ ${newElo})`;
    else if (outcome === 'loss') messageTitle = `💔 DEFEAT (${sign} ELO: ${oldElo} ➔ ${newElo})`;
    else messageTitle = `🤝 DRAW (${sign} ELO: ${oldElo} ➔ ${newElo})`;

    const detailText = `${messageTitle}\nOpponent ELO: ~${oppElo}\nProfile: ${prof.name}\nRecord: ${prof.wins}W - ${prof.draws}D - ${prof.losses}L (${wr}% Win Rate)`;

    setTimeout(() => {
        alert(detailText);
    }, 100);
}

function handleResign() {
    if (moveHistory.length === 0) {
        alert('No game in progress to resign.');
        return;
    }
    if (hasDeclaredGameOver) {
        alert('Game is already over.');
        return;
    }

    const activeColor = currentFen.split(' ')[1] || 'w';
    const resigningSideName = (activeColor === 'w') ? 'White' : 'Black';
    const winningSideName = (activeColor === 'w') ? 'Black' : 'White';

    if (!confirm(`Are you sure you want to resign as ${resigningSideName}? (${winningSideName} will be declared the winner).`)) {
        return;
    }

    hasDeclaredGameOver = true;
    stopClockTimer();
    if (!isAutoPaused) {
        isAutoPaused = true;
        updatePauseResumeButtonUI();
        if (autoMoveTimer) {
            clearTimeout(autoMoveTimer);
            autoMoveTimer = null;
        }
    }

    if (turnBadgeEl) {
        turnBadgeEl.textContent = `🏳️ Resignation - ${winningSideName} Wins!`;
        turnBadgeEl.className = `turn-badge ${winningSideName.toLowerCase()}`;
    }

    const isWhiteManual = (gameSettings.whitePlayerMode === 'manual');
    const isBlackManual = (gameSettings.blackPlayerMode === 'manual');
    const isWhiteAuto = (gameSettings.whitePlayerMode === 'auto');
    const isBlackAuto = (gameSettings.blackPlayerMode === 'auto');

    let oppElo = 1500;
    if (isWhiteManual && isBlackAuto) {
        oppElo = getOpponentEloForGame('b');
    } else if (isWhiteAuto && isBlackManual) {
        oppElo = getOpponentEloForGame('w');
    }

    let outcome = 'loss';
    if (isWhiteManual && !isBlackManual) {
        outcome = (activeColor === 'w') ? 'loss' : 'win';
    } else if (!isWhiteManual && isBlackManual) {
        outcome = (activeColor === 'b') ? 'loss' : 'win';
    } else {
        outcome = 'loss';
    }

    recordGameResult(outcome, oppElo);
}

function handleTimeFlagged(flaggedColor) {
    stopClockTimer();
    isClockFlagged = true;

    const flaggedName = flaggedColor === 'w' ? 'White' : 'Black';
    const winnerName = flaggedColor === 'w' ? 'Black' : 'White';

    const card = document.getElementById(flaggedColor === 'w' ? 'clock-card-white' : 'clock-card-black');
    if (card) card.classList.add('flagged-clock');

    const autoLoss = (gameSettings.flagAutomatedLoss ?? true);

    if (autoLoss && !hasDeclaredGameOver && moveHistory.length > 0) {
        hasDeclaredGameOver = true;
        const isWhiteManual = (gameSettings.whitePlayerMode === 'manual');
        const isBlackManual = (gameSettings.blackPlayerMode === 'manual');

        let oppElo = 1500;
        if (isWhiteManual && !isBlackManual) {
            oppElo = getOpponentEloForGame('b');
        } else if (!isWhiteManual && isBlackManual) {
            oppElo = getOpponentEloForGame('w');
        }

        let outcome = 'draw';
        if (isWhiteManual && !isBlackManual) {
            outcome = (flaggedColor === 'w') ? 'loss' : 'win';
        } else if (!isWhiteManual && isBlackManual) {
            outcome = (flaggedColor === 'b') ? 'loss' : 'win';
        } else {
            outcome = (flaggedColor === 'w') ? 'loss' : 'win';
        }

        recordGameResult(outcome, oppElo);
    } else {
        setTimeout(() => {
            alert(`🚩 TIME FLAGGED!\n${flaggedName}'s clock reached 00:00.\n(Automated loss is disabled — game can continue).`);
        }, 50);
    }
}


// ==========================================
// 🎓 ADVANCED AI MENTOR CAPABILITIES MODULE
// ==========================================

function initAdvancedMentorCapabilities() {
    // 1. Full Game Analysis
    const btnAnalysis = document.getElementById('btn-full-game-analysis');
    const modalAnalysis = document.getElementById('game-analysis-modal');
    const btnCloseAnalysis = document.getElementById('btn-close-analysis-modal');
    const btnRunAnalysis = document.getElementById('btn-run-full-game-analysis');

    if (btnAnalysis && modalAnalysis) {
        btnAnalysis.addEventListener('click', () => {
            modalAnalysis.classList.remove('hidden');
            runFullGameAnalysis();
        });
    }
    if (btnCloseAnalysis && modalAnalysis) {
        btnCloseAnalysis.addEventListener('click', () => modalAnalysis.classList.add('hidden'));
    }
    if (btnRunAnalysis) {
        btnRunAnalysis.addEventListener('click', runFullGameAnalysis);
    }

    // 2. Opening Book Explorer
    const btnOpening = document.getElementById('btn-opening-explorer');
    const modalOpening = document.getElementById('opening-explorer-modal');
    const btnCloseOpening = document.getElementById('btn-close-opening-modal');

    if (btnOpening && modalOpening) {
        btnOpening.addEventListener('click', () => {
            modalOpening.classList.remove('hidden');
            loadOpeningExplorer();
        });
    }
    if (btnCloseOpening && modalOpening) {
        btnCloseOpening.addEventListener('click', () => modalOpening.classList.add('hidden'));
    }

    // 3. Position Tutor Quiz
    const btnQuiz = document.getElementById('btn-position-quiz');
    if (btnQuiz) {
        btnQuiz.addEventListener('click', loadPositionQuiz);
    }
}

async function runFullGameAnalysis() {
    const reportArea = document.getElementById('analysis-coach-report');
    const tbody = document.getElementById('analysis-timeline-tbody');
    const catContainer = document.getElementById('analysis-category-counts');
    const wAccEl = document.getElementById('analysis-white-acc');
    const bAccEl = document.getElementById('analysis-black-acc');

    if (reportArea) reportArea.innerHTML = '<p class="placeholder-text">⚡ Stockfish engine is analyzing full game moves... Please wait...</p>';
    if (wAccEl) wAccEl.textContent = '--%';
    if (bAccEl) bAccEl.textContent = '--%';

    try {
        const isWhiteManual = (gameSettings.whitePlayerMode === 'manual');
        const isBlackManual = (gameSettings.blackPlayerMode === 'manual');
        let studentColor = 'white';
        if (!isWhiteManual && isBlackManual) {
            studentColor = 'black';
        } else if (isWhiteManual && !isBlackManual) {
            studentColor = 'white';
        } else if (isFlipped) {
            studentColor = 'black';
        }

        const activeProfile = typeof getActiveProfile === 'function' ? getActiveProfile() : null;

        const resp = await fetch('/api/game/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                fen: startFen,
                moves: moveHistory,
                student_color: studentColor,
                user_profile: activeProfile,
                notebook_id: currentNotebookId || null
            })
        });
        const data = await resp.json();

        if (!resp.ok) throw new Error(data.detail || 'Analysis failed');

        // Render Accuracies
        if (wAccEl) wAccEl.textContent = `${data.white_accuracy}%`;
        if (bAccEl) bAccEl.textContent = `${data.black_accuracy}%`;

        // Render Move Classifications
        if (catContainer) {
            const wC = data.white_counts;
            const bC = data.black_counts;
            catContainer.innerHTML = `
                <div class="cat-pill brilliant" title="Brilliant Moves">🌟 Brilliant: ⚪${wC.brilliant} | ⚫${bC.brilliant}</div>
                <div class="cat-pill best" title="Best Engine Moves">✨ Best: ⚪${wC.best} | ⚫${bC.best}</div>
                <div class="cat-pill good" title="Good Moves">👍 Good: ⚪${wC.good} | ⚫${bC.good}</div>
                <div class="cat-pill mistake" title="Mistakes">⚠️ Mistakes: ⚪${wC.mistake} | ⚫${bC.mistake}</div>
                <div class="cat-pill blunder" title="Blunders">💥 Blunders: ⚪${wC.blunder} | ⚫${bC.blunder}</div>
                <div class="cat-pill" title="Book Moves">📖 Book: ⚪${wC.book} | ⚫${bC.book}</div>
            `;
        }

        // Render Coach Report
        if (reportArea) {
            let html = data.coach_report
                .replace(/\n\n/g, '<br><br>')
                .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
            reportArea.innerHTML = `
                <div style="margin-bottom:8px; font-size:11px; color:var(--accent-color);">Provider: ${data.provider}</div>
                <div>${html}</div>
            `;
        }

        // Render Timeline Table
        if (tbody) {
            if (!data.move_evals || data.move_evals.length === 0) {
                tbody.innerHTML = '<tr><td colspan="6" class="placeholder-text">No moves played yet. Start a game to see analysis!</td></tr>';
            } else {
                tbody.innerHTML = data.move_evals.map((m) => `
                    <tr>
                        <td>${m.move_num}</td>
                        <td>${m.side === 'White' ? '⚪' : '⚫'} ${m.side}</td>
                        <td><strong>${m.move_san}</strong></td>
                        <td><span class="cat-pill ${m.category}">${m.badge} ${m.category.toUpperCase()}</span></td>
                        <td><code>${m.score}</code></td>
                        <td><small style="color:#bababa;">${m.best_move || '-'}</small></td>
                    </tr>
                `).join('');
            }
        }
    } catch (err) {
        if (reportArea) reportArea.innerHTML = `<p class="placeholder-text" style="color:#e74c3c;">Analysis Error: ${err.message}</p>`;
    }
}

async function loadOpeningExplorer() {
    const titleEl = document.getElementById('opening-modal-title');
    const ecoEl = document.getElementById('opening-modal-eco');
    const descEl = document.getElementById('opening-modal-desc');
    const listEl = document.getElementById('opening-continuations-list');

    if (listEl) listEl.innerHTML = '<p class="placeholder-text">Loading opening tree...</p>';

    try {
        const resp = await fetch('/api/openings/explore', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ fen: startFen, moves: moveHistory })
        });
        const data = await resp.json();
        const op = data.opening;

        if (titleEl) titleEl.textContent = op.name || 'Standard Position';
        if (ecoEl) ecoEl.textContent = `ECO ${op.eco || 'A00'}`;
        if (descEl) descEl.textContent = op.desc || 'Standard opening position.';

        if (listEl) {
            if (!op.continuations || op.continuations.length === 0) {
                listEl.innerHTML = `
                    <div class="continuation-card">
                        <div class="continuation-header">
                            <span class="continuation-move">Main Line Continuation</span>
                            <span class="continuation-name">Standard Classical Setup</span>
                        </div>
                        <p style="font-size:12px; color:#bababa; margin:4px 0;">Play standard central pawn pushes (1. e4 / 1. d4) or develop minor pieces towards central control.</p>
                    </div>
                `;
            } else {
                listEl.innerHTML = op.continuations.map(c => `
                    <div class="continuation-card">
                        <div class="continuation-header">
                            <span class="continuation-move">1. ${c.san} (${c.move})</span>
                            <span class="continuation-name">${c.name}</span>
                        </div>
                        <div class="winrate-bar-container">
                            <div class="win-segment" style="width: ${c.win}%;" title="White Win: ${c.win}%"></div>
                            <div class="draw-segment" style="width: ${c.draw}%;" title="Draw: ${c.draw}%"></div>
                            <div class="loss-segment" style="width: ${c.loss}%;" title="Black Win: ${c.loss}%"></div>
                        </div>
                        <div class="winrate-legend">
                            <span>⚪ White Win: ${c.win}%</span>
                            <span>🤝 Draw: ${c.draw}%</span>
                            <span>⚫ Black Win: ${c.loss}%</span>
                        </div>
                    </div>
                `).join('');
            }
        }
    } catch (err) {
        if (listEl) listEl.innerHTML = `<p class="placeholder-text" style="color:#e74c3c;">Failed to load opening tree: ${err.message}</p>`;
    }
}

async function loadPositionQuiz() {
    closeAllOtherModals();
    backupMainBoardState();

    const modal = document.getElementById('placement-test-modal');
    const container = document.getElementById('placement-question-container');
    const stepEl = document.getElementById('placement-question-step');
    const fillEl = document.getElementById('placement-progress-fill');

    if (!modal || !container) return;

    modal.classList.add('quiz-floating-mode');
    const boardWrapper = document.querySelector('.board-wrapper');
    if (boardWrapper) boardWrapper.classList.add('quiz-board-highlight');

    modal.classList.remove('hidden');
    if (stepEl) stepEl.textContent = '🎓 AI Mentor Position Quiz';
    if (fillEl) fillEl.style.width = '100%';
    container.innerHTML = '<p class="placeholder-text">Evaluating position & creating quiz...</p>';

    try {
        const resp = await fetch('/api/mentor/quiz', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ fen: startFen, moves: moveHistory })
        });
        const quiz = await resp.json();

        const quizFen = quiz.fen || currentFen || startFen;
        currentFen = quizFen;
        parseFenToState(currentFen);
        renderBoard();
        updatePositionEvaluation(currentFen, []);

        container.innerHTML = `
            <div class="quiz-box">
                <h4 style="font-size:15px; margin-bottom:6px; color:var(--text-heading);">${quiz.question}</h4>
                <div style="font-size:11px; color:var(--accent-color); margin-bottom:12px;">Position Eval: ${quiz.eval_summary}</div>
                <div class="placement-options" style="display:flex; flex-direction:column; gap:8px;">
                    ${quiz.options.map((opt, idx) => `
                        <button class="placement-opt-btn btn btn-secondary" style="text-align:left; justify-content:flex-start;" data-idx="${idx}">
                            ${opt.text}
                        </button>
                    `).join('')}
                </div>
                <div id="quiz-result-area" style="margin-top:14px; display:none;"></div>
            </div>
        `;

        const optBtns = container.querySelectorAll('.placement-opt-btn');
        const resArea = document.getElementById('quiz-result-area');

        optBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const idx = parseInt(btn.getAttribute('data-idx'));
                const chosen = quiz.options[idx];
                resArea.style.display = 'block';
                if (chosen.is_correct) {
                    resArea.innerHTML = `
                        <div style="background:rgba(46,204,113,0.15); border:1px solid #2ecc71; border-radius:6px; padding:10px; color:#2ecc71; font-weight:600;">
                            🎉 CORRECT! ${chosen.explanation}
                        </div>
                    `;
                } else {
                    resArea.innerHTML = `
                        <div style="background:rgba(231,76,60,0.15); border:1px solid #e74c3c; border-radius:6px; padding:10px; color:#e74c3c; font-weight:600;">
                            ❌ INCORRECT. ${chosen.explanation}
                        </div>
                    `;
                }
            });
        });
    } catch (err) {
        container.innerHTML = `<p class="placeholder-text" style="color:#e74c3c;">Quiz generation error: ${err.message}</p>`;
    }
}

// ==========================================
// 🧠 STRATEGIC TURN GUIDELINES & PRACTICE SUBJECT MODULE
// ==========================================

function calculateMaterialBalance(bState) {
    const values = { 'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 0 };
    let whiteMat = 0;
    let blackMat = 0;
    Object.values(bState || {}).forEach(piece => {
        if (!piece) return;
        const color = piece[0];
        const type = piece[1].toUpperCase();
        const val = values[type] || 0;
        if (color === 'w') whiteMat += val;
        else if (color === 'b') blackMat += val;
    });
    return { white: whiteMat, black: blackMat, diff: whiteMat - blackMat };
}

function findLoosePieces(bState, colorChar) {
    const files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'];
    const ranks = ['1', '2', '3', '4', '5', '6', '7', '8'];
    const loose = [];

    const isDefended = (targetSq) => {
        const fileIdx = files.indexOf(targetSq[0]);
        const rankIdx = ranks.indexOf(targetSq[1]);
        if (fileIdx === -1 || rankIdx === -1) return false;

        // 1. Check pawn defenders
        const pawnRank = (colorChar === 'w') ? rankIdx - 1 : rankIdx + 1;
        if (pawnRank >= 0 && pawnRank < 8) {
            for (let dF of [-1, 1]) {
                const pF = fileIdx + dF;
                if (pF >= 0 && pF < 8) {
                    const sq = files[pF] + ranks[pawnRank];
                    if (bState[sq] === colorChar + 'P') return true;
                }
            }
        }

        // 2. Check knight defenders
        const knightOffsets = [
            [-2, -1], [-2, 1], [-1, -2], [-1, 2],
            [1, -2], [1, 2], [2, -1], [2, 1]
        ];
        for (let [dF, dR] of knightOffsets) {
            const f = fileIdx + dF;
            const r = rankIdx + dR;
            if (f >= 0 && f < 8 && r >= 0 && r < 8) {
                const sq = files[f] + ranks[r];
                if (bState[sq] === colorChar + 'N') return true;
            }
        }

        // 3. Check king defender
        for (let dF of [-1, 0, 1]) {
            for (let dR of [-1, 0, 1]) {
                if (dF === 0 && dR === 0) continue;
                const f = fileIdx + dF;
                const r = rankIdx + dR;
                if (f >= 0 && f < 8 && r >= 0 && r < 8) {
                    const sq = files[f] + ranks[r];
                    if (bState[sq] === colorChar + 'K') return true;
                }
            }
        }

        // 4. Check ray defenders
        const rayDirs = [
            { dirs: [[-1, -1], [-1, 1], [1, -1], [1, 1]], types: ['B', 'Q'] },
            { dirs: [[-1, 0], [1, 0], [0, -1], [0, 1]], types: ['R', 'Q'] }
        ];

        for (let group of rayDirs) {
            for (let [dF, dR] of group.dirs) {
                let stepF = fileIdx + dF;
                let stepR = rankIdx + dR;
                while (stepF >= 0 && stepF < 8 && stepR >= 0 && stepR < 8) {
                    const sq = files[stepF] + ranks[stepR];
                    const piece = bState[sq];
                    if (piece) {
                        if (piece[0] === colorChar && group.types.includes(piece[1].toUpperCase())) {
                            return true;
                        }
                        break;
                    }
                    stepF += dF;
                    stepR += dR;
                }
            }
        }

        return false;
    };

    Object.keys(bState || {}).forEach(sq => {
        const piece = bState[sq];
        if (piece && piece[0] === colorChar && piece[1] !== 'K') {
            if (!isDefended(sq)) {
                loose.push({ sq, piece });
            }
        }
    });

    return loose;
}

function checkKingLuft(bState, colorChar) {
    const files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'];
    const ranks = ['1', '2', '3', '4', '5', '6', '7', '8'];

    let kingSq = null;
    Object.keys(bState || {}).forEach(sq => {
        if (bState[sq] === colorChar + 'K') kingSq = sq;
    });

    if (!kingSq) return { kingSq: colorChar === 'w' ? 'e1' : 'e8', escapeCount: 1, luftNeeded: false };

    const fileIdx = files.indexOf(kingSq[0]);
    const rankIdx = ranks.indexOf(kingSq[1]);

    let escapeCount = 0;
    for (let dF of [-1, 0, 1]) {
        for (let dR of [-1, 0, 1]) {
            if (dF === 0 && dR === 0) continue;
            const f = fileIdx + dF;
            const r = rankIdx + dR;
            if (f >= 0 && f < 8 && r >= 0 && r < 8) {
                const sq = files[f] + ranks[r];
                const piece = bState[sq];
                if (!piece || piece[0] !== colorChar) {
                    escapeCount++;
                }
            }
        }
    }

    const backRank = (colorChar === 'w') ? '1' : '8';
    const isBackRank = (kingSq[1] === backRank);
    const luftNeeded = isBackRank && (escapeCount <= 1);

    return { kingSq, escapeCount, luftNeeded };
}

function getGlobalTurnGuidelines() {
    const saved = localStorage.getItem('chess_global_turn_guidelines');
    if (saved) {
        try {
            const parsed = JSON.parse(saved);
            if (Array.isArray(parsed) && parsed.length > 0) {
                return parsed;
            }
        } catch (e) {
            console.error('Failed to parse global turn guidelines:', e);
        }
    }
    localStorage.setItem('chess_global_turn_guidelines', JSON.stringify(DEFAULT_TURN_GUIDELINES));
    return DEFAULT_TURN_GUIDELINES;
}

function saveGlobalTurnGuidelines(guidelinesList) {
    localStorage.setItem('chess_global_turn_guidelines', JSON.stringify(guidelinesList));
}

function renderTurnGuidelines(bState = boardState, fenStr = currentFen, evalData = latestEvalData || {}) {
    const cardEl = document.getElementById('card-turn-guidelines');
    const listEl = document.getElementById('turn-guidelines-list');
    const badgeEl = document.getElementById('guidelines-count-badge');

    if (!cardEl || !listEl) return;

    if (!gameSettings.showTurnGuidelines) {
        cardEl.classList.add('hidden');
        return;
    }
    cardEl.classList.remove('hidden');

    const guidelines = getGlobalTurnGuidelines();
    if (badgeEl) badgeEl.textContent = `${guidelines.length} Rules`;

    const turnChar = (fenStr || currentFen).split(' ')[1] || 'w';
    const loosePieces = findLoosePieces(bState, turnChar);
    const kingLuft = checkKingLuft(bState, turnChar);
    const matBalance = calculateMaterialBalance(bState);
    const activeMatDiff = (turnChar === 'w') ? matBalance.diff : -matBalance.diff;

    listEl.innerHTML = '';

    guidelines.forEach(g => {
        let isTriggered = false;
        let statusText = 'Turn Reminder 📌';

        if (g.id === 'loose_piece_check' || (g.title && g.title.includes('Loose Piece'))) {
            if (loosePieces.length > 0) {
                isTriggered = true;
                const names = loosePieces.map(p => `${p.piece[1].toUpperCase()} on ${p.sq}`).join(', ');
                statusText = `⚠️ ALERT ACTIVE: Undefended (${names})`;
            }
        } else if (g.id === 'luft_rule' || (g.title && g.title.includes('Luft'))) {
            if (kingLuft.luftNeeded) {
                isTriggered = true;
                statusText = `⚠️ ALERT ACTIVE: King on ${kingLuft.kingSq} lacks escape square`;
            }
        } else if (g.id === 'simplify_material' || (g.title && g.title.includes('Simplify'))) {
            if (activeMatDiff >= 3) {
                isTriggered = true;
                statusText = `🎯 ALERT ACTIVE: Ahead +${activeMatDiff} material — Trade active pieces!`;
            }
        }

        const itemEl = document.createElement('div');
        itemEl.className = `guideline-item ${isTriggered ? 'active-trigger' : ''}`;
        itemEl.innerHTML = `
            <div class="guideline-item-header">
                <div class="guideline-title-group">
                    <span class="guideline-icon">${g.icon || '📌'}</span>
                    <span class="guideline-title">${g.title}</span>
                </div>
                <span class="guideline-status-badge ${isTriggered ? 'active' : ''}">${statusText}</span>
            </div>
            <p class="guideline-text">${g.text}</p>
            <div class="guideline-footer">
                <span class="guideline-citation-tag">${g.citations || ''}</span>
                <span class="guideline-category-tag">${g.category || 'General'}</span>
                <div class="guideline-actions-group">
                    <button class="guideline-edit-btn" data-id="${g.id}" title="Edit this rule">✏️ Edit</button>
                    <button class="guideline-delete-btn" data-id="${g.id}" title="Remove rule from global guidelines">🗑️</button>
                </div>
            </div>
        `;

        itemEl.querySelector('.guideline-edit-btn').addEventListener('click', (e) => {
            e.stopPropagation();
            openGuidelineModal(g);
        });

        itemEl.querySelector('.guideline-delete-btn').addEventListener('click', (e) => {
            e.stopPropagation();
            if (confirm(`Delete rule "${g.title}" from global guidelines shared across all profiles?`)) {
                const updated = getGlobalTurnGuidelines().filter(item => item.id !== g.id);
                saveGlobalTurnGuidelines(updated);
                renderTurnGuidelines(bState, fenStr, evalData);
            }
        });

        listEl.appendChild(itemEl);
    });
}

function openGuidelineModal(ruleToEdit = null) {
    const modal = document.getElementById('add-guideline-modal');
    if (!modal) return;

    const titleHeader = modal.querySelector('.modal-header h3');
    const titleInput = document.getElementById('guideline-title-input');
    const catSelect = document.getElementById('guideline-category-select');
    const textInput = document.getElementById('guideline-text-input');
    const citeInput = document.getElementById('guideline-citation-input');

    if (ruleToEdit) {
        editingGuidelineId = ruleToEdit.id;
        if (titleHeader) titleHeader.textContent = '✏️ Edit Turn Guideline Rule';
        if (titleInput) titleInput.value = ruleToEdit.title || '';
        if (catSelect) catSelect.value = ruleToEdit.category || 'Tactics';
        if (textInput) textInput.value = ruleToEdit.text || '';
        if (citeInput) citeInput.value = ruleToEdit.citations || '';
    } else {
        editingGuidelineId = null;
        if (titleHeader) titleHeader.textContent = '➕ Add Turn Guideline from Game Analysis';
        if (titleInput) titleInput.value = '';
        if (catSelect) catSelect.value = 'Tactics';
        if (textInput) textInput.value = '';
        if (citeInput) citeInput.value = '';
    }
    modal.classList.remove('hidden');
}

function renderPracticeSubjectInstruction(bState, fenStr, evalData) {
    const cardEl = document.getElementById('card-practice-subject');
    const selectEl = document.getElementById('practice-subject-select');
    const boxEl = document.getElementById('practice-instruction-content');
    const iconEl = document.getElementById('practice-instruction-icon');
    const titleEl = document.getElementById('practice-instruction-title');
    const textEl = document.getElementById('practice-instruction-text');

    if (!cardEl || !boxEl) return;

    if (!gameSettings.showPracticeSubject) {
        cardEl.classList.add('hidden');
        return;
    }
    cardEl.classList.remove('hidden');

    let activeSubject = selectEl ? selectEl.value : (gameSettings.activePracticeSubject || 'auto');

    const turnChar = (fenStr || currentFen).split(' ')[1] || 'w';
    const turnName = turnChar === 'w' ? 'White' : 'Black';
    const loosePieces = findLoosePieces(bState, turnChar);
    const kingLuft = checkKingLuft(bState, turnChar);
    const matBalance = calculateMaterialBalance(bState);
    const activeMatDiff = (turnChar === 'w') ? matBalance.diff : -matBalance.diff;

    // Auto Prioritization
    let effectiveSubject = activeSubject;
    if (activeSubject === 'auto') {
        const isCheck = evalData && (evalData.is_check || evalData.white_in_check || evalData.black_in_check);
        if (isCheck || kingLuft.luftNeeded) {
            effectiveSubject = 'king_safety';
        } else if (loosePieces.length > 0) {
            effectiveSubject = 'loose_pieces';
        } else if (activeMatDiff >= 3) {
            effectiveSubject = 'material_simplification';
        } else {
            effectiveSubject = 'piece_activity';
        }
    }

    let icon = '🎯';
    let title = 'Strategic Focus';
    let text = '';
    let isAlert = false;

    if (effectiveSubject === 'loose_pieces') {
        icon = '🛡️';
        title = 'Subject: Loose Pieces & Tactical Security';
        if (loosePieces.length > 0) {
            isAlert = true;
            const names = loosePieces.map(p => `${p.piece[1].toUpperCase()} on ${p.sq}`).join(', ');
            text = `🔍 <strong>Current Situation (${turnName}):</strong> Undefended loose piece(s) detected: <strong>${names}</strong>.<br>💡 <strong>Mentor Action:</strong> Before advancing or attacking, verify that these loose pieces aren't exposed to tactical combinations or double attacks!`;
        } else {
            text = `🔍 <strong>Current Situation (${turnName}):</strong> All active pieces have friendly defenders.<br>💡 <strong>Mentor Action:</strong> Keep your piece coordination intact. Check opponent's pieces for undefended targets to exploit.`;
        }
    } else if (effectiveSubject === 'king_safety') {
        icon = '👑';
        title = 'Subject: King Safety & Escape Squares (Luft)';
        if (kingLuft.luftNeeded) {
            isAlert = true;
            text = `🔍 <strong>Current Situation (${turnName}):</strong> Your King on <strong>${kingLuft.kingSq}</strong> is enclosed with restricted retreat options.<br>💡 <strong>Mentor Action:</strong> Prevent back-rank mate threats! Create a "luft" escape square (e.g. h3 or g3 for White) before pushing forward.`;
        } else {
            text = `🔍 <strong>Current Situation (${turnName}):</strong> King on <strong>${kingLuft.kingSq}</strong> has ${kingLuft.escapeCount} escape square(s).<br>💡 <strong>Mentor Action:</strong> Keep your pawn shield intact and ensure rooks maintain defense on key ranks.`;
        }
    } else if (effectiveSubject === 'material_simplification') {
        icon = '🎯';
        title = 'Subject: Material Advantage & Simplification';
        if (activeMatDiff >= 3) {
            isAlert = true;
            text = `🔍 <strong>Current Situation (${turnName}):</strong> You are up by <strong>+${activeMatDiff} material points</strong> (piece/rook lead)!<br>💡 <strong>Mentor Action:</strong> Trade off active enemy pieces (especially rooks & queens) to neutralize counterplay and enter a won endgame.`;
        } else if (activeMatDiff <= -3) {
            text = `🔍 <strong>Current Situation (${turnName}):</strong> You are down by <strong>-${Math.abs(activeMatDiff)} material points</strong>.<br>💡 <strong>Mentor Action:</strong> Keep pieces active, avoid passive trades, and create complications or pawn imbalances.`;
        } else {
            text = `🔍 <strong>Current Situation (${turnName}):</strong> Material balance is roughly equal (${activeMatDiff >= 0 ? '+' : ''}${activeMatDiff}).<br>💡 <strong>Mentor Action:</strong> Focus on positional gains, piece outposts, and king safety before tactical simplify trades.`;
        }
    } else if (effectiveSubject === 'piece_activity') {
        icon = '🏰';
        title = 'Subject: Piece Activity & Center Control';
        const bestMove = (evalData && evalData.eval && evalData.eval.best_move_san) ? evalData.eval.best_move_san : null;
        text = `🔍 <strong>Current Situation (${turnName}):</strong> Evaluating central control (d4, d5, e4, e5) and piece mobility.` + (bestMove ? ` Best line recommendation: <strong>${bestMove}</strong>.` : '') + `<br>💡 <strong>Mentor Action:</strong> Activate your least active piece and place knights/bishops on strong central outposts.`;
    } else if (effectiveSubject === 'pawn_structure') {
        icon = '♟️';
        title = 'Subject: Pawn Structure & Weak Squares';
        text = `🔍 <strong>Current Situation (${turnName}):</strong> Monitoring pawn chain integrity and key backward/isolated pawns.<br>💡 <strong>Mentor Action:</strong> Protect weak squares near your king and avoid creating unnecessary pawn levers that open lines for opponent rooks.`;
    }

    if (iconEl) iconEl.textContent = icon;
    if (titleEl) titleEl.textContent = title;
    if (textEl) textEl.innerHTML = text;

    if (isAlert) {
        boxEl.classList.add('alert-active');
    } else {
        boxEl.classList.remove('alert-active');
    }
}

// ==========================================
// 🤖 AUTOMATED LIVE AI COACHING QUEUE & FEED
// ==========================================
let liveCoachingQueue = [];
let isCoachingProcessing = false;
let isSquareAnalysisThinking = false;
let liveCoachingLog = [];

function triggerAutoLiveCoaching(currentMoveNum) {
    if (gameSettings.enableAutoLLMAnalysis === false) return;
    const interval = parseInt(gameSettings.autoCoachingInterval !== undefined ? gameSettings.autoCoachingInterval : 2, 10);
    if (!interval || interval <= 0 || currentMoveNum <= 0) return;

    if (currentMoveNum % interval === 0) {
        if (!liveCoachingQueue.includes(currentMoveNum) && !liveCoachingLog.some(item => item.moveNumber === currentMoveNum)) {
            liveCoachingQueue.push(currentMoveNum);
            processLiveCoachingQueue();
        }
    }
}

async function processLiveCoachingQueue() {
    if (isCoachingProcessing || liveCoachingQueue.length === 0) return;

    const moveNum = liveCoachingQueue.shift();
    isCoachingProcessing = true;

    const statusBadge = document.getElementById('coaching-status-badge');
    if (statusBadge) {
        statusBadge.innerHTML = `<span style="display:inline-flex; align-items:center; gap:6px; color:#e58f2a; font-weight:700;"><span>🎓 AI Mentor is thinking for Move ${moveNum}...</span><span class="typing-dots"><span></span><span></span><span></span></span></span>`;
    }

    renderLiveCoachLogFeed();

    try {
        const subjectSelect = document.getElementById('practice-subject-select');
        const activeSubject = subjectSelect ? subjectSelect.value : (gameSettings.activePracticeSubject || 'auto');
        const currentRules = getGlobalTurnGuidelines();

        const studentColor = (gameSettings.whitePlayerMode === 'manual' && gameSettings.blackPlayerMode === 'auto') ? 'white'
            : (gameSettings.whitePlayerMode === 'auto' && gameSettings.blackPlayerMode === 'manual') ? 'black'
            : 'both';

        const activeProfile = typeof getActiveProfile === 'function' ? getActiveProfile() : null;

        const resp = await fetch('/api/mentor/live-coaching', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                fen: currentFen,
                moves: moveHistory.slice(0, moveNum),
                move_number: moveNum,
                student_color: studentColor,
                practice_subject: activeSubject,
                turn_guidelines: currentRules,
                user_profile: activeProfile,
                notebook_id: currentNotebookId
            })
        });

        const data = await resp.json();
        if (data.success && data.response) {
            const coachingEntry = {
                id: 'item_' + Date.now() + '_' + Math.random(),
                moveNumber: moveNum,
                studentColor: data.student_color || studentColor,
                fen: data.fen || currentFen,
                response: data.response,
                provider: data.provider || 'NotebookLM',
                timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
            };

            liveCoachingLog.push(coachingEntry);
        }
    } catch (e) {
        console.error('Live coaching request failed for move', moveNum, e);
    } finally {
        isCoachingProcessing = false;
        if (statusBadge) {
            if (gameSettings.enableAutoLLMAnalysis === false) {
                statusBadge.textContent = 'Paused';
                statusBadge.style.color = '#8b8987';
            } else {
                statusBadge.textContent = 'Standby';
                statusBadge.style.color = '#81b64c';
            }
        }
        renderLiveCoachLogFeed();
        processLiveCoachingQueue();
    }
}

const collapsedLogItems = new Set();

function renderLiveCoachLogFeed() {
    const listEl = document.getElementById('live-coach-log-list');
    const statusBadge = document.getElementById('coaching-status-badge');
    if (!listEl) return;

    if (statusBadge && !isCoachingProcessing) {
        if (gameSettings.enableAutoLLMAnalysis === false) {
            statusBadge.textContent = 'Paused';
            statusBadge.style.color = '#8b8987';
        } else {
            statusBadge.textContent = 'Standby';
            statusBadge.style.color = '#81b64c';
        }
    }

    if (liveCoachingLog.length === 0 && !isCoachingProcessing) {
        if (gameSettings.enableAutoLLMAnalysis === false) {
            listEl.innerHTML = `<div class="empty-coaching-placeholder" style="font-size:11px; color:#8b8987; font-style:italic; padding:6px 0;">Live AI Coach auto-analysis is currently paused. Check "Auto LLM Analysis" to enable automatic commentary.</div>`;
        } else {
            const interval = gameSettings.autoCoachingInterval || 2;
            listEl.innerHTML = `<div class="empty-coaching-placeholder" style="font-size:11px; color:#8b8987; font-style:italic; padding:6px 0;">Live AI Coach commentary will appear here automatically every ${interval} moves as you play...</div>`;
        }
        return;
    }

    listEl.innerHTML = '';

    if (isCoachingProcessing) {
        const thinkingEl = document.createElement('div');
        thinkingEl.className = 'coach-log-item thinking';
        const isSqThinking = isSquareAnalysisThinking;
        const thinkingBg = isSqThinking ? 'background:rgba(52,152,219,0.12); border:1px dashed #3498db; color:#3498db;' : 'background:rgba(229,143,42,0.12); border:1px dashed #e58f2a; color:#e58f2a;';
        const thinkingTitle = isSqThinking ? '🎯 Mentor considers square weaknesses and strengths...' : '🎓 AI Mentor is analyzing turn...';

        thinkingEl.style.cssText = `${thinkingBg} border-radius:6px; padding:8px 10px; font-size:11px; margin-bottom:6px;`;
        thinkingEl.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="font-weight:700;">${thinkingTitle}</span>
                <div class="typing-dots"><span></span><span></span><span></span></div>
            </div>
        `;
        listEl.appendChild(thinkingEl);
    }

    [...liveCoachingLog].reverse().forEach(item => {
        const itemKey = item.id || `m_${item.moveNumber}`;
        const isCollapsed = collapsedLogItems.has(itemKey);

        const sColor = (item.studentColor || 'white').toLowerCase();
        let colorTag = '⚪ Mentoring White';
        if (sColor === 'black') colorTag = '⚫ Mentoring Black';
        else if (sColor === 'both') colorTag = '☯️ Mentoring Both';

        const isSquareAnalysis = item.isSquareAnalysis || false;
        const headerTitle = isSquareAnalysis ? (item.title || '🎯 Mentor Analysis: Key Square Weaknesses & Strengths') : `🎓 Move ${item.moveNumber} — ${colorTag}`;
        const headerColor = isSquareAnalysis ? '#3498db' : '#81b64c';
        const cardBorder = isSquareAnalysis ? 'border:1px solid #3498db;' : 'border:1px solid var(--card-border);';

        const itemEl = document.createElement('div');
        itemEl.className = 'coach-log-item';
        itemEl.style.cssText = `background:#161512; ${cardBorder} border-radius:6px; padding:8px 10px; color:#d0cecc; display:flex; flex-direction:column; gap:6px;`;
        itemEl.innerHTML = `
            <div class="coach-log-header clickable" style="display:flex; justify-content:space-between; align-items:center; cursor:pointer;" title="Click to collapse / expand commentary">
                <div style="display:flex; align-items:center; gap:6px;">
                    <button class="collapse-btn" style="padding:0 2px; font-size:10px; pointer-events:none;">${isCollapsed ? '►' : '▼'}</button>
                    <span style="font-weight:700; color:${headerColor}; font-size:12px;">${headerTitle}</span>
                </div>
                <div style="display:flex; align-items:center; gap:6px;">
                    <span style="font-size:10px; color:#8b8987;">${item.timestamp}</span>
                    ${!isSquareAnalysis ? `<button class="btn btn-xs btn-secondary btn-replay-move" data-movenum="${item.moveNumber}" style="padding:2px 6px; font-size:10px;">🔍 Replay Move ${item.moveNumber}</button>` : ''}
                    <button class="btn btn-xs btn-secondary btn-delete-coach-item" data-itemkey="${itemKey}" style="padding:2px 6px; font-size:10px;" title="Clear this mentor comment block">🗑️ Clear</button>
                </div>
            </div>
            <div class="coach-log-body" style="${isCollapsed ? 'display:none;' : 'display:flex; flex-direction:column; gap:6px; margin-top:4px;'}">
                <div class="coach-log-item-content">
                    ${formatMarkdownToHtml(item.response)}
                </div>
            </div>
        `;

        itemEl.querySelector('.coach-log-header').addEventListener('click', (e) => {
            if (e.target.closest('.btn-replay-move') || e.target.closest('.btn-delete-coach-item')) return;
            if (collapsedLogItems.has(itemKey)) {
                collapsedLogItems.delete(itemKey);
            } else {
                collapsedLogItems.add(itemKey);
            }
            renderLiveCoachLogFeed();
        });

        if (!isSquareAnalysis) {
            itemEl.querySelector('.btn-replay-move')?.addEventListener('click', (e) => {
                e.stopPropagation();
                if (collapsedLogItems.has(itemKey)) {
                    collapsedLogItems.delete(itemKey);
                }
                viewHistoricalMove(item.moveNumber - 1);
                renderLiveCoachLogFeed();
            });
        }

        itemEl.querySelector('.btn-delete-coach-item')?.addEventListener('click', (e) => {
            e.stopPropagation();
            liveCoachingLog = liveCoachingLog.filter(x => (x.id || `m_${x.moveNumber}`) !== itemKey);
            renderLiveCoachLogFeed();
        });

        listEl.appendChild(itemEl);
    });
}

function scrollToSquareCommentary(sqName) {
    if (!sqName) return;
    const sqUpper = sqName.toUpperCase();
    const sqLower = sqName.toLowerCase();

    const listEl = document.getElementById('live-coach-log-list');
    if (!listEl) return;

    const items = listEl.querySelectorAll('.coach-log-item');
    let targetItem = null;

    for (let item of items) {
        const text = item.textContent || '';
        if (text.includes(sqLower) || text.includes(sqUpper) || text.includes(`\`${sqLower}\``) || text.includes(`(${sqUpper})`)) {
            targetItem = item;
            break;
        }
    }

    if (targetItem) {
        const bodyEl = targetItem.querySelector('.coach-log-body');
        if (bodyEl) bodyEl.style.display = 'flex';

        targetItem.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

        targetItem.classList.remove('commentary-highlight-pulse');
        void targetItem.offsetWidth;
        targetItem.classList.add('commentary-highlight-pulse');
        setTimeout(() => targetItem.classList.remove('commentary-highlight-pulse'), 2500);

        showGameToast(`🎯 Scrolled to <strong>${sqUpper}</strong> in Mentor Analysis`);
    } else {
        showGameToast(`ℹ️ Square <strong>${sqUpper}</strong> commentary in Mentor Feed`);
    }
}

function showBoardLlmScanningOverlay(messageText = 'LLM Analyzing Square Labels & Motifs...') {
    const overlayEl = document.getElementById('board-llm-scanning-overlay');
    const textEl = document.getElementById('llm-scan-text');
    const scanlineEl = overlayEl ? overlayEl.querySelector('.llm-scanline') : null;

    if (textEl) textEl.textContent = messageText;

    if (scanlineEl) {
        // Randomly pick between linear scanline and laser raster grid scan!
        if (Math.random() < 0.5) {
            scanlineEl.classList.add('laser-grid');
        } else {
            scanlineEl.classList.remove('laser-grid');
        }
    }

    if (overlayEl) {
        overlayEl.classList.remove('hidden');
    }
}

function hideBoardLlmScanningOverlay() {
    const overlayEl = document.getElementById('board-llm-scanning-overlay');
    if (overlayEl) {
        overlayEl.classList.add('hidden');
    }
}

async function requestManualLiveCoachComment() {
    const btnGet = document.getElementById('btn-get-mentor-comment');
    if (btnGet) {
        btnGet.disabled = true;
        btnGet.innerHTML = '🎓 Thinking...';
    }

    showBoardLlmScanningOverlay("🎓 AI Mentor is analyzing current move...");

    const currentMoveNum = moveHistory.length;
    if (!liveCoachingQueue.includes(currentMoveNum)) {
        liveCoachingQueue.push(currentMoveNum);
    }

    try {
        await processLiveCoachingQueue();
    } catch (e) {
        console.error('Manual live coach request failed:', e);
    } finally {
        hideBoardLlmScanningOverlay();
        if (btnGet) {
            btnGet.disabled = false;
            btnGet.innerHTML = '🎓 Get Comment';
        }
    }
}

async function fetchLlmSquareLabels() {
    const btnLlm = document.getElementById('btn-fetch-llm-square-labels');
    if (btnLlm) {
        btnLlm.disabled = true;
        btnLlm.innerHTML = '⏳ Analyzing...';
    }

    showBoardLlmScanningOverlay("🤖 LLM analyzing square weaknesses, outposts & motifs...");

    isCoachingProcessing = true;
    isSquareAnalysisThinking = true;
    renderLiveCoachLogFeed();

    try {
        const targetFen = isEditBoardMode ? currentFen : startFen;
        const targetMoves = isEditBoardMode ? [] : moveHistory;
        const activeProfile = typeof getActiveProfile === 'function' ? getActiveProfile() : null;

        const resp = await fetch('/api/board/llm-square-analysis', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                fen: targetFen,
                moves: targetMoves,
                notebook_id: currentNotebookId || null,
                user_profile: activeProfile
            })
        });

        const data = await resp.json();
        if (data.success) {
            if (data.overlays) {
                if (latestEvalData) {
                    latestEvalData.overlays = data.overlays;
                }
                renderBoardOverlays(data.overlays);
            }
            if (data.response) {
                const sqEntry = {
                    id: 'sq_' + Date.now(),
                    moveNumber: moveHistory.length || 1,
                    isSquareAnalysis: true,
                    title: '🎯 Mentor Analysis: Key Square Weaknesses & Strengths',
                    response: data.response,
                    timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
                    studentColor: (gameSettings.whitePlayerMode === 'manual') ? 'white' : 'black'
                };
                liveCoachingLog.push(sqEntry);
            }
        }
    } catch (e) {
        console.error('Failed to fetch LLM square analysis:', e);
    } finally {
        isCoachingProcessing = false;
        isSquareAnalysisThinking = false;
        hideBoardLlmScanningOverlay();
        if (btnLlm) {
            btnLlm.disabled = false;
            btnLlm.innerHTML = '🤖 LLM Square Labels';
        }
        renderLiveCoachLogFeed();
        const listEl = document.getElementById('live-coach-log-list');
        if (listEl) listEl.scrollTop = 0;
    }
}

function initStrategicDisplaysModule() {
    const btnGetComment = document.getElementById('btn-get-mentor-comment');
    if (btnGetComment) {
        btnGetComment.addEventListener('click', requestManualLiveCoachComment);
    }

    const btnFetchLlmLabels = document.getElementById('btn-fetch-llm-square-labels');
    if (btnFetchLlmLabels) {
        btnFetchLlmLabels.addEventListener('click', fetchLlmSquareLabels);
    }

    const chkFeedAutoLLM = document.getElementById('chk-auto-llm-analysis');
    if (chkFeedAutoLLM) {
        chkFeedAutoLLM.checked = gameSettings.enableAutoLLMAnalysis !== false;
        chkFeedAutoLLM.addEventListener('change', () => {
            gameSettings.enableAutoLLMAnalysis = chkFeedAutoLLM.checked;
            const modalChk = document.getElementById('setting-enable-auto-llm-analysis');
            if (modalChk) modalChk.checked = chkFeedAutoLLM.checked;
            saveGameSettingsToStorage();
            renderLiveCoachLogFeed();
        });
    }

    const btnClearFeed = document.getElementById('btn-clear-coach-feed');
    if (btnClearFeed) {
        btnClearFeed.addEventListener('click', () => {
            liveCoachingLog = [];
            renderLiveCoachLogFeed();
        });
    }
    const subjectSelect = document.getElementById('practice-subject-select');
    if (subjectSelect) {
        subjectSelect.addEventListener('change', () => {
            gameSettings.activePracticeSubject = subjectSelect.value;
            saveGameSettingsToStorage();
            if (latestEvalData) {
                renderPracticeSubjectInstruction(boardState, currentFen, latestEvalData);
            }
        });
    }

    const btnSuggest = document.getElementById('btn-suggest-subjects');
    if (btnSuggest) {
        btnSuggest.addEventListener('click', async () => {
            btnSuggest.disabled = true;
            btnSuggest.textContent = '⏳ Thinking...';
            try {
                const activeProfile = typeof getActiveProfile === 'function' ? getActiveProfile() : null;
                const resp = await fetch('/api/mentor/suggest-subjects', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        fen: currentFen,
                        moves: moveHistory,
                        user_profile: activeProfile,
                        notebook_id: currentNotebookId
                    })
                });
                const data = await resp.json();
                if (data.success && data.suggestions && data.suggestions.length > 0) {
                    const selectEl = document.getElementById('practice-subject-select');
                    const activeProf = typeof getActiveProfile === 'function' ? getActiveProfile() : null;

                    data.suggestions.forEach(s => {
                        const opt = document.createElement('option');
                        opt.value = s.id || ('subj_' + Date.now());
                        opt.textContent = `${s.is_pitfall ? '⚠️ Pitfall:' : '🎯'} ${s.title}`;
                        selectEl.appendChild(opt);

                        if (activeProf && activeProf.concepts && (s.category || s.title)) {
                            const catName = s.category || s.title;
                            const catKey = catName.toLowerCase().replace(/[^a-z0-9]/g, '_');
                            if (!activeProf.concepts[catKey]) {
                                activeProf.concepts[catKey] = {
                                    name: catName,
                                    rating: 1450,
                                    icon: s.is_pitfall ? '⚠️' : '🎯'
                                };
                            }
                        }
                    });

                    if (activeProf) saveUserProfilesToStorage();
                    alert(`✅ Mentor suggested ${data.suggestions.length} new practice subject(s) & pitfall(s) from your game history! Added to your profile's Skill Matrix.`);
                } else {
                    alert('No new subjects suggested for current game state.');
                }
            } catch (e) {
                alert('Failed to suggest subjects: ' + e.message);
            } finally {
                btnSuggest.disabled = false;
                btnSuggest.textContent = '🤖 Suggest';
            }
        });
    }

    const coachingSelect = document.getElementById('setting-coaching-interval');
    if (coachingSelect) {
        coachingSelect.value = gameSettings.autoCoachingInterval !== undefined ? gameSettings.autoCoachingInterval : 2;
        coachingSelect.addEventListener('change', () => {
            gameSettings.autoCoachingInterval = parseInt(coachingSelect.value, 10);
            saveGameSettingsToStorage();
            const indicator = document.getElementById('coaching-interval-indicator');
            if (indicator) indicator.textContent = gameSettings.autoCoachingInterval;
        });
    }

    // Collapse toggle handlers for all Analysis Tab cards
    const btnMaximizeLiveFeed = document.getElementById('btn-maximize-live-feed');
    function updateMaximizeLiveFeedBtnState() {
        if (!btnMaximizeLiveFeed) return;
        const subjectCard = document.getElementById('card-practice-subject');
        const guidelinesCard = document.getElementById('card-turn-guidelines');
        const subjectCollapsed = subjectCard ? subjectCard.classList.contains('collapsed') : false;
        const guidelinesCollapsed = guidelinesCard ? guidelinesCard.classList.contains('collapsed') : false;

        if (subjectCollapsed && guidelinesCollapsed) {
            btnMaximizeLiveFeed.innerHTML = '📖 Show Prep Cards';
            btnMaximizeLiveFeed.title = 'Expand Focus Subject and Turn Guidelines cards';
            btnMaximizeLiveFeed.classList.remove('btn-accent');
            btnMaximizeLiveFeed.classList.add('btn-secondary');
        } else {
            btnMaximizeLiveFeed.innerHTML = '⚡ Maximize Live Feed';
            btnMaximizeLiveFeed.title = 'Collapse Focus & Guidelines together to give maximum space to Live AI Coach Feed';
            btnMaximizeLiveFeed.classList.remove('btn-secondary');
            btnMaximizeLiveFeed.classList.add('btn-accent');
        }
    }

    const setupCardCollapse = (headerId, cardId) => {
        const header = document.getElementById(headerId);
        const card = document.getElementById(cardId);
        if (header && card) {
            header.addEventListener('click', (e) => {
                if (
                    e.target.tagName === 'SELECT' || 
                    e.target.tagName === 'OPTION' || 
                    e.target.id === 'btn-add-guideline-modal' || 
                    e.target.closest('#btn-add-guideline-modal') || 
                    e.target.id === 'btn-auto-extract-guidelines' || 
                    e.target.closest('#btn-auto-extract-guidelines') ||
                    e.target.id === 'btn-maximize-live-feed' ||
                    e.target.closest('#btn-maximize-live-feed') ||
                    e.target.id === 'btn-suggest-subjects' ||
                    e.target.closest('#btn-suggest-subjects')
                ) return;

                e.stopPropagation();
                card.classList.toggle('collapsed');
                updateMaximizeLiveFeedBtnState();
            });
        }
    };

    setupCardCollapse('header-stockfish-tools', 'card-stockfish-tools');
    setupCardCollapse('header-mentoring-tools', 'card-mentoring-tools');
    setupCardCollapse('header-practice-subject', 'card-practice-subject');
    setupCardCollapse('header-turn-guidelines', 'card-turn-guidelines');

    if (btnMaximizeLiveFeed) {
        btnMaximizeLiveFeed.addEventListener('click', (e) => {
            e.stopPropagation();
            const subjectCard = document.getElementById('card-practice-subject');
            const guidelinesCard = document.getElementById('card-turn-guidelines');
            const subjectCollapsed = subjectCard ? subjectCard.classList.contains('collapsed') : false;
            const guidelinesCollapsed = guidelinesCard ? guidelinesCard.classList.contains('collapsed') : false;

            const shouldCollapse = !(subjectCollapsed && guidelinesCollapsed);

            if (subjectCard) {
                if (shouldCollapse) subjectCard.classList.add('collapsed');
                else subjectCard.classList.remove('collapsed');
            }
            if (guidelinesCard) {
                if (shouldCollapse) guidelinesCard.classList.add('collapsed');
                else guidelinesCard.classList.remove('collapsed');
            }

            updateMaximizeLiveFeedBtnState();
        });

        // Sync initial state on load
        updateMaximizeLiveFeedBtnState();
    }

    function toggleBoardCollapse(forceState = null) {
        const boardSectionEl = document.getElementById('board-section');
        if (!boardSectionEl) return;

        let isCollapsed;
        if (forceState !== null) {
            if (forceState) boardSectionEl.classList.add('collapsed');
            else boardSectionEl.classList.remove('collapsed');
            isCollapsed = forceState;
        } else {
            isCollapsed = boardSectionEl.classList.toggle('collapsed');
        }

        const btnFloating = document.getElementById('btn-toggle-board-collapse');
        const btnCtrl = document.getElementById('btn-collapse-board-ctrl');
        const btnHeader = document.getElementById('header-btn-toggle-board');

        const labelText = isCollapsed ? '❯❯ Show Board' : '❮❮ Hide Board';
        const titleText = isCollapsed ? 'Expand board pane' : 'Collapse board pane to left side';

        if (btnFloating) {
            btnFloating.textContent = isCollapsed ? '❯❯' : '❮❮ Hide Board';
            btnFloating.title = titleText;
        }
        if (btnCtrl) {
            btnCtrl.textContent = labelText;
            btnCtrl.title = titleText;
        }
        if (btnHeader) {
            btnHeader.textContent = labelText;
            btnHeader.title = titleText;
        }

        if (!isCollapsed) {
            setTimeout(() => {
                renderBoard(boardState, lastMoveSquares);
                renderBoardOverlays(boardState);
            }, 50);
        }
    }

    const btnFloating = document.getElementById('btn-toggle-board-collapse');
    if (btnFloating) btnFloating.addEventListener('click', (e) => { e.stopPropagation(); toggleBoardCollapse(); });

    const btnCtrl = document.getElementById('btn-collapse-board-ctrl');
    if (btnCtrl) btnCtrl.addEventListener('click', (e) => { e.stopPropagation(); toggleBoardCollapse(); });

    const btnHeader = document.getElementById('header-btn-toggle-board');
    if (btnHeader) btnHeader.addEventListener('click', (e) => { e.stopPropagation(); toggleBoardCollapse(); });

    const btnAddModal = document.getElementById('btn-add-guideline-modal');
    if (btnAddModal) {
        btnAddModal.addEventListener('click', () => openGuidelineModal(null));
    }

    const btnOpenRulesManager = document.getElementById('btn-open-turn-rules-manager');
    if (btnOpenRulesManager) {
        btnOpenRulesManager.addEventListener('click', () => {
            const modalSettings = document.getElementById('game-settings-modal');
            if (modalSettings) modalSettings.classList.add('hidden');

            const cardTools = document.getElementById('card-mentoring-tools');
            if (cardTools) cardTools.classList.remove('collapsed');
            const cardGuidelines = document.getElementById('card-turn-guidelines');
            if (cardGuidelines) cardGuidelines.classList.remove('collapsed');

            if (cardGuidelines) cardGuidelines.scrollIntoView({ behavior: 'smooth' });
            openGuidelineModal(null);
        });
    }

    const btnReturnLive = document.getElementById('btn-return-live-game');
    if (btnReturnLive) {
        btnReturnLive.addEventListener('click', returnToLiveGame);
    }

    const btnAutoExtract = document.getElementById('btn-auto-extract-guidelines');
    if (btnAutoExtract) {
        btnAutoExtract.addEventListener('click', async () => {
            btnAutoExtract.disabled = true;
            btnAutoExtract.textContent = '⏳ Extracting...';
            try {
                const chatBox = document.getElementById('mentor-chat-messages');
                const lastBubble = chatBox ? chatBox.querySelector('.mentor-bubble:last-child .bubble-content') : null;
                const analysisText = lastBubble ? lastBubble.textContent : '';

                const resp = await fetch('/api/mentor/extract-guidelines', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        fen: currentFen,
                        moves: moveHistory,
                        analysis_text: analysisText
                    })
                });
                const data = await resp.json();
                if (data.success && data.guidelines && data.guidelines.length > 0) {
                    const currentRules = getGlobalTurnGuidelines();
                    const updated = [...currentRules, ...data.guidelines];
                    saveGlobalTurnGuidelines(updated);
                    renderTurnGuidelines(boardState, currentFen, latestEvalData);
                    alert(`✅ Automatically extracted ${data.guidelines.length} new Turn Guideline rule(s) from analysis!`);
                } else {
                    alert('No new rules extracted for current position.');
                }
            } catch (e) {
                alert('Auto-extraction failed: ' + e.message);
            } finally {
                btnAutoExtract.disabled = false;
                btnAutoExtract.textContent = '🤖 Auto-Extract';
            }
        });
    }

    const closeBtn = document.getElementById('btn-close-guideline-modal');
    if (closeBtn) closeBtn.addEventListener('click', () => document.getElementById('add-guideline-modal').classList.add('hidden'));

    const cancelBtn = document.getElementById('btn-cancel-guideline');
    if (cancelBtn) cancelBtn.addEventListener('click', () => document.getElementById('add-guideline-modal').classList.add('hidden'));

    const saveBtn = document.getElementById('btn-save-guideline');
    if (saveBtn) {
        saveBtn.addEventListener('click', () => {
            const title = document.getElementById('guideline-title-input').value.trim();
            const category = document.getElementById('guideline-category-select').value;
            const text = document.getElementById('guideline-text-input').value.trim();
            const citations = document.getElementById('guideline-citation-input').value.trim();

            if (!title || !text) {
                alert('Please provide a rule title and explanation.');
                return;
            }

            let icon = '🛡️';
            if (category === 'King Safety') icon = '👑';
            else if (category === 'Strategy') icon = '🎯';
            else if (category === 'Opening') icon = '♟️';
            else if (category === 'Endgame') icon = '🏰';

            const ruleData = {
                id: editingGuidelineId || ('rule_' + Date.now()),
                icon,
                title,
                text,
                citations: citations || '',
                category
            };

            let currentRules = getGlobalTurnGuidelines();
            if (editingGuidelineId) {
                currentRules = currentRules.map(r => r.id === editingGuidelineId ? ruleData : r);
            } else {
                currentRules.push(ruleData);
            }

            saveGlobalTurnGuidelines(currentRules);
            document.getElementById('add-guideline-modal').classList.add('hidden');
            editingGuidelineId = null;
            renderTurnGuidelines(boardState, currentFen, latestEvalData);
        });
    }
}

function initSidebarResizer() {
    const workspace = document.querySelector('.workspace');
    if (!workspace) return;

    const setupResizer = (resizerId, sidebarSelector, isRightSide) => {
        const resizer = document.getElementById(resizerId);
        const sidebar = document.querySelector(sidebarSelector);
        if (!resizer || !sidebar) return;

        let isResizing = false;

        const onMouseDown = (e) => {
            isResizing = true;
            resizer.classList.add('dragging');
            document.body.style.cursor = 'col-resize';
            document.body.style.userSelect = 'none';
            e.preventDefault();
        };

        const onMouseMove = (e) => {
            if (!isResizing) return;
            const workspaceRect = workspace.getBoundingClientRect();
            const clientX = e.touches ? e.touches[0].clientX : e.clientX;

            let newWidth;
            if (isRightSide) {
                newWidth = workspaceRect.right - clientX;
            } else {
                newWidth = clientX - workspaceRect.left;
            }

            const minWidth = 240;
            const maxWidth = Math.max(minWidth, workspaceRect.width * 0.45);

            if (newWidth < minWidth) newWidth = minWidth;
            if (newWidth > maxWidth) newWidth = maxWidth;

            sidebar.style.width = `${newWidth}px`;
            sidebar.style.flex = `0 0 ${newWidth}px`;
        };

        const onMouseUp = () => {
            if (isResizing) {
                isResizing = false;
                resizer.classList.remove('dragging');
                document.body.style.cursor = '';
                document.body.style.userSelect = '';
            }
        };

        resizer.addEventListener('mousedown', onMouseDown);
        document.addEventListener('mousemove', onMouseMove);
        document.addEventListener('mouseup', onMouseUp);

        resizer.addEventListener('touchstart', onMouseDown, { passive: false });
        document.addEventListener('touchmove', onMouseMove, { passive: false });
        document.addEventListener('touchend', onMouseUp);
    };

    setupResizer('left-sidebar-resizer', '.left-sidebar', false);
    setupResizer('right-sidebar-resizer', '.right-sidebar', true);
}









