import sys
import time
import getpass
from pywinauto.application import Application
import psutil
from colors import color


def err(s):
    errstr = color("ERROR", bg="RED", fg="WHITE")
    print(f"{errstr}: {s}", file=sys.stderr)


def is_multiaccess_running():
    return "MultiAccess.exe" in (p.name() for p in psutil.process_iter())


print("Checking if MultiAccess is running...", end="")
if is_multiaccess_running():
    app = Application(backend="uia").connect(path="C:\\Program Files (x86)\\MultiAccess\\MultiAccess.exe")
    app.kill()

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

    print("Trying to login to MultiAccess...", end="")
    app_win.NamnEdit.draw_outline()
    app_win.NamnEdit.set_text(username)
    app_win.LösenordEdit.draw_outline()
    app_win.LösenordEdit.set_text(password)
    app_win.OK.draw_outline()
    app_win.OK.click()

    logged_in = not app_win.window(title="Felaktigt namn eller lösenord!").exists(timeout=1)
    if not logged_in:
        print(" ERROR\n")
        err("The login was incorrect. Try again...")
        app_win.OK.click()
    else:
        print(" OK!")

app_win = app.MultiAccess
app_win.restore()

print("Starting synchronization")
send_changes_button = app_win.Toolbar.Button9
send_changes_button.draw_outline()
send_changes_button.click()

print("Checking that synchronization starts")
app_win.window(title_re="Kommunikation").wait("exists")

print("Waiting for synchronization to finish")
update_ok = None
start_time = time.time()
while True:
    if app_win["Serieport ej tillgänglig."].exists():
        update_ok = False
        err("Connect serial port and try again.")
        app.kill()
        sys.exit(-1)
    if app_win["Uppdatering fullständig."].exists():
        update_ok = True
        break
    if time.time() - start_time > 15:
        err("Timeout...")
        app.kill()
        sys.exit(-1)

print("Synchronization done. Closing.")
ok_button = app_win.OK
ok_button.draw_outline()
ok_button.click()
app_win.close()



