from smbus import SMBus
import time

BUS = 1
ADDR = 0x48   # change if your ADDR pin is tied differently

CONVERSION_REG = 0x00
CONFIG_REG = 0x01

# Single-shot conversion settings.
# To measure microvolt-level signals you should:
# - use the smallest full-scale range (GAIN = 0x0A00 => ±0.256V)
# - measure differentially (AIN0 - AIN1)
# - use a low data rate and average many samples

# Differential MUX: AIN0 - AIN1
# MUX options (bits 14-12):
# 0x0000 = AIN0 - AIN1 (differential)
# 0x1000 = AIN0 - AIN3
# 0x2000 = AIN1 - AIN3
# 0x3000 = AIN2 - AIN3
# 0x4000 = AIN0 vs GND (single-ended)
MUX = 0x0000

# Use the highest gain for smallest LSB (±0.256V)
GAIN = 0x0A00      # ±0.256V

# Lower data rate reduces noise; start with 8 SPS for best noise performance
DATA_RATE = 0x0000  # 8 SPS

# Number of conversions to average (higher -> lower noise, slower)
SAMPLES = 32

# Build config: OS=1 (start), MUX differential, PGA, MODE=single-shot, DR, comparator disable
CONFIG = 0x8000 | MUX | GAIN | DATA_RATE | 0x0003

def to_signed_16(value):
    if value & 0x8000:
        return value - 65536
    return value

bus = SMBus(BUS)
try:
    print("Scanning I2C bus...")
    found = []
    for addr in range(0x03, 0x78):
        try:
            bus.read_byte(addr)
            found.append(hex(addr))
        except OSError:
            pass

    print("Found devices:", found)

    if ADDR not in [int(x, 16) for x in found]:
        print("ADS1114 not found at", hex(ADDR))
        print("Check wiring, power, and the ADDR pin.")
        raise SystemExit

    # Data-rate to SPS mapping for delay calculation
    DR_SPS = {
        0x0000: 8,
        0x0020: 16,
        0x0040: 32,
        0x0060: 64,
        0x0080: 128,
        0x00A0: 250,
        0x00C0: 475,
        0x00E0: 860,
    }
    sps = DR_SPS.get(DATA_RATE, 128)
    conv_delay = 1.0 / sps + 0.002

    while True:
        sum_raw = 0
        for i in range(SAMPLES):
            # Start a conversion (OS bit set in CONFIG)
            bus.write_i2c_block_data(ADDR, CONFIG_REG, [(CONFIG >> 8) & 0xFF, CONFIG & 0xFF])
            time.sleep(conv_delay)
            data = bus.read_i2c_block_data(ADDR, CONVERSION_REG, 2)
            raw = (data[0] << 8) | data[1]
            raw = to_signed_16(raw)
            sum_raw += raw

        avg_raw = int(sum_raw / SAMPLES)

        full_scale = {
            0x0000: 6.144,
            0x0200: 4.096,
            0x0400: 2.048,
            0x0600: 1.024,
            0x0800: 0.512,
            0x0A00: 0.256,
        }[GAIN]
        voltage = avg_raw * full_scale / 32768.0
        print(f"AvgRaw: {avg_raw:6d}   Voltage: {voltage:.6f} V (avg of {SAMPLES} samples)")

        time.sleep(0.2)
finally:
    bus.close()
