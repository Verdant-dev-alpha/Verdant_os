# pump_config.py

# MCP23017 pin mapping:
# GPA0-GPA7 = pins 0-7
# GPB0-GPB7 = pins 8-15

# Nutrient pumps 1–6
PUMPS = {
    "calcium_nitrate":  0,  # GPA0
    "magnesium_sulfate": 1,  # GPA1
    "micronutrients":   2,  # GPA2
    "ph_down":          3,  # GPA3
    "ph_up":            4,  # GPA4
    "potassium":        5,  # GPA5

    # High-volume pumps 7–10
    "flush_1":          6,  # GPA6
    "flush_2":          7,  # GPA7
    "fill_1":           8,  # GPB0
    "fill_2":           9,  # GPB1
}
