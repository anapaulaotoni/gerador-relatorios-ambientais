import matplotlib.pyplot as plt
import numpy as np

# Supondo que 'df' seja o DataFrame contendo as colunas 'Espécie', 'Altura (m)' e 'Diâmetro (cm)'

# Calcular altura e diâmetro médios por espécie
especies = df.groupby('Espécie').agg({'Altura (m)': 'mean', 'Diâmetro (cm)': 'mean'}).reset_index()

# Ordenar espécies por altura média para melhor visualização
especies = especies.sort_values(by='Altura (m)', ascending=False)

# Definir posições horizontais para as árvores
x_positions = np.linspace(1, len(especies) * 2, len(especies))

# Criar figura
fig, ax = plt.subplots(figsize=(12, 8))

for i, row in especies.iterrows():
    x = x_positions[i]
    altura = row['Altura (m)']
    dap = row['Diâmetro (cm)'] / 100  # Convertendo para metros
    copa_diametro = dap * 1.5  # Estimativa do diâmetro da copa

    # Desenhar tronco
    ax.plot([x, x], [0, altura], color='saddlebrown', linewidth=dap * 10)

    # Desenhar copa
    copa = plt.Circle((x, altura), copa_diametro / 2, color='green', alpha=0.6)
    ax.add_patch(copa)

    # Adicionar rótulo da espécie
    ax.text(x, altura + copa_diametro / 2 + 0.5, row['Espécie'], ha='center', fontsize=10, style='italic')

# Configurações finais do gráfico
ax.set_xlim(0, max(x_positions) + 1)
ax.set_ylim(0, especies['Altura (m)'].max() + 5)
ax.set_xlabel('Posição')
ax.set_ylabel('Altura (m)')
ax.set_title('Perfil Esquemático da Comunidade Florestal')
ax.axis('off')  # Opcional: remover os eixos para uma aparência mais limpa

plt.show()
