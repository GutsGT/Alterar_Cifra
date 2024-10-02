import re

while(True):
	print("\n\n\n")
	nomeArquivo = input("Insira o nome do arquivo (sem a extensão): ")
	arquivo = open("./cifras/"+nomeArquivo+".txt", "r", encoding="utf-8")
	linhas = arquivo.readlines()
	novasLinhas = ""
	linhaCifra = True

	sizeHeader = 1
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

		if(tom.find("m") > 0):
			tipoEscala = "menores"
		else:
			tipoEscala = "maiores"
		
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


	# Encontrar o tom atual da cifra:
	for f in range(sizeHeader):
		while((linhas[f][-1:] == " " or linhas[f][-1:] == "\n") and len(linhas[f]) > 0):
			linhas[f] = linhas[f][0:-1]


		if(linhas[f].find("Tom:") != -1):
			tomAtual = linhas[f][linhas[f].find("Tom:")+4:len(linhas[f])]
			
			tomAtual = tomAtual.replace(" ", "")
			print(tomAtual)

			idTomAtual = encontrarIdNota(tomAtual)
			if(idTomAtual == -1):
				quit()


	# Perguntar o próximo tom da cifra para o usuário
	while(idProxTom == -1):
		print("O tom atual é: "+tomAtual)
		proxTom = input("Para qual tom deseja converter? ")
		# proxTom = proxTom.upper()

		idProxTom = encontrarIdNota(proxTom)

		diffTons = idProxTom-idTomAtual


	print("\n\n\n")
	novasLinhas += "Tom: "+proxTom+"\n";
	for f in range(0, len(linhas)):
		# Pular a(s) primeira(s) linha(s), que representa(m) o tom da música
		if(sizeHeader > 0):
			sizeHeader -= 1
			continue
		
		# Reconhecer se a linha atual é de cifra ou letra
		# pattern = "([A-G]+([^( ,a-zá-ù)]|[#mb]+( *(^[a-z]|[A-Z]|[2-9]|\n)))|( [A-G] )|([A-G]\s*\n))"
		# pattern = "/([A-G]+([#|m|b|°|\d]?)+(\)|M)?)*\n/g"
		pattern = "(?!( ))+[A-G]+((m|#|b|°|((((Maj)?)+\d+((M|\+)?))|\+|aug)|(-)|(add)|(dim)|\(|\)|\/)*3?)+((\/+[A-G]+(b|#)?)?)+( )*?\n"
		linhaCifra = (re.search(pattern, linhas[f]) != None)
		
		
		# Retirar a quebra de linha do final
		if(linhas[f][-1:] == "\n"):
			linhas[f] = linhas[f][0: len(linhas[f])-1]
		
		
		novaLinha = ""
		if(linhaCifra):	
			notas = re.split(r"\s", linhas[f])
			for nota in notas:
				if nota == "":
					continue
				nota = re.findall("[A-G]#?b?", nota)

				for f2 in range(0, len(nota)):
					idNota = encontrarIdNota(nota[f2])
					idNovaNota = idNota+diffTons
					if(idNovaNota > 11):
						idNovaNota -= 12
					if(nota[f2].find("b") != -1 and len(escala["maiores"][idNovaNota]) > 1):
						novaNota = escala["maiores"][idNovaNota][1]
					else:
						novaNota = escala["maiores"][idNovaNota][0]
					
					# Faz a substituição da nota
					linhas[f] = linhas[f].replace(nota[f2], novaNota, 1)
					novaLinha += linhas[f][0:linhas[f].find(novaNota)+len(novaNota)]
					linhas[f] = linhas[f][linhas[f].find(novaNota)+len(novaNota):]
					
					
					posEspaco = linhas[f].find(" ")
					if(posEspaco != -1):
						if(len(novaNota) > len(nota[f2])):
							linhas[f] = linhas[f].replace(" ", "", 1)
						elif(len(novaNota) < len(nota[f2])):
							linhas[f] = linhas[f][:posEspaco]+" "+linhas[f][posEspaco:]

					
					posDivisao = (len(novaLinha)-len(novaNota))
					if((novaLinha[0:posDivisao][-1:] not in [" ", "/"]) and posDivisao > 0):
						if(len(linhas[f+1][posDivisao-1:]) > 0 and linhas[f+1][posDivisao-1:][0] != " "):
							linhas[f+1] = linhas[f+1][0:posDivisao]+"_"+linhas[f+1][posDivisao:]
						else:
							linhas[f+1] = linhas[f+1][0:posDivisao]+" "+linhas[f+1][posDivisao:]	
						novaLinha = novaLinha[0:posDivisao]+" "+novaLinha[posDivisao:]
								

			
			novaLinha += linhas[f]
			linhas[f] = ""
		else:
			novaLinha = linhas[f]

		novasLinhas += novaLinha+"\n"

	print(novasLinhas)
	print("\n\n\n")

	salvar = ""
	while(salvar not in ["s", "n"]):
		salvar = input("Deseja salvar essa versão?(s/n)\n")
		if(salvar not in ["s", "n"]):
			print("Opção inválida")
	
	if(salvar == "s"):
		novoArquivo = open("./cifras/"+nomeArquivo+"_"+proxTom+".txt", "w", encoding="utf-8")
		novoArquivo.write(novasLinhas)
		novoArquivo.close()
	
	alterarProxima = ""
	while(alterarProxima not in ["s", "n"]):
		alterarProxima = input("Deseja converter outra cifra?(s/n)\n")
		if(alterarProxima not in ["s", "n"]):
			print("Opção inválida")
	if(alterarProxima == "n"):
		break;

	print("\n\n\n\n\n\n")

print("Obrigado, tenha um bom dia :)")