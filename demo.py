import mido
import time
from effects import TextScroll
from layouts import LaunchpadMiniMk1
from scene import Scene

mk1ioport = mido.open_ioport(name="Launchpad Mini:Launchpad Mini MIDI 1 28:0")
mk1 = LaunchpadMiniMk1(mk1ioport)

ts = TextScroll(mk1, 0, (0, 0), "KUPA")
s = Scene([mk1])

s.add_effect(ts)

while True:
    s.tick()
    if len(s.effects) == 0:
        break

    time.sleep(1.0 / 15)


# pb = PointBloom(mk1, 43, (2,4))
#
# for x in range(6):
#     pb.tick()
#     mk1.draw_full_next()
#     time.sleep(1)
#
# In [164]: while True:
#      ...:     if randint(0, 4) == 0:
#      ...:         x = randint(0, 8)
#      ...:         y = randint(0, 8)
#      ...:         s.add_effect(PointBloom(mk1, i, (x, y)))
#      ...:     s.tick()
#      ...:     i += 1
#      ...:     time.sleep(0.125)
#
