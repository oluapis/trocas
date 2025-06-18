import pyautogui as py


# Continuously display mouse position and pixel color
print('Press Ctrl-C to quit.')
try:
    while True:
        x, y = py.position()
        pixel_color = py.pixel(x, y)
        print(f'{x}, {y} : {pixel_color}', end='\r')
except KeyboardInterrupt:
    print('\nDone.')