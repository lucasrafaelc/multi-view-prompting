import json
import os

CAMINHO_DATASET = "D:/Doutorado/SemEval2022/semeval22_structured_sentiment-master/data/"
CAMINHO_SAIDA = "C:\\Users\\Usuario\\Documents\\GitHub\\multi-view-prompting\\data\\ssa"

def extrai_expressao(contexto: str, lista_exprs: list) -> str:
    #print(len(lista_exprs[0]), lista_exprs)
    if len(lista_exprs[0]) == 0:
        return "NULL"
    elif len(lista_exprs[0]) == 1:
        return lista_exprs[0][0]
    else:
        min = 9999
        max = -1
        for par in lista_exprs[1]:
            i, s = par.split(":")
            i, s = int(i), int(s)
            if i < min:
                min = i
            if s > max:
                max = s
        #print(min, max)
        return contexto[min:max]

def cria_dataset(dataset_name):
    if not os.path.exists(os.path.join(CAMINHO_SAIDA, dataset_name)):
        os.mkdir(os.path.join(CAMINHO_SAIDA, dataset_name))
        
    for particao in ["dev", "test", "train"]:
        # Carrega o dataset original
        with open(os.path.join(CAMINHO_DATASET, dataset_name, particao + ".json"), "r") as o, open(os.path.join(CAMINHO_SAIDA, dataset_name, particao + ".txt"), "w", encoding="utf-8") as output_file:
            all_dataset = json.loads(o.read())
            for data_point in all_dataset:
                contexto = data_point["text"]
                saida = contexto + "####"
                grupo_tuplas = []
                lista_tuplas = data_point["opinions"]
                for tupla in lista_tuplas:
                    '''
                    if len(tupla["Source"][1]) > 1:
                        print(tupla["Source"])
                        print(extrai_expressao(contexto, tupla["Source"]))
                        print()
                    if len(tupla["Target"][1]) > 1:
                        print(tupla["Target"])
                        print(extrai_expressao(contexto, tupla["Target"]))
                        print()
                    if len(tupla["Polar_expression"][1]) > 1:
                        print(tupla["Polar_expression"])    
                        print(extrai_expressao(contexto, tupla["Polar_expression"]))
                        print()
                    '''
                    h = extrai_expressao(contexto,tupla["Source"])
                    a = extrai_expressao(contexto,tupla["Target"])
                    o = extrai_expressao(contexto,tupla["Polar_expression"])
                    p = tupla["Polarity"]
                    grupo_tuplas.append([h,a,o,p])
                        
                
                if len(grupo_tuplas) != 0:
                    saida += str(grupo_tuplas)
                    output_file.write(saida + "\n")
                

if __name__ == "__main__":
    #dataset_list = ['darmstadt_unis']
    dataset_list = ['norec', 'multibooked_ca', 'multibooked_eu', 'opener_es', 'opener_en', 'mpqa', 'darmstadt_unis']
    
    for dataset in dataset_list:
        cria_dataset(dataset)