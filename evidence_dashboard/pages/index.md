---
title: User Analytics Dashboard
---
Welcome to your user analytics dashboard.

## MAU

```sql mau
with monthly_totals as (
    select 
        month,
        count(*) as total_users,
        sum(case when is_active then 1 else 0 end) as active_users
    from user_states_monthly
    group by month
)
select 
    month,
    active_users as user_count,
    active_users / total_users as mau_percentage
from monthly_totals
```

<BarChart 
    data={mau}
    x="month"
    y="user_count"
    y2="mau_percentage"
    y2Fmt=pct0
    title="Monthly Active Users"
    labels=true
    yAxisTitle="Active Users"
    y2AxisTitle="MAU %"
    y2SeriesType=line
    chartAreaHeight=280
/>

## Monthly Dynamics

```sql monthly_dynamics
select 
    month,
    user_state,
    case 
        when user_state = 'Churned' then -count(*)
        else count(*)
    end as user_count
from user_states_monthly
where user_state in ('New', 'Retained', 'Reactivated', 'Resurrected', 'Churned')
group by month, user_state
order by month, user_state
```


<BarChart 
    data={monthly_dynamics}
    x="month"
    y="user_count"
    series="user_state"
    title="Monthly Users by State"
    colorPalette={[
        '#1d4ed8', // Blue for Retained  
        '#ef4444'  // Red for Churned
    ]}
    chartAreaHeight=280
/>

## Monthly Churn Rate

```sql churn_rate
select 
    month,
    sum(case when user_state = 'Churned' then 1 else 0 end) as churned_users,
    sum(case when user_state = 'Retained' then 1 else 0 end) as retained_users,
    sum(case when user_state = 'Churned' then 1 else 0 end) / 
    nullif(sum(case when user_state = 'Churned' then 1 else 0 end) + 
           sum(case when user_state = 'Retained' then 1 else 0 end), 0) as churn_rate
from user_states_monthly
group by month
order by month
```

<BarChart 
    data={churn_rate}
    x="month"
    y="churned_users"
    y2="churn_rate"
    title="Monthly Churn Rate: Churned / (Churned + Retained)"
    yAxisTitle="# Churned Users"
    y2AxisTitle="Churn Rate"
    y2Fmt=pct
    y2SeriesType=line
    chartAreaHeight=280
    labels=true
/>


## Pulse Ratio

What it measures:
- Pulse above 1 = More users being acquired/recovered than churning (healthy growth)
- Pulse below 1 = More users churning than being acquired/recovered (concerning trend)
- Pulse = 1 = Balanced - equal acquisition/recovery and churn



```sql pulse_ratio
select 
    month,
    sum(case when user_state = 'New' then 1 else 0 end) as new_users,
    sum(case when user_state = 'Reactivated' then 1 else 0 end) as reactivated_users,
    sum(case when user_state = 'Resurrected' then 1 else 0 end) as resurrected_users,
    sum(case when user_state = 'Churned' then 1 else 0 end) as churned_users,
    (sum(case when user_state = 'New' then 1 else 0 end) + 
     sum(case when user_state = 'Reactivated' then 1 else 0 end) +
     sum(case when user_state = 'Resurrected' then 1 else 0 end)) / 
    nullif(sum(case when user_state = 'Churned' then 1 else 0 end), 0) as pulse_ratio
from user_states_monthly
where month >= '2022-03-01'
group by month
order by month
```

<LineChart 
    data={pulse_ratio}
    x="month"
    y="pulse_ratio"
    title="Pulse Ratio: (New + Reactivated + Resurrected) / Churned"
    yAxisTitle="Pulse Ratio"
    chartAreaHeight=280
>
    <ReferenceArea yMin=1 yMax=10 label="Healthy (Pulse > 1)" color=positive labelPosition=center/>
    <ReferenceArea yMin=0 yMax=1 label="Concerning (Pulse < 1)" color=negative labelPosition=center/>
    <ReferenceLine y=1 label="Break-even (Pulse = 1)" labelPosition=aboveStart/>
</LineChart>


## The underlying data

### user_states_monthly

```sql user_states_monthly
select * from user_states_monthly
```

<DataTable data={user_states_monthly}>
</DataTable>


### Users

```sql users_data
select * from users
```

<DataTable data={users_data}>
</DataTable>

### Transactions

```sql transactions_data
select * from transactions
```

<DataTable data={transactions_data}>
</DataTable>