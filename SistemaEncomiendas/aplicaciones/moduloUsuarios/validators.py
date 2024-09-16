import re
from django.core.exceptions import ValidationError

#funcion verifica que el dui tenga el formato correcto y verifica si el dui es valido
def validar_dui(dui):
    # Verificar el formato del DUI usando una expresión regular
    if not re.match(r'^\d{8}-\d$', dui):
        raise ValidationError("El formato del DUI es inválido. Debe ser ########-#.")

    # Separar el número y el dígito verificador
    numero, digito_verificador = dui.split('-')
    numero = list(map(int, numero))
    digito_verificador = int(digito_verificador)
    # Calcular el dígito verificador
    suma = sum((9 - i) * numero[i] for i in range(8))
    digito_calculado = suma % 10
    # Comparar el dígito calculado con el dígito verificador
    if (10-digito_calculado) != digito_verificador:
        raise ValidationError("El DUI es inválido. Favor revisar nuevamente.")
    
def validar_telefono(telefono):
    if not re.match(r'^\d{4}-\d{4}$' , telefono):
        raise ValidationError("Formato de teléfono inválido. Debe ser ####-####.")
        
def validar_password(password):
    #al menos 8 caracteres
    if len(password) < 8:
        raise ValidationError("La contraseña debe tener al menos 8 caracteres.")
    
    #al menos una letra mayuscula
    if not re.search(r'[A-Z]',password):
        raise ValidationError("La contraseña debe contener al menos una letra mayúscula.")
    
    #al menos una letra minuscula
    if not re.search(r'[a-z]',password):
        raise ValidationError("La contraseña debe contener al menos una letra minúscula.")
    
    #al menos un numero
    if not re.search(r'[0-9]',password):
        raise ValidationError("La contraseña debe contener al menos un número.")
    
    #caracter especial
    if not re.search(r'[@#$%^&+=*]',password):
        raise ValidationError("La contraseña debe contener al menos un caracter especial (@, #, $, %, ^, &, +, =).")