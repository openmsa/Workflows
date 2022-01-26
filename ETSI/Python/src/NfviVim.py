import requests
from requests.exceptions import HTTPError
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from custom.ETSI.BaseApi import BaseApi


class NfviVim(BaseApi):

    VIM_URL = 'admin/vim'

    def nfvi_vim_register(self, _payload):
        _url = self.VIM_URL + '/register'
        response = self.do_post(_url, _payload)
        return response

    def nfvi_vim_delete(self, _vimId):
        _url = self.VIM_URL + "/" + _vimId
        response = self.do_delete(_url)
        return response

    def nfvi_vim_get(self):
        _url = self.VIM_URL
        response = self.do_get(_url)
        return response
