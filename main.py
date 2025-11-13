import pygame
import sys

# --- Constants ---
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 750
FPS = 60

# Colors
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GRAY = (128, 128, 128)
COLOR_DARK_GRAY = (50, 50, 50)
COLOR_ALIEN_GREEN = (124, 252, 0)

# --- Class Data ---
CLASS_INFO = {
    "Assault": [
        "High Damage",
        "",
        "Strike: 20 dmg",
        "Slash: Self dmg, high enemy dmg",
        "Concussive: Stun stacking",
        "Charged: Skip turn, huge dmg"
    ],
    "Sentinel": [
        "Tank / Defense",
        "",
        "Defend: Absorb/Reflect dmg",
        "Shield: Gain Shield",
        "Cover: Shield Team",
        "Slam: Dmg based on shield"
    ],
    "Specialist": [
        "Support / Healer",
        "",
        "Debuff: Reduce enemy atk",
        "Buff: Increase ally atk",
        "Freeze: Stun enemy",
        "Heal: Restore ally HP"
    ]
}

# Class Selection Buttons (3 Columns)
assault_button = pygame.Rect(50, 150, 280, 500)
sentinel_button = pygame.Rect(360, 150, 280, 500)
specialist_button = pygame.Rect(670, 150, 280, 500)

# --- Help Text (Formatted into pages) ---
# Each page is a list of strings. Each string is a line.
HELP_PAGES = [
    # Page 1: Title & Abstract
    [
        "--- AGHHH ALIENS! ---",
        "",
        "Abstract:",
        "Two space cadets had their spaceship invaded by aliens.",
        "Their goal is to get to the opposite end of their ship",
        "where the alien queen resides so they can gain control",
        "of the ship again.",
        "",
        "Players: Two-Player cooperative game",
    ],
    # Page 2: Core Rules
    [
        "--- Core Rules ---",
        "",
        "Roll a six-sided die to move across a board of 68 tiles.",
        "Every time a die is rolled, an enemy encounter begins.",
        "A random enemy card is chosen, and players must fight.",
        "",
        "After an enemy is defeated, each player rolls a die for an item:",
        "  1-3: No item",
        "  4-6: Get item",
        "",
        "Reach the 68th tile for the final encounter with the Alien Queen.",
        "Defeat her to win the game.",
    ],
    # Page 3: Player Resources
    [
        "--- Player Resources ---",
        "",
        "Health Points (HP): 75 Total (Red Tokens)",
        "  When it runs out, the player dies.",
        "",
        "Armor Points (AP): (Blue Tokens)",
        "  Additional health given by abilities.",
        "",
        "Skill Points (SP): Start with 5, Max 10.",
        "  Attacks cost SP. Regain 2 SP at the start of your turn.",
    ],
    # Page 4: Rest Points & Alien Resources
    [
        "--- Rest & Aliens ---",
        "",
        "Rest Points:",
        "  Every 11 tiles. Both players regain all health.",
        "  Revives a downed teammate with 50% health.",
        "  Every 2 rests, aliens get 50% more health.",
        "",
        "Alien Resources:",
        "  Health Points (HP): When it runs out, the alien dies.",
        "  Enemy Moves (Dice Roll):",
        "    1-3: Basic Attack",
        "    4-5: Heavy Attack",
        "    6: Special Attack",
        "  (Another roll determines which player is attacked)",
    ],
    # Page 5: Class - Assault
    [
        "--- Class: Assault (Damage) ---",
        "",
        "Strike (1 SP): Deal 20 damage.",
        "Barbaric Slash (2 SP): Take 10 damage, Deal 30 damage.",
        "Concussive Strike (3 SP): Deal 7 damage. +3 damage",
        "  if used consecutively. Stuns after 9 damage increase.",
        "Charged Punch (6 SP): Skips turn. Next cast deals 50 damage.",
    ],
    # Page 6: Class - Sentinel
    [
        "--- Class: Sentinel (Defense) ---",
        "",
        "Defend (1 SP): Absorb teammate's damage, reflect 50%.",
        "Shield (2 SP): Gain 25 shield.",
        "Cover (3 SP): Give 10 shield to the team.",
        "Slam (5 SP): Removes all shield, deals 45 damage,",
        "  and removes stun from all enemies.",
    ],
    # Page 7: Class - Specialist
    [
        "--- Class: Specialist (Support) ---",
        "",
        "Debuff (1 SP): Deal 10 damage, reduce enemy attack by 10.",
        "Buff (1 SP): Increase ally attack by 15.",
        "Freeze (1 SP): Stun an enemy for 1 turn.",
        "Heal (1 SP): Heal an ally by 15 HP.",
    ],
    # Page 8: Alien Types
    [
        "--- Alien Types (Base HP) ---",
        "",
        "Goliath (120 HP):",
        "  Basic: -10, Heavy: -25, Special: -45 Fire Breath",
        "Kraken (100 HP):",
        "  Basic: -10, Heavy: -25, Special: -45 Lightning Strike",
        "Wraith (90 HP):",
        "  Basic: -10, Heavy: -25, Special: -45 Teleport Abduct",
        "Xenomorph (80 HP):",
        "  Basic: -10, Heavy: -25, Special: -45 Acid Bleed",
        "Alien Queen (200 HP):",
        "  Basic: -20, Heavy: -35, Special: -60 Group Attack",
        "  (Summons Xenomorph after 3 attacks)",
    ],
    # Page 9: Items
    [
        "--- Items (Level up on duplicate) ---",
        "",
        "Item 1: Add Burn damage (5) to attacks costing 5+ SP.",
        "  (Lvl+: +5 burn damage)",
        "",
        "Item 2: Reflect damage when shielded.",
        "  (Lvl+: +25% damage reflected)",
        "",
        "Item 3: Stun attacks now deal 30 instant damage.",
        "  (Lvl+: +15 damage)",
        "",
        "Item 4: Deal 10 less damage, gain 25 max HP.",
        "  (Lvl+: +5 max HP, -1 less damage)",
    ]
]


