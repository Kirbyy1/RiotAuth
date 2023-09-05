from time import time

import capmonster_python

from RiotAuth.exceptions import UnableToSolveCaptcha

CAPMONSTER_API = "<API>"


def solve_hcaptcha(data):
    try:
        site_key = data["captcha"]["hcaptcha"]["key"]
        rq_data = data["captcha"]["hcaptcha"]["data"]
        captcha_solving_start = time()
        print("solving captcha...")
        capmonster = capmonster_python.HCaptchaTask(CAPMONSTER_API)  # api key
        capmonster.set_user_agent(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36")
        task_id = capmonster.create_task(website_url="https://auth.riotgames.com", website_key=site_key,
                                         custom_data=rq_data)
        result = capmonster.join_task_result(task_id)
        print(f'It took {time() - captcha_solving_start}sec to complete captcha')
        return result.get("gRecaptchaResponse")
    except Exception as e:
        raise UnableToSolveCaptcha(e) from e
