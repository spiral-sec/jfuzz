#!/usr/bin/env bash

###
# This scripts manages the vcan interface for testing, using can-utils and cantools
# run vcan.sh help to get more info
###

help () {
  echo "\tvcan.sh"
  echo ""
  echo "helper script to manage vcan for CAN-related development"
  echo ""
  printf "\t-i\t\tinstalls all the necessary packages for the tool's usage. Runs automagically on first monitor run\n"
  printf "\t-s\t\tdisables vcan (you can use ip link to check if vcan0 is activated)\n"
  printf "\t-m file.dbc\tmonitors vcan0 and translates every message using provided .dbc file\n"
}

install () {
  [[ -d ./venv ]] || {
    python -m venv venv && python -m pip install -r requirements.txt ;
  }

  which candump >/dev/null || sudo apt install can-utils
  . venv/bin/activate
}

monitor () {
  # runs can-dump with while checking for "$1" (which should be a .dbc file)
  candump vcan0 | cantools decode "${1}"
}

disable () {
  # Deletes link manually (a reboot should also work)
  sudo ip link del vcan0
}

enable () {
  # Make sure the script runs with super user priviliges.
  [ "$UID" -eq 0 ] || exec sudo bash "$0" -i

  # Load the kernel module.
  modprobe vcan

  # Create the virtual CAN interface.
  ip link add dev vcan0 type vcan

  # Sets up CAN-FD
  sudo ip link set vcan0 mtu 72

  # Bring the virtual CAN interface online.
  ip link set up vcan0
}

while getopts "m:ish" o; do
    case "${o}" in
        m)
            install && enable 2>/dev/null && monitor ${OPTARG}
            ;;
        i)
            install && enable 2>/dev/null
            ;;

        s)
            disable
            ;;

        h)
            help && exit 0
            ;;

        *)
            help && exit 1
            ;;
    esac
done
shift $((OPTIND-1))
