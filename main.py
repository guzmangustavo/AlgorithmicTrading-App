import argparse
import pyRofex


# Classes definition
class Market:
    """
    A class used to represent a financial market's environment.

    """

    @staticmethod
    def connect(user, password, account):
        """
        Generate a connection with the REMARKET environment if the credentials
        entered by parameters are right.

        :param user: Remarkets' username.
        :type user: str
        :param password: Remarkets' password.
        :type password: str
        :param account: Remarkets' account.
        :type account: str

        """
        try:
            pyRofex.initialize(
                user=user,
                password=password,
                account=account,
                environment=pyRofex.Environment.REMARKET
            )
            print("Iniciando sesión en Remarkets")
        except pyRofex.components.exceptions.ApiException:
            print("La autenticación falló. Credenciales incorrectas")
            Market.disconnect()

    @staticmethod
    def get_existing_symbols():
        """
        Get an updated list of financial instruments' symbols traded in the
        market and return it.

        :return: Updated list of financial instruments' symbols traded in the
         market.
        :rtype: list
        """
        instruments = pyRofex.get_all_instruments()["instruments"]
        existing_symbols = []
        for instrument in instruments:
            existing_symbols.append(instrument["instrumentId"]["symbol"])
        return existing_symbols

    @staticmethod
    def disconnect():
        """
        Print an exit message.
        """
        print("Cerrando sesión en Remarkets")


class Symbol:
    """
    A class used to represent the symbols (tickers) corresponding to the
    financial instruments traded in financial markets.

    Attributes
    ----------
    symbol: str
    The symbol (ticker) associated to a financial instrument.
    """

    def __init__(self, symbol):
        self.symbol = symbol

    def validate_entered_symbol(self, existing_symbols):
        """
        Validate that the symbol is in the list entered by parameter and return
        it, if so.

        :param existing_symbols: list of financial instruments' symbols traded
        in the market.
        :type existing_symbols: list
        :return: financial instrument's symbol that is traded in the market.
        :rtype: str | NoneType

        """
        print("Consultando símbolo")
        if self.symbol in existing_symbols:
            print("Símbolo validado")
            validated_symbol = self.symbol
            return validated_symbol
        else:
            print("Símbolo no validado")
            return None


class Price:
    """
    A class used to represent the price of the symbol entered by parameter.

    Attributes
    ----------
    symbol: str
        The symbol (ticker) associated to a financial instrument.
    """

    def __init__(self, symbol):
        self.symbol = symbol

    def query_market_data(self, kind_of_price):
        """
        Query the symbol's Market Data according to the kind of price
        entered by parameter and return it.

        :param kind_of_price: Kind of prices supported by Primary's API,
        according to the enumeration specified by pyRofex library.
        For example:
        - pyRofex.MarketDataEntry.LAST for last price
        - pyRofex.MarketDataEntry.BIDS for BID price
        :type kind_of_price: List of MarketDataEntry (Enum by pyRofex library)
        :return: Market Data corresponding to entered parameters.
        :rtype: dict
        """
        market_data = pyRofex.get_market_data(
            ticker=self.symbol,
            entries=[kind_of_price]
        )
        return market_data


class LastPrice(Price):
    """
    A class used to represent the last price of the symbol entered by parameter.
    """

    @staticmethod
    def query_last_price(market_data):
        """
        Query the last price of the symbol and, if it is found, print it and
        return it. If not, return None.

        :param market_data: Financial instrument's Market Data corresponding to
        last price.
        :type market_data: dict
        :return: Financial instrument's last price traded in market.
        :rtype: float | NoneType

        """
        print("Consultando el último precio")
        if market_data["marketData"]["LA"]:
            last_price = market_data["marketData"]["LA"]["price"]
            print(
                f"Último precio operado: ${last_price:,.2f}".replace('.', ','))
            return last_price
        print("Último precio operado: No hay datos disponibles")
        return None


class BidPrice(Price):
    """
    A class used to represent the BID price of the symbol entered by parameter.
    """

    @staticmethod
    def query_bid_price(market_data):
        """
        Query the BID price of the symbol and, if it is found, print it and
        return it. If not, return None.

        :param market_data: Financial instrument's Market Data corresponding to
        BID price.
        :type market_data: dict
        :return: Financial instrument's BID price traded in market.
        :rtype: float | NoneType
        """
        print("Consultando BID")
        if market_data["marketData"]["BI"]:
            bid_price = market_data["marketData"]["BI"][0]["price"]
            print(f"Precio de BID: ${bid_price:,.2f}".replace('.', ','))
            return bid_price
        print("No hay BIDs activos")
        return None


