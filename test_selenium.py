from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def iniciar_driver():
    options = Options()
    options.binary_location = "/usr/bin/chromium-browser"
    service = Service("/usr/bin/chromedriver")
    return webdriver.Chrome(service=service, options=options)

def login(driver, rol):
    driver.get("http://127.0.0.1:8000")

    wait = WebDriverWait(driver, 10)

    # click en rol
    botones = driver.find_elements(By.XPATH, f"//*[contains(.,'{rol}')]")

    boton = None
    for b in botones:
        if b.is_displayed():
            boton = b
            break

    driver.execute_script("arguments[0].click();", boton)

    wait.until(lambda d: "/inicio/" in d.current_url)

def obtener_menu(driver):
    elementos = driver.find_elements(By.TAG_NAME, "a")
    return [e.text for e in elementos if e.text.strip() != ""]

# -------------------------
# TEST ADMINISTRADOR
# -------------------------
driver = iniciar_driver()
login(driver, "Administrador")

menu_admin = obtener_menu(driver)
print("\n🔵 MENU ADMINISTRADOR:")
for m in menu_admin:
    print("->", m)

driver.quit()

# -------------------------
# TEST OPERADOR
# -------------------------
driver = iniciar_driver()
login(driver, "Operador")

menu_operador = obtener_menu(driver)
print("\n🟢 MENU OPERADOR:")
for m in menu_operador:
    print("->", m)

driver.quit()

# -------------------------
# COMPARACIÓN
# -------------------------
print("\n🔐 COMPARACIÓN DE PERMISOS")

admin_set = set(menu_admin)
operador_set = set(menu_operador)

solo_admin = admin_set - operador_set

print("Funciones que SOLO ve Admin:")
for f in solo_admin:
    print("->", f)