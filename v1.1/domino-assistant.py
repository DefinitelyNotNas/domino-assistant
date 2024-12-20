import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Optional
import random
import json
from datetime import datetime

class DominoTile:
    """Represents a single domino tile with two sides."""
    def __init__(self, side1: int, side2: int):
        if not (0 <= side1 <= 6 and 0 <= side2 <= 6):
            raise ValueError("Domino values must be between 0 and 6")
        self.side1 = side1
        self.side2 = side2
        self.is_double = side1 == side2
        self.sum = side1 + side2
    
    def __str__(self):
        return f"[{self.side1}|{self.side2}]"
    
    def __repr__(self):
        return self.__str__()

    @classmethod
    def from_string(cls, tile_str: str) -> 'DominoTile':
        """Create a tile from string like '3-4' or '3,4'"""
        try:
            # Handle different separators
            if '-' in tile_str:
                side1, side2 = map(int, tile_str.split('-'))
            elif ',' in tile_str:
                side1, side2 = map(int, tile_str.split(','))
            else:
                raise ValueError
            return cls(side1, side2)
        except:
            raise ValueError("Invalid tile format. Use '3-4' or '3,4'")

class DominoBoard(ttk.Frame):
    """Visual representation of the domino game board."""
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, width=800, height=300, bg='forest green')
        self.canvas.pack(expand=True, fill=tk.BOTH)
        
        self.played_tiles = []
        self.tile_size = 40
        self.center_x = 400
        self.center_y = 150
        
    def add_tile(self, tile: DominoTile, position: str):
        """Add a tile to the board visualization."""
        self.played_tiles.append((tile, position))
        self.redraw_board()
        
    def redraw_board(self):
        """Redraw the entire board."""
        self.canvas.delete('all')
        
        # Start from center
        current_x = self.center_x
        current_y = self.center_y
        
        for tile, position in self.played_tiles:
            # Draw tile background
            self.canvas.create_rectangle(
                current_x, current_y,
                current_x + self.tile_size * 2, current_y + self.tile_size,
                fill='white', outline='black'
            )
            
            # Draw dividing line
            self.canvas.create_line(
                current_x + self.tile_size, current_y,
                current_x + self.tile_size, current_y + self.tile_size,
                fill='black'
            )
            
            # Draw numbers
            self.canvas.create_text(
                current_x + self.tile_size/2, current_y + self.tile_size/2,
                text=str(tile.side1)
            )
            self.canvas.create_text(
                current_x + self.tile_size*1.5, current_y + self.tile_size/2,
                text=str(tile.side2)
            )
            
            # Update position for next tile
            if position == 'right':
                current_x += self.tile_size * 2
            elif position == 'left':
                current_x -= self.tile_size * 2
                
    def clear_board(self):
        """Clear all tiles from the board."""
        self.played_tiles = []
        self.redraw_board()

