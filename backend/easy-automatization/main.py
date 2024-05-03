# If you need any other supported languages, run `brew install tesseract-lang`.
# import pyautogui
import pyautogui
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pynput import keyboard

from ..common.types import CloseAppException
from .actions import get_cursor_element, activate_cursor, on_close, display_all_images, solve_sudoku

# def test():
#     print('Starting Test...')
#     a = pyautogui.alert('Browser automatization started. Running global hotkeys...')
#     print(a)
#     print('Finishing Test...')
#     return a

        
if __name__ == '__main__':
    opt = Options()
    opt.add_experimental_option('debuggerAddress', 'localhost:8989')
    opt.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=opt)
    driver.get('https://manhuaus.com/manga/my-lucky-encounter-from-the-game-turned-into-reality/chapter-1/')
    # driver.get('https://w4.thebeginningaftertheend.live/manga/the-beginning-after-the-end-chapter-175/')
    # driver.get('https://harimanga.com/manga/vengeance-from-a-saint-full-of-wounds/')
    # driver.get('https://www.novelcool.com/chapter/Chapter-33-1/12098112/')

    try:
        with keyboard.GlobalHotKeys({
                '<ctrl>+<alt>+s': activate_cursor(driver),
                '<ctrl>+<alt>+g': get_cursor_element(driver),
                '<ctrl>+<alt>+l': display_all_images(driver),
                '<ctrl>+<alt>+q': on_close(),
                '<ctrl>+<alt>+v': solve_sudoku,
                # '<ctrl>+<alt>+t': test,
                }) as h:
            h.join()
    except CloseAppException as e:
        driver.close()
        driver.quit()
    except Exception as e:
        print(e)
        driver.close()
        driver.quit()






# # Read the image file and encode it as Base64
# with open("/Users/marcosrey/Desktop/ScreenTranslator/kanji.png", "rb") as f:
#     image_data = f.read()
#     base64_image = base64.b64encode(image_data).decode()

# # Construct a Data URL with the Base64-encoded image data
# data_url = f"data:image/png;base64,{base64_image}"

# # Execute JavaScript to update the src attribute of the image element
# script = f"""
# document.querySelector('img').src = '{data_url}';
# """
# driver.execute_script(script)



# >>> pyautogui.alert('This displays some text with an OK button.')
# >>> pyautogui.confirm('This displays text and has an OK and Cancel button.')
# 'OK'
# >>> pyautogui.prompt('This lets the user type in a string and press OK.')
# 'This is what I typed in.'