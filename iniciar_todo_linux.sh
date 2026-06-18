#!/bin/bash
gnome-terminal -- bash -c "./iniciar_backend_linux.sh; exec bash"
gnome-terminal -- bash -c "./iniciar_frontend_linux.sh; exec bash"