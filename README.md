# AlgorithmicTrading-App

An application that executes stocks trading strategies in a test environment.

## Table of contents

* [Introduction](#introduction)
* [Trading Strategy](#tradingstrategy)
* [Instructions](#instructions)
* [Disclaimer](#disclaimer)

### Introduction

AlgorithmicTrading is an application designed to apply stock trading strategies in Argentinean stock market by using the [pyRofex](https://github.com/matbarofex/pyRofex) library. 

It runs in a test environment, REMARKETS.

To use it you should get your credentials at [Remarket Website](https://remarkets.primary.ventures/).

### Trading Strategy

The trading strategy currently implemented is very simple. The software will check the last price of the instrument, whose ticker is entered by parameter. It will print it.
And then, it will do the same with BID price. If there is a BID price, it will send a buying order at one cent less than the current BID price. If not, it will send a buying order at $50,00. In both cases, stocks' quantity of the order will be one.

### Instructions

To use AlgorithmicTrading, you can type on a Python terminal:

	$ main.py ticker user password account

For example, suppose you want to apply the strategy implemented in the software to a financial instrument whose ticker is DOEne21. And your Remarkets' credential are testUser, testPassword and testAccount. Then you should type:

	$ main.py DOEne21 testUser testPassword testAccount

To run the unit tests, you should also complete your credentials in SetUp method.

**Note**: Remarket environment sometimes may not be available or may be under maintenance. 

### Disclaimer

AlgorithmicTrading is a software developed with an educational purpose. The strategy implemented must not be considered as an investment advice.
