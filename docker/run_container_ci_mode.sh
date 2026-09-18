# No X11 and GPU; just to run the scripts
docker run -it --rm \
    -u $(id -u):$(id -g) \
    -v /etc/localtime:/etc/localtime:ro \
    -v $PWD:/app \
    -e HOME=/app/.devcontainer-state/home \
    -e XDG_CACHE_HOME=/app/.devcontainer-state/home/.cache \
    -e XDG_CONFIG_HOME=/app/.devcontainer-state/home/.config \
    -e XDG_DATA_HOME=/app/.devcontainer-state/home/.local/share \
    -e LIBGL_ALWAYS_SOFTWARE=1 \
    -e MESA_LOADER_DRIVER_OVERRIDE=llvmpipe \
    -w /app \
    comet:v1.0.0 \
    bash