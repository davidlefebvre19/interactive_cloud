#!/bin/bash
bluetoothctl power on
bluetoothctl discoverable on
bluetoothctl pairable on
echo -e 'power on\ndiscoverable on\npairable on\nquit' | bluetoothctl