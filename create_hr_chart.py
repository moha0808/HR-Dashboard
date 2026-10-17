import os
import pandas as pd
import matplotlib.pyplot as plt

def generate_hr_chart():
    # 1. File Paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, "hr dataset.csv")
    output_image_path = os.path.join(current_dir, "hr_analytics_chart.png")

    # 2. Data Processing with Pandas
    df = pd.read_csv(csv_path)

    total_employees = len(df)
    total_attrition = (df['Attrition'] == 'Yes').sum()
    total_retained = total_employees - total_attrition
    overall_attrition_rate = (total_attrition / total_employees) * 100
    avg_income_all = df['Monthly_Income'].mean()

    # Aggregate by Job Role
    role_df = df.groupby('Job_Role').agg(
        total_count=('Employee_Count', 'sum'),
        attrition_count=('Attrition_flag', 'sum'),
        avg_income=('Monthly_Income', 'mean')
    ).reset_index()

    role_df['retained_count'] = role_df['total_count'] - role_df['attrition_count']
    role_df['attrition_rate'] = (role_df['attrition_count'] / role_df['total_count']) * 100

    # Sort ascending so highest attrition rate appears at the top
    role_df = role_df.sort_values('attrition_rate', ascending=True).reset_index(drop=True)

    # 3. Figure & Canvas Setup
    fig, ax = plt.subplots(figsize=(16, 10), dpi=300)
    bg_color = '#F8FAFC'
    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)

    y_pos = list(range(len(role_df)))
    bar_height = 0.56

    # Colors
    color_retained = '#2563EB'   # Professional Blue
    color_attrition = '#EF4444'  # Alert Red

    # 4. Plot Horizontal Stacked Bars
    ax.barh(
        y_pos,
        role_df['retained_count'],
        height=bar_height,
        color=color_retained,
        edgecolor='none',
        label='Retained Employees (Stayed)',
        alpha=0.92,
        zorder=3
    )

    ax.barh(
        y_pos,
        role_df['attrition_count'],
        left=role_df['retained_count'],
        height=bar_height,
        color=color_attrition,
        edgecolor='none',
        label='Attrited Employees (Left)',
        alpha=0.92,
        zorder=3
    )

    # Reference Line for Overall Attrition Benchmark (16.1%)
    # Let's add direct data labels for counts and metrics
    for i, row in role_df.iterrows():
        retained = int(row['retained_count'])
        attrition = int(row['attrition_count'])
        total = int(row['total_count'])
        rate = row['attrition_rate']
        income = row['avg_income']

        # Value inside retained bar
        if retained >= 40:
            ax.text(
                retained / 2,
                i,
                f"{retained:,}",
                va='center',
                ha='center',
                color='#FFFFFF',
                fontweight='bold',
                fontsize=11,
                zorder=4
            )

        # Value inside attrition bar
        if attrition >= 8:
            ax.text(
                retained + (attrition / 2),
                i,
                f"{attrition}",
                va='center',
                ha='center',
                color='#FFFFFF',
                fontweight='bold',
                fontsize=10.5,
                zorder=4
            )

        # Stat text immediately following the bar
        rate_color = '#DC2626' if rate > overall_attrition_rate else '#0F172A'
        
        ax.text(
            total + 6,
            i,
            f"{rate:.1f}% Attrition",
            va='center',
            ha='left',
            color=rate_color,
            fontweight='bold',
            fontsize=11,
            zorder=4
        )
        ax.text(
            total + 70,
            i,
            f"|   Total: {total:>3}   |   Avg Salary: USD {income:,.0f}/mo",
            va='center',
            ha='left',
            color='#475569',
            fontweight='normal',
            fontsize=10,
            zorder=4
        )

    # 5. Styling Axes and Spines
    ax.set_yticks(y_pos)
    ax.set_yticklabels(role_df['Job_Role'], fontsize=11.5, fontweight='bold', color='#1E293B')
    ax.set_xlabel('Employee Headcount', fontsize=12, fontweight='bold', color='#334155', labelpad=8)
    ax.set_xlim(0, 530)
    ax.xaxis.grid(True, linestyle='--', alpha=0.6, color='#CBD5E1', zorder=0)
    ax.set_axisbelow(True)

    for spine in ['top', 'right', 'left']:
        ax.spines[spine].set_visible(False)
    ax.spines['bottom'].set_color('#94A3B8')
    ax.spines['bottom'].set_linewidth(1.2)
    ax.tick_params(axis='x', colors='#475569', labelsize=10.5)
    ax.tick_params(axis='y', length=0)

    # 6. Header Title & Executive KPI Cards
    fig.text(0.06, 0.945, "HR ANALYTICS: EMPLOYEE RETENTION & ATTRITION BY JOB ROLE", 
             fontsize=17, fontweight='bold', color='#0F172A')

    # Top KPI summary cards
    kpi_cards = [
        ("TOTAL WORKFORCE", f"{total_employees:,} Employees", "#2563EB", 0.06),
        ("RETAINED TALENT", f"{total_retained:,} ({100 - overall_attrition_rate:.1f}%)", "#16A34A", 0.28),
        ("OVERALL ATTRITION", f"{total_attrition:,} ({overall_attrition_rate:.1f}%)", "#DC2626", 0.52),
        ("AVG MONTHLY SALARY", f"USD {avg_income_all:,.0f}", "#475569", 0.76),
    ]

    for label, val, color, x_offset in kpi_cards:
        fig.text(x_offset, 0.905, label, fontsize=8.5, fontweight='bold', color='#64748B')
        fig.text(x_offset, 0.880, val, fontsize=12, fontweight='bold', color=color)

    # Subtle divider line below KPIs
    line = plt.Line2D([0.06, 0.96], [0.865, 0.865], transform=fig.transFigure, 
                      color='#E2E8F0', linewidth=1.5)
    fig.add_artist(line)

    # 7. Legend
    legend = ax.legend(
        loc='lower right',
        frameon=True,
        facecolor='#FFFFFF',
        edgecolor='#CBD5E1',
        fontsize=10.5,
        framealpha=0.95,
        borderpad=0.8
    )
    for text in legend.get_texts():
        text.set_color('#1E293B')

    # 8. Footer Source Note
    fig.text(
        0.06, 0.015,
        "Source: HR Analytics Dataset ('hr dataset.csv')  •  Visualized with Python (Pandas & Matplotlib)  •  High Risk Threshold: > 16.1%",
        fontsize=9,
        color='#64748B',
        fontstyle='italic'
    )

    # Adjust layout & Save
    plt.subplots_adjust(left=0.20, right=0.97, top=0.83, bottom=0.10)
    plt.savefig(output_image_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()

    print(f"[SUCCESS] HR Analytics Chart generated and saved at:\n{output_image_path}")

if __name__ == "__main__":
    generate_hr_chart()
