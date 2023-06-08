
prompt = """Your main task is to educate the person. He has been through the course and you have to ask him questions from the course.
Your questions should help the person reinforce what they have learned. Ask only one question and one answer."""

promttTest = """

Your task is to grade the student's answer on a 20-point scale. You are given the correct answer and the student's answer. The closer the student's answer, the higher the score should be.
Answer in this format: 19 - Because...

"""

block1 = """
TIP-3
Just as ERC-20 is the most popular standard in the Ethereum network, TIP-3 assumes the same role in the Venom network. TIP-3 was designed to match the distributed system design of the Venom network and is cost-effective for its fee-paying model.

TIP-3 provides the following functionalities

transfer tokens from one account to another
get the current token balance of an account
get the total supply of the token available on the network
mint and burn tokens

As you may know, the ERC20 contract's main value is balance mapping. So users just have records about their balances and work only with this contract. TIP-3 working flow is different because of the asynchronous nature of TVM. Each user has his own wallet and operates with it. Wallet operates with another wallet for transfers (see scheme).
"""

block2 = """
Gas Model and Fees
In Ethereum, the gas model is used to limit the number of computational steps that a transaction can perform. Users pay gas fees for each transaction they send, and these fees are paid in the native currency of the network, Ether (ETH). The fees are determined by the amount of gas used by a transaction, and the gas price, which fluctuates according to network demand.

On the other hand, in Venom, the fee calculation is based on a combination of gas, data storage, and forward message fees. The user decides how many VENOM to attach as payment fees from their contract account for the call, and this value is the upper limit for the cost of executing the call chain for the user.

By including data storage fees in the fee calculation, Venom incentivizes efficient use of storage space on the network and encourages developers to design contracts that minimize storage usage. This helps to prevent network congestion in the long term.
"""

block3 = """
"""

block4 = """
"""

block5 = """
"""

block6 = """
"""

block7 = """
"""

block8 = """
"""

block10 = """
"""

block11= """
"""

block12 = """
"""

block13 = """
"""

block14 = """
"""

block15 = """
"""

block16 = """
"""

block17 = """
"""


block18 = """
"""

block19 = """
"""

block20 = """
"""

block21 = """
"""

block22 = """
"""