class TradingStrategy:
    """
    A class used to represent a trading strategy applied to a financial
    instrument traded in financial markets.

    Attributes
    ----------
    symbol: str
        The symbol (ticker) associated to a financial instrument.
    """

    def __init__(self, symbol):
        self.symbol = symbol


class BuyingStrategy(TradingStrategy):
    """
    A class used to represent a buying trading strategy applied to a financial
    instrument traded in financial markets.
    """

    def buy_fixed_price(self, buying_price):
        """
        Send a buying order to market at price specified by parameters.

        :param buying_price: Price to be offered in the buying order. It must be
        greater than zero.
        :type buying_price: float
        """

        print(f"Ingresando orden a ${buying_price:,.2f}".replace('.', ','))
        pyRofex.send_order(
            ticker=self.symbol,
            side=pyRofex.Side.BUY,
            price=buying_price,
            size=1,
            order_type=pyRofex.OrderType.LIMIT
        )
        return buying_price

    def buy_fixed_quantity_less_than_bid_price(self, bid_price, fixed_quantity):
        """
        Send a buying order to market at instrument's BID price minus a quantity
        specified by parameter.

        :param bid_price: BID price of the financial instrument.
        :type bid_price: float
        :param fixed_quantity: Quantity to be subtracted from BID price. It must
        be less than BID price.
        :type fixed_quantity: float
        """

        bid_price_minus_fixed_quantity = bid_price - fixed_quantity
        print(
            f"Ingresando orden a ${bid_price_minus_fixed_quantity:,.2f}".replace(
                '.', ',')
        )
        pyRofex.send_order(
            ticker=self.symbol,
            side=pyRofex.Side.BUY,
            price=bid_price_minus_fixed_quantity,
            size=1,
            order_type=pyRofex.OrderType.LIMIT
        )
        return bid_price_minus_fixed_quantity

    def buy_one_cent_less_than_bid_or_50(self, bid_price):
        """
        If bid_price parameter is not None, it sends a buying order at one cent
        less than BID Price. If not, it does at $50.00.
        :param bid_price: BID price of the financial instrument.
        :type bid_price: float

        """
        if bid_price:
            buying_price = self.buy_fixed_quantity_less_than_bid_price(
                bid_price=bid_price,
                fixed_quantity=0.01)
        else:
            buying_price = self.buy_fixed_price(50)
        return buying_price


def main():
    # Definition of program's parameters
    parser = argparse.ArgumentParser()
    parser.add_argument("symbol", type=str, help="Símbolo del instrumento")
    parser.add_argument("user", type=str, help="Usuario de Remarkets")
    parser.add_argument("password", type=str, help="Contraseña de Remarkets")
    parser.add_argument("account", type=str, help="Cuenta de Remarkets")
    args = parser.parse_args()

    # Conection to Remarkets' environment
    Market.connect(args.user, args.password, args.account)

    # Symbol instantiation and validation
    symbol = Symbol(args.symbol)
    existing_symbols_in_market = Market.get_existing_symbols()
    validated_symbol = symbol.validate_entered_symbol(
        existing_symbols_in_market)

    if validated_symbol:
        # Last Price instantiation and query
        last_price = LastPrice(validated_symbol)
        last_price_market_data = last_price.query_market_data(
            pyRofex.MarketDataEntry.LAST)
        last_price.query_last_price(last_price_market_data)

        # BID Price instantiation and query
        bid_price = BidPrice(validated_symbol)
        bid_price_market_data = bid_price.query_market_data(
            pyRofex.MarketDataEntry.BIDS)
        bid_price_of_validated_symbol = bid_price.query_bid_price(
            bid_price_market_data)

        # Buying Strategy
        buying_strategy = BuyingStrategy(validated_symbol)
        buying_strategy.buy_one_cent_less_than_bid_or_50(
            bid_price_of_validated_symbol)
        Market.disconnect()
    else:
        Market.disconnect()


if __name__ == '__main__':
    main()
