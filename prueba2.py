import os  # Asegúrate de importar el módulo os
from PIL import Image

test_icon_path = os.path.join('C:\\Users\\erick\\Documents\\Proyecto-ASO\\icons', "wifi.png")
if os.path.exists(test_icon_path):
    print(f"El ícono existe: {test_icon_path}")
    try:
        test_icon = Image.open(test_icon_path)
        test_icon.show()  # Abrir el ícono con el visor predeterminado
    except Exception as e:
        print(f"No se pudo abrir el ícono: {e}")
else:
    print(f"No se encontró el ícono en: {test_icon_path}")
