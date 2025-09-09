{{ config(materialized='table') }}

with transaction_enriched as (
    select
        t.transaction_id,
        t.user_id,
        t.created_at as transaction_created_at,
        u.created_at as user_created_at,
        extract(year from t.created_at) as transaction_year,
        extract(month from t.created_at) as transaction_month,
        extract(dow from t.created_at) as transaction_day_of_week,
        extract(day from (t.created_at - u.created_at)) as days_since_signup,
        row_number() over (partition by t.user_id order by t.created_at) as user_transaction_number
    from {{ ref('stg_transactions') }} t
    join {{ ref('stg_users') }} u on t.user_id = u.user_id
)

select
    transaction_id,
    user_id,
    transaction_created_at,
    user_created_at,
    transaction_year,
    transaction_month,
    transaction_day_of_week,
    days_since_signup,
    user_transaction_number,
    case
        when user_transaction_number = 1 then 'First Transaction'
        when user_transaction_number <= 5 then 'Early Transaction'
        else 'Recurring Transaction'
    end as transaction_type
from transaction_enriched