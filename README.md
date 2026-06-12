# Pipeline-de-ETL-Base-de-Dados-Olist-
Projeto desenvolvido como parte dos meus estudos focados em Engenharia de Dados e Business Intelligence durante a graduação em Ciência de Dados.

# Pipeline de ETL e Analytics: Auditoria Financeira e Métricas de Pagamento (Olist)

## 📌 Sobre o Projeto
Este projeto simula um desafio real do cotidiano de um **Estagiário / Analista de Dados**. O objetivo principal foi construir um pipeline de dados de ponta a ponta (End-to-End) para auditar o comportamento de compra e os métodos de pagamento dos clientes utilizando uma base de dados real e complexa de e-commerce brasileiro.

O pipeline realiza a extração de dados brutos (relacionais), aplica transformações avançadas, higienização e tradução de esquemas utilizando **Python e Pandas**, e carrega o resultado de forma automatizada no **Power BI Desktop** para a criação de um dashboard executivo interativo.

---

## 💼 O Desafio de Negócio (Contexto)
O Diretor Financeiro da empresa precisava de um relatório detalhado para entender a distribuição do faturamento por meio de pagamento e a dinâmica de parcelamento no cartão. Além disso, a área de segurança acionou um sinal de alerta: **compras acima de R$ 5.000,00 realizadas via Boleto ou Cupom precisavam ser mapeadas imediatamente por risco de fraude.**

---

## 🛠️ Tecnologias e Ferramentas Utilizadas
* **Python 3.x** (Linguagem principal)
* **Pandas** (Manipulação e tratamento dos dados)
* **NumPy** (Otimização de lógica condicional vetorizada)
* **Power BI Desktop** (Modelagem visual e Dashboard interativo)

---

## ⚙️ Arquitetura do Pipeline (ETL)

### 1. Extração (Extract) & Tradução de Esquema
* Consumo de múltiplos arquivos `.csv` reais e anonimizados do ecossistema da **Olist** (Dados de Pedidos e Dados de Pagamentos).
* **Tradução de Colunas:** Para adequar o projeto ao mercado nacional, foi aplicado um dicionário de mapeamento logo após a leitura, convertendo colunas globais (`order_id`, `payment_value`, etc.) para o português nativo corporativo.

### 2. Transformação (Transform)
* **Modelagem Relacional:** Cruzamento das tabelas de fatos e dimensões usando chaves estrangeiras (`id_pedido`) através do método `pd.merge(how='inner')`.
* **Tratamento de Strings:** Padronização e tradução dos registros internos da coluna de pagamentos (Ex: `credit_card` -> `Cartão de Crédito`).
* **Tipagem Temporal:** Conversão de strings de texto para o formato correto de data (`pd.to_datetime`) nas colunas de controle logístico.
* ** Engenharia de Recursos (Feature Engineering) & Performance:** Criação da coluna condicional `possivel_fraude`. Em vez de utilizar estruturas lentas como `.apply()`, o pipeline foi otimizado utilizando o método **`np.where` com operadores lógicos bitwise**, garantindo execução vetorizada de alta performance na memória para os mais de 100 mil registros.

### 3. Carga (Load) & Automação Visual
* Exportação dos dados consolidados para um arquivo higienizado (`pedidos_pagamentos.csv`), omitindo índices desnecessários para otimizar o tamanho do arquivo.
* Conexão estruturada no **Power BI**, permitindo que o dashboard seja atualizado com apenas um clique toda vez que o script Python rodar e sobrescrever a base local.

---

## 📊 Dashboard & Insights Gerados

### Principais Conclusões do Negócio:
* **Faturamento por Canal:** O **Cartão de Crédito** lidera o faturamento da plataforma de forma disparada, seguido pelo Boleto Bancário.
* **Comportamento do Consumidor:** O comprador brasileiro utiliza uma taxa média de parcelamento de **3,51 vezes** ao optar pelo cartão de crédito.
* **Segurança da Informação:** O filtro dinâmico de risco de fraude permitiu à equipe financeira isolar instantaneamente os pedidos que necessitam de revisão manual antes do envio do produto.
