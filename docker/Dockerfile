# Pull base image.
FROM ubuntu:noble

# Set the maintainer information for this Dockerfile
LABEL maintainer="Christoph Boehm<christoph.boehm@technikum-wien.at>"

# Set the default shell to bash for RUN commands
# This ensures all RUN commands use bash instead of sh
SHELL ["/bin/bash", "-c"]

# https://github.com/FreeCAD/Docker-packaging/tree/master

# Install FreeCAD.
# https://wiki.freecad.org/Compile_on_Linux#
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        ca-certificates \
        git \
        mesa-utils \
        wget \
        x11-apps \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

## Get dependencies
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        build-essential cmake doxygen git \
        libboost-date-time-dev libboost-dev libboost-filesystem-dev \
        libboost-graph-dev libboost-iostreams-dev libboost-program-options-dev \
        libboost-python-dev libboost-regex-dev libboost-serialization-dev \
        libboost-thread-dev libcoin-dev libeigen3-dev libgtkglext1-dev \
        libkdtree++-dev libkml-dev libmedc-dev libocct-data-exchange-dev \
        libocct-draw-dev libocct-foundation-dev libocct-modeling-algorithms-dev \
        libocct-modeling-data-dev libocct-ocaf-dev libocct-visualization-dev \
        libopencv-dev libproj-dev libpyside2-dev libqt5svg5-dev\
        libshiboken2-dev libvtk9-dev libvtk9-qt-dev \
        libvtk-dicom-dev libx11-dev libxerces-c-dev libxmu-dev libxmuu-dev \
        libyaml-cpp-dev libzipios++-dev netgen netgen-headers pyside2-tools python3-dev \
        python3-matplotlib python3-pivy python3-ply python3-pyside2.qtsvg \
        python3-pyside2.qtuitools qtchooser qttools5-dev shiboken2 swig \
        qtwayland5 python3-pyside2.qtnetwork python3-yaml \
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

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        mesa-utils \
        libgl1-mesa-dri \
        libglx-mesa0 \
        libglu1-mesa \
        libx11-xcb1 \
        libxrender1 \
        libxrandr2 \
        libxcb-glx0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Define default command.
# This keeps the container running indefinitely, allowing you to exec into it
# CMD ["/bin/bash", "-c", "tail -f /dev/null"]
CMD ["FreeCAD"]
