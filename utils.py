from typing import Callable, Dict
from os import path
from functools import lru_cache
import requests

from configs import cookies

def extract_year_day_from_path(pathstr: str) -> Dict:
    '''
    >>> extract_year_day_from_path(path: '/path/to/AdventofCode/2015/day15.py')
    {'year': 2015, 'day': 15}
    '''
    path_year, file_name = path.split(pathstr)
    _, year = path.split(path_year)
    day, ext = file_name.split('.')
    day_int = int(day.replace('day', ''))
    return {'year': int(year), 'day': day_int}

class AdventSession:
    '''
    To get the cookies of the current session:
    1. Go to an Advent input page, which requires login.
    2. Right click and go to "inspect element" of developer tool, click on Network tab
    3. Refresh the page, so "input" data would appear under name (bottom-left conner), click on that.
    4. On the right side, click on "Cookies" tab. You'll see a table with session under Name
    5. Copy the hash in session value column.
    6. Setup your cookies here: cookies = {'session': <YOUR_SESSION_HASH_VALUE>}
    '''
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
    
    def check_if_answer_can_be_submitted(self, ans: str, level: int) -> bool:
        '''Check if there's a form input at the right level with current cookies session'''
        question = requests.get(self.base_url, cookies=cookies)
        if question.status_code == 200:
            quest_html = question.text
            if '</form>' in quest_html:
                form_html = quest_html[quest_html.index('<form'):quest_html.index('</form>')]
                if 'name="level" value="1"' in form_html and level != 1:
                    print(f'Not submitting {ans} because its not for level 1')
                    return False
                elif 'name="level" value="2"' in form_html and level != 2:
                    print(f'Not submitting {ans} because its not for level 2')
                    return False
                return True
            else:
                print('Could not submit answer because theres no form input. Both answers may have already been submitted')
                return False
        else:
            print(f'Could not access site {self.base_url}')
            return False

    def post_answer(self, ans: str,  level: int=1) -> str:
        if not self.check_if_answer_can_be_submitted(ans, level):
            return None
        answer_resp = requests.post(self.base_url + '/answer',
                                    data={'answer': ans, 'level': level},
                                    cookies=self.cookies)
        if answer_resp.status_code == 200:
            result_html = answer_resp.text
            print(result_html[result_html.index('<main>'): result_html.index('</main>')])
        else:
            raise Exception(answer_resp.text)
        
    def submit_result(self, level=1):
        def innerf(solver: Callable):
            def wrapper(*args, **kwargs):
                result = solver(*args, **kwargs)
                print(f'part {level} result {result}')
                if not self.check_if_answer_can_be_submitted(result, level):
                    return None
                answer_resp = requests.post(self.base_url + '/answer',
                                            data={'answer': result, 'level': level},
                                            cookies=self.cookies)

                if answer_resp.status_code == 200:
                    result_html = answer_resp.text
                    print(result_html[result_html.index('<main>'): result_html.index('</main>')])
                else:
                    raise Exception(answer_resp.text)
                return result
            return wrapper
        return innerf
        
        