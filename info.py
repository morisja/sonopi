import soco
import sys
import pdb
from soco.plugins.sharelink import ShareLinkPlugin

devices = {device.player_name: device for device in soco.discover()}
x=devices['Living Room']


share_link = ShareLinkPlugin(x)
pdb.set_trace()

sys.exit(0)
print("current state")
print("")
for n, d in devices.items():
    print(d.all_groups)

for n, d in devices.items():
    d.unjoin()

print(devices['Living Room'].all_groups)

