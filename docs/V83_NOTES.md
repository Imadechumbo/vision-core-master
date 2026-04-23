# V8.3 NOTES

## Entregue
- histórico paginado em `/api/integration/history?page=<n>&page_size=<n>`
- paginação também no dashboard
- limite configurável por página com clamp de segurança (`1..100`)
- retenção de histórico ampliada para 200 execuções

## Objetivo operacional
Permitir volume maior de execuções sem despejar todo o histórico em uma única resposta do dashboard/API.

## Regra central preservada
Sem PASS GOLD não existe promotion, merge, release nem stable.
