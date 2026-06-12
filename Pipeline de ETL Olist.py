import pandas as pd
import numpy as np

# --- 1. EXTRAÇÃO ---
print("Carregando bases da Olist...")
tabela_1 = pd.read_csv(r"C:\Users\lucie\Downloads\archive (1)\olist_orders_dataset.csv")
tabela_2 = pd.read_csv(r"C:\Users\lucie\Downloads\archive (1)\olist_order_payments_dataset.csv")

# Dicionários de Tradução de Colunas
traducao_pedidos = {
    'order_id': 'id_pedido',
    'customer_id': 'id_cliente',
    'order_status': 'status_pedido',
    'order_purchase_timestamp': 'data_compra',
    'order_delivered_customer_date': 'data_entrega_real'
}

traducao_pagamentos = {
    'order_id': 'id_pedido',
    'payment_sequential': 'sequencial_pagamento',
    'payment_type': 'tipo_pagamento',
    'payment_installments': 'parcelas_pagamento', # Corrigido: o nome original no dataset é no plural 'payment_installments'
    'payment_value': 'valor_pagamento'
}

# Aplicando Tradução
tabela_1 = tabela_1.rename(columns=traducao_pedidos)
tabela_2 = tabela_2.rename(columns=traducao_pagamentos)

# --- 2. TRANSFORMAÇÃO ---
# Cruzamento (Merge)
df_pedidos_pagamentos = pd.merge(tabela_1, tabela_2, on='id_pedido', how='inner')

# Tradução dos registros internos da coluna (Substituindo a própria coluna para evitar duplicados)
forma_pagamento = {
    'debit_card': 'Cartão de Débito',
    'boleto': 'Boleto',
    'voucher': 'Cupom',
    'credit_card': 'Cartão de Crédito'
}
df_pedidos_pagamentos['tipo_pagamento'] = df_pedidos_pagamentos['tipo_pagamento'].map(forma_pagamento)

# Conversão de Datas
df_pedidos_pagamentos['data_compra'] = pd.to_datetime(df_pedidos_pagamentos['data_compra'])
df_pedidos_pagamentos['data_entrega_real'] = pd.to_datetime(df_pedidos_pagamentos['data_entrega_real'])

# --- 3. REGRAS DE NEGÓCIO (NP.WHERE CORRIGIDO) ---
# Condição: (Tipo igual a Cupom OU Tipo igual a Boleto) E Valor maior que 5000
condicao_fraude = (
    (df_pedidos_pagamentos['tipo_pagamento'] == 'Cupom') |
    (df_pedidos_pagamentos['tipo_pagamento'] == 'Boleto')
) & (df_pedidos_pagamentos['valor_pagamento'] > 5000)

df_pedidos_pagamentos['possivel_fraude'] = np.where(
    condicao_fraude,
    'necessita_revisao',
    'normal'
)

# --- 4. ANÁLISES PARA O DIRETOR ---
print("\n--- Resultados Financeiros ---")

# Faturamento por tipo de pagamento
df_total_pagamento = df_pedidos_pagamentos.groupby('tipo_pagamento')['valor_pagamento'].sum().sort_values(ascending=False)
print("Faturamento Total por Meio de Pagamento:\n", df_total_pagamento)

# CORREÇÃO: Média de PARCELAS para o Cartão de Crédito
# Agrupamos pela coluna 'parcelas_pagamento'
df_medias = df_pedidos_pagamentos.groupby('tipo_pagamento')['parcelas_pagamento'].mean()
parcelas_cartao_credito = df_medias['Cartão de Crédito']

print('\nQuantidade média de parcelas no Cartão de Crédito:')
print(f"{parcelas_cartao_credito:.2f} parcelas")

# --- 5. CARGA ---
df_pedidos_pagamentos.to_csv('pedidos_pagamentos.csv', index=False)
print('\nDados tratados e salvos com sucesso em "pedidos_pagamentos.csv"!')
