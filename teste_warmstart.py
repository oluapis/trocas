import pyautogui as py
import keyboard

import time

key_pressed = False
phase = 0
state = 'logged_in'
insert_pressed = False
Amount_OnlineChanges = 0 + 1197
recteste_iscommented = True

py.PAUSE = 0.3

pixel_gatewaynotconfigured = (750, 465)
pixel_loginconfirmation = (750, 460)
pixel_confirmonlinechange = (650, 490)


region_clpstate = {"top": 750, "left": 450, "width": 100, "height": 15} # só le RUN (não identifica stop)
region_loginconfirmation = {"top": 390, "left": 545, "width": 335, "height": 40} # "Are you sure you want to login to the node ‘PH’ with address ‘0000'7"
regio_confirmonlinechange = {"top": 290, "left": 450, "width": 370, "height": 30} # "The application changed since last download, What do you want to do?"

while True:
    try:
        if keyboard.is_pressed('insert'):
            if not insert_pressed:
                insert_pressed = True
                phase = not phase
                print(f'phase changed: {phase}')
            else:
                insert_pressed = False


        if keyboard.is_pressed('enter'):
            if not key_pressed:
                x, y = py.position()
                print(f"Mouse position: X={x}, Y={y}")
                key_pressed = True
                
                color = py.pixel(x, y)
                print(color)
        else:
            key_pressed = False


        if phase == 1:
            
            py.sleep(3)
            login = py.pixel(547, 54)
            print("Waiting for Login...")
            while login != (0, 255, 0):
                login = py.pixel(547, 54)
                logoff = py.pixel(571, 53)
                if logoff == (255, 0, 0):
                    py.leftClick(571, 53)
                    py.sleep(2)
                    py.hotkey("ctrl", "f8")
                    print("MasterTool isn't logged out! logging out...")
            

            py.sleep(1)

            print("Changing the project!")
            pixel = py.pixel(277, 107)
            while (pixel != (255, 255, 255)):
                pixel = py.pixel(277, 107)
                if pixel == (249, 249, 249):
                    py.leftClick(277, 107)
                py.sleep(1)

            py.sleep(1)

            py.leftClick(246, 670)
            
            if recteste_iscommented:
                py.write("Rec_Teste: INT;")
            else:
                py.hotkey("shift", "home")
                py.press("delete")


            py.sleep(1)
            pixel = py.pixel(410, 110)
            while (pixel != (255, 255, 255)):
                pixel = py.pixel(410, 110)
                if pixel == (247, 247, 247):
                    py.leftClick(410, 110)
                py.sleep(1)
            
            py.sleep(1)

            py.leftClick(797, 492)
            py.press("left")
            py.press("left")
            py.hotkey("ctrl", "backspace")
            if recteste_iscommented:
                py.write("Rec_Teste")  
            else:
                py.write("Rec_IDMisturadorAuxiliar")
            recteste_iscommented = not recteste_iscommented 

            pixel = py.pixel(693, 464)
            has_pressed = False
            print("Waiting for Login Confirmation...")
            while pixel != (255, 255, 255) or not has_pressed:
                py.click(547, 54)
                pixel = py.pixel(693, 464)
                if pixel == (229, 241, 251) or pixel == (225, 225, 225):
                    py.click(693, 464)
                    has_pressed = True
                py.sleep(1)

            py.sleep(2)

            pixel = py.pixel(631, 493)
            has_pressed = False
            print("Waiting for Online Change Warning...")
            while pixel != (255, 255, 255) or has_pressed == False:
                pixel = py.pixel(631, 493)
                if pixel == (229, 241, 251) or pixel == (225, 225, 225):
                    py.leftClick(631, 493)
                    print("Pressed the button!")
                    has_pressed = True
                #pixel2 = py.pixel(-779, 499)
            # if pixel2 == (229, 241, 251) or pixel2 == (225, 225, 225):
                #    break
                py.sleep(1)

            py.sleep(1)
            
            
            """pixel = py.pixel(-779, 499)
            has_pressed = False
            print("Waiting for Online Change Confirmation...")
            while pixel != (255, 255, 255) or has_pressed == False:
                logoff = py.pixel(571, 53)
                if logoff == (255, 0, 0):
                    break
                login = py.pixel(547, 54)
                if login == (0, 255, 0):
                    break
                pixel = py.pixel(-779, 499)
                if pixel == (229, 241, 251) or pixel == (225, 225, 225):
                    py.leftClick(-779, 499)
                    print("Pressed the button!")
                    has_pressed = True
                py.sleep(1)"""
            
            Amount_OnlineChanges += 1
            print(f"Total Amount of Online Changes: {Amount_OnlineChanges}")
            
            py.sleep(1)
    except OSError as e:
        print(f"Erro ao tentar ler o pixel na tentativa {Amount_OnlineChanges}: {e}")

        time.sleep(1)
        
        