# --- Main Game Function ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("AGHHH ALIENS!!!")
    clock = pygame.time.Clock()

    title_font = pygame.font.SysFont('Arial', 72)
    button_font = pygame.font.SysFont('Arial', 40)
    
    game_state = "main_menu"
    help_page_index = 0
    
    # --- NEW: Track Player Classes ---
    p1_class = None
    p2_class = None

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Update to unpack 4 return values
                    game_state, help_page_index, p1_class, p2_class = handle_menu_clicks(
                        event.pos, game_state, help_page_index, p1_class, p2_class
                    )

        if game_state == "main_menu":
            draw_main_menu(screen, title_font, button_font)
        elif game_state == "class_select":
            # Pass class info so we know what to draw
            draw_class_select(screen, title_font, p1_class, p2_class)
        elif game_state == "game_board":
            draw_game_board(screen, title_font)
        elif game_state == "help":
            draw_help(screen, title_font, button_font, help_page_index)
        elif game_state == "settings":
            draw_settings(screen, title_font)
        elif game_state == "about":
            draw_about(screen, title_font)
        
        pygame.display.flip()
        clock.tick(FPS)

# --- Click Handling ---

# Define our button rectangles. We define them here so we can check
# against them in the click handler.
# (x, y, width, height)
start_button = pygame.Rect(350, 250, 300, 60)
help_button = pygame.Rect(350, 330, 300, 60)
settings_button = pygame.Rect(350, 410, 300, 60)
about_button = pygame.Rect(350, 490, 300, 60)

# A 'back' button for all our sub-menus
back_button = pygame.Rect(20, 20, 150, 50)

# Help screen pagination buttons
prev_page_button = pygame.Rect(250, 680, 200, 50)
next_page_button = pygame.Rect(550, 680, 200, 50)


