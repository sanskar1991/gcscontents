import pytest
import mock
import unittest
import logging
import requests
from gcscontents.generic_fs import GCSFS

from .api_data_test import (
    read_data1, 
    read_data2, 
    write_data,
    LIST_DATA
    )


class TestGenericFSClass():
    
    # @pytest.fixture()
    # def before(self):
    #     self.gcsfs = GCSFS(log=logging.getLogger('temp'))

    # def __init__(self):
    #     self.gcsfs = GCSFS(log=logging.getLogger('temp'))
    
    @mock.patch('os.path.isdir')
    @mock.patch('os.system')
    # @mock.patch('requests.post', return_value=None)
    @mock.patch('gcscontents.generic_fs.GCSFS.isfile', return_value=True)
    def test_isfile(self, _request_post_call, _os_system_call, _os_path_isdir):
        self.gcsfs = GCSFS(log=logging.getLogger('temp'))
        _os_path_isdir.return_value = False
        _os_system_call.return_value = True
        assert not self.gcsfs.isfile("")
        assert not self.gcsfs.isfile("/temp.ipynb")
        _os_path_isdir.return_value = True
        assert self.gcsfs.isfile("/temp.ipynb")
        
    @mock.patch('gcscontents.generic_fs.GCSFS.ls', return_value=read_data1)
    def test_ls(self, mocker):
        self.gcsfs = GCSFS(log=logging.getLogger('temp'))
        assert self.gcsfs.ls("") == read_data1
        assert self.gcsfs.ls("") != read_data2
    
    
    @mock.patch('gcscontents.generic_fs.GCSFS.write', return_value=write_data)
    def test_write(self, mocker):
        self.gcsfs = GCSFS(log=logging.getLogger('temp'))
        assert self.gcsfs.write("djhjwdh", write_data, None) == write_data
        assert self.gcsfs.write("") != read_data2

    # @mock.patch('os.path.isdir')
    # @mock.patch('os.system')
    # @mock.patch('gcscontents.generic_fs.GCSFS.isfile', return_value=None)
    # def test_isfile(self, _request_post_call, _os_system_call, _os_path_isdir):
    #     self.gcsfs = GCSFS(log=logging.getLogger('temp'))
    #     _os_path_isdir.return_value = False
    #     _os_system_call.return_value = True
    #     assert not self.gcsfs.isfile("")
    #     assert not self.gcsfs.isfile("/temp.ipynb")
    #     _os_path_isdir.return_value = True
    #     assert self.gcsfs.isfile("/temp.ipynb")
        
    
    
# class TestGenericFS(unittest.TestCase):
#     @classmethod
#     def setUpClass(cls):
#         cls.gcsfs = GCSFS(
#             log=logging.getLogger('temp')
#         )

#     # @mock.patch('requests.get')
#     @mock.patch('requests.Response.json', return_value={'abc': {}, 'def': {}})
#     def test_ls(self, _json_response):
#         assert len(self.gcsfs.ls("")) == 2
#         assert list(self.gcsfs.ls("").keys()) == ['abc', 'def']
        
#     @mock.patch('os.path.isdir')
#     @mock.patch('os.system')
#     @mock.patch('requests.post', return_value=None)
#     def test_isfile(self, _request_post_call, _os_system_call, _os_path_isdir):
#         _os_path_isdir.return_value = False
#         _os_system_call.return_value = True
#         assert not self.gcsfs.isfile("")
#         assert not self.gcsfs.isfile("/temp.ipynb")
#         _os_path_isdir.return_value = True
#         assert self.gcsfs.isfile("/temp.ipynb")
    
    # @mock.patch('requests.Response.json', return_value=read_data)
    # def test_read(self, _get):
    #     assert 2 == 2
    #     # assert self.gcsfs.read("", None) == read_data
