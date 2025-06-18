import cv2
import numpy as np
import pytesseract
import mss
import os
from time import sleep
import pyautogui as py

# Caminho do Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

pixel_gatewaynotconfigured = (750, 465)
pixel_loginconfirmation = (750, 460)
pixel_onlinechangeconfirmation = (650, 490)
pixel_onlinechangewarning = (650, 490) # NAO SEI AINDA TEM QUE ADICIONAR
pixel_login = (547, 54)
pixel_logoff = (570, 53)

pixel_receitagvl = (277, 107)
pixel_rectesteline = (246, 670)
pixel_functionblockprg = (410, 110)
pixel_linechange = (797, 492)

region_clpstate = {"top": 750, "left": 450, "width": 100, "height": 15} # só le RUN (não identifica stop)
region_loginconfirmation = {"top": 390, "left": 545, "width": 335, "height": 40} # "Are you sure you want to login to the node ‘PH’ with address ‘0000'7"
region_onlinechangeconfirmation = {"top": 290, "left": 450, "width": 370, "height": 30} # "The application changed since last download, What do you want to do?"
region_onlinechangewarning = {"top": 290, "left": 450, "width": 370, "height": 30} # TEM QUE DESCOBRIR AINDA

def get_text_from_region(region, tesseract_cmd=r'C:\Program Files\Tesseract-OCR\tesseract.exe', debug_dir="debug_imgs"):

    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    with mss.mss() as sct:
        sct_img = sct.grab(region)
        img = np.array(sct_img)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        os.makedirs(debug_dir, exist_ok=True)
        cv2.imwrite(os.path.join(debug_dir, "captura.png"), img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(thresh, config=custom_config, lang='eng')
    return text

startrunning = False
recteste_iscommented = False
py.PAUSE = 0.3

while True:
    try:
        clp_state = get_text_from_region(region_clpstate)
        login_confirmation = get_text_from_region(region_loginconfirmation)
        online_change_confirmation = get_text_from_region(region_onlinechangeconfirmation)
        online_change_warning = get_text_from_region(region_onlinechangewarning)

        print(f"CLPState: {clp_state}")
        print(f"Login Confirmation: {login_confirmation}")
        print(f"Online Change Confirmation: {online_change_confirmation}")
        print()


        if startrunning is True:
            py.leftClick(pixel_login[0], pixel_login[1])
            sleep(1)
        elif 'RUN' in clp_state:
            print("Entrou em RUN! Esperando 10 segundos...")
            sleep(10)
            py.leftClick(pixel_logoff[0], pixel_logoff[1])
        elif 'Are you sure you want to login to the node' in login_confirmation:
            print("Confirmação de login! Apertando o botão...")
            py.leftClick(pixel_loginconfirmation[0], pixel_loginconfirmation[1])
            sleep(1)
        elif 'The application changed since last download, What do you want to do?' in online_change_confirmation:
            print("Confirmação de Online Change! Apertando o botão...")
            py.leftClick(pixel_onlinechangeconfirmation[0], pixel_onlinechangeconfirmation[1])
            sleep(1)
        elif 'SO MANY CHANGES OMG (algo assim)' in online_change_warning:
            print("Aviso de Online Change! Apertando o botão...")
            py.leftClick(pixel_onlinechangewarning[0], pixel_onlinechangewarning[1])
        else:
            # Implementar a lógica
            py.sleep(1)

            print("Alterando o projeto!")
            pixel = py.pixel(pixel_receitagvl[0], pixel_receitagvl[1])
            while (pixel != (255, 255, 255)):
                pixel = py.pixel(pixel_receitagvl[0], pixel_receitagvl[1])
                if pixel == (249, 249, 249):
                    py.leftClick(pixel_receitagvl[0], pixel_receitagvl[1])
                py.sleep(1)

            py.sleep(1)

            py.leftClick(pixel_rectesteline[0], pixel_rectesteline[1])
            
            if recteste_iscommented:
                py.write("Rec_Teste: INT;")
            else:
                py.hotkey("shift", "home")
                py.press("delete")


            py.sleep(1)
            pixel = py.pixel(pixel_functionblockprg[0], pixel_functionblockprg[1])
            while (pixel != (255, 255, 255)):
                pixel = py.pixel(pixel_functionblockprg[0], pixel_functionblockprg[1])
                if pixel == (247, 247, 247):
                    py.leftClick(pixel_functionblockprg[0], pixel_functionblockprg[1])
                py.sleep(1)
            
            py.sleep(1)

            py.leftClick(pixel_linechange[0], pixel_linechange[1])
            py.press("left")
            py.press("left")
            py.hotkey("ctrl", "backspace")
            if recteste_iscommented:
                py.write("Rec_Teste")  
            else:
                py.write("Rec_IDMisturadorAuxiliar")

            recteste_iscommented = not recteste_iscommented

            startrunning = True
    except Exception as e:
        print(f"Deu um erro: {e}")
            

