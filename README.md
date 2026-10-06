# Deepwell

Managed liquidity and credit for Robinhood Stock Tokens, on Robinhood Chain (chain id 4663), in USDG.

- **DeepwellLiquidityVault** (a Well): deposit USDG; the Well keeps a concentrated Uniswap v4 position in one stock's
  pool around the Chainlink price. Shares are valued at Chainlink. 70% of swap fees compound for holders; 30% goes to
  the protocol. Exits in USDG, or in kind with no price check.
- **DeepwellCreditDesk** (Borrow): an isolated lending market per Well. Lenders supply USDG; borrowers pledge Well
  shares and borrow against them.
- **DeepwellOracle**, **DeepwellFeeRouter**, **DeepwellBuyBurn**, **DeepwellSwapAdapter**, **DeepwellRegistry** and
  **DeepwellTimelock** (48 hours) around them. Protocol fees buy and burn $DEEP.

The Wells and credit lines build on the MIT-licensed Stonkwell contracts; see `LICENSE`.

| Folder | Contents |
|---|---|
| `contracts/` | Hardhat project: the contracts, their tests and the deploy, verify and governance scripts |
| `keeper/` | The keeper bot: Well rebalances and harvests, credit-line reserves, fee routing, buy and burn |
| `tools/` | Wallet tools: encrypted keystores, the keeper key straight into a GitHub secret |

## Tests

```bash
cd contracts && npm install && npx hardhat test
cd ../keeper && npm install && npm test
```

The keeper also has an end-to-end smoke test against a local node; see `keeper/README.md`.

## Using the contracts

There is no website: everything is done from a wallet on the Robinhood Chain explorer, where every contract is
verified (Contract → Write). Addresses are in `contracts/deployments/robinhood.json`.

- **Deposit into a Well:** on USDG, `approve(well, amount)`; then on the Well, `deposit(amount, yourAddress)`.
  USDG has 6 decimals, so 100 USDG is `100000000`.
- **Withdraw:** read your shares with `balanceOf(yourAddress)` on the Well, then `redeem(shares, yourAddress, yourAddress)` for USDG, or
  `redeemInKind(shares, yourAddress, yourAddress, 0, 0)` for your share of the stock and USDG with no price check.
- **Lend on a credit line:** on USDG, `approve(creditLine, amount)`; then `deposit(amount, yourAddress)`.
- **Borrow:** on the Well, `approve(creditLine, shares)`; on the credit line, `pledge(shares)`, then
  `borrow(amount, yourAddress)`. Repay with `repay(amount, yourAddress)` after approving USDG, and take shares back
  with `release(shares, yourAddress)`.

Not independently audited. Nothing here is investment advice.
