#!/bin/bash

# This script should be run before development because vCAN is not necessarily
# on by default.

# Make sure the script runs with super user priviliges.
[ "$UID" -eq 0 ] || exec sudo bash "$0" "$@"

# Load the kernel module.
modprobe vcan

# Create the virtual CAN interface.
ip link add dev vcan0 type vcan

# Sets up CAN-FD
sudo ip link set vcan0 mtu 72

# Bring the virtual CAN interface online.
ip link set up vcan0


# Bring up real CAN interface.
# sudo ip link set vcan0 up type can bitrate 1000000

