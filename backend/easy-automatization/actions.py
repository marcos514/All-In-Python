import base64
import json
import cv2
import pyautogui
from pynput import mouse

from selenium.webdriver.common.by import By

from ..common.types import CloseAppException
from ..common.image.manipulator import img_to_base64, translate_text_boxes
from ..common.image.reader import url_to_image, image_to_df_text_data, get_text_positions


def activate_cursor(driver):
    def activate():
        print('Started onmousemove event')
        script = """
            document.addEventListener('mousemove', e => {
            localStorage.setItem('cursorPosition',JSON.stringify({'x':e.clientX, 'y':e.clientY }))
            let cursorPosition = JSON.parse(localStorage.getItem('cursorPosition'))
        }, {passive: true})
        """
        driver.execute_script(script)
        print('Finished onmousemove event')

    return activate

def get_cursor_element(driver):
    def activate():
        print('Started LocalStorage')
        local_storage_value = json.loads(driver.execute_script("return localStorage.getItem('cursorPosition');"))
        script = """
            console.log('arguments')
            console.log(arguments)
            var element = document.elementFromPoint(arguments[0], arguments[1]);
            return element;
        """
        element = driver.execute_script(script, local_storage_value['x'], local_storage_value['y'])
        if element:
            if element.tag_name == "img":
                src = element.get_attribute("src")
                img = url_to_image(src, is_online=True,)
                # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                # a = driver.execute_script("return prompt('Enter language of the image','eng')")
                img_df = image_to_df_text_data(img)
                sentences_places = get_text_positions(img_df)
                translate_text_boxes(img, sentences_places, target='spanish')

                base64_img = img_to_base64(img, '.jpg')
                driver.execute_script(f"arguments[0].setAttribute('src','data:image/png;base64,'+ arguments[2])", element, '.jpg', base64_img)
                # extension = src.split('.')[-1]
                
                # driver.execute_script(f"arguments[0].setAttribute('src','data:image/png;base64,'+ arguments[2])", element, extension, base64_img)
                return element
        else:
            print(f"No element found at position ({local_storage_value})")    
    return activate

def display_all_images(driver):
    def activate():
        print('display all images')
        # lwe: list[WebElement] = driver.findElements(By.cssSelector("img"));
        # r:list[WebElement] = driver.find_elements_by_tag_name('img')
        imgResults = driver.find_elements(By.TAG_NAME,"img")

        uri = []
        for v in imgResults:
            src = v.get_attribute("src")
            uri.append(src)
            # pos = len(src) - src[::-1].index('/')
            # print(pos)
            # g=urllib.urlretrieve(src, "/".join([folder, src[pos:]]))
        print('\n\n\nuri')
        print(uri)

    return activate
    

def solve_sudoku():
    start_x, start_y = pyautogui.position()
    def on_click(x, y, button, pressed):
        screenshot = pyautogui.screenshot(region=(
            start_x,
            start_y,
            int(x) - start_x,
            int(y) - start_y))
        screenshot.save('zzzZ_screenshot_from_cursor_1.png')
        return False
                
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()

def on_close():
    def activate():
        raise CloseAppException('Clossing app')
    return activate