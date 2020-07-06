from the_app import app
from the_app.form import CompraForm
from flask import render_template, request, redirect, url_for
from requests import Request, Session
from datetime import datetime

import requests, sqlite3,json


def SaldoCrypto():
		conn = sqlite3.connect(app.config['BASE_DATOS'])
		cur = conn.cursor()

		Saldo = "SELECT sum(to_quantity) from compras WHERE from_quantity = '{}'".format(request.values.get('MonedaFrom'))
		cantidadFrom=cur.execute(Saldo).fetchall()
		saldoFrom = cantidadFrom[0]

		Saldo = "SELECT sum(to_currency) from compras WHERE from_currency = '{}'".format(request.values.get('MonedaFrom'))
		cantidadTo=cur.execute(Saldo).fetchall()
		saldoTo = cantidadTo[0]
		
		if saldoFrom[0] is not None or saldoTo[0] is not None:

					if saldoFrom[0] and saldoTo[0] is not None:
						saldo = saldoFrom[0] - saldoTo[0]
						return float(saldo)

					elif saldoFrom[0] == None and saldoTo[0] is not None:
						saldo = saldoTo[0]
						return  float(saldo)

					else:
						saldo = saldoFrom[0]
						return float(saldo) 

		conn.close()
		

@app.route("/")
def index():
	conn = sqlite3.connect(app.config['BASE_DATOS'])
	cur = conn.cursor()

	hayregistros = "SELECT * FROM compras"
	registros=cur.execute(hayregistros).fetchall()
	
	try:
		if len(registros) == 0:
				return render_template('sinmovimientos.html')
					
		else:	
				query = "SELECT date,time,from_currency,from_quantity,to_currency,to_quantity,P_U from compras"
				movimientos= cur.execute(query).fetchall()
				return render_template('movimientos.html', movimientos=movimientos)
	except Exception as e:
				error_acceso = ('Se ha producido un error de acceso a la base de datos: {}'.format(e))
				return render_template('movimientos.html', acceso_base_datos= error_acceso)

	conn.close()


@app.route("/purchase", methods=['GET','POST'])
def purchase():
	
	now = datetime.now()
	time = str(now.time())
	time = time[0:8]

	form = CompraForm(request.form)

	if request.method == 'GET':
		return render_template('compras.html', form=form)

	elif request.form.get('rechazar'):
			return redirect(url_for("index"))

	
	else:
		if request.form.get('calcular'):
			if form.validate():
				APY = app.config['APY_KEY']
				URL = 'https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol={}&convert={}&CMC_PRO_API_KEY={}'
				respuesta = requests.get(URL.format(request.values.get('Q_Form'), request.values.get('MonedaFrom'), request.values.get('MonedaTo'),APY))
				
				#try:
				if respuesta.status_code == 200:
					json = respuesta.json()
			
					price =json.get('data').get('quote').get(request.values.get('MonedaTo'))['price']
					cantidad = request.values.get('Q_Form')
				
					price = float(price) 
					cantidad = float(cantidad)

		
					precio_unitario = price/cantidad

					form.Q_to.data = price
					form.P_U.data = precio_unitario

					price = round(price, 8)
					precio_unitario = round(precio_unitario, 8)
					
					
					return render_template('compras.html',form=form, price=price, precio_unitario=precio_unitario)
				
				#except Exception as e:
				else:
					error_api = ('Se ha producido un error al consultar el valor actual de su moneda. Inténtelo de nuevo o contacte con el administrador') 
					print("Error de consulta en API:", errorApi.get(resutls.status_code), errorApi.get(mensaje))
					return render_template('compras.html', form=form, acceso_error_api= error_api)
				
			else:
				return render_template('compras.html',form=form)
		
		elif request.form.get('rechazar'):
			return redirect(url_for("index"))

		else:
					if form.Q_to.data == '':
						 error = ('Por favor, pulsa el botón "CAL" para poder calcular el precio')
						 return render_template('compras.html', form=form, calculaPrecio=error)
					
					else:
						
						if form.validate():		
	
							conn = sqlite3.connect(app.config['BASE_DATOS'])
							cur = conn.cursor()

							consultaSaldo = SaldoCrypto()
							cantidadCompra = float(request.values.get('Q_Form'))
							if consultaSaldo > cantidadCompra:
								query = "INSERT INTO compras (date,time,from_currency,from_quantity,to_currency,to_quantity,P_U) values (?,?,?,?,?,?,?);"
								datos =(now.date(),time,request.values.get('MonedaFrom'), request.values.get('MonedaTo'), request.values.get('Q_Form'),round(float(form.Q_to.data), 8),round(float(form.P_U.data), 8))
							else:
								errorsaldo = ('Saldo insuficiente. No tienes suficiente cantidad de {} para comprar: {} - {}. Por favor, intentalo con una cantidad menor o con otra criptomoneda de la que disponga con más saldo.'.format(request.values.get('MonedaFrom'),request.values.get('Q_Form'),request.values.get('MonedaTo')))
								return render_template('compras.html',form=form, error_saldo=errorsaldo)
							try:
									cur.execute(query,datos)
									conn.commit()
									return redirect(url_for("index"))	
								

							except Exception as e:
									errorbd = ('Error de acceso a la base de datos: {}'.format(e))
									return render_template('compras.html',form=form, error_bd=errorbd)
							
							conn.close()

