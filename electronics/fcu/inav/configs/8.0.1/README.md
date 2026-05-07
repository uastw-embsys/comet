<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# INAV 8.0.1 Configurations

This folder contains CLI diffs ("diff all") for the supported flight controller targets that have been tested with COMET. Flash your flight controller with the official INAV 8.0.1 release, then apply the appropriate diff.

- INAV 8.0.1 release: https://github.com/iNavFlight/inav/releases/tag/8.0.1
- INAV Configurator 8.0.1 release: https://github.com/iNavFlight/inav-configurator/releases/tag/8.0.1

## Supported targets

- [MICOAIR743V2](https://micoair.com/flightcontroller_micoair743v2/): [configs/8.0.1/MICOAIR743V2/diff-inav-8.0.1-MICOAIR743V2.txt](/MICOAIR743V2/diff-inav-8.0.1-MICOAIR743V2.txt)

If your build uses a different target, create a new subfolder under `8.0.1/` with the target name as it appears in the INAV Configurator.

## Prerequisites

- INAV Configurator installed
- Correct USB drivers for your flight controller
- **Propellers removed** and LiPo disconnected for configuration

## Apply the configuration

Steps to follow:
1) Flash INAV 8.0.1 using the official instructions for your specific target (check the board's silkscreen and the INAV target name).
2) Connect using the INAV Configurator and open the CLI tab.
3) Paste the contents of the selected `diff-inav-8.0.1-<TARGET>.txt` into the CLI tab.
4) Press Enter and wait for the commands to take effect.
5) Type "save" to reboot.

## Post-flash calibrations and checks

After applying the new settings:
- Calibrate the accelerometer and magnetometer. Then, verify the barometer's function.
- Verify motor order and direction. Use the INAV Configurators Output tab to spin individual motors.
- Bind the RC remote and receiver according to the manual and verify or reconfigure the receiver protocol and channel mapping.
- Set the failsafe to "drop" or according to your regulations.

## Troubleshooting

- CLI rejects lines: Ensure that the flight controller target matches and that you are using INAV 8.0.1.
- Resources conflict: Compare your wiring to the [wiring diagram](../../../../wiring/wiring-diagram.svg).
- Sensor (gyro) init fails: Check the mounting orientation and vibration isolation.
