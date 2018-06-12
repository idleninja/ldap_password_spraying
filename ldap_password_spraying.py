#!/usr/bin/python
import ldap, sys, os
from getpass import getpass
from time import sleep


def checkCredential(username="", password="", server="exampleDC.domain.tld"):

	if username and password:
		baseDN = 'dc=domain,dc=tld'
		usersDN = 'ou=production,ou=users'

		l = ldap.initialize('ldap://%s:389' % server) 

		try:
		    l.protocol_version = ldap.VERSION3
		    l.simple_bind_s("cn=%s,ou=production,ou=users,dc=domain,dc=tld" % username, password)
		    l.set_option(ldap.OPT_REFERRALS,0)
		    return True

		except(ldap.INVALID_CREDENTIALS):
		    return False

		except Exception, error:
		    print error
		    return None


def main():
	if not sys.argv[1]:
		print "Usage: ./%s %s" % (sys.argv[0], "Username List File")
		exit()

	users_file_path = sys.argv[1]
	if os.path.exists(users_file_path):
		users = [user for user in open(users_file_path, "r").read().splitlines() if user]

	if users:
		password = getpass()
		for user in users:
			print("Attempting credential check on %s with password %s" % (user, password)) 
			print checkCredential(user, password)
			sleep(1)
			

if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt):
        print("^C")
        exit()
