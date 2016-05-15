import time
import struct
import urllib.parse, urllib.request


def construct_request_body(timestamp, itunes_identifier):
    hex = "61 6a 43 41 00 00 00 45 6d 73 74 63 00 00 00 04 55 94 17 a3 6d 6c 69 64 00 00 00 04 00 00 00 00 6d 75 73 72 00 00 00 04 00 00 00 81 6d 69 6b 64 00 00 00 01 02 6d 69 64 61 00 00 00 10 61 65 41 69 00 00 00 08 00 00 00 00 11 8c d9 2c 00"

    body = bytearray.fromhex(hex);
    body[16:20] = struct.pack('>I', timestamp)
    body[-5:] = struct.pack('>I', itunes_identifier)
    return body


def add_song(itunes_identifier):
    data = construct_request_body(int(time.time()), itunes_identifier)

    headers = {
        "Host" : "ld-2.itunes.apple.com:443",
        "Proxy-Connection" : "keep-alive",
        "X-Apple-Store-Front" : "143441-1,32 ab:SEED1",
        "Client-iTunes-Sharing-Version" : "3.13",
        "Accept-Language" : "en-us, en;q=0.50",
        "Client-Cloud-DAAP-Version" : "1.2/iTunes-12.3.3.17",
        "Accept-Encoding" : "gzip",
        "X-Apple-itre" : "0",
        "Content-Length" : "77",
        "Client-DAAP-Version" : "3.13",
        "User-Agent" : "iTunes/12.3.3 (Macintosh; OS X 10.11) AppleWebKit/601.1.56",
        "Connection" : "keep-alive",
        "Content-Type" : "application/x-dmap-tagged",
        # Replace the values of the next three headers with the values you intercepted
        "X-Dsid" : "1226709022",
        "Cookie" : "amia-1226709022=mfE1qoe4RGJ1g7i2yXcXhAxlAEoG6+GtSH3+cDz54zoOt5xItzYopDMJckrrx6hB0Re1aIAvDdLgLD9H2bidsg==; amp=UxdMcoFncFCCgRcUryCOjo4/JCVXZwtQ1lXrdS0ReOEZ8AzVwcwzDo7vTu3oCbVHXl5M1uILzzYnVlBAKlA/J/1v14nHJte80n7BO976FPCV21IoVoOKxdpMCWxFA7C2xHzf0DgQtr8PVPAM5Nrdj9Myv5/DWvaqmbTJwMnwp9HLnXIKLa/Vb9Q/1Oy9SPwjlaetvh1XTpYL70is1QoK4oLpWwPcqUm0u4zJ/loZ4TyGSSbifktqhTlboGfW4+FF; groupingPillToken=1_iphone; mt-asn-1226709022=15; mt-tkn-1226709022=AqlYPRyImMeIPQ1YJoGRUTE0BpqcUYtLe47N3Zik4ybVG8cSjfTnD2c8MBwEqqgsaB8kwNmtBS2WOBv2e7CY3wKPYIVy7nNCsNjupTjH5Xy+mjxffBAZ05f5hrR6L7AU7MBpRLQcoBYIolYPdeTgII6NE8WgnfqImcgQHSDO6N4fvMnun3w7TUVElVmpg3qjMDdUlto=; mzf_in=302345; a=QQAVAAAACwAyxIEIMTAwMGw0UUoBMwAAAAE=; itspod=30; mz_at0-1226709022=AwQAAAEBAAHV7wAAAABXLpTNIX7hZ0YCqVtKf2fQd/fiVOsrYC4=; mz_at_ssl-1226709022=AwUAAAEBAAHV7wAAAABXNX94UfRE9cfMRmn+5cMhLzjde4fyA38=; s_vi=[CS]v1|2AD292BF05013F91-6000010B40000241[CE]; TrPod=2; X-Dsid=1226709022; xp_ci=3z3FXUjazDXvz4YLzBmszKqkEcYDb",
        "X-Guid" : "E0ACCB62B5A6"
    }

    request = urllib.request.Request("https://ld-2.itunes.apple.com/WebObjects/MZDaap.woa/daap/databases/1/cloud-add", data, headers)
    urllib.request.urlopen(request)


with open('itunes.csv') as itunes_identifiers_file:
    for line in itunes_identifiers_file:
        itunes_identifier = int(line)

        try:
            add_song(itunes_identifier)
            print("Successfuly inserted a song!")
            # Try playing with the interval here to circumvent the API rate limit
        except Exception as e:
            print("Something went wrong while inserting " + str(itunes_identifier) + " : " + str(e))
