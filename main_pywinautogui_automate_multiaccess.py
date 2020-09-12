import sys
import time
import getpass
from pywinauto.application import Application
import psutil


def is_multiaccess_running():
    return "MultiAccess.exe" in (p.name() for p in psutil.process_iter())


print("Checking if MultiAccess is running...", end="")
if is_multiaccess_running():
    app = Application(backend="uia").connect(path="C:\\Program Files (x86)\\MultiAccess\\MultiAccess.exe")
    app.MultiAccess.kill()

if False:
    print(" ERROR!\n")
    print("Please exit MultiAccess and try again")
    sys.exit(-1)

print(" OK!\n")
print("Starting MultiAccess application")
app = Application(backend="uia").start("C:\\Program Files (x86)\\MultiAccess\\MultiAccess.exe")

print("Trying to find MultiAccess application")
app_win = app.MultiAccess
app_win.draw_outline()

logged_in = False
while not logged_in:
    print("Input MultiAccess authentication")
    app_win.minimize()
    username = input("Username: ")
    password = getpass.getpass("Password: ")

    app_win.NamnEdit.draw_outline()
    app_win.NamnEdit.set_text(username)
    app_win.LösenordEdit.draw_outline()
    app_win.LösenordEdit.set_text(password)
    app_win.OK.draw_outline()
    app_win.OK.click()

    logged_in = not app_win.window(title="Felaktigt namn eller lösenord!").exists(timeout=1)
    if not logged_in:
        print("The login was incorrect. Try again...")
        app_win.OK.click()

app_win = app.MultiAccess
app_win.restore()
send_changes_button = app_win.Toolbar.Button9
send_changes_button.draw_outline()
send_changes_button.click()

app_win.Kommunikation.wait("exists")

app_win["Uppdatering fullständig."].wait("exists", timeout=70)
ok_button = app_win.OK
ok_button.draw_outline()
ok_button.click()
app_win.close()



