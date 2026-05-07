<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# FCU and ESC Configuration - NOTES

### 5) Flash and configure INAV

- Flash official INAV 8.0.1 for your target (linked in docs/firmware.md).
- INAV Configurator → CLI → paste electronics/inav/configs/8.0.1/<target>/diff.txt → save.
- Calibrate accelerometer, magnetometer, radio; verify failsafe and motor order/direction.

- See [INAV Configuration](#inav-configuration) for details.
- Install INAV 8.0.1 for your <target> board 
- In INAV CLI: paste the diff from electronics/inav/configs/8.0.1/<target>/diff.txt.
- Safety: [`docs/build-manual/safety.md`](/docs/build-manual/safety.md)
- Flash the official INAV 8.0.1 for your flight controller target (linked in docs/firmware/).
- Apply the configuration diff at: electronics/inav/configs/8.0.1/<target>/diff.txt.
- Calibrate (accel, mag, radio) and verify failsafe before flight.

- Target firmware: INAV 8.0.1 for target <YOUR_FC_TARGET> (flight controller target)
  - We do not distribute INAV. Official releases: https://github.com/iNavFlight/inav/releases
- Apply configuration: electronics/inav/configs/8.0.1/<target>/diff.txt
- How: INAV Configurator → CLI → paste diff → save → reboot
- Instructions: docs/firmware/index.md
- Tuning and presets
  - Initial PID/rates and filters are noted in electronics/inav/configs/…/README.md

4) Flash iNav 8.0.1 to your FC target and apply config diff.
5) Validate motor order/direction; check OSD and failsafe.

Checklist
- Arming works only when safe (switch + checks).
- Failsafe behavior set (e.g., disarm or RTH if GPS present).
- OSD elements visible; voltage alarm configured.

## Firmware (iNav) setup

We do not ship firmware binaries. We link to iNav and provide a reproducible configuration.

- Version: iNav 8.0.1
- Target: [e.g., MATEKF405] — see flight/inav/target.md
- Links: flight/inav/links.md (official release and Configurator)
- Apply config:
  1) Flash iNav 8.0.1, then Reset to defaults once.
  2) Configurator → CLI → paste flight/inav/config/inav-8.0.1/TARGET_<YOURTARGET>/diff_all.txt
  3) Enter `save`. Calibrate sensors, verify receiver and motor order.
- Reference:
  - dump_all.txt for verification
  - osd_layout.json and rates_pid_profiles.json (if provided)
- ESC:
  - See flight/esc/ notes for protocol (e.g., DSHOT600), bidirectional RPM, and motor directions.
  

- Target firmware: INAV 8.0.1 for target <YOUR_FC_TARGET> (flight controller target)
  - We do not distribute INAV. Official releases: https://github.com/iNavFlight/inav/releases
- Apply configuration: electronics/inav/configs/8.0.1/<target>/diff.txt
- How: INAV Configurator → CLI → paste diff → save → reboot
- Instructions: docs/firmware/index.md
- Tuning and presets
  - Initial PID/rates and filters are noted in electronics/inav/configs/…/README.md


