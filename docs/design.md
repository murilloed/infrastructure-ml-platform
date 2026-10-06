# Decisões de engenharia

## Escopo
Ingestão assíncrona, qualidade dos dados e processamento em lote. O cenário é um benchmark sintético independente.

## Entregas atuais
Fila asyncio limitada, validação, deduplicação transacional em SQLite, dead-letter persistente e métricas; adapters MongoDB e Spark opcionais; template AWS SAM para ingestão S3/SQS/Lambda com DLQ e IAM restrito ao bucket do projeto.

## Evolução
Testar adapters com serviços reais; executar Spark distribuído; orquestração Step Functions; treinamento em compute dedicado; API autenticada; monitoramento e custos; não há infraestrutura provisionada.

## Qualidade e colaboração
CI executa testes de comportamento. Revisões devem conferir contratos de entrada,
invariantes, divisão de dados e métricas. Evoluções de infraestrutura exigem avaliação
de custo, autorização e observabilidade. Não há recursos cloud provisionados.

## Limitações
Validar a hipótese com dados públicos licenciados ou dados autorizados antes de uso
operacional. Relatar baseline, várias sementes, intervalos de incerteza, consumo
de recursos e resultados negativos. O backlog não constitui funcionalidade implementada.
