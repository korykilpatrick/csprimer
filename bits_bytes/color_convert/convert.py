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
    rgb = "rgb"
    hex_len = len(hex)
    if hex_len == 3:
        rgb += '('
        for i in range(3):
            rgb += f"{(int(hex[i],16) << 4) + int(hex[i],16)} "
        rgb = rgb[:-1]
    elif hex_len == 4:
        rgb += 'a('
        for i in range(4):
            if i < 3:
                rgb += f"{(int(hex[i],16) << 4) + int(hex[i],16)} "
            else:
                rgb += f"/ {round(((int(hex[i],16) << 4) + int(hex[i],16))/255,5)}"
    elif hex_len == 6:
        rgb += '('
        for i in range(0, 6, 2):
            rgb += f"{int(hex[i:i+2],16)} "
        rgb = rgb[:-1]
    elif hex_len == 8:
        rgb += 'a('
        for i in range(0, 8, 2):
            if i < 6:
                rgb += f"{int(hex[i:i+2],16)} "
            else:
                rgb += f"/ {round(int(hex[i:i+2],16) / 255,5)}"
    else:
        raise Exception(f"Hex length {hex_len} is invalid.")
    
    return rgb + ")"
    
assert hex_to_rgb('123') == 'rgb(17 34 51)'
assert hex_to_rgb('0000FFC0') == 'rgba(0 0 255 / 0.75294)'
assert hex_to_rgb('00f8') == 'rgba(0 0 255 / 0.53333)'
assert hex_to_rgb('fe030a') == 'rgb(254 3 10)'
assert hex_to_rgb('0f0def') == 'rgb(15 13 239)'
"""
3 digits -> multiply each digit by 256(?)/17 
4 digits -> same as 3 digit. 4th digit interpeted as percentage so divide by 16(?)
6 digits -> each pair of digits is color channel
8 digits -> same as 6 digits, interpet last 2 digits as percentage (divide by 256)
"""


# assert hex_to_rgb('#00ff00') == 'rgb(0 255 0)'
# print(hex_to_rgb('fe030a'))
# print(hex_to_rgb('00ff00'))
# print(hex_to_rgb('#0f0def'))
# print(hex_to_rgb('00f8'))
# print(hex_to_rgb('0000FFC0'))