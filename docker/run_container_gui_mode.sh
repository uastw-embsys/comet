# Host X11, software OpenGL; to edit files with a GUI
xhost +si:localuser:$(id -un)

docker run -it --rm \
    -u $(id -u):$(id -g) \
    -v ${XAUTHORITY:-$HOME/.Xauthority}:${XAUTHORITY:-$HOME/.Xauthority}:ro \
    -v /tmp/.X11-unix:/tmp/.X11-unix:ro \
    -v /etc/localtime:/etc/localtime:ro \
    -v $PWD:/app \
    -e HOME=/app/.devcontainer-state/home \
    -e XDG_CACHE_HOME=/app/.devcontainer-state/home/.cache \
    -e XDG_CONFIG_HOME=/app/.devcontainer-state/home/.config \
    -e XDG_DATA_HOME=/app/.devcontainer-state/home/.local/share \
    -e DISPLAY=$DISPLAY \
    -e XAUTHORITY=${XAUTHORITY:-$HOME/.Xauthority} \
    -e QT_X11_NO_MITSHM=1 \
    -e XDG_RUNTIME_DIR=/tmp/runtime-$(id -u) \
    -e LIBGL_ALWAYS_SOFTWARE=1 \
    -e MESA_LOADER_DRIVER_OVERRIDE=llvmpipe \
    -w /app \
    comet:v1.0.0 \
    FreeCAD

xhost -si:localuser:$(id -un)