def handle_menu_clicks(mouse_pos, current_state, help_page_index, p1_class, p2_class):
    """
    Returns: (new_state, new_help_page, new_p1_class, new_p2_class)
    """
    
    # --- Main Menu ---
    if current_state == "main_menu":
        if start_button.collidepoint(mouse_pos):
            # Reset classes when starting new game
            return "class_select", help_page_index, None, None
        if help_button.collidepoint(mouse_pos):
            return "help", 0, p1_class, p2_class
        if settings_button.collidepoint(mouse_pos):
            return "settings", help_page_index, p1_class, p2_class
        if about_button.collidepoint(mouse_pos):
            return "about", help_page_index, p1_class, p2_class

    # --- Back Button Logic ---
    elif current_state in ["help", "settings", "about", "class_select"]:
        if back_button.collidepoint(mouse_pos):
            return "main_menu", help_page_index, p1_class, p2_class

    # --- Class Selection Logic ---
    if current_state == "class_select":
        selected = None
        if assault_button.collidepoint(mouse_pos):
            selected = "Assault"
        elif sentinel_button.collidepoint(mouse_pos):
            selected = "Sentinel"
        elif specialist_button.collidepoint(mouse_pos):
            selected = "Specialist"
            
        if selected:
            # If Player 1 hasn't picked yet
            if p1_class is None:
                print(f"Player 1 chose {selected}")
                return current_state, help_page_index, selected, None
            
            # If Player 1 has picked, but Player 2 hasn't
            elif p2_class is None:
                # Constraint: P2 cannot pick the same class as P1
                if selected != p1_class:
                    print(f"Player 2 chose {selected}")
                    # Both picked! Go to game board
                    return "game_board", help_page_index, p1_class, selected
                else:
                    print("Class already taken!")

    # --- Help Screen Logic ---
    if current_state == "help":
        if next_page_button.collidepoint(mouse_pos) and help_page_index < len(HELP_PAGES) - 1:
            return current_state, help_page_index + 1, p1_class, p2_class
        if prev_page_button.collidepoint(mouse_pos) and help_page_index > 0:
            return current_state, help_page_index - 1, p1_class, p2_class

    # Default return (no change)
    return current_state, help_page_index, p1_class, p2_class


# --- Drawing Functions (one for each game state) ---

def draw_text(screen, text, font, color, rect, center=True):
    """A helper function to draw text on a surface."""
    text_surface = font.render(text, True, color)
    if center:
        text_rect = text_surface.get_rect(center=rect.center)
    else:
        text_rect = text_surface.get_rect(topleft=rect.topleft)
        text_rect.x += 10 # Add padding
    screen.blit(text_surface, text_rect)

def draw_text_block(screen, text_lines, font, color, rect):
    """
    Draws multiple lines of text, left-aligned, starting at the 
    top-left of the given rect.
    """
    y = rect.y
    line_spacing = font.get_linesize() + 5 # 5 pixels of space between lines

    for line in text_lines:
        text_surface = font.render(line, True, color)
        # Use rect.x for the x-coordinate
        screen.blit(text_surface, (rect.x, y))
        y += line_spacing # Move y down for the next line

def draw_main_menu(screen, title_font, button_font):
    """Draws the main menu screen."""
    screen.fill(COLOR_BLACK)
    
    # Draw Title
    title_rect = pygame.Rect(0, 100, SCREEN_WIDTH, 100)
    draw_text(screen, "AGHHH ALIENS!!!", title_font, COLOR_ALIEN_GREEN, title_rect)

    # Draw Buttons (Rectangle and Text)
    pygame.draw.rect(screen, COLOR_DARK_GRAY, start_button, border_radius=10)
    draw_text(screen, "Start Game", button_font, COLOR_WHITE, start_button)
    
    pygame.draw.rect(screen, COLOR_DARK_GRAY, help_button, border_radius=10)
    draw_text(screen, "Help / Rules", button_font, COLOR_WHITE, help_button)

    pygame.draw.rect(screen, COLOR_DARK_GRAY, settings_button, border_radius=10)
    draw_text(screen, "Settings", button_font, COLOR_WHITE, settings_button)

    pygame.draw.rect(screen, COLOR_DARK_GRAY, about_button, border_radius=10)
    draw_text(screen, "About", button_font, COLOR_WHITE, about_button)

def draw_simple_screen(screen, title_font, text):
    """Helper for drawing placeholder screens."""
    screen.fill(COLOR_BLACK)
    
    # Draw Back Button
    pygame.draw.rect(screen, COLOR_DARK_GRAY, back_button, border_radius=10)
    draw_text(screen, "< Back", pygame.font.SysFont('Arial', 30), COLOR_WHITE, back_button)

    # Draw placeholder text
    text_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
    draw_text(screen, text, title_font, COLOR_WHITE, text_rect)

# --- Screen Drawing Functions ---

