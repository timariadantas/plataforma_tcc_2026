#!/bin/bash

set -e


echo " Plataforma TCC - E2E Flow"
echo "==============================="

EMAIL="maria$(date +%s)@test.com"
echo " => Fluxo de Venda"
echo ""
echo "1) Criando cliente..."

curl -s -X POST http://localhost:5000/clients \
-H "Content-Type: application/json" \
-d "{
\"name\":\"Maria\",
\"surname\":\"Dantas\",
\"email\":\"$EMAIL\",
\"password\":\"123456\",
\"birthdate\":\"1999-05-20\"
}" > /dev/null

echo "Cliente criado."

echo ""
echo "2) Fazendo login..."

TOKEN=$(curl -s -X POST http://localhost:5000/auth/login \
-H "Content-Type: application/json" \
-d "{
\"email\":\"$EMAIL\",
\"password\":\"123456\"
}" | jq -r '.token')

echo "JWT recebido."

echo ""
echo "3) Criando produto..."

PRODUCT=$(curl -s -X POST http://localhost:5001/products \
-H "Authorization: Bearer $TOKEN" \
-H "Content-Type: application/json" \
-d '{
"name":"Notebook",
"description":"RTX",
"price":5000,
"quantity":10
}')

PRODUCT_ID=$(echo "$PRODUCT" | jq -r '.id')

echo "Produto criado."

echo ""
echo "4) Criando venda..."

SALE=$(curl -s -X POST http://localhost:5008/sales \
-H "Authorization: Bearer $TOKEN")

SALE_ID=$(echo "$SALE" | jq -r '.id')

echo "Venda criada."

echo ""
echo "5) Adicionando item..."

curl -s -X POST \
http://localhost:5008/sales/$SALE_ID/items \
-H "Authorization: Bearer $TOKEN" \
-H "Content-Type: application/json" \
-d "{
\"productId\":\"$PRODUCT_ID\",
\"quantity\":2
}" > /dev/null

echo "Item adicionado."

echo ""
echo "6) Finalizando venda..."

curl -s -X POST \
http://localhost:5008/sales/$SALE_ID/finish \
-H "Authorization: Bearer $TOKEN" > /dev/null

echo "Venda finalizada."

echo ""
echo "7) Consultando venda..."

curl -s \
http://localhost:5008/sales/$SALE_ID \
-H "Authorization: Bearer $TOKEN"

echo ""
echo ""
echo "Fluxo concluído com sucesso!"