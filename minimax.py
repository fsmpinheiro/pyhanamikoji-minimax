"""
def minimax(position, depth, maximizingPlayer):
    if depth == 0 or game over in position
        return static evaluation of position

    if maximizingPlayer:
        maxEval = -infinity
        for each child in positions:
            eval = minimax(child, depth-1, False)
            maxEval = max(maxEval, eval)
        return maxEval

    else:
        minEval = infinity
        for each child in positions:
            eval = minimax(child, depth - 1, True)
            minEval = min(minEval, eval)
        return minEval
"""

"""
def minimax(position, depth, alpha, beta, maximizingPlayer):
    if depth == 0 or game over in position
        return static evaluation of position

    if maximizingPlayer:
        maxEval = -infinity
        for each child in positions:
            eval = minimax(child, depth-1, alpha, beta, False)
            maxEval = max(maxEval, eval)
            
            alpha = max(alpha, eval)
            if beta <= alpha
                break
                
        return maxEval

    else:
        minEval = infinity
        for each child in positions:
            eval = minimax(child, depth - 1, alpha, beta, True)
            minEval = min(minEval, eval)
            
            beta = min(beta, eval)
            if beta <= alpha
                break
            
        return minEval
"""

# initial call:
# minimax(currentPosition, 4, -inf, +inf, true)
