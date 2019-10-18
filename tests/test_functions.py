import unittest
import datetime
import hashlib
from listdir_pkg import listdir
# import listdir_pkg


class TestFunctions(unittest.TestCase):

    def test_add_datetime(self):
        formats = ['%Y%m%d_%H-%M-%S', '%Y%B%d_%H-%M-%S']

        for time_format in formats:
            filename = listdir.add_datetime('samplefile.csv', time_format)

            curr_date = datetime.datetime.now()
            str_date = curr_date.strftime(time_format)

            self.assertEqual(filename, "{}_{}".format(str_date, 'samplefile.csv'))

    def test_hash(self):
        file = 'output.csv'

        hash_value_SHA1 = listdir.get_hash(file, 'sha1')
        hash_value_MD5 = listdir.get_hash(file, 'md5')
        hash1 = 'E7C88FA52FFAF0E5D9F48BC2E86FBEC730BA981C'.lower()
        hash2 = '95F241FF64ED54E8339663C209822520'.lower()
        self.assertEqual(hash_value_SHA1, hash1)
        self.assertEqual(hash_value_MD5, hash2)


if __name__ == '__main__':

    unittest.main()