class DominoAssistant:
    """Core game logic and strategy assistant."""
    def __init__(self):
        self.my_tiles = []
        self.played_tiles = []
        self.board_ends = []  # Current playable ends
        self.players_count = 4
        self.numbers_frequency = {i: 0 for i in range(7)}  # Track frequency of each number (0-6)
        self.player_patterns = {i: {j: 0 for j in range(7)} for i in range(4)}
        
    def add_tiles(self, tiles: List[DominoTile]):
        """Add tiles to your hand."""
        self.my_tiles.extend(tiles)
        for tile in tiles:
            self.numbers_frequency[tile.side1] += 1
            if not tile.is_double:
                self.numbers_frequency[tile.side2] += 1

    def remove_tile(self, tile: DominoTile):
        """Remove a tile from your hand after playing it."""
        if tile in self.my_tiles:
            self.my_tiles.remove(tile)
            self.update_game_state(tile, 0)

    def analyze_hand(self, my_tiles: List[DominoTile] = None) -> dict:
        """Analyzes the current hand and provides strategic insights."""
        if my_tiles is None:
            my_tiles = self.my_tiles

        analysis = {
            'strong_numbers': [],
            'weak_numbers': [],
            'doubles': [],
            'scoring_potential': 0,
            'suggested_play': None
        }
        
        hand_frequency = {i: 0 for i in range(7)}
        for tile in my_tiles:
            hand_frequency[tile.side1] += 1
            if not tile.is_double:
                hand_frequency[tile.side2] += 1
            if tile.is_double:
                analysis['doubles'].append(tile)
            analysis['scoring_potential'] += tile.sum
                
        for num, freq in hand_frequency.items():
            if freq >= 2:
                analysis['strong_numbers'].append(num)
            elif freq == 1:
                analysis['weak_numbers'].append(num)
                
        return analysis

    def calculate_probability(self, number: int) -> float:
        """Calculate probability of opponents having a specific number."""
        if not (0 <= number <= 6):
            raise ValueError("Number must be between 0 and 6")
            
        total_instances = 7
        known_instances = self.numbers_frequency[number]
        remaining = total_instances - known_instances
        
        if len(self.played_tiles) >= 28:
            return 0.0
            
        return remaining / max(1, (28 - len(self.played_tiles)))

    def suggest_play(self, board_ends: List[int]) -> Optional[DominoTile]:
        """Suggests the best tile to play based on current game state."""
        if not self.my_tiles or not board_ends:
            return None
            
        play_scores = []
        for tile in self.my_tiles:
            if tile.side1 in board_ends or tile.side2 in board_ends:
                score = 0
                # Basic score from number frequency
                score += self.numbers_frequency[tile.side1] + self.numbers_frequency[tile.side2]
                
                # Consider opponent probabilities
                for end in [tile.side1, tile.side2]:
                    if end not in board_ends:
                        opponent_prob = self.calculate_probability(end)
                        score -= opponent_prob * 5
                
                # Early game double bonus
                if tile.is_double and len(self.played_tiles) < 10:
                    score += 3
                    
                # Flexibility score
                remaining_tiles = [t for t in self.my_tiles if t != tile]
                playable_numbers = set()
                for t in remaining_tiles:
                    playable_numbers.add(t.side1)
                    playable_numbers.add(t.side2)
                score += len(playable_numbers)
                
                play_scores.append((score, tile))
        
        if play_scores:
            return max(play_scores, key=lambda x: x[0])[1]
        return None

    def update_game_state(self, played_tile: DominoTile, player_position: int):
        """Updates game state after each play."""
        if not (0 <= player_position < self.players_count):
            raise ValueError(f"Player position must be between 0 and {self.players_count-1}")
            
        self.played_tiles.append(played_tile)
        
        self.numbers_frequency[played_tile.side1] += 1
        if not played_tile.is_double:
            self.numbers_frequency[played_tile.side2] += 1
        
        self.player_patterns[player_position][played_tile.side1] += 1
        if not played_tile.is_double:
            self.player_patterns[player_position][played_tile.side2] += 1

    def get_endgame_strategy(self) -> str:
        """Provides endgame strategy based on remaining tiles."""
        if len(self.played_tiles) > 20:
            remaining_numbers = []
            for num, freq in self.numbers_frequency.items():
                if freq < 7:
                    remaining_numbers.append((num, 7 - freq))
            
            strategy = "Endgame strategy:\n"
            strategy += f"Unplayed numbers: {remaining_numbers}\n"
            
            if len(self.my_tiles) > 3:
                strategy += "Focus on blocking opponents by playing tiles that reduce their options"
            else:
                strategy += "Focus on getting rid of high-value tiles to minimize potential points"
                
            return strategy
        return "Not in endgame yet"

