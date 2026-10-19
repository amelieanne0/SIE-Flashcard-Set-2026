---
agent: claude-research
created: 2026-10-19T16:47:17.701659
tags: ["sie", "options", "comprehensive-guide"]
---

# Options Trading - Comprehensive Study Guide

## 1. Introduction to Options

### What are Options?
Options are derivative contracts that give the holder the right (but not obligation) to buy or sell an underlying asset at a predetermined price on or before a specific date.

### Key Characteristics
- **Strike Price**: The predetermined price at which the option can be exercised
- **Expiration Date**: The last date the option can be exercised
- **Premium**: The price paid to purchase the option
- **Intrinsic Value**: The immediate profit if exercised (max(spot-strike, 0) for calls)
- **Time Value**: Remaining value in the option from time until expiration

## 2. Types of Options

### Call Options
- Right to buy the underlying asset
- Profits when asset price rises
- Max loss = premium paid
- Unlimited profit potential

### Put Options
- Right to sell the underlying asset
- Profits when asset price falls
- Max loss = premium paid
- Max profit = strike price - premium

## 3. The Greeks

### Delta (Δ)
- Rate of change of option price with underlying price
- Range: 0 to 1 (for calls), -1 to 0 (for puts)
- Approximately equals probability ITM at expiration

### Gamma (Γ)
- Rate of change of delta
- Highest for ATM options
- Increases as expiration approaches

### Theta (Θ)
- Time decay of option value
- Benefits short positions, hurts long positions
- Accelerates as expiration approaches
- Usually negative for long positions

### Vega (ν)
- Sensitivity to volatility changes
- Positive for both calls and puts
- Higher for ATM options

### Rho (ρ)
- Sensitivity to interest rate changes
- More important for longer-dated options

## 4. Option Pricing Models

### Black-Scholes Model
Primary model used for European options:
- Inputs: Stock price, strike price, time to expiration, volatility, risk-free rate
- Output: Theoretical option price
- Assumes: No dividends, European exercise, lognormal distribution

### Binomial Model
Used for American options:
- More flexible than Black-Scholes
- Can handle early exercise
- Recombining tree of price movements

## 5. Option Strategies

### Bullish Strategies
1. **Long Call**: Buy call - profit from rising prices
2. **Bull Call Spread**: Buy call, sell higher strike call - reduced cost
3. **Bull Put Spread**: Sell lower strike put, buy higher strike put - credit spread

### Bearish Strategies
1. **Long Put**: Buy put - profit from falling prices
2. **Bear Call Spread**: Short lower strike call, long higher strike call
3. **Bear Put Spread**: Short higher strike put, long lower strike put

### Neutral Strategies
1. **Straddle**: Buy call and put at same strike - profit from volatility
2. **Strangle**: Buy OTM call and put - cheaper than straddle
3. **Iron Condor**: Sell call spread and put spread - profit from theta decay
4. **Butterfly**: Long 1 ITM, short 2 ATM, long 1 OTM - limited risk

### Volatility Strategies
1. **Calendar Spread**: Same strike, different expirations - profit from time decay
2. **Diagonal Spread**: Different strikes and expirations
3. **Ratio Spread**: Different number of contracts

## 6. Risk Management

### Assignment Risk
- Short option holders subject to assignment
- Increases as option goes ITM
- Certain for ITM options at expiration

### Early Exercise
- American options can be exercised anytime
- Early exercise usually on puts (for dividends/interest)
- Considered in pricing

### Position Greeks
- Calculate Greeks for entire portfolio
- Manage delta exposure (hedge if needed)
- Monitor gamma risk
- Plan for theta decay effects

## 7. Key Concepts for SIE Exam

- Understand calls vs puts
- Know the Greeks and what they measure
- Recognize basic strategies and their risk/reward
- Understand assignment and exercise
- Know Black-Scholes inputs and assumptions
