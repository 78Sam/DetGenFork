A web app for signing up to a newsletter that is vulnerable to XXE. The underlying XML reader uses PHP and has the expect module loaded, allowing for RCE.

Attack0 reads the passwd file.

Attack1 reads the shadow file.

Attack2 is the RCE.

Usage is ./capture-xxe.sh [DURATION] [REPEAT] [ATTACK]
