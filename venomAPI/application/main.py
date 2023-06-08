from fastapi import Depends, FastAPI, Response, status
from fastapi.security import HTTPBearer
from .utils import VerifyToken
from os.path import exists
import random
import string
import sqlite3
import openai
import text as msg
from tonclient.types import ClientConfig
from tonclient.client import TonClient
from tonclient.types import NetworkConfig, ClientConfig
from tonclient.client import TonClient, DEVNET_BASE_URLS
from tonclient.types import (
    Abi,
    KeyPair,
    CallSet,
    Signer,
    ParamsOfEncodeMessage,
    ParamsOfProcessMessage
)


#VENOM CHAIN-----------------------------------------
network = NetworkConfig(
server_address='https://gql-devnet.venom.network/graphql')
config = ClientConfig(network=network)
config.abi.message_expiration_timeout = 30000
client = TonClient(config=config)
address = "0:06d5ee9886fd93e47e7860182d8ce354b159ce56d5fc90e67216f8c61836a5fc"
events_abi = Abi.from_path(
            'Sample.abi.json'
        )
keypair = KeyPair(
            public='',
            secret='',
        )
#---------------------------------------------------


#FastAPI-------------------------------------------
app = FastAPI()
token_auth_scheme = HTTPBearer()
#---------------------------------------------------


#TO_Do 2auth
tokenVer = "Bse8iIm5SAVSTH7zMIiAdcOODmPkpZt5"
openai.api_key = "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"

#GPT------------------------------------------
def claster_response(student,ansver,question):
    model_engine = "gpt-3.5-turbo"

    completion = openai.ChatCompletion.create(
        model=model_engine,
        messages=[
            {"role": "system", "content": msg.promttTest},
            {"role": "user", "content": f"Question ->{question}\nStudent-> {student}\nAnsver ->{ansver}"},
            
        ],
        temperature=0.4,
    )

    print (completion.choices[0].message)


    return completion['choices'][0]['message']['content']


def createrQuestion():
    model_engine = "gpt-3.5-turbo"

    completion = openai.ChatCompletion.create(
        model=model_engine,
        messages=[
            {"role": "system", "content": msg.prompt},
            {"role": "user", "content": f"Draw on this text. {msg.block1}.\n\n Generate a question and answer in this format. What is the main purpose of TIP-3 in the Venom network? -> It's a erc20 token."},
            
        ],
        temperature=1,
    )

    print (completion.choices[0].message)


    return completion['choices'][0]['message']['content']
#---------------------------------------------------

def generate_random_string():
    letters_and_digits = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(letters_and_digits) for _ in range(32))
    return random_string



@app.get("/api/registration")
def private(response: Response, wallet: str, token: str = Depends(token_auth_scheme)):
    """A valid access token is required to access this route"""
    if tokenVer != token.credentials:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return result
    

    #       IN PROD WILL BE POSTGRESS
    #   JUST FOR TEST
    #                 

    connection = sqlite3.connect("venom.db")
    cursor = connection.cursor()
    with connection:
        result = cursor.execute("SELECT * FROM `venom` WHERE `wallet` = ?", (wallet,)).fetchall()

    if not result:
        randToken = generate_random_string()

        with connection:
            cursor.execute("INSERT INTO `venom` (`wallet`) VALUES (?)", (wallet,))
            cursor.execute("UPDATE `venom` SET `secret` = ? WHERE `wallet` = ? ", (randToken, wallet,))

        connection.close()
        return randToken
    else:
        connection.close()
        return "Already registered"

@app.get("/api/claimPoints")
def private(response: Response, secret: str, token: str = Depends(token_auth_scheme)):
    """A valid access token is required to access this route"""
    if tokenVer != token.credentials:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return result
    
    connection = sqlite3.connect("venom.db")
    cursor = connection.cursor()
    with connection:
        result = cursor.execute("SELECT `wallet` FROM `venom` WHERE `secret` = ?", (secret,)).fetchall()  
    if result == []:
        return "ERROR KEY"
    else:
        if result[0][0] is None:
            return "ERROR KEY"
        else:
            print(result[0][0])
            wallet = result[0][0]

            userPoints = 0
            with connection:
                result = cursor.execute("SELECT `points` FROM `venom` WHERE `secret` = ?", (secret,)).fetchall()  
                print(result)
                if result == []:
                    userPoints = 0
                else:
                    if result[0][0] is None:
                        userPoints = 0
                    else:
                        userPoints = int(result[0][0])

                    if userPoints == 0:
                        return "ZERO POINTS"
                    else:

                        call_set = CallSet(
                            function_name='addUser',
                            header=None,
                            input={"point" : userPoints,
                                "userAdress" : wallet}
                        )

                        signer = Signer.Keys(keys=keypair)

                        encode_params = ParamsOfEncodeMessage(
                            abi=events_abi, signer=signer, address=address, call_set=call_set
                        )

                        paramsProcess = ParamsOfProcessMessage(encode_params, send_events=True)

                        result = client.processing.process_message(paramsProcess)



@app.get("/api/setPoints")
def private(response: Response, secret: str, ansver: str, rightAnsver: str, question:  str, token: str = Depends(token_auth_scheme)):
    """A valid access token is required to access this route"""
    if tokenVer != token.credentials:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return result
    
    connection = sqlite3.connect("venom.db")
    cursor = connection.cursor()
    with connection:
        result = cursor.execute("SELECT `wallet` FROM `venom` WHERE `secret` = ?", (secret,)).fetchall()  
    if result == []:
        return "ERROR KEY"
    else:
        if result[0][0] is None:
            return "ERROR KEY"
        else:
            print(result[0][0])
            wallet = result[0][0]

            ansv = claster_response(ansver,rightAnsver,question)
            parts = ansv.split("-")
            resp = {
                "ponts" : parts[0],
                "gpt": parts[1]
            }

            pointInt = int(parts[0])
            userPoints = 0
            with connection:
                result = cursor.execute("SELECT `points` FROM `venom` WHERE `secret` = ?", (secret,)).fetchall()  
                print(result)
                if result == []:
                    userPoints = 0
                else:
                    if result[0][0] is None:
                        userPoints = 0
                    else:
                        userPoints = int(result[0][0])

                sumPoints = userPoints + pointInt
                with connection:
                    cursor.execute("UPDATE `venom` SET `points` = ? WHERE `secret` = ? ", (sumPoints, secret,))

            connection.close()
            return resp

    