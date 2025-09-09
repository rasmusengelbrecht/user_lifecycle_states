{{ config(materialized='view') }}

select
    transaction_id,
    user_id,
    created_at
from {{ source('raw_data', 'transactions') }}