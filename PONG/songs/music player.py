from pygame import mixer
mixer.init()
mixer.music.load("cool songs/Boss Ice Cave.mp3")
mixer.music.set_volume(1)
mixer.music.play(-1)
while True:
    print("Press 'p' to pause, 'r' to resume")
    print("Press 'e' to exit the program")
    query = input()
    if query == 'p':
        mixer.music.pause()     
    elif query == 'r':
        mixer.music.unpause()
    elif query == 'e':
        mixer.music.stop()
        break