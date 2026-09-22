# Pull base image.
FROM ubuntu:noble

# Set the maintainer information for this Dockerfile
LABEL maintainer="Christoph Boehm<christoph.boehm@technikum-wien.at>"

# Set the default shell to bash for RUN commands
# This ensures all RUN commands use bash instead of sh
SHELL ["/bin/bash", "-c"]

# Install FreeCAD.
# https://wiki.freecad.org/Compile_on_Linux#

## Get dependencies
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        build-essential \
        ca-certificates \
        cmake \
        doxygen \
        git \
        libboost-date-time-dev \
        libboost-dev \
        libboost-filesystem-dev \
        libboost-graph-dev \
        libboost-iostreams-dev \
        libboost-program-options-dev \
        libboost-python-dev \
        libboost-regex-dev \
        libboost-serialization-dev \
        libboost-thread-dev \
        libcoin-dev \
        libeigen3-dev \
        libgl1-mesa-dri \
        libglu1-mesa \
        libglx-mesa0 \
        libgtkglext1-dev \
        libkdtree++-dev \
        libkml-dev \
        libmedc-dev \
        libocct-data-exchange-dev \
        libocct-draw-dev \
        libocct-foundation-dev \
        libocct-modeling-algorithms-dev \
        libocct-modeling-data-dev \
        libocct-ocaf-dev \
        libocct-visualization-dev \
        libopencv-dev \
        libproj-dev \
        libpyside2-dev \
        libqt5svg5-dev \
        libshiboken2-dev \
        libvtk9-dev \
        libvtk9-qt-dev \
        libvtk-dicom-dev \
        libx11-dev \
        libx11-xcb1 \
        libxcb-glx0 \
        libxerces-c-dev \
        libxmu-dev \
        libxmuu-dev \
        libxrandr2 \
        libxrender1 \
        libyaml-cpp-dev \
        libzipios++-dev \
        mesa-utils \
        netgen \
        netgen-headers \
        pyside2-tools \
        python3-dev \
        python3-matplotlib \
        python3-pivy \
        python3-ply \
        python3-pyside2.qtnetwork \
        python3-pyside2.qtsvg \
        python3-pyside2.qtuitools \
        python3-yaml \
        qtchooser \
        qttools5-dev \
        qtwayland5 \
        shiboken2 \
        swig \
        wget \
        x11-apps \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

## Get FreeCAD source
RUN wget https://github.com/FreeCAD/FreeCAD/releases/download/1.1.3/freecad_source_1.1.3.tar.gz \
    && mkdir -p /freecad-source \
    && tar -xvzf freecad_source_1.1.3.tar.gz -C freecad-source

## Build from Source
# https://servercake.in/guides/package-management/building-from-source
RUN cd /freecad-source \
    && mkdir -p ./build \
    && cd ./build \
    && cmake ../

WORKDIR /freecad-source/build

RUN make -j$(nproc --ignore=2)

RUN make install


# # Install PrusaSlicer.
WORKDIR /

## Get dependencies
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        git \
        build-essential \
        autoconf \
        doxygen \
        graphviz \
        cmake \
        libglu1-mesa-dev \
        libgtk-3-dev \
        libdbus-1-dev \
        libwebkit2gtk-4.1-dev \
        texinfo \
        file \
        libtool \
        automake \
        m4 \
        pkg-config \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

## Get PrusaSlicer source
# https://github.com/prusa3d/PrusaSlicer/releases/tag/version_2.9.6
RUN wget https://github.com/prusa3d/PrusaSlicer/archive/refs/tags/version_2.9.6.tar.gz \
    && mkdir -p /prusaslicer-source \
    && tar -xvzf version_2.9.6.tar.gz -C /prusaslicer-source

## Build from Source
# https://github.com/prusa3d/PrusaSlicer/blob/version_2.9.6/doc/How%20to%20build%20-%20Linux%20et%20al.md

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

### Build Dependencies
RUN cd /prusaslicer-source/PrusaSlicer-version_2.9.6/deps \
    && mkdir -p ./build \
    && cd ./build \
    && cmake .. -DDEP_WX_GTK3=ON \
    && make
    #  -j$(nproc --ignore=2)

## Get dependencies
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        libhidapi-dev \
        libusb-1.0-0-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

### Build PrusaSlicer
RUN cd /prusaslicer-source/PrusaSlicer-version_2.9.6 \
    && mkdir -p ./build \
    && cd ./build \
    && cmake .. -DCMAKE_BUILD_TYPE=Release -DSLIC3R_STATIC=1 -DSLIC3R_GTK=3 -DSLIC3R_PCH=OFF -DCMAKE_PREFIX_PATH=$(pwd)/../deps/build/destdir/usr/local \
    && make -j$(nproc --ignore=2)

WORKDIR /prusaslicer-source/PrusaSlicer-version_2.9.6

RUN cmake --install build --prefix /opt/prusaslicer

### RUN-TIME
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        locales \
        xdg-utils \
        librsvg2-common \
        shared-mime-info \
        adwaita-icon-theme \
        hicolor-icon-theme \
        libgdk-pixbuf2.0-bin \
        dbus \
        dbus-x11 \
        dbus-user-session \
    && sed -i 's/^# *\(en_US.UTF-8 UTF-8\)/\1/' /etc/locale.gen \
    && locale-gen en_US.UTF-8 \
    && update-locale LANG=en_US.UTF-8 \
    && rm -rf /var/lib/apt/lists/*

ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8

ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
ENV SSL_CERT_DIR=/etc/ssl/certs
ENV CURL_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt

# Define default command.
# This keeps the container running indefinitely, allowing you to exec into it
# ENV PATH="/opt/prusaslicer/bin:${PATH}"
CMD ["FreeCAD"]
