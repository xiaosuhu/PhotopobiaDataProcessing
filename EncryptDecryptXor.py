import base64, gzip, zlib
from urllib.parse import quote,unquote

def EncryptXor(stren, key):
  # EncryptXor(file, key):
    #with open(file, mode='rb') as file: # b is important -> binary
    #  data = file.read()
    
    data = stren
    d = 0
    k = 0
    output = bytearray(len(data))
    # print(data[1]^key[1])
    # print(key[0])

    while d < len(data):
      while k < len(key) and d < len(data):
        output[d] = data[d] ^ key[k]
        d += 1
        k += 1
        # print(str(d) + 'k' + str(k) + 'one byte encrypted...')

      k = 0
    
    #outputb64=base64.b64encode(output)
    #newfile = open('testxor','wb')
    #newfile.write(outputb64)

    return output


def DecryptXor(datab64, key):
   # with open(file, mode='rb') as file: # b is important -> binary
   #   datab64 = file.read()
    data = base64.b64decode(datab64,validate=True)
    
    d = 0
    k = 0
    output = bytearray(len(data))
    # print(data[1]^key[1])
    # print(key[0])

    while d < len(data):
      while k < len(key) and d < len(data):
        output[d] = data[d] ^ key[k]
        d += 1
        k += 1
        # print(str(d) + 'k' + str(k) + 'one byte decrypted...')

      k = 0
  
    output = gzip.decompress(output)
    # newfile = open('testb64.gz','wb')
    # newfile.write(output)
    return output


def datacompress(data):
  # Get the data going with pako inflate in the client
  compdata=pako_deflate(data)
  bdata=base64.b64encode(compdata)
  return bdata

def pako_deflate(data):
    compress  = zlib.compressobj(zlib.Z_DEFAULT_COMPRESSION, zlib.DEFLATED, 15, 
        memLevel=8, strategy=zlib.Z_DEFAULT_STRATEGY)
    # compressed_data = compress.compress(js_string_to_byte(js_encode_uri_component(data)))
    compressed_data = compress.compress(data)
    compressed_data += compress.flush()
    return compressed_data

def pako_inflate(data):
    decompress = zlib.decompressobj(15)
    decompressed_data = decompress.decompress(data)
    decompressed_data += decompress.flush()
    return decompressed_data

def js_encode_uri_component(data):
    return quote(data, safe='~()*!.\'')


def js_decode_uri_component(data):
    return unquote(data)


def js_string_to_byte(data):
    return bytes(data, 'iso-8859-1')


def js_bytes_to_string(data):
    return data.decode('iso-8859-1')


def js_btoa(data):
    return base64.b64encode(data)


def js_atob(data):
    return base64.b64decode(data)