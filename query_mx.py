#! /usr/bin/python
import dns.resolver
import string
domain = 'browan.com'
for x in dns.resolver.query(domain, 'MX'):
    string_mx = x.to_text()
    answer = dns.resolver.query(string_mx.split(" ")[1],'A')
    print answer.address
