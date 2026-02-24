import time
import os
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")
    
logo1 = [
"   ______",
"  / ____/",
" / /",
"/ /___",
"\\____/"
]
logo2 = [
"   ______",
"  / ____/___ _",
" / /   / __ `/",
"/ /___/ /_/ /",
"\\____/\\__,_/"
]
logo3 = [
"   ______      __",
"  / ____/___ _/ /",
" / /   / __ `/ /",
"/ /___/ /_/ / /",
"\\____/\\__,_/_/"
]
logo4 = [
"   ______      __",
"  / ____/___ _/ /____",
" / /   / __ `/ / ___/",
"/ /___/ /_/ / / /__",
"\\____/\\__,_/_/\\___/"
]
logo5 = [
"   ______      __",
"  / ____/___ _/ /______  __",
" / /   / __ `/ / ___/ / / /",
"/ /___/ /_/ / / /__/ /_/ /",
"\\____/\\__,_/_/\\___/\\__,_/"
]
logo6 = [
"   ______      __           __",
"  / ____/___ _/ /______  __/ /",
" / /   / __ `/ / ___/ / / / /",
"/ /___/ /_/ / / /__/ /_/ / /",
"\\____/\\__,_/_/\\___/\\__,_/_/"
]
logo7 = [
"   ______      __           __",
"  / ____/___ _/ /______  __/ /___ _",
" / /   / __ `/ / ___/ / / / / __ `/",
"/ /___/ /_/ / / /__/ /_/ / / /_/ /",
"\\____/\\__,_/_/\\___/\\__,_/_/\\__,_/"
]
logo8 = [
"   ______      __           __      __",
"  / ____/___ _/ /______  __/ /___ _/ /_",
" / /   / __ `/ / ___/ / / / / __ `/ __/",
"/ /___/ /_/ / / /__/ /_/ / / /_/ / /_",
"\\____/\\__,_/_/\\___/\\__,_/_/\\__,_/\\__/"
]
logo9 = [
"   ______      __           __      __",
"  / ____/___ _/ /______  __/ /___ _/ /_____",
" / /   / __ `/ / ___/ / / / / __ `/ __/ __ \\",
"/ /___/ /_/ / / /__/ /_/ / / /_/ / /_/ /_/ /",
"\\____/\\__,_/_/\\___/\\__,_/_/\\__,_/\\__/\\____/"
]
logo10 = [
"   ______      __           __      __            ",
"  / ____/___ _/ /______  __/ /___ _/ /_____  _____",
" / /   / __ `/ / ___/ / / / / __ `/ __/ __ \\/ ___/",
"/ /___/ /_/ / / /__/ /_/ / / /_/ / /_/ /_/ / /    ",
"\\____/\\__,_/_/\\___/\\__,_/_/\\__,_/\\__/\\____/_/     "
]

for i in range(11):
    if i == 0:
        time.sleep(1)
        pass
    else:
        for b in range(5):
            if i == 1:
                print(logo1[b])
            elif i == 2:
                print(logo2[b])
            elif i == 3:
                print(logo3[b])
            elif i == 4:
                print(logo4[b])
            elif i == 5:
                print(logo5[b])
            elif i == 6:
                print(logo6[b])
            elif i == 7:
                print(logo7[b])
            elif i == 8:
                print(logo8[b])
            elif i == 9:
                print(logo9[b])
            elif i == 10:
                print(logo10[b])
        time.sleep(0.1)
        clear_screen()
#!/usr/bin/python3
import os
import time
import sys

# -------------------------------------------------------
# ANSI Colors (no install needed)
# -------------------------------------------------------
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"
RESET = "\033[0m"
BOLD = "\033[1m"

# -------------------------------------------------------
# Clear screen
# -------------------------------------------------------
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

# -------------------------------------------------------
# Animated ASCII logo (pure Python)
# -------------------------------------------------------
logo = [
"   ______      __           __      __            ",
"  / ____/___ _/ /______  __/ /___ _/ /_____  _____",
" / /   / __ `/ / ___/ / / / / __ `/ __/ __ \\/ ___/",
"/ /___/ /_/ / / /__/ /_/ / / /_/ / /_/ /_/ / /    ",
"\\____/\\__,_/_/\\___/\\__,_/_/\\__,_/\\__/\\____/_/     "
]

def animate_logo():
    for line in logo:
        print(CYAN + line + RESET)
        time.sleep(0.12)

# -------------------------------------------------------
# Safe multi-operation evaluator
# (Only + - * / // % ** () allowed)
# -------------------------------------------------------
def safe_eval(expr):
    allowed = "0123456789+-*/().% "
    for char in expr:
        if char not in allowed:
            raise ValueError("Invalid character")

    expr = expr.replace(" ", "")
    return eval(expr)

# -------------------------------------------------------
# Main Program
# -------------------------------------------------------
history = []

while True:
    clear_screen()
    animate_logo()
    print()

    print(BOLD + YELLOW + "Enter expression (example: 2+3*4). Press E to exit." + RESET)
    print(BOLD + CYAN + "History saved → max 8 items.\n" + RESET)

    # show history
    if history:
        print(GREEN + "Previous results:" + RESET)
        for h in history:
            print("   " + CYAN + h + RESET)
        print()

    expr = input(BOLD + "Calculate = " + RESET)

    if expr.lower() == "e":
        clear_screen()
        print(RED + "Bye Prime!" + RESET)
        sys.exit(0)

    try:
        result = safe_eval(expr)
        out = f"{expr} = {result}"
        print(GREEN + BOLD + out + RESET)
        history.append(out)
        if len(history) > 8:
            history.pop(0)

    except ZeroDivisionError:
        print(RED + "Error: Division by zero." + RESET)

    except Exception:
        print(RED + "Error: Invalid expression." + RESET)

    print("\n" + MAGENTA + "Press ENTER to continue..." + RESET)
    input()


        
            

