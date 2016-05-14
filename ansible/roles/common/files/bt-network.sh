#!/bin/bash

br=bnep

[[ -n "$(brctl show $br 2>&1 1>/dev/null)" ]] && {
        brctl addbr $br
        brctl setfd $br 0
        brctl stp $br off
        ip addr add 10.1.2.3/24 dev $br
        ip link set $br up
}

exec fgtk/bt-pan --debug client $1
