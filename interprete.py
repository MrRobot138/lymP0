
#correr programa para verificar archivos


def lector_de_texto(archivo_path):
    file = open(archivo_path, "r")
    string_completo = file.read()
    string_completo = string_completo.replace("\n"," ").replace("\t"," ").lower()
    string_completo = string_completo.split(" ")
    string_completo = list(filter(None, string_completo))
    string_completo = " ".join(string_completo)
    i = 0
    while i < len(string_completo):
        if i > 1 and i < len(string_completo)-1:
            char1 = string_completo[i-1]
            char2 = string_completo[i]
            char3 = string_completo[i+1]
            if char1 == " " and char2 == ",":
                char1 = ""
            if char2 == "," and char3 == " ":
                char3 = ""
            if char1 == "{" and char2 == " ":
                char2 = ""
            if char2 == " " and char3 == "}":
                char2 = ""
    return " ".join(string_completo)

def lector(texto, metodosDeclarados, listaVariables, currentPos=0, correcto=True):
    currentWord = ""
    finishedWord = False
    while finishedWord == False and currentPos < len(texto) and correcto == True:
        if char != " ":
            char = texto[currentPos]
            currentWord += char
        else:
            finishedWord = True
            verificacion = (checkWord(finishedWord, currentPos, texto, listaVariables, metodosDeclarados))
            lector(texto, metodosDeclarados, listaVariables, currentPos+1, verificacion[0])
        currentPos += 1
    return correcto
            
def checkWord(word, currentPos, texto, listaVariables, metodosDeclarados, vocab):
    textoAVerificar = texto[currentPos-len(word): len(texto)]
    palabraLimpia = word.replace("{", "").replace("}","").replace(",","").replace(";","").replace("(","").replace(")","").replace(" ","")
    if palabraLimpia not in vocab or word not in listaVariables or word not in list(metodosDeclarados.keys()):
        correcto = False
    if word == "DefVar":
        correcto =verificacion_variables_declaradas(textoAVerificar, currentPos, listaVariables)
    elif word == "DefProc":
        correcto = verificacion_metodos_declarados(currentPos, textoAVerificar, listaVariables, metodosDeclarados)
    if "{" in word:
        correcto = (bloqueComandos(textoAVerificar, metodosDeclarados, listaVariables))
    if word in metodos_declarados:
        correcto = (verSimpleCommands(textoAVerificar, listaVariables, metodosDeclarados))
    elif "(" in word:
        correcto = parametros(textoAVerificar, listaVariables)
    return correcto
    
def verificacion_variables_declaradas(texto, pos1, lista_variables_declaradas):
    correcto = True
    lista = texto.split(" ")
    palabra2 = lista[pos1+1]
    palabra3 = lista[pos1+2]
    if palabra3 == None:
        correcto = False
    lista_variables_declaradas.append(palabra2)
    return correcto

def verificacion_metodos_declarados(pos1, texto, lista_variables,  dict_metodos):
    correcto = True
    lista = texto.split(" ")
    palabra2 = lista[pos1+1]
    palabra3 = lista[pos1+2]
    if palabra3 == None:
        correcto = False
    else:
        stringCompleto = texto[pos1: len(texto)]
        posParam = stringCompleto.index("(")
        nombreProc = texto[pos1 : posParam]
        correcto = anadirProc(nombreProc, stringCompleto, dict_metodos)
        bloque = stringCompleto[stringCompleto.index("{"): len(stringCompleto)]
        correcto = bloqueComandos(bloque, dict_metodos, lista_variables)
        
    return correcto

def verSimpleCommands(texto, lista_variables, dict_metodos):
    correcto = True
    if "(" in texto:
        pos_parametro = texto.index("(")
        nombre_metodo = texto[0:pos_parametro-1]
        if nombre_metodo in dict_metodos.keys():
            correcto = parametros(texto, lista_variables, dict_metodos[nombre_metodo])
        else:
            texto.split("=")
            if texto[1] not in lista_variables:
                correcto = False
    return correcto
        
    

