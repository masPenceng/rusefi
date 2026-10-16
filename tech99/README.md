# TECH99 Standalone TCU — development branch

**Branch:** `tech99/tcu-f407vet6`
**Target MCU:** STM32F407VET6 (512 KiB internal Flash).
**Upstream baseline:** `6cf917c59e68c75c8fa0ea0c08f841f116629b25` from `rusefi/rusefi`.
**Status:** integration in progress. **Do not flash or connect to any transmission.**

## Goals
- Retain rusEFI TCU gear selection, shift control and essential system / TunerStudio / CAN infrastructure.
- Remove unused engine-management functions from the *build*, not blindly from sources.
- Read RPM, throttle, and vehicle speed from per-vehicle configurable CAN messages, with optional dedicated sensors.
- Read shifter and transmission sensors directly, implement fault handling, and support bench-only dummy solenoid outputs first.
- Provide a measured 512 KiB Flash and RAM report from a real custom-board build before declaring hardware compatibility.

## Confirmed upstream modules
- `firmware/controllers/tcu/gc_auto.cpp` — uses throttle intent and vehicle speed.
- `firmware/controllers/tcu/gc_generic.cpp` — shifter decode.
- `firmware/controllers/tcu/simple_tcu.cpp` and `tc_4.cpp` — solenoid and generic 4-speed control.

## Open upstream safety issues
- `tc_4.cpp::setTccState`: lower-speed unlock branch sets pin value `1`, and invalid sensor branch returns without commanding an explicitly known safe state. Determine electrical polarity and correct with transmission-specific tests.
- `tc_4.cpp::setPcState`: depends on `engine->engineState.airflowEstimate`; standalone pressure source and default state need implementation.
- `simple_tcu.cpp`: gear enum used as index to solenoid table; validate indices and all selector/transition states before enabling outputs.
- Failure states cannot be universal: gear obtained on solenoid-off is transmission-dependent.

## Milestones
1. Prove that stock F407 reference build succeeds in GitHub Actions. **This does not mean VET6 firmware fits.**
2. Create TECH99 VET6 board definition (clock, pins, flash sectors, storage, bootloader decisions).
3. Strip non-TCU build dependencies while retaining rusEFI communication/configuration; compile real TCU target.
4. Obtain `.elf`, `.map`, `.hex`, `.bin`, matching TunerStudio `.ini` and size report.
5. Bench-test CAN, input validity, shifter, watchdog and solenoid outputs with dummy loads.
6. Vehicle integration only after independent review and transmission-specific safety validation.

This document is a planning and verification record, **not** a claim that steps 1–6 are complete.
