from novaclient.v1_1 import Client as NovaClient
import unittest

def hibernate(username, password, tenant_name, auth_url, serverID):
    nova = NovaClient(username = username,
            api_key = password,
            project_id = tenant_name,
            auth_url = auth_url)
    server = nova.servers.get(serverID)
    server.shelve()

class VMHibernationTest(unittest.TestCase):
    
    # to run the test, a VM must be created on openstack first

    # after shelve() is invoked on the server, its state changes from
    # "ACTIVE" to "SHELVED" and then to "SHELVED_OFFLOADED"
    def test(self):
        nova = NovaClient(username = "admin",
                api_key = "password",
                project_id = "demo",
                auth_url = "http://192.168.50.4:5000/v2.0")
        server = nova.servers.list()[0]
        self.failUnless(server.status == "ACTIVE")
        hibernate("admin", 
                "password", 
                "demo", 
                "http://192.168.50.4:5000/v2.0",
                server.id)
        while server.status == "ACTIVE" or server.status == "SHELVED":
            server = nova.servers.list()[0]

        self.failUnless(server.status == "SHELVED_OFFLOADED")

def main():
    unittest.main()

if __name__ == "__main__":
    main()
