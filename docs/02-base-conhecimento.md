# Base de Conhecimento

## Dados Utilizados

Descreva se usou os arquivos da pasta `data`, por exemplo:

| Arquivo | Formato | Para que serve o Sam? |
|---------|---------|---------------------|
| `dados_usuario.json` | JSON | Armazenar as informações fornecidas pelo usuário no formulário |
| `regras_classificacao.json` | JSON | Definir critérios para classificar o perfil financeiro do usuário |



---

## Adaptações nos Dados

Os dados foram adaptados para refletir a realidade de usuários sem organização financeira prévia.

Foi criado um modelo simplificado de dados contendo:
- Renda mensal
- Gastos fixos e variáveis
- Dívidas
- Informações sobre moradia e bens

Além disso, foi estruturado um modelo de classificação baseado nesses dados para permitir a análise do perfil financeiro do usuário.

---

## Estratégia de Integração

### Como os dados são carregados?
Os dados são coletados dinamicamente a partir de um formulário na interface (Streamlit) e convertidos em um objeto JSON durante a execução da aplicação.

Não há carregamento inicial de base fixa, pois os dados são fornecidos pelo próprio usuário em tempo real.

### Como os dados são usados no prompt?
Os dados do usuário são utilizados principalmente na lógica de negócio da aplicação para classificar o perfil financeiro.

Após a classificação, essas informações podem ser incluídas no contexto do prompt enviado ao modelo de linguagem, permitindo que o agente gere respostas personalizadas e contextualizadas.

A decisão principal (classificação do perfil) não é feita pelo modelo de linguagem, mas sim por regras determinísticas definidas no sistema.

---

## Exemplo de Contexto Montado

```
Dados do Usuário:
- Renda mensal: R$ 2.000
- Gastos fixos: R$ 1.200
- Gastos variáveis: R$ 500
- Dívidas: R$ 3.000
- Possui veículo: Sim
- Moradia: Alugada

Classificação do Perfil:
- Endividado

Ação sugerida:
- Foco na quitação de dívidas e controle de gastos
...
```
