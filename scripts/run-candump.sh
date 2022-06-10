#!/usr/bin/env bash

# runs can-dump with while checking for "$1" (which should be a .dbc file)
candump vcan0 | cantools decode "${1}"