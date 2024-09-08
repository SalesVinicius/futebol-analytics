# %%
import pandas as pd
import sqlalchemy
import matplotlib.pyplot as plt
from mplsoccer import VerticalPitch, Pitch
import matplotlib.font_manager as font_manager



engine = sqlalchemy.create_engine("sqlite:///../data/database.db")

with open('chutes.sql', 'r') as open_file:
    query = open_file.read()

df = pd.read_sql_query(query, engine)

df['coordenadaXX'] = 100 - df['coordenadaX'] # inversão para entrar no formato do pitch desejado
df['coordenadaYY'] = 100 - df['coordenadaY'] # inversão para entrar no formato do pitch desejado

# Jogador que mais finaliza.
df_chutes=df.groupby(by=['jogadorId','jogadorNome'])['resultadoChute'].count().sort_values(ascending=False)

idx_max = df_chutes.idxmax()
nome_jogador_max = idx_max[1]
nome_jogador_max


df_shotmap = df[df['jogadorNome']==nome_jogador_max]

# Estatísitcas
total_chutes = df_shotmap.shape[0] #número de linhas
total_gols = df_shotmap[df_shotmap['resultadoChute'] == 'goal'].shape[0]
totalxG = df_shotmap['xG'].sum()
xg_p_chute = totalxG/total_chutes

# %%
background_color = '#3C3940'
gol_color = '#73141B'
font_path = ('../font/static/Montserrat-Regular.ttf')
font_props = font_manager.FontProperties(fname=font_path)

fig = plt.figure(figsize=(8,12))
fig.patch.set_facecolor(background_color)

ax1 = fig.add_axes([0, .7, 1, .2])
ax1.set_facecolor(background_color)
ax1.set_xlim(0,1)
ax1.set_ylim(0,1)
#Nome Jogador
ax1.text(
    x=.5,
    y=.75,
    s=nome_jogador_max,
    fontsize = 20,
    fontproperties=font_props,
    fontweight='bold',
    color = 'white',
    ha = 'center'
)
# Subtitulo do gráfico
ax1.text(
    x=.5,
    y=.65,
    s='Todos os Chutes no Brasileirão 2024 até Rodada 15',
    fontsize = 14,
    fontproperties=font_props,
    fontweight='bold',
    color = 'white',
    ha = 'center'
)
gollegendlX =.41
gollegendY =.2
#Gol
ax1.text(
    x=gollegendlX,
    y=gollegendY,
    s='Gol',
    fontsize = 12,
    fontproperties=font_props,
    fontweight='bold',
    color = 'white',
    ha = 'right'

)
ax1.scatter(
    x=gollegendlX + 0.03,
    y=gollegendY+0.03,
    s=200,
    color=gol_color,
    edgecolor='white',
    linewidth=0.8,
    alpha=0.7
)
#Não Gol
ax1.text(
    x=gollegendlX + .15,
    y=gollegendY,
    s='Não Gol',
    fontsize = 12,
    fontproperties=font_props,
    fontweight='bold',
    color = 'white',
    ha = 'right'
)
ax1.scatter(
    x=gollegendlX+0.17,
    y=gollegendY+0.03,
    s=200,
    color=background_color,
    edgecolor='white',
    linewidth=0.8,
    alpha=0.7
)

ax1.set_axis_off()

ax2 = fig.add_axes([.05, .25, .9, .5])
ax2.set_facecolor(background_color)

pitch = VerticalPitch(
    pitch_type='opta',
    half = True,
    pitch_color= background_color,
    pad_bottom=.5,
    line_color='white',
    linewidth= .75,
    axis=True,
    label=True,
    
)

# pitch = Pitch(pitch_type='opta',

#               axis=True,
#               label=True,
#               pitch_color= background_color,
#               pad_right=-75

#             )

pitch.draw(ax=ax2)

for index, row in df_shotmap.iterrows():
    plt.scatter(
        y=row['coordenadaXX'],
        x =row['coordenadaYY'],
        color=gol_color if row['resultadoChute']=='goal' else background_color,
        s=700 * row['xG'],
        alpha=0.7,
        edgecolors='white',
        linewidth = .8
    )

ax2.set_axis_off()

plt
# %%
plt.savefig("../img/chute-vegetti.png")
