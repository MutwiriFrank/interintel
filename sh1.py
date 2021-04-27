import hashlib

def sh1(object):
    #encode() : Converts the string into bytes to be acceptable by hash function.


    hash_object = hashlib.sha1(object.encode())

    #To generate, sequence of bytes

    return(hash_object.digest())


print(sh1('interintel'))
 # it returns b'\xbc\xfe\xe63\x88Y9^\xd3\x0f\x04\xd2\x0c\xfdG\xfa\xcd4r\x17'