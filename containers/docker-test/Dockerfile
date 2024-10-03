FROM debian:buster-slim

RUN set -ex \
    # Official Mopidy install for Debian/Ubuntu along with some extensions
    # (see https://docs.mopidy.com/en/latest/installation/debian/ )
 && apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get install -y \
        curl \
        dumb-init \
        gnupg \
        gstreamer1.0-alsa \
        gstreamer1.0-plugins-bad \
        python3-crypto \
        python3-distutils \
 && curl -L https://bootstrap.pypa.io/pip/3.7/get-pip.py | python3 - \
 && pip install pipenv \
    # Clean-up
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* ~/.cache