import time
import copy
from hexplode import algo_player

def criticality (tile_id, board):
    return len(board[tile_id]["neighbours"]) - board[tile_id]["counters"]

def vulnerability (tile_id, player_id, board):
    vul = 7
    for neighbourId in board[tile_id]["neighbours"]:
        if (board[neighbourId]["player"] is not None and board[neighbourId]["player"] != player_id):
            vul = min(vul, criticality(neighbourId, board))
    return vul

def winCount (checkedTiles, tile_id, player_id, board):
    if (tile_id in checkedTiles or board[tile_id]["player"] is None or criticality(tile_id, board) != 1):
        return 0
    checkedTiles.append(tile_id)
    count = 0
    for neighbourId in board[tile_id]["neighbours"]:
        if (vulnerability (neighbourId, player_id, board) == 1):
            return -1000
        if (board[neighbourId]["player"] != player_id):
            count += 1 + winCount(checkedTiles, neighbourId, player_id, board)
    return count
    
def isTileSafe(tile_id, player_id, board):
    for neighbourId in board[tile_id]["neighbours"]:
        if (board[neighbourId]["player"] != player_id):
            return False
    return True
    
@algo_player(name="Liuri Loami 14 - Ultimate 5",
             description="liuriloami@gmail.com")
def liuriloami(board, game_id, player_id):
    corner = False
    exploding = False
    bestCorner = 4
    bestWin = -100.0
    bestCell = None
    for tile_id, tile in board.items():
        vul = vulnerability(tile_id, player_id, board)
        neighbours = len(tile["neighbours"])
        
        ## Corner, if not vulnerable
        if (tile["player"] is None and neighbours < bestCorner and vul > 3 and isTileSafe(tile_id, player_id, board) is False):
            corner = True
            bestCorner = neighbours
            bestCell = tile_id
            
        ## If a corner was chosen, forget about the rest
        if (corner):
            continue
            
        if (tile["player"] == player_id):
            crit = criticality(tile_id, board)
            
            # If it is safe, avoid it
            if (isTileSafe(tile_id, player_id, board) is True):
                continue
                
            # If enemy is about to explode, explode first
            if (crit == 1 and vul == 1):
                bestCell = tile_id
                bestWin = 999
                    
            #Search for the biggest explosion
            checkedTiles = []
            win = winCount(checkedTiles, tile_id, player_id, board)
           
            if (win < 0):
                continue
                 
            if (crit == 1 and vul != 7 and win > bestWin):
                bestWin = win
                bestCell = tile_id
                exploding = True
                
            if (exploding is False and vul >= crit):
                if (-1*(vul-crit) > bestWin):
                    bestWin = -1*(vul-crit)
                    bestCell = tile_id
                if (-1*(vul-crit) == bestWin and win > bestWin):
                    bestWin = -1*(vul-crit)
                    bestCell = tile_id
                
   # If a tile was chosen, return if
    if (bestCell is not None):
        return bestCell
        
   # If not, return a random tile
    for tile_id, tile in board.items():
        if (tile["player"] == player_id):
            return tile_id
