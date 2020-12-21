from webdriver_manager.firefox import GeckoDriverManager
import selenium
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import Select
import os
import re
import time
import csv

opts = Options()
opts.add_argument('--headless')
binary = FirefoxBinary(os.path.join('c:/', 'Program Files', 'Mozilla Firefox', 'firefox.exe'))
opts.binary = binary
#assert opts.headless  # Operating in headless mode
browser = Firefox(executable_path=GeckoDriverManager().install(), options=opts)
browser.implicitly_wait(3)
browser.get("https://finance.yahoo.com/quote/TSLA/options")
time.sleep(5)
calls = {}
puts = {}
select_dropdown = browser.find_element_by_tag_name("select")
element_select = Select(select_dropdown)
options = element_select.options
ticker = "TSLA"
for date in range(len(options)):
    try:
        select_dropdown = browser.find_element_by_tag_name("select")
        element_select = Select(select_dropdown)
        options = element_select.options
        time.sleep(8)
        element_select.select_by_index(date)
        time.sleep(5)
        rows = browser.find_elements_by_tag_name("tr")
        for row in rows:
            try:
                if row.text.find("TSLA") != -1:
                    formatted_row = row.text.replace(" EST", "_EST").split(" ")
                    exp_date = formatted_row[0].replace(ticker, "")[:6]
                    if len(re.findall(r"\dC\d", formatted_row[0] )) > 0:
                        calls["EXP DATE"] = f"{exp_date[2:4]}-{exp_date[4:]}-20{exp_date[:2]}"
                        calls["AVAILABLE_CONTRACTS"] = {} if "AVAILABLE_CONTRACTS" not in calls else calls["AVAILABLE_CONTRACTS"]
                        calls["AVAILABLE_CONTRACTS"][formatted_row[0]] = {"LAST_TRADE_DATE": formatted_row[1],
                                                                     "STRIKE": formatted_row[2],
                                                                    "LAST_PRICE": formatted_row[3],
                                                                   "BID": formatted_row[4],
                                                                  "ASK": formatted_row[5],
                                                                 "CHANGE": formatted_row[6],
                                                                "PERCENT_CHANGE": formatted_row[7],
                                                               "VOLUME": formatted_row[8],
                                                              "OPEN_INTEREST": formatted_row[9],
                                                             "IMPLIED_VOLATILITY": formatted_row[10]}
                        print(calls["EXP DATE"], calls["AVAILABLE_CONTRACTS"][formatted_row[0]])
                    elif len(re.findall(r"\dP\d", formatted_row[0] )) > 0:
                        puts["EXP DATE"] = f"{exp_date[2:4]}-{exp_date[4:]}-20{exp_date[:2]}"
                        puts["AVAILABLE_CONTRACTS"] = {} if "AVAILABLE_CONTRACTS" not in puts else puts["AVAILABLE_CONTRACTS"]
                        puts["AVAILABLE_CONTRACTS"][formatted_row[0]] = {"LAST_TRADE_DATE": formatted_row[1],
                                                                     "STRIKE": formatted_row[2],
                                                                    "LAST_PRICE": formatted_row[3],
                                                                   "BID": formatted_row[4],
                                                                  "ASK": formatted_row[5],
                                                                 "CHANGE": formatted_row[6],
                                                                "PERCENT_CHANGE": formatted_row[7],
                                                               "VOLUME": formatted_row[8],
                                                              "OPEN_INTEREST": formatted_row[9],
                                                             "IMPLIED_VOLATILITY": formatted_row[10]}
                        print(calls["EXP DATE"], puts["AVAILABLE_CONTRACTS"][formatted_row[0]])
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
browser.close()

        