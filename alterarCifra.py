import re

print("\n\n\n")
# nomeArquivo = input("nomeArquivo: ")
nomeArquivo = input("Insira o nome do arquivo (sem a extensão): ")
arquivo = open("./cifras/"+nomeArquivo+".txt", "r", encoding="utf-8")
linhas = arquivo.readlines()
linhaCifra = True
prevEmpty = False

sizeHeader = 2

tomAtual = ""
idTomAtual = -1

proxTom = ""
idProxTom = -1

diffTons = -1
tipoEscala = ""

escala = {
	"maiores": [
		["C"],
		["C#", "Db"],
		["D"], 
		["D#", "Eb"],
		["E"], 
		["F"], 
		["F#", "Gb"],
		["G"], 
		["G#", "Ab"],
		["A"], 
		["A#", "Bb"],
		["B"]
	],
	"menores": [
		["Cm"], 
		["C#m", "Dbm"],
		["Dm"], 
		["D#m", "Ebm"],
		["Em"], 
		["Fm"], 
		["F#m", "Gbm"],
		["Gm"], 
		["G#m", "Abm"],
		["Am"], 
		["A#m", "Bbm"],
		["Bm"]
	]
}

def encontrarIdNota(tom):
	idTom = -1

	if(tom.find("M") == -1):
		# Tom maior
		tipoEscala = "maiores"
	else:
		# Tom menor
		tipoEscala = "menores"
		tom = tom.replace("M", "m")
	
	for f in range(0, len(escala[tipoEscala])):
		for f2 in range(0, len(escala[tipoEscala][f])):
			if(tom == escala[tipoEscala][f][f2]):
				idTom = f
				break
		
		if(idTom >= 0):
			break
	
	if(idTom == -1):
		print("Tom não encontrado.")
	
	return idTom


for f in range(sizeHeader):
	while((linhas[f][-1:] == " " or linhas[f][-1:] == "\n") and len(linhas[f]) > 0):
		linhas[f] = linhas[f][0:-1]

	if(linhas[f].find("Tom:") != -1):
		tomAtual = linhas[f][linhas[f].find("Tom:")+4:len(linhas[f])]
		tomAtual = tomAtual.replace(" ", "")

		idTomAtual = encontrarIdNota(tomAtual)
		if(idTomAtual == -1):
			quit()

while(idProxTom == -1):
	print("O tom atual é: "+tomAtual)
	proxTom = input("Para qual tom deseja converter? ")
	proxTom = proxTom.upper()

	idProxTom = encontrarIdNota(proxTom)

	diffTons = idProxTom-idTomAtual

print("\n\n\n")


print("Tom: "+proxTom+"\n")
underlines = []
for linha in linhas:
	# Pular as primeiras linhas, que representam o tom da música
	if(sizeHeader > 0):
		sizeHeader -= 1
		continue
	
	# Reconhecer se a linha atual é de cifra ou letra
	if(linha == ""):
		if(prevEmpty):
			linhaCifra = True
			prevEmpty = False
			continue
		prevEmpty = True
	else:
		prevEmpty = False

	# Retirar a quebra de linha do final
	if(linha[-1:] == "\n"):
		linha = linha[0: len(linha)-1]

	if(linhaCifra):
		# print(linha)
		
		novaLinha = ""
		
		notas = re.split("\s", linha)
		for nota in notas:
			if nota == "":
				continue
			nota = re.findall("[A-G]#?b?", nota)

			for f in range(0, len(nota)):
				idNota = encontrarIdNota(nota[f])
				idNovaNota = idNota+diffTons
				if(idNovaNota > 11):
					idNovaNota -= 12
				if(nota[f].find("b") != -1):
					novaNota = escala["maiores"][idNovaNota][1]
				else:
					novaNota = escala["maiores"][idNovaNota][0]
				
				
				linha = linha.replace(nota[f], novaNota, 1)
				novaLinha += linha[0:linha.find(novaNota)+len(novaNota)]
				linha = linha[linha.find(novaNota)+len(novaNota):]
				if(linha[0] != " "):
					if(linha[0] in ["#", "m"]):
						print("Inserir espaco")


				if(len(novaNota) != len(nota[f])):
					posEspaco = linha.find(" ")
					if(posEspaco != -1):
						if(len(novaNota) > len(nota[f])):
							linha = linha.replace(" ", "", 1)
						else:
							linha = linha[0:posEspaco]+" "+linha[posEspaco:]
							

		
		novaLinha += linha
		linha = ""
		print(novaLinha)
	else:
		print(linha)
	linhaCifra = not linhaCifra

print("\n\n\n\n\n\n")