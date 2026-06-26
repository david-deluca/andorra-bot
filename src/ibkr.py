from ib_async import IB
from config.settings import IBKR_HOST, IBKR_PORT, IBKR_CLIENT_ID

BASE_CURRENCY = "EUR"

async def get_account_data() -> dict:
    ib = IB()

    await ib.connectAsync(
        host=IBKR_HOST,
        port=IBKR_PORT,
        clientId=IBKR_CLIENT_ID
    )

    summary = await ib.accountSummaryAsync()

    ib.disconnect()

    return _parse_account_summary(summary)

def _parse_account_summary(values: list) -> dict:
    # Tags normales filtrados por divisa base
    simple_tags = {
        "NetLiquidation",
        "TotalCashValue",
        "GrossPositionValue"
    }
    # Tags de PnL: vienen como $LEDGER-X y los queremos en BASE (consolidado)
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