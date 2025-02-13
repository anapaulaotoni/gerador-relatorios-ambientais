# Carregar pacotes necessários
library(vegan)
library(ggplot2)
library(ggforce)
library(ggrepel)
library(dplyr)
library(readxl)
library(knitr)
library(kableExtra)
library(tidyr)
library(forcats)

# Função para calcular Índices Ecológicos
calcular_indices <- function(abundancias) {
  abundancias <- as.numeric(strsplit(abundancias, ",")[[1]])
  shannon <- diversity(abundancias, index = "shannon")
  simpson <- diversity(abundancias, index = "simpson")
  
  cat("Shannon:", shannon, "\\n")
  cat("Simpson:", simpson, "\\n")
}

# Função para análise da estrutura horizontal
analisar_estrutura_horizontal <- function(dados_file, area_ua, tipo_inventario) {
  dados <- read_excel(dados_file)
  
  # Definir tamanho da unidade amostral (m²)
  n_ua <- length(unique(dados$Parcela))
  A <- ifelse(tipo_inventario == "amostragem", area_ua * n_ua, area_ua)
  
  # Calcular área basal dos indivíduos
  dados$g <- pi * dados$DAP^2 / 40000
  
  # Contar número de indivíduos por espécie
  N <- table(dados$Especie)
  
  # Densidades absoluta e relativa
  DA <- N * 10000 / A
  DR <- DA / sum(DA) * 100
  
  # Frequências absoluta e relativa
  FA <- sapply(unique(dados$Especie),
               function(x) {
                 length(unique(subset(dados, dados$Especie == x)$Parcela)) / n_ua
               }) * 100
  FA <- FA[order(names(FA))]
  FR <- FA / sum(FA) * 100
  
  # Dominâncias absoluta e relativa
  DOA <- aggregate(dados$g, list(dados$Especie), sum)$x * 10000 / A
  DOR <- DOA / sum(DOA) * 100
  
  # Criar tabela de fitossociologia
  tabela_fito <- data.frame(Especie = names(N),
                            N = as.vector(N),
                            DA = round(as.vector(DA), 1),
                            DR = round(as.vector(DR), 1),
                            FA = round(as.vector(FA), 1),
                            FR = round(as.vector(FR), 1),
                            DoA = round(DOA, 1),
                            DoR = round(DOR, 1),
                            IVI = round(as.vector(DR + FR + DOR), 1))
  
  # Ordenar tabela pelo IVI
  tabela_fito <- tabela_fito[order(tabela_fito$IVI, decreasing = T),]
  
  # Salvar tabela em CSV
  write.csv(tabela_fito, "tabela_fitossociologica.csv", row.names = FALSE)
  
  # Criar gráfico de Valor de Importância (IVI)
  n_sp_plot <- 10
  tabela_fito_long <- tabela_fito %>%
    mutate(Especie = fct_reorder(Especie, IVI)) %>%
    select(Especie, DR, FR, DoR) %>%
    filter(Especie != 'NI') %>%
    filter(row_number() <= n_sp_plot) %>%
    pivot_longer(2:4, names_to = 'par', values_to = 'val')
  
  # Plotar gráfico
  iv_plot <- ggplot(tabela_fito_long, aes(x = Especie, fill = par)) +
    geom_bar(aes(y = val), stat = 'identity') +
    geom_text(aes(y = val, label = paste0(round(val), '%')), hjust = 1, nudge_y = -0.2) +
    coord_flip() +
    scale_fill_brewer(name = 'Parâmetro', palette = 'Set2') +
    labs(title = 'Valor de Importância de espécies', subtitle = paste0(n_sp_plot, ' espécies mais importantes')) +
    theme_minimal() +
    theme(axis.title = element_blank(), axis.text.y = element_text(face = 'italic'))
  
  ggsave("iv_plot.png", iv_plot, width = 8, height = 5, dpi = 300)
  
  cat("Análise de estrutura horizontal concluída!\\n")
}

# Função principal para rodar as análises
main <- function() {
  args <- commandArgs(trailingOnly = TRUE)
  abundancias <- args[1]
  dados_file <- args[2]
  quantidade_de_arvores <- as.numeric(args[3])
  area_ua <- as.numeric(args[4])
  tipo_inventario <- args[5]
  
  calcular_indices(abundancias)
  analisar_estrutura_horizontal(dados_file, area_ua, tipo_inventario)
}

# Executar a função principal
main()
