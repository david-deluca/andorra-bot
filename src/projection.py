import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from io import BytesIO

def calculate_projection(
    initial_capital: float,
    monthly_contribution: float,
    annual_return: float,
    years: int
) -> dict:
    """
    Calcula proyección de interés compuesto con aportaciones mensuales.
    Devuelve diccionario con series temporales para el gráfico.
    """
    i_monthly = (1 + annual_return) ** (1 / 12) - 1
    months = years * 12

    capital_values = []
    contributed_values = []
    total = initial_capital
    total_contributed = initial_capital

    for month in range(1, months + 1):
        total = total * (1 + i_monthly) + monthly_contribution
        total_contributed += monthly_contribution
        capital_values.append(total)
        contributed_values.append(total_contributed)

    final_value = capital_values[-1]
    total_invested = contributed_values[-1]
    total_return = final_value - total_invested

    return {
        "capital_values": capital_values,
        "contributed_values": contributed_values,
        "final_value": final_value,
        "total_invested": total_invested,
        "total_return": total_return,
        "months": months,
        "years": years
    }

def generate_projection_chart(
    initial_capital: float,
    monthly_contribution: float,
    annual_return: float,
    years: int
) -> BytesIO:
    data = calculate_projection(
        initial_capital, monthly_contribution, annual_return, years
    )

    x = list(range(1, data["months"] + 1))
    year_labels = [m / 12 for m in x]

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.fill_between(year_labels, data["contributed_values"],
                    alpha=0.4, color="#FF9800", label="Capital aportado")
    ax.fill_between(year_labels, data["contributed_values"],
                    data["capital_values"],
                    alpha=0.4, color="#2196F3", label="Rendimiento compuesto")
    ax.plot(year_labels, data["capital_values"],
            color="#2196F3", linewidth=2)

    ax.set_title(
        f"Proyección {years} años | "
        f"CI: €{initial_capital:,.0f} | "
        f"Aport: €{monthly_contribution:,.0f}/mes | "
        f"Retorno: {annual_return*100:.1f}%",
        fontsize=11
    )
    ax.set_xlabel("Años")
    ax.set_ylabel("Valor (€)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(
        lambda x, _: f"€{x:,.0f}"
    ))
    ax.legend()
    plt.tight_layout()

    buf = BytesIO()
    plt.savefig(buf, format="png", dpi=150)
    buf.seek(0)
    plt.close(fig)

    return buf, data