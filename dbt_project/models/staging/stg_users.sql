{{ config(materialized='view') }}

select
    user_id,
    created_at
from {{ source('raw_data', 'users') }}