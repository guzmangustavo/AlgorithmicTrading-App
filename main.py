import argparse
import pyRofex
from classes import Market, Symbol, LastPrice, BidPrice, BuyingStrategy


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
