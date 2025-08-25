CREATE OR REPLACE VIEW FACT_DAILY_STOCK_LEVELS AS 
WITH stock_movements AS (
  -- Get all supplier deliveries (stock increases)
  SELECT 
    fsd.PRODUCT_ID,
    fsd.DATE_KEY,
    fsd.QUANTITY_DELIVERED AS stock_change
  FROM FACT_SUPPLIER_DELIVERIES fsd
  
  UNION ALL
  
  -- Get all customer transactions (stock decreases)
  SELECT 
    ft.PRODUCT_ID,
    ft.DATE_KEY,
    -ft.QUANTITY AS stock_change  -- Negative because it reduces stock
  FROM FACT_TRANSACTIONS ft
),

daily_stock_changes AS (
  -- Aggregate all stock movements by product and date
  SELECT 
    PRODUCT_ID,
    DATE_KEY,
    SUM(stock_change) AS daily_change
  FROM stock_movements
  GROUP BY PRODUCT_ID, DATE_KEY
),

product_date_grid AS (
  -- Create a complete grid of all products and all dates
  SELECT 
    dp.PRODUCT_ID,
    dd.DATE_KEY
  FROM DIM_PRODUCTS dp
  CROSS JOIN DIM_DATES dd
),

complete_daily_changes AS (
  -- Left join to include all product-date combinations
  SELECT 
    pdg.PRODUCT_ID,
    pdg.DATE_KEY,
    COALESCE(dsc.daily_change, 0) AS daily_change
  FROM product_date_grid pdg
  LEFT JOIN daily_stock_changes dsc 
    ON pdg.PRODUCT_ID = dsc.PRODUCT_ID 
    AND pdg.DATE_KEY = dsc.DATE_KEY
),

stock_with_running_total AS (
  -- Calculate running stock balance
  SELECT 
    PRODUCT_ID,
    DATE_KEY,
    daily_change,
    SUM(daily_change) OVER (
      PARTITION BY PRODUCT_ID 
      ORDER BY DATE_KEY 
      ROWS UNBOUNDED PRECEDING
    ) AS available_stock
  FROM complete_daily_changes
)

-- Final result with product names and proper ordering
SELECT 
  swrt.DATE_KEY,
  swrt.PRODUCT_ID,
  --dd.DATE,
  swrt.daily_change AS STOCK_CHANGE,
  swrt.available_stock AS AVAILABLE_STOCK
FROM stock_with_running_total swrt;