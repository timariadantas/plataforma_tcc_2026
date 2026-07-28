#!/bin/bash

echo " Plataforma TCC - Runner E2E"


echo ""
echo "1) Executando fluxo completo via Shell..."
echo ""

./flows/platform-flow.sh

if [ $? -ne 0 ]; then
    echo ""
    echo "Erro durante o platform-flow.sh"
    exit 1
fi

echo ""
echo "2) Executando testes E2E em C#..."
echo ""

cd SalesPlatform.E2E.Tests

dotnet test

if [ $? -ne 0 ]; then
    echo ""
    echo "Os testes E2E falharam."
    exit 1
fi

echo ""

echo " Todos os testes executados com sucesso!"
