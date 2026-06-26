def format_portfolio_message(data: dict) -> str:
    if not data:
        return "❌ No se pudieron obtener datos de la cuenta."

    def fmt(key: str) -> str:
        value = data.get(key, 0.0)
        return f"€{value:,.2f}"

    pnl = data.get("UnrealizedPnL", 0.0)
    pnl_emoji = "📈" if pnl >= 0 else "📉"

    return (
        f"💼 *Portfolio — Cuenta Paper IBKR*\n\n"
        f"Valor neto liquidación: {fmt('NetLiquidation')}\n"
        f"Cash disponible: {fmt('TotalCashValue')}\n"
        f"Valor posiciones: {fmt('GrossPositionValue')}\n"
        f"{pnl_emoji} PnL no realizado: {fmt('UnrealizedPnL')}\n"
        f"PnL realizado: {fmt('RealizedPnL')}"
    )