@app.route("/status")
def status():
	conn = sqlite3.connect(app.config['BASE_DATOS'])
	cur = conn.cursor()
	
	try:
			## Conocer la Inversión Atrapada
			consultasaldo = "SELECT sum(to_quantity) from compras WHERE from_quantity = 'EUR'"
			saldoEuros=cur.execute(consultasaldo).fetchall()
			saldoenEuros = saldoEuros[0]
			
			consultasaldo = "SELECT sum(to_currency) from compras WHERE from_currency = 'EUR'"
			invierteEuros=cur.execute(consultasaldo).fetchall()
			InvierteEuros = invierteEuros[0]

			Monedas = ("BTC", "ETH", "XRP", "LTC", "BCH", "BNB", "USDT", "EOS", "BSV", "XLM", "ADA", "TRX")
			
			## Almacenar la Inversión Atrapada
			d = {}
			for moneda in Monedas: 
				consultacryto = "SELECT sum(to_quantity) from compras WHERE from_quantity = '{}'".format(moneda)
				compraCrypto=cur.execute(consultacryto).fetchall()
				compracrypto = compraCrypto[0]

				consultacrypto = "SELECT sum(to_currency) from compras WHERE from_currency = '{}'".format(moneda)
				invierteCrypto=cur.execute(consultacrypto).fetchall()
				ICrypto = invierteCrypto[0]

				if compracrypto[0] is not None or ICrypto[0] is not None:

					if compracrypto[0] and ICrypto[0] is not None:
						d[moneda] = compracrypto[0] - ICrypto[0]

					elif compracrypto[0] == None and ICrypto[0] is not None:
						d[moneda] = ICrypto[0]

					else:
						d[moneda] = compracrypto[0]
				

			## Convertir a Euros la Inversión Atrapada
			Euros = []
			for key in d:

				APY = app.config['APY_KEY']
				URL = 'https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol={}&convert=EUR&CMC_PRO_API_KEY={}'
				respuesta = requests.get(URL.format(d.get(key),key,APY))
				json = respuesta.json()
				Euros.append(json.get('data').get('quote').get('EUR')['price'])

			SumaEuros = sum(Euros)
			IAEuros = round(SumaEuros,2)

			#Calcular el Valor Actual de la cantidad Invertida

			if saldoenEuros[0] == None:
				valorActual = InvierteEuros[0] + IAEuros

			elif InvierteEuros[0] == None:
				valorActual = saldoenEuros[0] + IAEuros

			else:
				valorActual = saldoenEuros[0] + InvierteEuros[0] + IAEuros

	
			return render_template('estado.html', saldoenEuros= InvierteEuros[0], valorActual = round(valorActual,2))

			
	except Exception as e:
					error_acceso = ('Se ha producido un error de acceso a la base de datos: {}'.format(e))
					return render_template('estado.html', acceso_base_datos= error_acceso)

	conn.close()






