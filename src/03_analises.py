# Fazer scatter Soma xG por Gol.
# %%
import json
import pandas as pd
import sqlalchemy
import matplotlib.pyplot as plt
import seaborn as sn
from adjustText import adjust_text
from matplotlib.ticker import MaxNLocator
# %%
engine = sqlalchemy.create_engine("sqlite:///../data/database.db")

with open('jogadores.sql', 'r') as open_file:
    query = open_file.read()

df = pd.read_sql_query(query, engine)

df.columns.tolist()
# %%

# Soma xG por Gol
df = df[df['gols']>2]
plt.figure(dpi=500)

x ='gols'
y = 'somaXG'


sn.scatterplot(data=df,
               x= x,
               y= y
               )

df_filtered = df[df['gols'] >= 5]

# Cria uma lista para armazenar as anotações
texts = []

# Adiciona anotações para cada ponto no gráfico onde 'gols' >= 5
for i, row in df_filtered.iterrows():
    x_pos = row[x]
    y_pos = row[y]
    name = row['jogadorCodigoNome']
    texts.append(plt.text(x_pos, y_pos, name, fontsize=8))

adjust_text(texts,
                force_points=0.0002, force_text=0.4,
                expand_points=(0.5, 0.75), expand_text=(0.5, 0.75),
                arrowprops=dict(arrowstyle='->', color='black', lw=0.4),
                pull_threshold=10000
                )
# adjust_text(texts,
#             only_move={'points':'y','texts':'xy'},
#             arrowprops=dict(arrowstyle='->'))

plt.grid("True")
plt.suptitle("Jogadores Brasileirão 2024 - Gols por Soma xG")
plt.title("Até 15a Rodada. Apenas jogadores com 3 ou mais gols.",fontdict={'size':9})
plt.xlabel("Gols")
plt.ylabel("Soma xG")

# Ajusta a escala dos eixos
ax = plt.gca()  # Obtém o eixo atual
ax.xaxis.set_major_locator(MaxNLocator(integer=True))  # Define o eixo X para mostrar apenas inteiros
# ax.yaxis.set_major_locator(MaxNLocator(integer=False, prune='both', nbins='auto'))  # Define o eixo Y para mostrar incrementos de 0.5
ax.yaxis.set_major_locator(plt.MultipleLocator(0.5))
plt.savefig("../img/jogadores-gols-somaxG.png")

# %%

#Média de xG por totalChutes
plt.figure(dpi=500)

x ='totalChutes'
y = 'avgXG'


sn.scatterplot(data=df,
               x= x,
               y= y
               )

df_filtered = df[(df['avgXG'] >= 0.15) | (df['totalChutes']>=35)]

# Cria uma lista para armazenar as anotações
texts = []

# Adiciona anotações para cada ponto no gráfico onde 'gols' >= 5
for i, row in df_filtered.iterrows():
    x_pos = row[x]
    y_pos = row[y]
    name = row['jogadorCodigoNome']
    texts.append(plt.text(x_pos, y_pos, name, fontsize=8))

adjust_text(texts,
                force_points=0.0002, force_text=0.4,
                expand_points=(0.5, 0.75), expand_text=(0.5, 0.75),
                arrowprops=dict(arrowstyle='->', color='black', lw=0.4),
                pull_threshold=10000
                )
# adjust_text(texts,
#             only_move={'points':'y','texts':'xy'},
#             arrowprops=dict(arrowstyle='->'))

plt.grid("True")
plt.suptitle("Jogadores Brasileirão 2024 - Total de Chutes por Média de xG")
plt.title("Até 15a Rodada. Apenas jogadores com 3 ou mais gols.",fontdict={'size':9})
plt.xlabel("Total de Chutes")
plt.ylabel("Média de xG")

plt.savefig("../img/jogadores-totalChute-avgXG.png")
plt
# %%
