import logging
import logging.config

from basetypes.Broker.tdaBroker import TdaBroker
from basetypes.Database.sqliteDatabase import SqliteDatabase
from basetypes.Mediator.botMediator import Bot
from basetypes.Notifier.telegramnotifier import TelegramNotifier
from basetypes.Strategy.longsharesstrategy import LongSharesStrategy
from basetypes.Strategy.singlebydeltastrategy import SingleByDeltaStrategy
from basetypes.Strategy.spreadsbydeltastrategy import SpreadsByDeltaStrategy

if __name__ == "__main__":
    # Create Logging
    logging.config.fileConfig(
        "logConfig.ini",
        defaults={"logfilename": "autotrader.log"},
        disable_existing_loggers=False,
    )

    # Create our strategies
    vgshstrat = LongSharesStrategy(
        strategy_name="VGSH Core", underlying="VGSH", portfolio_allocation_percent=0.9
    )
    cspstrat = SingleByDeltaStrategy(
        strategy_name="Puts",
        put_or_call="PUT",
        targetdelta=0.07,
        mindelta=0.03,
        profittargetpercent=0.7,
    )
    nakedcalls = SingleByDeltaStrategy(
        strategy_name="Calls",
        put_or_call="CALL",
        targetdelta=0.02,
        mindelta=0.01,
        profittargetpercent=0.78,
    )
    spreadstrat = SpreadsByDeltaStrategy(strategy_name="spreads")

    # Create our brokers
    individualbroker = TdaBroker(id="individual")
    irabroker = TdaBroker(id="ira")

    # Create our local DB
    sqlitedb = SqliteDatabase("LoopTrader.db")

    # Create our notifier
    telegram_bot = TelegramNotifier()

    # Create our Bot
    bot = Bot(
        brokerstrategy={
            spreadstrat: irabroker,
            cspstrat: individualbroker,
            nakedcalls: individualbroker,
            vgshstrat: individualbroker,
        },
        database=sqlitedb,
        notifier=telegram_bot,
    )

    # Run Bot
    bot.process_strategies()