def draw_help(screen, title_font, button_font, page_index):
    """Draws the help/rules screen with pagination."""
    
    # Use a smaller font for the rules text
    rules_font = pygame.font.SysFont('Arial', 24)
    
    screen.fill(COLOR_BLACK)
    
    # --- Draw Back Button ---
    pygame.draw.rect(screen, COLOR_DARK_GRAY, back_button, border_radius=10)
    draw_text(screen, "< Back", pygame.font.SysFont('Arial', 30), COLOR_WHITE, back_button)

    # --- Draw Page Title ---
    title_rect = pygame.Rect(0, 50, SCREEN_WIDTH, 80)
    draw_text(screen, "Help / Instructions", title_font, COLOR_WHITE, title_rect)
    
    # --- Draw Page Number ---
    page_num_text = f"Page {page_index + 1} of {len(HELP_PAGES)}"
    page_num_rect = pygame.Rect(0, 680, 1000, 50) # Positioned near buttons
    draw_text(screen, page_num_text, rules_font, COLOR_GRAY, page_num_rect)

    # --- Draw the Rule Text for the Current Page ---
    # Define the area where the text will be drawn
    text_block_rect = pygame.Rect(100, 150, 800, 500)
    
    # Get the current page of text
    current_page_lines = HELP_PAGES[page_index]
    
    # Draw the block of text
    draw_text_block(screen, current_page_lines, rules_font, COLOR_WHITE, text_block_rect)

    # --- Draw Pagination Buttons ---
    # Only draw "Previous" if not on page 0
    if page_index > 0:
        pygame.draw.rect(screen, COLOR_DARK_GRAY, prev_page_button, border_radius=10)
        draw_text(screen, "Previous", button_font, COLOR_WHITE, prev_page_button)
    
    # Only draw "Next" if not on the last page
    if page_index < len(HELP_PAGES) - 1:
        pygame.draw.rect(screen, COLOR_DARK_GRAY, next_page_button, border_radius=10)
        draw_text(screen, "Next", button_font, COLOR_WHITE, next_page_button)

# --- Placeholder Screen Functions ---
# We'll fill these in later!

def draw_class_select(screen, title_font, p1_class, p2_class):
    screen.fill(COLOR_BLACK)
    
    # Draw Back Button
    pygame.draw.rect(screen, COLOR_DARK_GRAY, back_button, border_radius=10)
    draw_text(screen, "< Back", pygame.font.SysFont('Arial', 30), COLOR_WHITE, back_button)

    # Determine Header Text
    header_text = "Player 1: Choose your Class"
    if p1_class is not None:
        header_text = "Player 2: Choose your Class"
    
    # Draw Header
    header_rect = pygame.Rect(0, 20, SCREEN_WIDTH, 100)
    draw_text(screen, header_text, pygame.font.SysFont('Arial', 50), COLOR_WHITE, header_rect)

    # Helper to draw a single class card
    def draw_card(rect, name, color):
        # Check if this card is already taken by Player 1
        is_taken = (name == p1_class)
        
        # Background color (Grey out if taken)
        bg_color = COLOR_DARK_GRAY if is_taken else color
        
        pygame.draw.rect(screen, bg_color, rect, border_radius=15)
        
        # If taken, draw a big "TAKEN" text or cross
        if is_taken:
            draw_text(screen, "TAKEN", title_font, (255, 0, 0), rect)
        else:
            # Draw Name
            name_rect = pygame.Rect(rect.x, rect.y + 20, rect.width, 50)
            draw_text(screen, name, pygame.font.SysFont('Arial', 40), COLOR_BLACK, name_rect)
            
            # Draw Stats/Info
            stats = CLASS_INFO[name]
            text_block_rect = pygame.Rect(rect.x + 20, rect.y + 100, rect.width - 40, rect.height - 100)
            draw_text_block(screen, stats, pygame.font.SysFont('Arial', 24), COLOR_BLACK, text_block_rect)

    # Draw the 3 cards
    # We use different colors for visual flair
    draw_card(assault_button, "Assault", (255, 100, 100))    # Red-ish
    draw_card(sentinel_button, "Sentinel", (100, 100, 255))  # Blue-ish
    draw_card(specialist_button, "Specialist", (100, 255, 100)) # Green-ish

def draw_game_board(screen, title_font):
    draw_simple_screen(screen, title_font, "Game Board Screen")

def draw_settings(screen, title_font):
    # This is the "empty" settings page
    draw_simple_screen(screen, title_font, "Settings Screen (Empty)")

def draw_about(screen, title_font):
    draw_simple_screen(screen, title_font, "About Screen")


# --- Run the Game ---
if __name__ == "__main__":
    main()