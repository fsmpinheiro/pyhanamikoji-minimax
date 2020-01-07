# hanamikoyi_ai
Let's make an AI to play the card game hanamikoyi to see what the best strategy is.
Deck consists of: 2x blue twos, 2x red twos, 2x purple twos, 3x blue threes, 3x orange threes, 4x green fours, 5x pink fives.
There are four actions: 
- double swap: choose four cards, split them into two groups of two and offer the choice to the opponent.
- triple choose: choose three cards and offer the opponent to choose one
- burn cards: discard two cards from your hand
- conceal card: choose a card from your hand and hide it. It will be revealed and placed at the end of the game.

The game starts with burning a random card from the deck and dealing 6 cards to each player.
Each turn starts with a player pulling a random card.
Each player has 4 actions to choose from. Once an action is played, it cannot be played again. After 4 rounds, the game ends and the player with more points wins.

Use a Neural Network to handle inputs to output mapping. The input the agent sees are the following:
  - Cards in hand.
  - Cards on the table.
  - Previous actions / remaining actions of the agent.
  - Previous actions / remaning actions of the opponent.
  
The output of the agent is a choice of action and depending on the action a choice of cards to play.
