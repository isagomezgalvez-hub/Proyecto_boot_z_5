# Conversor Cryptomonedas

Web App para almacenar las diferentes inversiones que realizamos en Criptomonedas conociendo su valor de mercado al conectar con la Api de Coinmarketcap

## Instalación

1. Ejecutar

```
pip install - r requirements.txt

```

2. Crear config.py

Renombrar `config_template.py` a `config.py` e informar correctamente sus claves.


3. Informar correctamente .env(opcional)

Renombrar `.env_template` a `.env` e informar las claves

	- FLASK_APP=run.py
	- FLASK_ENV= el que quieras `development` o `production`


4. Necesitas una clave Api key de Coinmarket para consultar el valor de tus criptos

Coinmarketcap te proporcionará una Api key para las diferentes consultas sobre el valor de las cryptomonedas.
Recuerda añadir tu clave Api en `config.py`

5. Necesitas una Secret Key para tu formulario WTF.

Recuerda añadir una clave Secreta a tu archivo `config.py`









