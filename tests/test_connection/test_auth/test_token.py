import unittest
from datetime import datetime
from src.connection.client import Token


class TestToken(unittest.TestCase):
    """Test for src.connection.auth.token.Token class"""
    def test_token_init(self):
        test_token_value = "testtesttesttesttesttest"
        test_init_time = 1729083208.760576
        test_expire_time = test_init_time + 86400
        test_token = Token(test_token_value, test_init_time)

        self.assertTrue(test_token.value == test_token_value)
        self.assertTrue(test_token.get_init_time() == datetime.fromtimestamp(test_init_time))
        self.assertTrue(test_token.get_expire_time() == datetime.fromtimestamp(test_expire_time))




    def test_token_reset(self):
        test_token_value = "testtesttesttesttesttest"
        test_init_time = 1729083208.760576
        test_token = Token(test_token_value, test_init_time)
        new_token_value = "test2"
        new_init_time1 = 1729083208.760576
        new_expire_time1 = new_init_time1 + 86400

        new_init_time2 = 1729083210
        new_expire_time2 = new_init_time2 + 86400

        test_token.reset_value(new_token_value)
        self.assertTrue(test_token.value == new_token_value)

        test_token.reset_init_time(new_init_time1)
        self.assertTrue(test_token.get_init_time() == datetime.fromtimestamp(new_init_time1))
        self.assertTrue(test_token.get_expire_time() == datetime.fromtimestamp(new_expire_time1))

        test_token.reset_init_time(new_init_time2)
        self.assertTrue(test_token.get_init_time() == datetime.fromtimestamp(new_init_time2))
        self.assertTrue(test_token.get_expire_time() == datetime.fromtimestamp(new_expire_time2))



    def test_token_validate(self):
        test_token_value = "testtesttesttesttesttest"
        test_init_time1 = 729082100.760576
        test_token1 = Token(test_token_value, test_init_time1)
        self.assertTrue(test_token1.is_expired())

        test_init_time2 = 1729083208.760576
        test_token2 = Token(test_token_value, test_init_time2)
        self.assertTrue(not test_token2.is_expired())

        test_init_time3 = 1729083208.760576


    def test_token_clean(self):
        test_token_value = "testtesttesttesttesttest"
        test_init_time = 1729083208.760576
        test_token = Token(test_token_value, test_init_time)
        test_token.clean_token()
        self.assertTrue(test_token.value is None)