# Hyundai LFA_ALT TEST firmware

This TEST branch enables CARROT-compatible Hyundai `LFA_ALT` angle steering only when CAN-FD message `0x0CB` is observed on the camera bus.

Safety boundaries enforced in both openpilot and Panda:

- steering-wheel command: -175 to +175 degrees
- CARROT angle rate tables: 1.8/1.6/1.3/0.8 degrees per control tick while winding up and 2.4/2.0/1.6/1.0 while unwinding
- maximum LFA angle torque field: 200
- angle actuation blocked when controls are not allowed
- the ordinary Hyundai torque modes do not allow transmission of `0x0CB`

The signed firmware was built from Sunnypilot Panda commit `114b85a649341d55d6beb36d7414eda5e6d324a2` plus validation commit `20a7e1f7`, with the existing CARROT longitudinal limits (+2.5/-4.0 m/s²) retained and the guarded LFA_ALT safety mode added.

- `panda.bin.signed`: SHA256 `73d083ae5691c47d986d464d144fa519e499e334c3be81c3d5df3223ee64ea94`
- `panda_h7.bin.signed`: SHA256 `41bd4684e9311e77c7a7b75e63dd05d3aeba36e43a1ca59605879214550519cd`

This is an experimental vehicle-control path. Validate CAN recognition while parked, then perform the first steering test at low speed on a closed road before normal use.
