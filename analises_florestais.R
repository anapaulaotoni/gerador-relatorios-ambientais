# Carregar pacotes necessários
library(vegan)

# Índice de Shannon-Weaver
calcular_shannon <- function(abundancias) {
  abundancias <- as.numeric(strsplit(abundancias, ",")[[1]])
  return(diversity(abundancias, index = "shannon"))
}

# Índice de Simpson
calcular_simpson <- function(abundancias) {
  abundancias <- as.numeric(strsplit(abundancias, ",")[[1]])
  return(diversity(abundancias, index = "simpson"))
}

# Função principal para rodar as análises
main <- function() {
  args <- commandArgs(trailingOnly = TRUE)
  abundancias <- args[1]
  
  shannon <- calcular_shannon(abundancias)
  simpson <- calcular_simpson(abundancias)
  
  cat("Shannon:", shannon, "\\n")
  cat("Simpson:", simpson, "\\n")
}

# Executar a função principal
main()