class DominoAssistantGUI:
    """Base GUI for the domino assistant."""
    def __init__(self, root):
        self.root = root
        self.root.title("Domino Assistant")
        self.assistant = DominoAssistant()
        
        # Create main frames
        self.create_frames()
        self.create_hand_management()
        self.create_game_actions()
        self.create_analysis_section()
        
        # Initialize status bar
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.set_status("Ready")

    def create_frames(self):
        """Create main organizational frames."""
        self.hand_frame = ttk.LabelFrame(self.root, text="Hand Management", padding="5")
        self.hand_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.action_frame = ttk.LabelFrame(self.root, text="Game Actions", padding="5")
        self.action_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.analysis_frame = ttk.LabelFrame(self.root, text="Analysis", padding="5")
        self.analysis_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def create_hand_management(self):
        """Create hand management section."""
        ttk.Label(self.hand_frame, text="Add tile (format: 3-4):").pack(side=tk.LEFT)
        self.tile_entry = ttk.Entry(self.hand_frame, width=10)
        self.tile_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(self.hand_frame, text="Add", command=self.add_tile).pack(side=tk.LEFT)
        ttk.Button(self.hand_frame, text="Clear Hand", command=self.clear_hand).pack(side=tk.LEFT, padx=5)

    def create_game_actions(self):
        """Create game actions section."""
        play_frame = ttk.Frame(self.action_frame)
        play_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(play_frame, text="Record play:").pack(side=tk.LEFT)
        self.play_entry = ttk.Entry(play_frame, width=10)
        self.play_entry.pack(side=tk.LEFT, padx=5)
        
        self.player_var = tk.StringVar(value="0")
        ttk.Label(play_frame, text="Player:").pack(side=tk.LEFT)
        player_spin = ttk.Spinbox(play_frame, from_=0, to=3, width=5, textvariable=self.player_var)
        player_spin.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(play_frame, text="Record", command=self.record_play).pack(side=tk.LEFT)
        
        ends_frame = ttk.Frame(self.action_frame)
        ends_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(ends_frame, text="Board ends:").pack(side=tk.LEFT)
        self.ends_entry = ttk.Entry(ends_frame, width=10)
        self.ends_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(ends_frame, text="Get Suggestion", command=self.get_suggestion).pack(side=tk.LEFT)

    def create_analysis_section(self):
        """Create analysis display section."""
        self.analysis_text = tk.Text(self.analysis_frame, height=10, width=50)
        self.analysis_text.pack(fill=tk.BOTH, expand=True)
        
        button_frame = ttk.Frame(self.analysis_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="Analyze Hand", command=self.show_analysis).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Endgame Strategy", command=self.show_endgame).pack(side=tk.LEFT)

    def add_tile(self):
        """Add a tile to the hand."""
        try:
            tile = DominoTile.from_string(self.tile_entry.get())
            self.assistant.add_tiles([tile])
            self.tile_entry.delete(0, tk.END)
            self.set_status(f"Added tile {tile}")
            self.show_analysis()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def clear_hand(self):
        """Clear all tiles from hand."""
        self.assistant.my_tiles = []
        self.set_status("Hand cleared")
        self.show_analysis()

    def record_play(self):
        """Record a played tile."""
        try:
            tile = DominoTile.from_string(self.play_entry.get())
            player = int(self.player_var.get())
            
            if player == 0:
                self.assistant.remove_tile(tile)
            else:
                self.assistant.update_game_state(tile, player)
                
            self.play_entry.delete(0, tk.END)
            self.set_status(f"Recorded play: {tile} by player {player}")
            self.show_analysis()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def get_suggestion(self):
        """Get and display play suggestion."""
        try:
            ends = [int(x) for x in self.ends_entry.get().split(',')]
            suggestion = self.assistant.suggest_play(ends)
            if suggestion:
                self.analysis_text.delete(1.0, tk.END)
                self.analysis_text.insert(tk.END, f"Suggested play for ends {ends}:\n{suggestion}")
                self.set_status("Generated play suggestion")
            else:
                self.set_status("No valid plays available")
        except ValueError as e:
            messagebox.showerror("Error", "Invalid board ends format. Use format: 6,4")

    def show_analysis(self):
        """Display current hand analysis."""
        analysis = self.assistant.analyze_hand()
        
        self.analysis_text.delete(1.0, tk.END)
        self.analysis_text.insert(tk.END, "Current Hand Analysis\n")
        self.analysis_text.insert(tk.END, "=" * 30 + "\n\n")
        self.analysis_text.insert(tk.END, f"Current tiles: {self.assistant.my_tiles}\n\n")
        self.analysis_text.insert(tk.END, f"Strong numbers: {analysis['strong_numbers']}\n")
        self.analysis_text.insert(tk.END, f"Weak numbers: {analysis['weak_numbers']}\n")
        self.analysis_text.insert(tk.END, f"Doubles: {analysis['doubles']}\n")
        self.analysis_text.insert(tk.END, f"Scoring potential: {analysis['scoring_potential']}\n")
        
        self.set_status("Updated analysis")

    def show_endgame(self):
        """Display endgame strategy."""
        strategy = self.assistant.get_endgame_strategy()
        self.analysis_text.delete(1.0, tk.END)
        self.analysis_text.insert(tk.END, "Endgame Strategy\n")
        self.analysis_text.insert(tk.END, "=" * 30 + "\n\n")
        self.analysis_text.insert(tk.END, strategy)
        self.set_status("Displayed endgame strategy")

    def set_status(self, message: str):
        """Update status bar message."""
        self.status_var.set(message)

def main():
    """Initialize and run the application."""
    root = tk.Tk()
    root.geometry("600x500")
    
    # Set app style
    style = ttk.Style()
    style.theme_use('clam')  # You can try 'default', 'alt', 'classic', or 'clam'
    
    # Configure colors and styles
    style.configure('TLabel', padding=2)
    style.configure('TButton', padding=2)
    style.configure('TLabelframe', padding=5)
    
    app = DominoAssistantGUI(root)
    
    # Center the window on the screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'+{x}+{y}')

    # Add keyboard shortcuts
    root.bind('<Return>', lambda e: app.add_tile())
    root.bind('<Control-a>', lambda e: app.show_analysis())
    root.bind('<Control-e>', lambda e: app.show_endgame())
    root.bind('<Control-s>', lambda e: app.get_suggestion())
    root.bind('<Escape>', lambda e: app.clear_hand())
    
    root.mainloop()

if __name__ == "__main__":
    main()