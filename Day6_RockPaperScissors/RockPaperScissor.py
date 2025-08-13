import random
import json
import os
from datetime import datetime

class RockPaperScissors:
    """Rock Paper Scissors game with stats tracking and multiple difficulties."""
    
    def __init__(self):
        self.choices = ['rock', 'paper', 'scissors']
        self.stats_file = 'rps_stats.json'
        self.stats = self.load_stats()
        self.difficulty = 'normal'
    
    def load_stats(self):
        """Load stats from file or create default."""
        try:
            with open(self.stats_file, 'r') as f:
                return json.load(f)
        except:
            return {'wins': 0, 'losses': 0, 'ties': 0, 'games': 0, 'streak': 0, 
                   'best_streak': 0, 'choices': {'rock': 0, 'paper': 0, 'scissors': 0}}
    
    def save_stats(self):
        """Save current stats to file."""
        try:
            with open(self.stats_file, 'w') as f:
                json.dump(self.stats, f, indent=2)
        except Exception as e:
            print(f"Could not save stats: {e}")
    
    def get_player_choice(self):
        """Get and validate player input."""
        shortcuts = {'r': 'rock', 'p': 'paper', 's': 'scissors'}
        
        while True:
            choice = input("\nChoose (r)ock, (p)aper, (s)cissors, or (q)uit: ").lower().strip()
            
            if choice in ['q', 'quit']:
                return 'quit'
            elif choice in self.choices:
                return choice
            elif choice in shortcuts:
                return shortcuts[choice]
            else:
                print("Invalid choice! Try again.")
    
    def get_computer_choice(self):
        """Generate computer choice based on difficulty."""
        if self.difficulty == 'easy':
            # Slightly favor rock
            return random.choices(self.choices, weights=[0.4, 0.3, 0.3])[0]
        elif self.difficulty == 'hard' and self.stats['games'] > 3:
            # Counter player's most used choice 60% of the time
            favorite = max(self.stats['choices'], key=self.stats['choices'].get)
            counters = {'rock': 'paper', 'paper': 'scissors', 'scissors': 'rock'}
            return counters[favorite] if random.random() < 0.6 else random.choice(self.choices)
        else:
            return random.choice(self.choices)
    
    def determine_winner(self, player, computer):
        """Determine round winner."""
        if player == computer:
            return 'tie'
        
        winning = {'rock': 'scissors', 'paper': 'rock', 'scissors': 'paper'}
        return 'player' if winning[player] == computer else 'computer'
    
    def display_round(self, player, computer, result):
        """Display round results with ASCII art."""
        art = {
            'rock': "✊", 'paper': "✋", 'scissors': "✌️"
        }
        
        print(f"\nYou: {art[player]} {player.upper()}")
        print(f"Computer: {art[computer]} {computer.upper()}")
        
        if result == 'player':
            print("🎉 You win!")
        elif result == 'computer':
            print("💻 Computer wins!")
        else:
            print("🤝 It's a tie!")
    
    def update_stats(self, player_choice, result):
        """Update game statistics."""
        self.stats['games'] += 1
        self.stats['choices'][player_choice] += 1
        
        if result == 'player':
            self.stats['wins'] += 1
            self.stats['streak'] += 1
            self.stats['best_streak'] = max(self.stats['best_streak'], self.stats['streak'])
        elif result == 'computer':
            self.stats['losses'] += 1
            self.stats['streak'] = 0
        else:
            self.stats['ties'] += 1
    
    def display_stats(self):
        """Display game statistics."""
        s = self.stats
        print(f"\n📊 STATISTICS")
        print(f"Games: {s['games']} | Wins: {s['wins']} | Losses: {s['losses']} | Ties: {s['ties']}")
        
        if s['games'] > 0:
            win_rate = (s['wins'] / s['games']) * 100
            print(f"Win Rate: {win_rate:.1f}% | Current Streak: {s['streak']} | Best: {s['best_streak']}")
            
            print("Choice Frequency:", end=" ")
            for choice, count in s['choices'].items():
                pct = (count / s['games']) * 100
                print(f"{choice}: {count}({pct:.0f}%)", end=" ")
            print()
    
    def play_round(self):
        """Play a single round."""
        player_choice = self.get_player_choice()
        if player_choice == 'quit':
            return False
        
        computer_choice = self.get_computer_choice()
        result = self.determine_winner(player_choice, computer_choice)
        
        self.display_round(player_choice, computer_choice, result)
        self.update_stats(player_choice, result)
        return True
    
    def play_tournament(self, rounds=5):
        """Play a tournament of multiple rounds."""
        print(f"\n🏆 {rounds}-Round Tournament! (Difficulty: {self.difficulty.upper()})")
        
        start_wins = self.stats['wins']
        for i in range(1, rounds + 1):
            print(f"\n--- Round {i}/{rounds} ---")
            if not self.play_round():
                print("Tournament cancelled.")
                return
        
        tournament_wins = self.stats['wins'] - start_wins
        print(f"\n🏁 Tournament over! You won {tournament_wins}/{rounds} rounds!")
    
    def set_difficulty(self):
        """Change difficulty level."""
        print("\n1. Easy  2. Normal  3. Hard")
        choice = input("Select difficulty (1-3): ")
        
        difficulties = {'1': 'easy', '2': 'normal', '3': 'hard'}
        if choice in difficulties:
            self.difficulty = difficulties[choice]
            print(f"Difficulty set to: {self.difficulty.upper()}")
        else:
            print("Invalid selection.")
    
    def reset_stats(self):
        """Reset all statistics."""
        if input("Reset all stats? (y/n): ").lower() == 'y':
            self.stats = {'wins': 0, 'losses': 0, 'ties': 0, 'games': 0, 'streak': 0,
                         'best_streak': 0, 'choices': {'rock': 0, 'paper': 0, 'scissors': 0}}
            if os.path.exists(self.stats_file):
                os.remove(self.stats_file)
            print("Stats reset!")
    
    def run(self):
        """Main game loop."""
        while True:
            print(f"\n{'='*40}")
            print("🪨📄✂️  ROCK PAPER SCISSORS")
            print(f"{'='*40}")
            print("1. Quick Game    4. View Stats")
            print("2. Tournament    5. Reset Stats") 
            print("3. Difficulty    6. Quit")
            
            choice = input("\nSelect option (1-6): ")
            
            if choice == '1':
                self.play_round()
            elif choice == '2':
                self.play_tournament()
            elif choice == '3':
                self.set_difficulty()
            elif choice == '4':
                self.display_stats()
            elif choice == '5':
                self.reset_stats()
            elif choice == '6':
                self.save_stats()
                print("Thanks for playing! 👋")
                break
            else:
                print("Invalid option!")

def main():
    """Run the game."""
    try:
        game = RockPaperScissors()
        game.run()
    except KeyboardInterrupt:
        print("\n\nThanks for playing! 👋")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()