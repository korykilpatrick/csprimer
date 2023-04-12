"""
input
body {
    color: #fe030a;
    background-color: #0f0def;
}
"""
"""
output
body {
    color: rgb(254 3 10);
    background-color: rgb(15 13 239);
}
"""
def hex_to_rgb(hex):
    """Convert hex color to rgb color."""
    rgb = "rgb("
    curr_val = 0
    for i,h in enumerate(hex):
        if i == 0:
            continue
        elif i & 1:
            if i != 1:
                rgb += " "
            curr_val += int(h, 16) << 4
        else:
            curr_val += int(h, 16)
            rgb += str(curr_val)
            curr_val = 0
    return rgb + ")"

# print(hex_to_rgb('#fe030a'))
# print(hex_to_rgb('#0f0def'))
assert hex_to_rgb('#00ff00') == 'rgb(0 255 0)'
assert hex_to_rgb('#fe030a') == 'rgb(254 3 10)'
assert hex_to_rgb('#0f0def') == 'rgb(15 13 239)'