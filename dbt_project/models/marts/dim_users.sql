{{ config(materialized='table') }}

with user_metrics as (
    select
        u.user_id,
        u.created_at as user_created_at,
        count(t.transaction_id) as total_transactions,
        min(t.created_at) as first_transaction_at,
        max(t.created_at) as last_transaction_at,
        case
            when count(t.transaction_id) = 0 then 'Never Activated'
            when max(t.created_at) < current_date - interval '90 days' then 'Churned'
            when count(t.transaction_id) >= 10 then 'High Activity'
            when count(t.transaction_id) >= 5 then 'Medium Activity'
            else 'Low Activity'
        end as user_segment
    from {{ ref('stg_users') }} u
    left join {{ ref('stg_transactions') }} t on u.user_id = t.user_id
    group by u.user_id, u.created_at
)

select
    user_id,
    user_created_at,
    total_transactions,
    first_transaction_at,
    last_transaction_at,
    user_segment,
    case
        when first_transaction_at is not null
        then extract(day from (first_transaction_at - user_created_at))
        else null
    end as days_to_first_transaction
from user_metrics