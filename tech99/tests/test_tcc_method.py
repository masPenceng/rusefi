#!/usr/bin/env python3
"""Compile and execute the *actual* rusEFI TCC method with mocked I/O.

This is a software regression test: NOT hardware, hydraulic, or polarity validation.
It extracts Generic4TransmissionController::setTccState from tc_4.cpp.
"""
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
source = (ROOT / "firmware/controllers/tcu/tc_4.cpp").read_text()
match = re.search(
    r"void Generic4TransmissionController::setTccState\(gear_e gear\)\s*\{",
    source,
)
assert match, "setTccState not found in real rusEFI source"
brace = 0
end = None
for i in range(match.end() - 1, len(source)):
    if source[i] == "{":
        brace += 1
    elif source[i] == "}":
        brace -= 1
        if brace == 0:
            end = i + 1
            break
assert end is not None, "TCC source has unmatched braces"
method = source[match.start():end]
# Genuine method is embedded unchanged below; only hardware abstractions are mocked.
stub = r"""
#include <cassert>
#include <cstdio>
enum gear_e { NEUTRAL = 0, GEAR_1 = 1, GEAR_2 = 2, GEAR_3 = 3, GEAR_4 = 4 };
enum class SensorType { DriverThrottleIntent, VehicleSpeed };
struct Reading { bool Valid; float Value; };
Reading mockTps{true, 15.0f}, mockVss{true, 0.0f};
namespace Sensor {
    Reading get(SensorType type) {
        return type == SensorType::DriverThrottleIntent ? mockTps : mockVss;
    }
}
struct Pin {
    int level = -1;
    void setValue(int v) { level = v; }
};
struct Pins { Pin tcuTccOnoffSolenoid; } enginePins;
struct Calibration {
    float tcu_tccTpsBins[8]{};
    float tcu_tccLockSpeed[8]{50};
    float tcu_tccUnlockSpeed[8]{40};
} calib;
Calibration* config = &calib;
int interpolate2d(float, const float*, const float* values) {
    return static_cast<int>(values[0]);
}
struct Generic4TransmissionController {
    bool isShifting = false;
    int torqueConverterDuty = 0;
    void setTccState(gear_e);
};
"""
tests = r"""
int main() {
    Generic4TransmissionController t;
    auto check = [&](int level, int duty) {
        assert(enginePins.tcuTccOnoffSolenoid.level == level);
        assert(t.torqueConverterDuty == duty);
    };
    mockVss = {true, 90};
    t.setTccState(GEAR_4);
    check(1, 100);                      // lock in 4th above threshold
    t.isShifting = true;
    t.setTccState(GEAR_4);
    check(0, 0);                        // shift unlock
    t.isShifting = false;
    t.setTccState(GEAR_4);
    check(1, 100);
    mockTps.Valid = false;
    t.setTccState(GEAR_4);
    check(0, 0);                        // missing TPS unlock
    mockTps.Valid = true;
    mockVss.Valid = false;
    t.setTccState(GEAR_4);
    check(0, 0);                        // missing VSS unlock
    mockVss = {true, 10};
    t.setTccState(GEAR_4);
    check(0, 0);                        // low speed unlock
    mockVss.Value = 90;
    t.setTccState(GEAR_4);
    check(1, 100);
    mockVss.Value = 45;
    t.setTccState(GEAR_4);
    check(1, 100);                      // hysteresis band preserves prior state
    t.setTccState(GEAR_3);
    check(0, 0);                        // outside 4th unlock
    std::puts("PASS: 7 TCC scenarios on extracted production method");
}
"""
assert "uint8_t (*pcts)[TCU_TABLE_WIDTH] = nullptr;" in source, (
    "Pressure table pointer must be initialized before gear switch"
)
with tempfile.TemporaryDirectory(prefix="tech99-tcc-") as tmp:
    p = Path(tmp)
    (p / "test.cpp").write_text(stub + "\n" + method + "\n" + tests)
    subprocess.run(
        ["g++", "-std=c++20", "-O2", "-Wall", "-Wextra", "-Werror",
         str(p / "test.cpp"), "-o", str(p / "test")],
        check=True,
    )
    subprocess.run([str(p / "test")], check=True)
print("PASS: pressure-table pointer initialization verified by source assertion")
