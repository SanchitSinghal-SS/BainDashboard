import streamlit as st
import matplotlib.pyplot as plt

# Function to calculate effective production hours and repair costs


def calculate_metrics(capacity_utilization, repair_cost, revenue, cogs, repair_time):
    effective_production_hours = (
        1 - repair_time / 100) * capacity_utilization * 24 * 365
    repair_costs = repair_cost / 100 * cogs
    revenue_change = effective_production_hours * revenue / 1000000 - repair_costs

    return effective_production_hours, repair_costs, revenue_change

# Main Streamlit app


def main():
    st.title('Equipment Reconfiguration Impact Analysis')

    # Input variables panel
    st.sidebar.header('Input Variables (Initial Position of ABC Ltd.):')
    capacity_utilization = st.sidebar.slider(
        'Capacity Utilization (%)', 0, 100, 71)
    repair_cost = st.sidebar.number_input(
        'Repair Cost (Per Hour Wage Rate of Labour)', value=24)
    repair_time = st.sidebar.slider('Repair Time (%)', 0, 100, 15)
    revenue = st.sidebar.number_input('Revenue ($ million)', value=19)
    cogs = st.sidebar.number_input('COGS ($ million)', value=16)

    # Calculate metrics
    effective_hours_without_reconfig, repair_costs_without_reconfig, revenue_change_without_reconfig = calculate_metrics(
        capacity_utilization, repair_cost, revenue, cogs, repair_time
    )

    effective_hours_with_reconfig, repair_costs_with_reconfig, revenue_change_with_reconfig = calculate_metrics(
        capacity_utilization, repair_cost, revenue, cogs, 5
    )

    # Display graph
    st.header('Revenue Change Comparison:')
    fig, ax = plt.subplots(figsize=(12, 6))
    labels = ['Without Reconfiguration', 'With Reconfiguration']
    revenue_changes = [revenue_change_without_reconfig,
                       revenue_change_with_reconfig]
    bars = ax.bar(labels, revenue_changes, color=['skyblue', 'lightgreen'])

    # Add data labels to the bars
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval + 0.1,
                f'{yval:.2f}', ha='center', va='bottom')

    ax.set_ylabel('Revenue Change ($ million)')
    ax.set_title('Revenue Change Comparison')
    st.pyplot(fig)

    # Display results
    st.header('Results:')
    st.markdown('<p style="color: #808080;">Here we have assumed that cost as % of revenue remains same.</p>',
                unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.subheader('Without Equipment Reconfiguration (Base Case):')
        data = {
            'Metric': ['Total Production Hours (Yearly)', 'Downtime', 'Effective Production Hours',
                       'Revenue ($ million)', 'Cost ($ million)', 'Repair Costs ($ million)'],
            'Value': [
                f'{(capacity_utilization/100 * 24 * 365):.1f} hours',
                f'{(repair_time/100*capacity_utilization/100 * 24 * 365):.1f} hours',
                f'{(capacity_utilization/100 * 24 * 365-repair_time / 100*capacity_utilization/100 * 24 * 365):.1f} hours',
                f'{revenue:.1f} million',
                f'{cogs:.1f} million',
                f'{repair_time/100*capacity_utilization /100 * 24 * 365*repair_cost/1000000:.2f} million'
            ]
        }

# Display the table
        st.table(data)

    with col2:
        st.subheader('With Equipment Reconfiguration (5% Repair Time):')
        data = {
            'Metric': ['Total Production Hours (Yearly)', 'Downtime', 'Effective Production Hours',
                       'Revenue ($ million)', 'Cost ($ million)', 'Repair Costs ($ million)'],
            'Value': [
                f'{capacity_utilization/100 * 24 * 365:.1f} hours',
                f'{5/100*capacity_utilization/100 * 24 * 365:.1f} hours',
                f'{capacity_utilization/100 * 24 * 365-5 /100*capacity_utilization/100 * 24 * 365:.1f} hours',
                f'{(capacity_utilization/100 * 24 * 365-5 /100*capacity_utilization/100 * 24 * 365)*revenue/(capacity_utilization/100 * 24 * 365-repair_time /100*capacity_utilization/100 * 24 * 365):.1f} million',
                f'{(capacity_utilization/100 * 24 * 365-5 / 100*capacity_utilization/100 * 24 * 365)*cogs/(capacity_utilization/100 * 24 * 365-repair_time /100*capacity_utilization/100 * 24 * 365):.1f} million',
                f'{5/100*capacity_utilization/100 * 24 *
                    365*repair_cost/1000000:.2f} million'
            ]
        }

# Display the table
        st.table(data)
    revenue_change = (capacity_utilization/100 * 24 * 365-5 /
                      100*capacity_utilization/100 * 24 * 365)*revenue/(capacity_utilization/100 * 24 * 365-repair_time /
                                                                        100*capacity_utilization/100 * 24 * 365) - revenue
    cost_change = (capacity_utilization/100 * 24 * 365-5 /
                   100*capacity_utilization/100 * 24 * 365)*cogs/(capacity_utilization/100 * 24 * 365-repair_time /
                                                                     100*capacity_utilization/100 * 24 * 365) - cogs
    
    repair_change = (5/100*capacity_utilization/100 * 24 *
                    365*repair_cost/1000000)-(repair_time/100*capacity_utilization /
                    100 * 24 * 365*repair_cost/1000000)
    net_change = (revenue_change - cost_change - repair_change)-0.5
# Add a section to evaluate revenue increase and make a decision
    st.header('Decision Evaluation:')
    st.markdown(f'<h6 style="color: grey;">Revenue Change: {revenue_change:.1f}</h6>',
                unsafe_allow_html=True)
    st.markdown(f'<h6 style="color: grey;">Cost Change: {cost_change:.1f}</h6>',
                unsafe_allow_html=True)
    st.markdown(f'<h6 style="color: grey;">Repair Cost Change: {repair_change:.1f}</h6>',
                unsafe_allow_html=True)
    st.markdown(f'<h6 style="color: grey;">Net Change: {net_change:.1f}</h6>',
                    unsafe_allow_html=True)

    if net_change > 0:
        st.success('Recommendation: Equipment Reconfiguration is Suggested')
    else:
        st.warning('Recommendation: Equipment Reconfiguration is Not Accepted')

# Additional content or code can be added here as needed


if __name__ == '__main__':
    main()
