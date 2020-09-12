import pyautogui
from ahk import AHK
import time

ahk = AHK()

print(f"Active window: {ahk.active_window}")
print(f"Position: {ahk.active_window.rect}")
print(f"Title: {ahk.active_window.title}")
print(f"Windows: {ahk.windows()}")
# ahk.active_window.title = "Bashash"
# time.sleep(0.5)
# ahk.active_window.hide()
# time.sleep(0.5)
# ahk.active_window.show()
for w in ahk.windows():
	if b"bash" in w.title:
		w.restore()
ahk.mouse_move(x=100, y=100, blocking=True)  # Blocks until mouse finishes moving (the default)
ahk.mouse_move(x=150, y=150, speed=1, blocking=True) # Moves the mouse to x, y taking 'speed' seconds to move
print(ahk.mouse_position)  #  (150, 150)
