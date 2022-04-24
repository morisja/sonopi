import soco
import sys
import pdb

devices = {device.player_name: device for device in soco.discover()}


x = devices["Living Room"].all_groups
print(x)
devices["Living Room"].partymode()
x = devices["Living Room"].all_groups
print(x)
x = devices["Living Room"].group.coordinator
print(x)
print(x.volume)


sys.exit(0)
print("current state")
print("")
for n, d in devices.items():
    print(d.all_groups)

for n, d in devices.items():
    d.unjoin()

print(devices["Living Room"].all_groups)
