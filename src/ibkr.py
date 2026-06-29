import asyncio
from ib_async import IB
from config.settings import IBKR_HOST, IBKR_PORT, IBKR_CLIENT_ID

BASE_CURRENCY = "EUR"
TIMEOUT_SECONDS = 15

async def get_account_data() -> dict:
    ib = IB()

    try:
        await asyncio.wait_for(
            ib.connectAsync(
                host=IBKR_HOST,
                port=IBKR_PORT,
                clientId=IBKR_CLIENT_ID
            ),
            timeout=TIMEOUT_SECONDS
        )

        summary = await asyncio.wait_for(
            ib.accountSummaryAsync(),
            timeout=TIMEOUT_SECONDS
        )

    except asyncio.TimeoutError:
        raise ConnectionError("TWS no responde. ¿Está abierto y conectado?")
    finally:
        if ib.isConnected():
            ib.disconnect()

    return _parse_account_summary(summary)

def _parse_account_summary(values: list) -> dict:
    simple_tags = {
        "NetLiquidation",
        "TotalCashValue",
        "GrossPositionValue"
    }
    ledger_tags = {
        "$LEDGER-UnrealizedPnL": "UnrealizedPnL",
        "$LEDGER-RealizedPnL": "RealizedPnL"
    }

    result = {}
    for v in values:
        if v.tag in simple_tags and v.currency == BASE_CURRENCY:
            result[v.tag] = float(v.value)
        elif v.tag in ledger_tags and v.currency == "BASE":
            result[ledger_tags[v.tag]] = float(v.value)

    return result