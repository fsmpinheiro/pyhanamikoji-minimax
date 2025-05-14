# hanamikoji
This project is an implementation of the Hanamikoji card game using the Python arcade game engine. The game can be configured to be played against an agent that can use two heuristics, one using randomness and the other using the Minimax Algorithm. It is also possible to configure the game so that two agents compete against each other.


## Game Rules:
Deck consists of: 2x blue twos, 2x red twos, 2x purple twos, 3x blue threes, 3x orange threes, 4x green fours, 5x pink fives:

At the start of the game a random card is discarded from the deck and 6 cards are dealt to each player.

There are 4 actions to choose from: 
  1) SECRET:       	Choose 1 card from hand and hide it. It will be revealed and placed at the end of the game.
  2) BURN:         	Choose 2 cards from hand and discard them.
  3) GIFT:         	Choose 3 cards from hand and offer the opponent to choose one card. 
  The opponent places their choice and you place the remaining 2 cards.
  4) COMPETITION:  	Choose 4 cards from hand, split them into 2 groups of two cards and offer the opponent to choose 1 group. 
  The opponent places their choice of 2 cards and you place the remaining 2 cards.

Each turn starts with a player pulling a random card.
Each player has 4 actions to choose from (described above). 
Once an action is played, it cannot be played again. 
After 4 rounds, the game ends, because each player has placed 8 cards and discarded 2 cards.

The winner is determined by looking at each unique type of card and checking which player was able to place more of that type compared to the opponent. 

