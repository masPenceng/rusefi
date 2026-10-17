# TECH99 standalone TCU experimental STM32F407VET6 build.
# NOT a verified VET6 board pinout. No transmissions/solenoids may be connected.
# Use the upstream F407 Discovery hardware definition only for initial compilation.
BOARDCPPSRC = $(BOARDS_DIR)/f407-discovery/board_configuration.cpp

# No MMC/SDC controller is configured: exclude ChibiOS FatFS compilation.
USE_FATFS = no
DDEFS += -DEFI_SUPPORT_FATFS=FALSE
DDEFS += -DSTM32F407xx
DDEFS += -DFIRMWARE_ID=\"TECH99-TCU\"
DDEFS += -DSTATIC_BOARD_ID=STATIC_BOARD_ID_F407_DISCOVERY

# Retain rusEFI TCU, CAN, sensor, USB and TS infrastructure.
DDEFS += -DEFI_ENGINE_CONTROL=FALSE -DEFI_TCU=TRUE
DDEFS += -DEFI_CAN_SUPPORT=TRUE -DEFI_VEHICLE_SPEED=TRUE
DDEFS += -DEFI_TUNER_STUDIO=TRUE -DEFI_USB_SERIAL=TRUE
DDEFS += -DEFI_EMBED_INI_MSD=FALSE

# Remove engine-specific subsystems from this first linking experiment.
DDEFS += -DEFI_LUA=FALSE -DEFI_LUA_LOOKUP=FALSE
DDEFS += -DEFI_BOOST_CONTROL=FALSE -DEFI_LAUNCH_CONTROL=FALSE
DDEFS += -DEFI_IDLE_CONTROL=FALSE -DEFI_IDLE_PID_CIC=FALSE
DDEFS += -DEFI_VVT_PID=FALSE -DEFI_MAP_AVERAGING=FALSE
DDEFS += -DEFI_ELECTRONIC_THROTTLE_BODY=FALSE
DDEFS += -DEFI_FILE_LOGGING=FALSE -DEFI_STORAGE_SD=FALSE
DDEFS += -DEFI_ENGINE_SNIFFER=FALSE -DEFI_ENGINE_EMULATOR=FALSE
# Do NOT define EFI_SOFTWARE_KNOCK at all: ADC port uses #ifdef,
# so -DEFI_SOFTWARE_KNOCK=FALSE incorrectly enables knock-only code.
DDEFS += -DEFI_TOOTH_LOGGER=FALSE
DDEFS += -DEFI_MAX_31855=FALSE -DEFI_ALTERNATOR_CONTROL=FALSE

# This is strictly a compiler/linker experiment: do not flash the resulting binary.
