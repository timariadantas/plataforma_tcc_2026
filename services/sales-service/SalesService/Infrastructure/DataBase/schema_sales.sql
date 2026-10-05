CREATE TABLE IF NOT EXISTS sales (
    id VARCHAR(36) PRIMARY KEY,
    client_id VARCHAR(36) NOT NULL,
    status VARCHAR(50) NOT NULL,

    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL,

    CONSTRAINT ck_sales_status
        CHECK (
            status IN (
                'Started',
                'Progress',
                'Done',
                'Canceled'
            )
        )
);

CREATE TABLE IF NOT EXISTS sale_items (
    sale_id VARCHAR(36) NOT NULL,
    product_id VARCHAR(36) NOT NULL,
    quantity INT NOT NULL,
    unit_price NUMERIC(18,2) NOT NULL,

    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL,

    CONSTRAINT pk_sale_items
        PRIMARY KEY (sale_id, product_id),

    CONSTRAINT fk_sale
        FOREIGN KEY (sale_id)
        REFERENCES sales(id)
);

-- Buscar vendas por cliente
CREATE INDEX IF NOT EXISTS idx_sales_client_id
ON sales(client_id);

-- Buscar itens de uma venda
CREATE INDEX IF NOT EXISTS idx_sale_items_sale_id
ON sale_items(sale_id);

-- Buscar vendas por produto
CREATE INDEX IF NOT EXISTS idx_sale_items_product_id
ON sale_items(product_id);
