"""
Tests for host and role resolution.
"""
from unittest import TestCase
from fabric.api import env
from nose.tools import eq_
from confab.resolve import resolve_hosts_and_roles


class TestResolve(TestCase):

    def setUp(self):
        # define environments
        env.environmentdefs = {
            "test1": ["host1", "host2", "host3"],
            "test2": ["host2", "host3"],
            "test3": []
        }
        # define hosts
        env.roledefs = {
            "role1": ["host1", "host2", "host3"],
            "role2": ["host2", "host3"]
        }

    def test_only_environment(self):
        """
        Specifying only an environment, returns all of its hosts and roles.
        """
        eq_({"host1": set(["role1"]),
             "host2": set(["role1", "role2"]),
             "host3": set(["role1", "role2"])},
            resolve_hosts_and_roles("test1"))

    def test_only_empty_environment(self):
        """
        Specifying only an empty environment raises an exception.
        """
        with self.assertRaises(Exception):
            resolve_hosts_and_roles("test3")

    def test_only_unknown_environment(self):
        """
        Specifying only an unknown environment raises an exception.
        """
        with self.assertRaises(Exception):
            resolve_hosts_and_roles("test4")

    def test_host_without_roles(self):
        """
        Explicit hosts return all of their roles.
        """
        eq_({"host1": set(["role1"])}, resolve_hosts_and_roles("test1", ["host1"]))
        eq_({"host2": set(["role1", "role2"])}, resolve_hosts_and_roles("test1", ["host2"]))

    def test_unknown_host_without_roles(self):
        """
        Unknown host raises an exception.
        """
        with self.assertRaises(Exception):
            resolve_hosts_and_roles("test1", ["host4"])

    def test_host_without_roles_in_wrong_environment(self):
        """
        Explicit hosts don't have to be in the specified environment.
        """
        eq_({"host1": set(["role1"])}, resolve_hosts_and_roles("test2", ["host1"]))

    def test_hosts_without_roles(self):
        """
        Explicit host list returns all hosts and all of their roles.
        """
        eq_({"host1": set(["role1"]),
             "host2": set(["role1", "role2"])},
            resolve_hosts_and_roles("test1", ["host1", "host2"]))

    def test_role_without_hosts(self):
        """
        Explicit role returns all hosts in environment with that role.
        """
        eq_({"host1": set(["role1"]),
             "host2": set(["role1"]),
             "host3": set(["role1"])},
            resolve_hosts_and_roles("test1", [], ["role1"]))

    def test_roles_without_hosts(self):
        """
        Explicit role list returns all hosts in environment with any of those roles.
        """
        eq_({"host1": set(["role1"]),
             "host2": set(["role1", "role2"]),
             "host3": set(["role1", "role2"])},
            resolve_hosts_and_roles("test1", [], ["role1", "role2"]))

        eq_({"host2": set(["role1", "role2"]),
             "host3": set(["role1", "role2"])},
            resolve_hosts_and_roles("test2", [], ["role1", "role2"]))

    def test_unknown_role_without_hosts(self):
        """
        Explicit role returns all hosts in environment with that role.
        """
        with self.assertRaises(Exception):
            resolve_hosts_and_roles("test1", [], ["role4"])

    def test_unknown_environment_with_role_without_hosts(self):
        """
        Explicit role returns all hosts in environment with that role.
        """
        with self.assertRaises(Exception):
            resolve_hosts_and_roles("test4", [], ["role1"])

    def test_host_with_role(self):
        """
        Explicit host and role mappings return host and role.
        """
        eq_({"host1": set(["role1"])},
            resolve_hosts_and_roles("test1", ["host1"], ["role1"]))
        # Doesn't matter if host is in environment
        eq_({"host1": set(["role1"])},
            resolve_hosts_and_roles("test2", ["host1"], ["role1"]))
        # Or if environment is empty
        eq_({"host1": set(["role1"])},
            resolve_hosts_and_roles("test3", ["host1"], ["role1"]))
        # Or if environment exists
        eq_({"host1": set(["role1"])},
            resolve_hosts_and_roles("test4", ["host1"], ["role1"]))

    def test_hosts_with_role(self):
        """
        Explicit hosts and role mappings return role for all hosts.
        """
        eq_({"host1": set(["role1"]),
             "host2": set(["role1"])},
            resolve_hosts_and_roles("test1", ["host1", "host2"], ["role1"]))

    def test_host_with_roles(self):
        """
        Explicit host and roles mappings return all roles applicable for host.
        """
        eq_({"host1": set(["role1"])},
            resolve_hosts_and_roles("test1", ["host1"], ["role1", "role2"]))
        eq_({"host2": set(["role1", "role2"])},
            resolve_hosts_and_roles("test1", ["host2"], ["role1", "role2"]))

    def test_hosts_with_roles(self):
        """
        Explicit hosts and roles mappings return all roles applicable for hosts.
        """
        eq_({"host1": set(["role1"]),
             "host2": set(["role1", "role2"])},
            resolve_hosts_and_roles("test1", ["host1", "host2"], ["role1", "role2"]))
