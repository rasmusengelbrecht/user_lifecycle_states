WITH user_signup_months AS (
    SELECT 
        user_id,
        DATE_TRUNC('month', user_created_at) AS signup_month
    FROM {{ ref('dim_users') }}
),

user_activity_months AS (
    SELECT
        user_id,
        DATE_TRUNC('month', transaction_created_at) AS activity_month
    FROM {{ ref('fct_transactions') }}
    GROUP BY 1, 2
),

all_months AS (
    SELECT UNNEST(RANGE(DATE '2022-01-01', DATE '2023-01-01', INTERVAL 1 MONTH)) AS month
),

user_months_spine AS (
    SELECT
        u.user_id,
        u.signup_month,
        m.month
    FROM user_signup_months u
    CROSS JOIN all_months m
    WHERE m.month >= u.signup_month
),

user_monthly_activity AS (
    SELECT
        spine.user_id,
        spine.signup_month,
        spine.month,
        activity.user_id IS NOT NULL AS is_active,
        
        -- Track previous month activity
        COALESCE(LAG(activity.user_id IS NOT NULL, 1) OVER (
            PARTITION BY spine.user_id 
            ORDER BY spine.month
        ), FALSE) AS active_previous_month,
        
        -- Track activity 2 months ago
        COALESCE(LAG(activity.user_id IS NOT NULL, 2) OVER (
            PARTITION BY spine.user_id 
            ORDER BY spine.month
        ), FALSE) AS active_two_months_ago,
        
        -- Count total active periods up to this month
        SUM(CASE WHEN activity.user_id IS NOT NULL THEN 1 ELSE 0 END) OVER (
            PARTITION BY spine.user_id 
            ORDER BY spine.month 
            ROWS UNBOUNDED PRECEDING
        ) AS total_active_periods
    FROM user_months_spine spine
    LEFT JOIN user_activity_months activity
        ON spine.user_id = activity.user_id 
        AND spine.month = activity.activity_month
),

final AS (
    SELECT
        user_id,
        signup_month,
        month,
        is_active,
        active_previous_month,
        active_two_months_ago,
        total_active_periods,
        
        -- Determine user state
        CASE
            WHEN total_active_periods = 0 THEN 'Never Activated'
            WHEN total_active_periods = 1 AND is_active THEN 'New'
            WHEN is_active AND active_previous_month THEN 'Retained' 
            WHEN NOT is_active AND active_previous_month THEN 'Churned'
            WHEN is_active AND NOT active_previous_month AND active_two_months_ago AND total_active_periods > 1 THEN 'Reactivated'
            WHEN is_active AND NOT active_previous_month AND NOT active_two_months_ago AND total_active_periods > 1 THEN 'Resurrected'
            WHEN NOT is_active AND NOT active_previous_month THEN 'Dormant'
            ELSE 'Unknown'
        END AS user_state,
        
        -- Months since signup
        DATEDIFF('month', signup_month, month) AS months_since_signup
        
    FROM user_monthly_activity
)

SELECT
    user_id || '_' || month AS id,
    user_id,
    signup_month,
    month,
    is_active,
    user_state,
    months_since_signup
FROM final
ORDER BY user_id, month