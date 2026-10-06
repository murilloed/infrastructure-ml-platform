# Dados e MLOps para infraestrutura

Ingestão assíncrona, qualidade dos dados e processamento em lote.

**Status: MVP de pesquisa, v0.1.0.** Estudo de caso independente inspirado
em desafios dos setores relacionados à trajetória do autor (Marcopolo · SPData · AWS).
Não representa entrega contratada, resultado real ou endosso dessas organizações.
Todos os exemplos desta versão são sintéticos e reproduzíveis.

## Executar

```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -e .
python -m mlplatform.demo --events 200 --workers 4
python -m unittest discover -s tests -v
```

## Implementado

Fila asyncio limitada, validação, deduplicação transacional em SQLite, dead-letter persistente e métricas; adapters MongoDB e Spark opcionais; template AWS SAM para ingestão S3/SQS/Lambda com DLQ e IAM restrito ao bucket do projeto.

## Próximas etapas

Testar adapters com serviços reais; executar Spark distribuído; orquestração Step Functions; treinamento em compute dedicado; API autenticada; monitoramento e custos; não há infraestrutura provisionada.

## Reprodutibilidade e avaliação

A demonstração grava `artifacts/report.json`, com parâmetros e métricas.
Resultados de dados sintéticos validam o fluxo; não demonstram desempenho em produção.
Use a mesma semente e orçamento computacional para comparar abordagens.
Consulte `docs/design.md` para decisões e limitações.

## Contribuição

Abra uma issue com objetivo e critério de aceite. Entregue mudanças pequenas,
revisadas e acompanhadas de testes de comportamento. Não inclua dados de clientes,
credenciais ou resultados sem proveniência. Licença MIT para código e dados sintéticos próprios.
