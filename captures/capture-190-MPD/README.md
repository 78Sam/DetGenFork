This scenario consists of an MPC client interacting with a mopidy server to stream and play music. Songs can be stored in playlists in /media/playlists and then played via the commands:

mpc -h 172.16.238.40 ls Files/media/playlists/[PLAYLIST NAME] | mpc -h 172.16.238.40 add
mpc -h 172.16.238.40 play


Currently, there are 5 scenarios available.

Scenario 0 streams a playlist all the way through.
Scenario 1 shuffles the playlist before playing all the way through.
Scenario 2 plays through a playlist, stopping and restarting at fixed intervals.
Scenario 3 plays through all playlists.
Scenario 4 requests playing statistics before playing.

Each scenario plays a different set of music.

Playlists should be named as increasing integers (i.e. '0', '1', '2' ...)

We do not provide music files, which will need to be added to the correct folder.
