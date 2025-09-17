## TorCycle - A Tool to continously cycle your IP Address using Tor.

### How does it work?
Everytime you connect to Tor, it builds up a circuit for you. Those circuits are built of three random servers (also called relays).
This tool now uses that to change your IP - Every 10 Seconds, it sends a "SIGNAL NEWNYM" to Tor, which makes it build a new circuit
and gives you a new IP-Addresss.

Your regular IP (The one provided by your ISP) stays the same. This program is intended to route your Traffic through Tor.


### To-Do:
- Add local SOCKS5 proxy to route the traffic through the program which controls Tor
- Eventually add GUI to learn more QT




---
This Project was made to learn more about Tor, how it works and how to manually route traffic through it.
For ethical use only.

