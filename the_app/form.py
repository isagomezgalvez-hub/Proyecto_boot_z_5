from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, HiddenField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError


#  validacion 
def validacion(form, field):
	if field.data ==form.MonedaFrom.data:
		raise ValidationError("No se puede realizar ninguna compra entre monedas iguales")
	elif field.data != "BTC" and form.MonedaFrom.data == "EUR":
		raise ValidationError("No es posible intercambiar EUR, por {}. Sólo puede comprar {}, con otras criptomonedas.".format(field.data,field.data ))
	elif field.data == "EUR" and form.MonedaFrom.data != "BTC":
		raise ValidationError("No es posible cambiar {} por EUR, directamente. Sólo es posible cambiar BTC por EUR. Si desea EUR, intercambie  antes sus {} a BTC y vuelva a intentarlo.".format(form.Moneda_from.data, form.Moneda_from.data))

Monedas = ("EUR", "BTC", "ETH", "XRP", "LTC", "BCH", "BNB", "USDT", "EOS", "BSV", "XLM", "ADA", "TRX")



class CompraForm(FlaskForm):
		
	MonedaFrom = SelectField(label='From:', choices=[(moneda, moneda) for moneda in Monedas])
	MonedaTo = SelectField(label='To:',choices=[(moneda, moneda) for moneda in Monedas], validators=[validacion])
	
	Q_Form = FloatField('Cantidad From:', validators=[DataRequired(message="En el campo Cantidad From debes introducir un número superior a 0")])
	
	Q_to = HiddenField('Cantidad to:')
	P_U = HiddenField('Precio Unitario:')

	#Botón Calculadora
	calcular = SubmitField('CAL')

	#Botón Aceptar
	aceptar = SubmitField('Aceptar')

	#Botón Rechazar
	rechazar = SubmitField('Cancelar')

	def validate_Q_Form(form, field):
		if field.data < 0:
			raise ValidationError('La cantidad From debe ser un número entero')