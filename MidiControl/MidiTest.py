
import pygame
import pygame.midi

pygame.init()
pygame.midi.init()
 
# list all midi devices
i=-1
for x in range( 0, pygame.midi.get_count() ):
    inf = pygame.midi.get_device_info(x)
    # Looking specifically for the Novation Launchkey device here
    if inf[1]== b'Launchkey MIDI':
        i = x
 
# open a specific midi device
if i>0:
    inp = pygame.midi.Input(1)
 
    # run the event loop
    while True:
        if inp.poll():
            # no way to find number of messages in queue
            # so we just specify a high max value
            midi_in =inp.read(1000)
            for midi_data in midi_in:
                mi = midi_data[0]
                print ("%d %d %d %d" % (mi[0], mi[1], mi[2], mi[3]))

 
        # wait 10ms - this is arbitrary, but wait(0) still resulted
        # in 100% cpu utilization
        pygame.time.wait(10)
else:
    print ("Could not find Launchkey midi device")
