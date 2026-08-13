# release-c3-BDv2-source

This branch preserves the `release-c3-BDv2` prebuilt driving stack, Panda firmware,
DBC files, and Blue Diamond v2 model. UI and required support sources were restored
from Sunnypilot commit `1b49d24d`, the source revision immediately preceding the
December 24, 2023 `v0.9.5.3` release build.

## One-time UI build

`launch_chffrplus.sh` builds only `selfdrive/ui/_ui` once per Git revision. The
existing prebuilt UI is backed up first and restored automatically if the source
build fails. Build output is written to:

```text
/data/community/crashes/ui_source_build.txt
```

The successful revision is stored in `/data/ui_build_commit`.

## Ioniq 5 TPMS

The UI subscribes to the existing CAN stream and reads Hyundai CAN-FD frame
`0x3A0`. It displays front-left, front-right, rear-left, and rear-right pressures
as rounded PSI values above the driver-monitoring icon. The unit label is omitted,
values below 31 PSI are red, invalid values are `-`, and stale values disappear
after ten seconds.

This is display-only. It does not transmit CAN messages or change Panda safety,
DBC, vehicle control, or steering behavior.

## Calibration reset

Reset Calibration remains available while the vehicle is on and communicating.
It is blocked while openpilot is actively engaged. After confirmation it removes
`CalibrationParams` and `LiveTorqueParameters`, then reboots the device so a new
calibration starts cleanly.

## Device checks

1. Confirm the first boot completes the UI build without falling back.
2. With openpilot disengaged but the vehicle on, reset calibration and confirm the
   device reboots and calibration restarts.
3. Confirm the button refuses the action while openpilot is engaged.
4. Drive until TPMS frame `0x3A0` is present and compare all four displayed values
   with the vehicle cluster.
5. Confirm the Blue Diamond v2 hash remains
   `b298caa4be035dbe25b9158f0ba3d0b59a99e6a695a11fccda98b69f5050f29f`.
