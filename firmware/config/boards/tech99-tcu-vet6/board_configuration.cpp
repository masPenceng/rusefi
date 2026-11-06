// TECH99 TCU F407VET6 compile-only board stub.
// No pin allocation or driver initialization until hardware is verified.
// This deliberately does NOT reuse the f407-discovery/Frankenso board file:
// that file assumes communityCommsLedPin and engine->fuelComputer,
// which are not present in this TCU-only configuration.
#include "pch.h"

Gpio getCommsLedPin() { return Gpio::Unassigned; }
Gpio getWarningLedPin() { return Gpio::Unassigned; }
Gpio getRunningLedPin() { return Gpio::Unassigned; }

void setup_custom_board_overrides() {
    // Compiler bring-up only; no solenoid, TCC, or other output is assigned.
}
