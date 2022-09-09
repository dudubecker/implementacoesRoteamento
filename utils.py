import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style('whitegrid')

### Função de obtenção de tabela com distâncias euclidianas calculadas!

def matriz_2d_distancias(problema, coords):

    """ Retorna um dataframe n x n com as distâncias euclidianas calculadas. """
    
    N = len(coords)
    
    lista_1d = []
    lista_2d = []
    
    if problema == 'CVRP':
        
        for i in range(1,len(coords)+1):
            lista_1d = []
            for j in range(1,len(coords)+1):
                d = np.linalg.norm(np.array(tuple(coords.loc[i]))-np.array(tuple(coords.loc[j]))) # função para a distância euclidiana
                lista_1d.append(d)
            lista_2d.append(lista_1d)

        df = pd.DataFrame(lista_2d, index=list(range(1,len(lista_2d)+1)), columns=list(range(1,len(lista_2d)+1)))

        return df

    
    else:
        
        for i in range(N):
            lista_1d = []
            for j in range(N):
                d = np.linalg.norm(np.array(tuple(coords.loc[i]))-np.array(tuple(coords.loc[j])))
                lista_1d.append(d)
            lista_2d.append(lista_1d)



        df = pd.DataFrame(lista_2d, index=list(range(len(lista_2d))), columns=list(range(len(lista_2d))))

        return df


### Função de obtenção de instâncias de CVRP

def CVRP_intancia(path):
    
    """CVRP: Retorna uma tupla na qual o primeiro objeto é um dataframe com a instância e o
    segundo objeto é um dicionário com os parâmetros do modelo"""

    
    string = open(path, 'r').read()
    
    K = int(string[string.find('No of trucks')+14:string.find('Optimal value')].replace(',','').split()[0]) # número de veículos
    
    Q = int(string[string.find('CAPACITY')+10:string.find('NODE_COORD_SECTION')].split()[0]) # capacidade
    
    coords = np.array(list(map(int,string[string.find('NODE_COORD_SECTION')+19:string.find('DEMAND_SECTION')].split()))) # coordenadas

    df = pd.DataFrame(coords.reshape(int(len(coords)/3), 3), columns=['Cliente','X','Y']).set_index('Cliente')

    df.index.name = None
    
    demandas = np.array(list(map(int,string[string.find('DEMAND_SECTION')+15:string.find('DEPOT_SECTION')].split()))) # demandas
    
    df['qtd'] = [demanda[1] for demanda in demandas.reshape(int(len(demandas)/2), 2)]
    
    dict_K_Q = dict(zip(['K','Q'],[K,Q]))
    
    return (df, dict_K_Q)



### Função de obtenção de instâncias de VRPTW

def VRPTW_instancia(path):
    
    """VRPTW: Retorna uma tupla na qual o primeiro objeto é um dataframe com a instância e o
    segundo objeto é um dicionário com os parâmetros do modelo"""
    
    string = open(path, 'r').read()
    
    k_Q = string[string.find('CAPACITY\n')+11:string.find('\n\nCUSTOMER\n')].split() # lista com n_trucks e capacidade
    
    dict_K_Q = dict(zip(['n_trucks','Q'],list(map(int,k_Q))))

    lista_coords = string[string.find('\n    0'):].split('\n')[1:]
    
    lista = list()
    
    for c in range(len(lista_coords)-1):
        
        
        split = lista_coords[c].split()
        
        if len(split) > 2:
        
            lista.append(split)

    df = pd.DataFrame([tuple(map(int,(row[1],row[2],row[3],row[4],row[5],row[6]))) for row in lista], columns=['XCOORD','YCOORD','DEMAND','READY TIME','DUE DATE','SERVICE'])
    
    return (df, dict_K_Q)



### Função de obtenção de instâncias de PDPTW

def PDPTW_instancia(path):
    
    """PDPTW: Retorna uma tupla na qual o primeiro objeto é um dataframe com a instância e o
    segundo objeto é um dicionário com os parâmetros do modelo"""

    string = open(path, 'r').read() # lendo o arquivo e separando em uma string com valores separados por "\n"
    
    lista_values = list(map(float, string.split()))
    
    n_requests = int(lista_values[1]) # como consta no README, o segundo valor corresponde ao número de requests
    
    Q = int(lista_values[3]) # como consta no README, o quarto valor corresponde à capacidade dos veículos
    
    df = pd.DataFrame(np.array(lista_values[5:]).reshape(n_requests*2 + 2, 7))[range(1,7)]
    
    df.columns = ['XCOORD','YCOORD','SERVICE','DEMAND','READY TIME','DUE DATE']
    
    return (df, {'n_requests': n_requests, 'Q': Q})

def plot_inst_PDPTW(df, instancia):
    
    df_plot = df.copy()
    
    df_plot['NODE_TYPE'] = ['Depot'] + ['Pickup' if demand >= 0 else 'Delivery' for demand in df_plot['DEMAND'] if demand != 0] + ['Depot']
    
    plt.figure(figsize=(15,10))
    
    sns.scatterplot(x=df_plot['XCOORD'],y=df_plot['YCOORD'], hue=df_plot['NODE_TYPE'])
    
    plt.title('Vértices da instância {}'.format(instancia), fontsize=20)
    
    plt.xlabel('X', fontsize=20)

    plt.ylabel('Y', fontsize=20)

    plt.legend(fontsize=16)
    plt.yticks(fontsize=16)
    plt.xticks(fontsize=16)

    plt.show()
    