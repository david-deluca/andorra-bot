import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from io import BytesIO

TICKERS = {
    "IWDA": "IWDA.AS",
    "EIMI": "EIMI.L"
}
SHARES = {
    "IWDA": 100,
    "EIMI": 100
}
BENCHMARK_TICKER = "IWDA.AS"
PERIOD = "6mo"

def _download_prices() -> pd.DataFrame:
    tickers = list(set(TICKERS.values()))
    data = yf.download(tickers, period=PERIOD, auto_adjust=True, progress=False)
    return data["Close"]

def _normalize(series: pd.Series) -> pd.Series:
    """Convierte precios a rendimiento % desde el primer día."""
    return ((series / series.iloc[0]) - 1) * 100

def generate_performance_chart() -> BytesIO:
    prices = _download_prices()
    prices = prices.dropna()

    # Rendimiento de cada ETF normalizado
    iwda_ret = _normalize(prices[TICKERS["IWDA"]])
    eimi_ret = _normalize(prices[TICKERS["EIMI"]])

    # Portfolio ponderado — mismas participaciones, normalizamos la suma de valores
    portfolio_value = (
        prices[TICKERS["IWDA"]] * SHARES["IWDA"] +
        prices[TICKERS["EIMI"]] * SHARES["EIMI"]
    )
    portfolio_ret = _normalize(portfolio_value)

    # Benchmark — solo IWDA
    benchmark_ret = _normalize(prices[BENCHMARK_TICKER])

    # Gráfico
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(portfolio_ret.index, portfolio_ret.values, label="Mi Portfolio", linewidth=2, color="#2196F3")
    ax.plot(benchmark_ret.index, benchmark_ret.values, label="Benchmark (IWDA)", linewidth=1.5, color="#FF9800", linestyle="--")

    ax.axhline(0, color="gray", linewidth=0.8, linestyle=":")
    ax.set_title("Rendimiento Portfolio vs Benchmark — Últimos 6 meses", fontsize=13)
    ax.set_ylabel("Rendimiento (%)")
    ax.set_xlabel("")
    ax.legend()
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Guardar en memoria como bytes (no en disco)
    buf = BytesIO()
    plt.savefig(buf, format="png", dpi=150)
    buf.seek(0)
    plt.close(fig)

    return buf