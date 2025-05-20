# Título - TPC4: Analisador Léxico

## Autor
Adélio José Ferreira Fernandes, A78778

## Resumo
Neste TPC, é pedido para se construir um analisador léxico para uma liguagem de query com a qual se podem escrever frases do
género:
# DBPedia: obras de Chuck Berry
select ?nome ?desc where {
?s a dbo:MusicalArtist.
?s foaf:name "Chuck Berry"@en .
?w dbo:artist ?s.
?w foaf:name ?nome.
?w dbo:abstract ?desc
} LIMIT 1000