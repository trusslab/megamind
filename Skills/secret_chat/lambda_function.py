# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.ui import SimpleCard


from ask_sdk_model import Response

#for Asymetric public/private key encryption
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.serialization import load_pem_public_key
import base64
#for symetric AES
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers.algorithms import AES
from cryptography.hazmat.primitives.ciphers.modes import CBC,OFB,CFB
from hashlib import sha3_256
from os import urandom
from cryptography.hazmat.backends import default_backend

import hmac

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
backend = default_backend()

class AES_Cipher:
    def __init__(self,key):
        self.key = key
        
    def encrypt(self,plain_text):
        initialization_vector = urandom(16)
        cipher = Cipher(AES(self.key),OFB(initialization_vector),backend)
        encryption_engine = cipher.encryptor()
        return initialization_vector + encryption_engine.update(plain_text.encode("utf-8")) + encryption_engine.finalize()

    def decrypt(self,cipher_text):
        initialization_vector = cipher_text[:16]
        cipher = Cipher(AES(self.key),OFB(initialization_vector),backend)
        decryption_engine = cipher.decryptor()
        return (decryption_engine.update(cipher_text[16:]) + decryption_engine.finalize()).decode("utf-8")

AES_engine = AES_Cipher("")


count = 0
rsa_key = b"-----BEGIN RSA PRIVATE KEY-----\nProc-Type: 4,ENCRYPTED\nDEK-Info: AES-256-CBC,F039845938688FA23061D24753A3DBF4\n\nfDtwuM+3UjTbrCZaLuS0UqTGGRF5xIvuOqTXHnOA3IZxIChEjxvIU0y8IuaIcqHJ\nHHlQ+siKmqZoBUgFiw0Hm+lnYg7O2zkii7ULGx9VR2gbKkNqMWsDYJkFqFLFzUa0\ne2LhyJ8/JXpuAyGwUM/AXWKsshd2t2u8uoYmvEOEwCn0XERLFHkPuUIaxuiQCWxt\nRzKlSopwQUGxVJ/OcBMvn2ZTR63+2dvonk1zbOK7Vc6S/JKr0ic+Xhtlxv8Ka3Lk\ntHf8NMwu0pRi+EnFQ8nWw8u8jb7BwKT46FoqZlGFAvNGElmpua4a5551vXvihwJd\nCKW2I7VXxgR2B0N7ZjT6XHIkFs4yvvdYLvKByyWmfV+rHJl/0KQqr0CQ+EKjBX35\nDHJRBdm3Fyh5fhut55yyY+IuEwhhMgOW7dlxxujsL403KEyCwDq3dsizSfOMnwta\nI4BF3H7E1Vxg53f5BpV4tWhJyyjOtiNoADwuA6dPjAXKXDPfEgXwl/zBNg7VyJB8\n13IozGdV7SSJtPoUsuVZ3QZy+gtxVJgq/OlRp/bcDovGF9qxPR7WPSPUnBirIyCF\nkjk+ddFzDwkhdWjGv4MhQ8MxMhZdr9498Ok8NBVEjq5/f+cA0jmoKIZ7oSKk00kb\nqMiom8O04lPySy+wQPnm4RVjQZwW6Amg2REQoGm883QjYwHFb6pO8GfzJ+6Kt9au\nQf0kJJ1T2IDO9n69q3xHLeNCtHHK/VvcH50nggsU2rCVXBHg9tcMN0NDvJFnzDQz\nNkPB3beRtsrKUUS6ICB7WuXgtei/I+77XUlt9Vyf6ZgiGLf4m1fSBdZeTeLqMBK2\n-----END RSA PRIVATE KEY-----\n"
PrivKey = load_pem_private_key(rsa_key,b"popPdPd",default_backend())

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Welcome to the confidential conversation skill. Do you want to start a secret conversation?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class HelloWorldIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("HelloWorldIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Hello World!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
class KeyIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("key_intent")(handler_input)

    def handle(self, handler_input):
        global user_name
        global AES_engine
        # type: (HandlerInput) -> Response
        #print speech_text
        slots = handler_input.request_envelope.request.intent.slots
        name = slots['cmd']
        sym_key_cyphered = name.value
        print(name)
        sym_key_cyphered = sym_key_cyphered.upper()
        sym_key_cyphered = sym_key_cyphered + "==="
        print (sym_key_cyphered)
        sym_key_cyphered_bytes = base64.b32decode(sym_key_cyphered)
        print('after')
        sym_key_plain = PrivKey.decrypt(
            sym_key_cyphered_bytes,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
        )
        print(str(sym_key_plain))
        AES_engine.key = sym_key_plain
        speech_text = "A secure connection has established. Tell me some thing"
#        handler_input.response_builder.speak(speech_text).set_card(
#            SimpleCard("sure", speech_text)).set_should_end_session(
#            True)
        handler_input.response_builder.speak(speech_text).set_should_end_session(
            False)
        return handler_input.response_builder.response

def encrypt_request(req):
    AES_KEY = AES_engine.key
    cypher = AES_engine.encrypt(req)
    digest = hmac.new(AES_KEY, cypher, sha3_256).digest()
 #   print(digest)
    coded_digest = base64.b32encode(digest)
    coded_cypher = base64.b32encode(cypher)
#   print('[1]', coded_cypher)
    coded_cypher = coded_cypher.decode().replace('=','').lower()
    coded_digest = coded_digest.decode().replace('=','').lower()
#    print(coded_digest)
#   print('[2]',coded_cypher)
    return coded_cypher + '8' + coded_digest

def decrypt_response(resp):
    AES_KEY = AES_engine.key
    index = resp.find('8')
    new_resp = resp[0:index]
    hash_resp = resp[index+1:]
    resp = new_resp
    old_resp = resp
    l = len(resp)
    r = l % 8
    if( r != 0):
        for i in range(0,8-r):
            resp = resp + '='
    l = len(hash_resp)
    r = l % 8
    if( r != 0):
        for i in range(0,8-r):
            hash_resp = hash_resp + '='
    hash_text = hash_resp.upper()

    try:
        cypher_text = resp.upper()
    #   print(cypher_text)
        cypher_text_bytes = base64.b32decode(cypher_text)
    #   print(cypher_text_bytes)
        digest = hmac.new(AES_KEY, cypher_text_bytes, sha3_256).digest()
        coded_digest = base64.b32encode(digest)
        coded_digest = coded_digest.decode()
        print('coded_digest ',coded_digest,'  len= ', len(coded_digest))
        print('hash_text    ',hash_text, '  len= ',len(hash_text))
        if(coded_digest != hash_text):
            return 'HMAC does not match'
        plain_text = AES_engine.decrypt(cypher_text_bytes)
    except:
        plain_text = old_resp
    return plain_text

class SecretIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("secret_chat")(handler_input)

    def handle(self, handler_input):
        global user_name
        global AES_engine
        # type: (HandlerInput) -> Response
        #print speech_text
        slots = handler_input.request_envelope.request.intent.slots
        name = slots['cmd']
        user_name = name.value
        print(name)
        print (name.value)
        rtext = name.value
 #       l = len(rtext)
 #       r = l % 8
 #       if( r != 0):
 #           for i in range(0,8-r):
 #               rtext = rtext + '='
 #       cypher_text = rtext.upper()
 #       print(cypher_text)
 #       cypher_text_bytes = base64.b32decode(cypher_text)
 #       print(cypher_text_bytes)
 #       plain_text = AES_engine.decrypt(cypher_text_bytes)
        plain_text = decrypt_response(rtext)
        speech_text_plain = "You said " + plain_text + " . what next"
 #       print('[1] plain text ',plain_text)
 #       speech_text_cipher = AES_engine.encrypt(speech_text_plain)
 #       print('[2]')
 #       coded_cypher = base64.b32encode(speech_text_cipher)
        print('[3] speech_text_plain ',speech_text_plain)
 #       speech_text = coded_cypher.decode().replace('=','').lower()
        speech_text = encrypt_request(speech_text_plain)
        print('[4] speech text ',speech_text)
        handler_input.response_builder.speak('mega card you have a secret message short wait here to complete reading and a little bit more speeech is ').set_card(
            SimpleCard('title',speech_text)).set_should_end_session(
            False)
#        handler_input.response_builder.speak(speech_text).set_should_end_session(
#            False)
        return handler_input.response_builder.response

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(SecretIntentHandler())
sb.add_request_handler(KeyIntentHandler())

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelloWorldIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
