<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# Bluejay 0.21.0 Configurations

This folder contains configuration files for supported electronic speed controller targets tested with COMET using Bluejay. Use the ESC Configurator to flash your electronic speed controller(s) with the official Bluejay 0.21.0 release, then apply the appropriate settings.

- Bluejay 0.21.0 release: https://github.com/bird-sanctuary/bluejay/releases/tag/v0.21.0
- ESC Configurator: https://esc-configurator.com/

Note: These configurations are intended for BLHeli_S electronic speed controllers that are compatible with Bluejay (no support for BLHeli_32).

## Supported targets

- [J-H-50 (4-in-1)](https://www.speedybee.com/speedybee-f405-bls-50a-30x30-4-in-1-esc/): [configs/0.21.0/J-H-50/parameters-bluejay-0.21.0-J-H-50.yaml](/J-H-50/parameters-bluejay-0.21.0-J-H-50.yaml)
- [Q-H-50 (4-in-1)](https://www.rotorama.com/product/skystars-ko50a-bls): [configs/0.21.0/Q-H-50/parameters-bluejay-0.21.0-Q-H-50.yaml](/Q-H-50/parameters-bluejay-0.21.0-Q-H-50.yaml)

If your build uses a different target, create a new subfolder under `0.21.0/` using the Bluejay target name, as shown in the ESC Configurator.

## Prerequisites

- ESC Configurator reachable and up to date
- **Propellers removed** and LiPo connected and powering the ESC(s)
- Stable USB connection through FCU pass-through

## Apply the configuration

Steps to follow:
1) Open https://esc-configurator.com/ in a Chromium-based browser.
2) Connect to the ESC(s) and click "Read Settings" to ensure a stable USB connection and pass-through.
3) Click on "Flash All ESCs" and select the following settings:
   - Firmware: Bluejay
   - ESC (Target): Select the exact target (e.g., Q-H-30). If you are unsure, use Auto-Detect, then confirm against the ESC silkscreen or datasheet.
   - Version: 0.21.0
   - PWM Frequency: Select the value defined by the `pwm_khz` variable in the chosen target parameters file: `parameters-bluejay-0.21.0-<TARGET>.txt`.
4) Wait until all the ESCs have been flashed.
5) Update the values of the parameters in the "Common Parameters" section to match the values specified in the file `parameters-bluejay-0.21.0-<TARGET>.txt.`
6) Click "Write Settings" and, if prompted, power-cycle the ESC.

A note about the motor spin direction: You can adjust the motor direction through the motor ESC wiring, the Bluejay configuration, or the INAV configuration. **The first option is preferred for consistency.**

## Post-flash checks

After applying the new settings:
- Verify motor order and direction. Use the INAV Configurators Output tab to spin individual motors.
- Perform a short throttle range test without the propellers to confirm that there is no desyncing (stuttering or stopping) or excessive heat.

## Troubleshooting

- ESC not detected: Provide external power or follow the bootloader pad procedure for your ESC. Refer to its documentation for more information.
- Desync or rough running: Set the PWM to 24 kHz, increase the demag compensation to "High", and/or increase the motor timing.
- Wrong motor order: Either switch the DShot ESC connector wires or correct the INAV resource/motor mapping. **The first option is preferred for consistency.**
