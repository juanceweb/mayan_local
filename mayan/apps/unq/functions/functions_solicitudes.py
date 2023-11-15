import json

######################################################################################
# FUNCION QUE PASA A JSON LOS TUTORES
######################################################################################
def json_tutores(data):
    index = 0
    tutores_dict = {}

    try:
        while f"tutores[{index}][nombres]" in data:
            tutores_dict[index] =   {"nombres" : data[f"tutores[{index}][nombres]"],
                                    "apellido" : data[f"tutores[{index}][apellido]"],
                                    "username" : data[f"tutores[{index}][username]"]}
            index += 1

    except:
        tutores_dict = {}

    return json.dumps(tutores_dict)

######################################################################################
# FUNCION QUE PASA A JSON LOS DOCENTES
######################################################################################
def json_docentes(data):
    num = 0
    docentes_dict = {}

    try:
        while f"docentes[{num}][apellido_nombres]" in data:
            docentes_dict[num] =   {"apellido_nombres" : data[f"docentes[{num}][apellido_nombres]"],
                                    "email" : data[f"docentes[{num}][email]"]}
            num += 1

    except:
        docentes_dict = {}

    return json.dumps(docentes_dict)


######################################################################################
# FUNCION QUE PASA A JSON EL DOMICILIO
######################################################################################
def json_domicilio(data):
    domicilio_dict = {}

    try:
        for key in data:
            if "domicilio" == key[:9]:
                var = key[10:-1]
                value = data[f"domicilio[{var}]"]
                domicilio_dict[var] = value
    except:
        domicilio_dict = {}

    return json.dumps(domicilio_dict)
