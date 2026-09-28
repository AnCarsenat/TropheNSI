"""ANSI/ASCII terminal colour escape codes."""
# WRITTEN BY CHATGPT
# As idk all color codes and this is manual stupid copy paste job :p

# Reset and text styles.
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
ITALIC = "\033[3m"
UNDERLINE = "\033[4m"
BLINK = "\033[5m"
REVERSE = "\033[7m"
HIDDEN = "\033[8m"
STRIKETHROUGH = "\033[9m"

# Standard foreground colours (30-37).
BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"

# Standard background colours (40-47).
BG_BLACK = "\033[40m"
BG_RED = "\033[41m"
BG_GREEN = "\033[42m"
BG_YELLOW = "\033[43m"
BG_BLUE = "\033[44m"
BG_MAGENTA = "\033[45m"
BG_CYAN = "\033[46m"
BG_WHITE = "\033[47m"

# Bright foreground colours (90-97).
BRIGHT_BLACK = "\033[90m"
BRIGHT_RED = "\033[91m"
BRIGHT_GREEN = "\033[92m"
BRIGHT_YELLOW = "\033[93m"
BRIGHT_BLUE = "\033[94m"
BRIGHT_MAGENTA = "\033[95m"
BRIGHT_CYAN = "\033[96m"
BRIGHT_WHITE = "\033[97m"

# Bright background colours (100-107).
BG_BRIGHT_BLACK = "\033[100m"
BG_BRIGHT_RED = "\033[101m"
BG_BRIGHT_GREEN = "\033[102m"
BG_BRIGHT_YELLOW = "\033[103m"
BG_BRIGHT_BLUE = "\033[104m"
BG_BRIGHT_MAGENTA = "\033[105m"
BG_BRIGHT_CYAN = "\033[106m"
BG_BRIGHT_WHITE = "\033[107m"

class colors:
	RESET = RESET
	BOLD = BOLD
	DIM = DIM
	ITALIC = ITALIC
	UNDERLINE = UNDERLINE
	BLINK = BLINK
	REVERSE = REVERSE
	HIDDEN = HIDDEN
	STRIKETHROUGH = STRIKETHROUGH

	BLACK = BLACK
	RED = RED
	GREEN = GREEN
	YELLOW = YELLOW
	BLUE = BLUE
	MAGENTA = MAGENTA
	CYAN = CYAN
	WHITE = WHITE

	BG_BLACK = BG_BLACK
	BG_RED = BG_RED
	BG_GREEN = BG_GREEN
	BG_YELLOW = BG_YELLOW
	BG_BLUE = BG_BLUE
	BG_MAGENTA = BG_MAGENTA
	BG_CYAN = BG_CYAN
	BG_WHITE = BG_WHITE

	BRIGHT_BLACK = BRIGHT_BLACK
	BRIGHT_RED = BRIGHT_RED
	BRIGHT_GREEN = BRIGHT_GREEN
	BRIGHT_YELLOW = BRIGHT_YELLOW
	BRIGHT_BLUE = BRIGHT_BLUE
	BRIGHT_MAGENTA = BRIGHT_MAGENTA
	BRIGHT_CYAN = BRIGHT_CYAN
	BRIGHT_WHITE = BRIGHT_WHITE

	BG_BRIGHT_BLACK = BG_BRIGHT_BLACK
	BG_BRIGHT_RED = BG_BRIGHT_RED
	BG_BRIGHT_GREEN = BG_BRIGHT_GREEN
	BG_BRIGHT_YELLOW = BG_BRIGHT_YELLOW
	BG_BRIGHT_BLUE = BG_BRIGHT_BLUE
	BG_BRIGHT_MAGENTA = BG_BRIGHT_MAGENTA
	BG_BRIGHT_CYAN = BG_BRIGHT_CYAN
	BG_BRIGHT_WHITE = BG_BRIGHT_WHITE


def foreground(color: int) -> str:
	"""Return the ANSI code for a 256-colour foreground (0-255)."""
	if not 0 <= color <= 255:
		raise ValueError("colour must be between 0 and 255")
	return f"\033[38;5;{color}m"


def background(color: int) -> str:
	"""Return the ANSI code for a 256-colour background (0-255)."""
	if not 0 <= color <= 255:
		raise ValueError("colour must be between 0 and 255")
	return f"\033[48;5;{color}m"


def rgb(red: int, green: int, blue: int, *, background_color: bool = False) -> str:
	"""Return an ANSI true-colour code for an RGB value."""
	if not all(0 <= value <= 255 for value in (red, green, blue)):
		raise ValueError("RGB values must be between 0 and 255")
	mode = 48 if background_color else 38
	return f"\033[{mode};2;{red};{green};{blue}m"
