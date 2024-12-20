# domino-assistant

# Domino Game Assistant

A Python-based strategic assistant for playing dominoes with a full-featured graphical user interface. This tool helps players make optimal decisions during domino games by providing real-time analysis, move suggestions, and strategic insights.

## Features

### Core Game Analysis
- Hand composition analysis
- Probability calculations for opponent tiles
- Strategic move suggestions
- Endgame strategy recommendations
- Player pattern tracking
- Comprehensive game state management

### GUI Features
- Intuitive graphical interface
- Real-time hand management
- Interactive game state tracking
- Visual analysis display
- Status feedback system
- Error handling with user-friendly messages

### Keyboard Shortcuts
- `Enter`: Add tile to hand
- `Ctrl + A`: Show hand analysis
- `Ctrl + E`: Show endgame strategy
- `Ctrl + S`: Get move suggestion
- `Escape`: Clear current hand

## Installation

### Requirements
- Python 3.6 or higher
- tkinter (usually comes with Python installation)

### Setup
1. Clone the repository or download the script:
```bash
git clone [repository-url]
cd domino-assistant
```

2. Run the application:
```bash
python domino_assistant.py
```

## Usage Guide

### Hand Management
1. **Adding Tiles**
   - Enter tile in format "3-4" or "3,4" in the tile input field
   - Click "Add" or press Enter
   - Status bar will confirm addition

2. **Clearing Hand**
   - Click "Clear Hand" button or press Escape
   - All tiles will be removed from current hand

### Game Actions
1. **Recording Plays**
   - Enter played tile in "Record play" field
   - Select player number (0 for you, 1-3 for opponents)
   - Click "Record" to log the play
   
2. **Getting Suggestions**
   - Enter current board ends (e.g., "6,4")
   - Click "Get Suggestion" or press Ctrl+S
   - System will analyze and suggest optimal play

### Analysis Tools
1. **Hand Analysis (Ctrl+A)**
   - Shows current tiles
   - Lists strong numbers (multiple tiles)
   - Lists weak numbers (single tiles)
   - Shows doubles in hand
   - Displays scoring potential

2. **Endgame Strategy (Ctrl+E)**
   - Provides strategic advice based on game state
   - Shows unplayed numbers
   - Suggests focus areas (blocking vs. point minimization)

### Status Feedback
- Real-time status updates in status bar
- Error messages for invalid inputs
- Confirmation of successful actions
- Game state updates

## Strategy Implementation

The assistant uses a sophisticated scoring system for move suggestions:

1. **Number Frequency Analysis**
   - Tracks frequency of each number (0-6)
   - Identifies strong and weak numbers in hand
   - Considers opponent's likely holdings

2. **Positional Strategy**
   - Early game: Focuses on establishing strong positions
   - Mid game: Balances blocking and point accumulation
   - End game: Adapts to remaining tiles and opponent patterns

3. **Scoring Criteria**
   - Multiple number preference
   - Double tile timing
   - Hand flexibility maintenance
   - Opponent blocking opportunities

4. **Endgame Optimization**
   - Tracks unplayed numbers
   - Adjusts strategy based on remaining hand size
   - Focuses on either blocking or point minimization

## Input Formats

1. **Tile Format**
   - Use either hyphen (-) or comma (,) as separator
   - Examples: "3-4" or "3,4"
   - Values must be between 0 and 6

2. **Board Ends**
   - Comma-separated values
   - Example: "6,4"
   - Represents both playable ends of the domino line

## Error Handling

The system includes comprehensive error handling for:
- Invalid tile formats
- Out-of-range values
- Invalid board positions
- Impossible game states
- Input validation with user-friendly error messages

## Contributing

Contributions are welcome! Areas for potential enhancement:
- Network play support
- Game history tracking
- Statistical analysis features
- AI opponent mode
- Advanced visualization options
- Support for variant game rules

## Future Enhancements

Planned features:
- Game state persistence
- Multiple hand comparison
- Advanced probability modeling
- Pattern recognition improvements
- Tournament mode support
- Custom rule sets

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, questions, or suggestions:
1. Open an issue in the repository
2. Contact the maintainers
3. Check the documentation for updates

## Version History

### Current Version: 1.0.0
- Full GUI implementation
- Keyboard shortcuts
- Real-time analysis
- Status feedback system
- Error handling

---
