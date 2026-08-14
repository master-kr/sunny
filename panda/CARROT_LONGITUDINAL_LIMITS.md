# Carrot Hyundai longitudinal limits

The bundled Panda firmware was built from sunnypilot/panda commit
`114b85a649341d55d6beb36d7414eda5e6d324a2`, matching the December 2023
generation used by this release.

Only the Hyundai longitudinal safety command limits were changed:

- maximum acceleration: `2.00` to `2.50 m/s^2`
- maximum deceleration: `-3.50` to `-4.00 m/s^2`

The firmware was built with the repository debug certificate in release mode.
Build and Hyundai safety-test record:
<https://github.com/master-kr/openpilot/actions/runs/31786638578>

Safety-test result: `782 passed, 180 skipped`.

SHA-256:

- `panda.bin.signed`: `e5c1eb768b4eb9bf980fe489c392f44f2d12e2a926efb7800be4bcf088a58ce4`
- `panda_h7.bin.signed`: `6c7b7cb92309e05d838ade0409263947fed8da5b64c71ec32429fce954204a3a`
