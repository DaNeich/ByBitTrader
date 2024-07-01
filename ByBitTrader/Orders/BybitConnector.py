from pybit.unified_trading import HTTP

##############  ByBit API own generated KEYS  ##########################################################################
############## Keep ApiKey and SecretKey safe, not share them to anyone ################################################

key = 'YOUR_SECRET'
secret = 'YOUr_API_KEY'


############# Autheticantion ###########################################################################################

def newSession():
    session = HTTP(api_key=key, api_secret=secret, testnet=False)
    return session