def bloqueComandos(texto: str, dict_metodos, lista_variables_asignadas):
    correcto = True
    cerrado_parametros = False
    i = 0
    pos1 = 0
    pos2 = 0
    abiertos = 0
    while cerrado_parametros == False and i < texto:
        if texto[i] == "{":
            abierto_parametros = True
            pos1 = i
            abiertos += 1
        elif texto[i] == "}" and abierto_parametros == True:
            abiertos = abiertos -1
        elif texto[i] == "}" and cerrado_parametros == False:
            correcto = False
        if abiertos == 0:
            cerrado_parametros = True
            pos2 = i
        i += 1
    if abiertos > 0:
        correcto = False
    contenido = texto[pos1, pos2].replace("{", "").replace("}", "")
    metodos = contenido.split(";")
    for metodo in metodos:

        partes = metodo.split(" ")
        resto = partes.slice(1, len(partes)-1)
        resto = " ".join(resto)
        if partes[0] == "if":
            
            if "facing" in resto:
                correcto = parametros(resto, lista_variables_asignadas, dict_metodos["facing"])
            elif "can" in resto:
                correcto = parametros(resto, lista_variables_asignadas, dict_metodos["can"])
            elif "not" in resto:
                correcto = parametros(resto, lista_variables_asignadas, dict_metodos["not"])
        elif partes[0] == "while":
            if "facing" in resto:
                correcto = parametros(resto, lista_variables_asignadas, dict_metodos["facing"])
            elif "can" in resto:
                correcto = parametros(resto, lista_variables_asignadas, dict_metodos["can"])
            elif "not" in resto:
                correcto = parametros(resto, lista_variables_asignadas, dict_metodos["not"])
        elif partes[0] == "repeat":
                partesRepeticiones = resto.split(" ")
                if partesRepeticiones[1] != "times":
                    correcto = False
                else:
                    correcto = bloqueComandos(" ".join(partesRepeticiones, dict_metodos, lista_variables_asignadas))
        elif "(" in metodo:
            correcto = verSimpleCommands(metodo, lista_variables_asignadas, dict_metodos)
        else:
            correcto = False
    return correcto
            
def parametros(texto, lista_variables_asignadas, parametros_debidos):
    correcto = True
    cerrado_parametros = False
    i = 0
    pos1 = 0
    pos2 = 0
    abiertos = 0
    while cerrado_parametros == False and i < texto:
        if texto[i] == "(":
            abierto_parametros = True
            pos1 = i
            abiertos += 1
        elif texto[i] == ")" and abierto_parametros == True:
            abiertos = abiertos -1
        elif texto[i] == ")" and cerrado_parametros == False:
            correcto = False
        if abiertos == 0:
            cerrado_parametros = True
            pos2 = i
        i += 1
    if abiertos > 0:
        correcto = False
    contenido = texto[pos1, pos2].replace("(", "").replace(")", "")
    variables = contenido.split(",")
    
    if parametros_debidos != None:
        if len(variables) > parametros_debidos:
            correcto = False
    for variable in variables:
        if variable not in lista_variables_asignadas:
            correcto = False
    return correcto

def anadirProc(nombre, texto, dict_metodos):
    correcto = True
    cerrado_parametros = False
    i = 0
    pos1 = 0
    pos2 = 0
    abiertos = 0
    while cerrado_parametros == False and i < texto:
        if texto[i] == "(":
            abierto_parametros = True
            pos1 = i
            abiertos += 1
        elif texto[i] == ")" and abierto_parametros == True:
            abiertos = abiertos -1
        elif texto[i] == ")" and cerrado_parametros == False:
            correcto = False
        if abiertos == 0:
            cerrado_parametros = True
            pos2 = i
        i += 1
    contenido = texto[pos1, pos2].replace("(", "").replace(")", "")
    variables = contenido.split(",")
    parametros = len(variables)
    dict_metodos[nombre] = parametros
    return correcto

metodos_declarados = {
    "jump": 2, "walk": 2,
    "leap": 2,
    "turn": 1,
    "turnto": 1,
    "drop": 1,
    "get": 1,
    "grab": 1,
    "letGo": 1,
    "nop": 0,
}
listaVariables = ["0","1","2","3","4","5","6","7","8","9","10","11","12","north","west"]
vocab = ["{","}","(",")","if","repeat","times",";","while","not"]


print("por favor dijiste el archivo que desea verificar: ")
archivo = input("\n")
print("\n verificando archivo...")
x = lector(lector_de_texto(archivo)), metodos_declarados, listaVariables
print(f"el archivo es {x}")