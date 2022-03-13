var gameboard;
var flagged_mines;
var unflagged_mines;
var original;
var gameover;
var first_uncover;

function create_board(width, height) {
    gameboard = new Array();
    for i in range(height):
        gameboard.push([]*width)
    return gameboard
}

function uncover_board(x, y) {
    if (gameboard[y][x] == null) {
        if
    }
}

function start() {
    gameboard = create_board(9, 9)
    flagged_mines = 0
    unflagged_mines = []
    original = {}
    gameover = False
    first_uncover = True
}

function Flag(x,y) {
    if (gameboard[y][x] != "f" && gameboard[y][x] != "F") {
        original[(x,y)] = gameboard[y][x];
        if (gameboard[y][x] === -1) {
            gameboard[y][x] = "F"
            flagged_mines += 1;
        } else {
            gameboard[y][x] = "f";
        }
    } else {
        unflagged_mines.push(y);
        gameboard[y][x] = original[(x,y)]
    }
}

function uncover(x, y) {
    var cell = gameboard[y][x]
    if (cell === -1) {
        return true;
    } else {
        uncover_board(x, y);
        return False, adjusted_board();
    }
}