# Fol Dhorar Mojar Khela (Fruit Catching Game)
## Documentation

### Overview
Fol Dhorar Mojar Khela is a PyGame-based arcade game where players control a basket to catch falling fruits while avoiding harmful objects. The game features dynamic backgrounds, multiple difficulty levels, and an engaging scoring system.

### Technical Specifications
- **Language:** Python 3.x
- **Framework:** Pygame
- **Resolution:** 800x800 pixels
- **Frame Rate:** 30 FPS

### Game Components

#### 1. Game Objects
- **Basket:** Player-controlled collector (150x100 pixels)
- **Fruits:** Collectible items (70x70 pixels)
- **Bugs:** Harmful objects (70x70 pixels)
- **Bombs:** Highly dangerous objects (50x50 pixels, appears in Medium and Hard modes)

#### 2. Game Mechanics
- **Movement:** Left/Right arrow keys control basket movement
- **Health System:** 
  - Starting health: 100 points
  - Bug collision: -20 health
  - Bomb collision: -50 health
- **Scoring:**
  - +1 point per fruit caught
  - Score saved as high score if it exceeds previous record

#### 3. Difficulty Levels
1. **Easy (Level 1)**
   - Initial fruit speed: 10
   - Initial bomb speed: 10
   - Initial bug speed: 5
   - No bombs

2. **Medium (Level 2)**
   - Initial fruit speed: 15
   - Initial bomb speed: 15
   - Initial bug speed: 15
   - Includes bombs

3. **Hard (Level 3)**
   - Initial fruit speed: 20
   - Initial bomb speed: 20
   - Initial bug speed: 20
   - Includes bombs

#### 4. Dynamic Elements
- **Background Cycle:**
  - Changes every 15 seconds
  - Cycles through: Morning, Day, Evening, Night
- **Progressive Difficulty:**
  - Fruit speed increases by 0.5 after each catch

### Asset Requirements

#### Images
1. **Fruits:** `fruit1.png` to `fruit9.png`
2. **Bugs:** `bug0.png` to `bug5.png`
3. **Backgrounds:**
   - `Dupur.jpg` (Day)
   - `Shokal.jpg` (Morning)
   - `Rat.jpg` (Night)
   - `Bikal.jpg` (Evening)
   - `bg_front.jpg` (Menu)
   - `bg_ending.jpg` (Game Over)
4. **Other:**
   - `basket.png`
   - `bomb.png`

#### Sound Effects
Located in `Assets/mp3/`:
- `bg_music.mp3`: Background music
- `menu_music.mp3`: Menu screen music
- `fruit_se.mp3`: Fruit collection sound
- `bug_se.mp3`: Bug collision sound
- `bomb.mp3`: Bomb collision sound
- `levelUp.mp3`: Level advancement sound

### Game States
1. **Dashboard (Menu)**
   - Displays difficulty selection
   - Controls: Keys 1-3 for level selection

2. **Active Gameplay**
   - Displays score and health bar
   - Dynamic background changes
   - Active game elements

3. **Game Over**
   - Displays final score and high score
   - Option to restart (Press 'R')

### File Management
- High scores stored in `high_score.txt`
- Automatic save/load of high scores

### Controls Summary
- **Left Arrow:** Move basket left
- **Right Arrow:** Move basket right
- **R:** Restart game (when game over)
- **1, 2, 3:** Select difficulty level (in menu)

### Error Handling
- Graceful handling of missing asset files
- Error messages for failed sound/image loading

This documentation provides a comprehensive overview of the game's functionality, requirements, and implementation details. It serves as a reference for both users and developers working with the codebase.