# hanamikoyi_ai
Let's make an AI to play the card game hanamikoyi to see what the best strategy is.

## Rules:
Deck consists of: 2x blue twos, 2x red twos, 2x purple twos, 3x blue threes, 3x orange threes, 4x green fours, 5x pink fives:
We can represent the deck as: 'AABBCCDDDEEEFFFFGGGGG', as not all cards and card combinations are unique.

There are 4 actions to choose from: 
  1) SECRET:       	Choose 1 card from hand and hide it. It will be revealed and placed at the end of the game.
  2) BURN:         	Choose 2 cards from hand and discard them.
  3) GIFT:         	Choose 3 cards from hand and offer the opponent to choose one card. The opponent places their choice and you place the 									 remaining 2 cards.
  4) COMPETITION:  	Choose 4 cards from hand, split them into 2 groups of two cards and offer the opponent to choose 1 group. The opponent 											places their choice of 2 cards and you place the remaining 2 cards.

The game starts with burning a random card from the deck and dealing 6 cards to each player.

Each turn starts with a player pulling a random card.
Each player has 4 actions to choose from (described above). Once an action is played, it cannot be played again. After 4 rounds, the game ends, because each player has placed 8 cards and discarded 2 cards.

The winner is determined by looking at each unique type of card: 'A', 'B', 'C', 'D', 'E', 'F', 'G' and checking which player was able to place more of that type compared to the opponent. For instance if player 1 places more 'E's than player 2 -> player 1 wins that type. Each type is worth as many points as many instances there are of the card in the deck, i.e. A is worth 2, D is worth 3 and G is worth 5.
The player who scores a total of 11 points or the player who wins 4 types wins the game. If neither reaches these goals, the player who scores more points wins.

## Agent:
The agent sees the following information:
  - Cards in hand.
  - Cards placed on the table by both players.
  - Previous actions and card choices of the agent.
  - Previous actions and card choices of the opponent.
 
The output of the agent is a choice of action and depending on the action a choice of cards to play.
The agent also has to choose cards to place when offered via a GIFT or a COMPETITION action.
