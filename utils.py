from typing import Dict
from os import path
from functools import lru_cache
import requests

from configs import cookies

def extract_year_day_from_path(pathstr: str) -> Dict:
    '''
    >>> extract_year_day_from_path(path: '/path/to/AdvenofCode/2015/day15.py')
    {'year': 2015, 'day': 15}
    '''
    path_year, file_name = path.split(pathstr)
    _, year = path.split(path_year)
    day, ext = file_name.split('.')
    day_int = int(day.replace('day', ''))
    return {'year': int(year), 'day': day_int}

class AdventSession:
    def __init__(self, year: int = 2015, day: int = 1) -> None:
        self.cookies = cookies
        self.base_url = f'https://adventofcode.com/{year}/day/{day}'

    @lru_cache(maxsize=32)
    def read_input(self) -> str:
        resp = requests.get(self.base_url + '/input',
                            cookies=self.cookies)
        if resp.status_code == 200:
            return resp.text
        else:
            raise Exception(resp.text)

    def post_answer(self, ans: str,  level: int=1) -> str:
        answer_resp = requests.post(self.base_url + '/answer',
                                    data={'answer': ans, 'level': level},
                                    cookies=self.cookies)
        if answer_resp.status_code == 200:
            result_html = answer_resp.text
            print(result_html[result_html.index('<main>'): result_html.index('</main>')])
        else:
            raise Exception(answer_resp.text)