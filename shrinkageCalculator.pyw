import undetected_chromedriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from itertools import repeat, chain 
from missing_trays import missed_planting
import time

def shrinkageReport(profile, date, hps):

    options = webdriver.ChromeOptions()

    options.add_argument(f"user-data-dir={profile}")

    driver = webdriver.Chrome(options = options, use_subprocess = True)
    url = f'https://farmboard.infarm.com/locations/f1903b06-fe2c-4131-bfe9-6de379508289/daily/{date}/workstations/product/packing/shrinkage'

    driver.get(url)
    driver.maximize_window()

    driver.execute_script("window.open('');")
    driver.implicitly_wait(150)

    def expand_shadow_element(element):
      shadow_root = driver.execute_script('return arguments[0].shadowRoot', element)
      return shadow_root

    root = driver.find_element(By.TAG_NAME, 'inhub-shrinkage-table')
    shadow_root = expand_shadow_element(root)

    #batch_ids = shadow_root.find_elements(By.CLASS_NAME, "batchid") 
    varieties =  shadow_root.find_elements(By.CLASS_NAME, "varietyName")
    expected_plants = shadow_root.find_elements(By.CLASS_NAME, "expectedPlants")
    missing_elements = shadow_root.find_elements(By.ID, "missingInput")
    shrinkage_elements = shadow_root.find_elements(By.ID, "shrinkageInput")
    expected_plants_num = [expected_plants[x].text for x in range(len(expected_plants))]
    variety =  shadow_root.find_elements(By.CLASS_NAME, "variety")
    variety_style = [variety[x].get_attribute("style")[19:31] for x in range(len(variety))]

    missing = missed_planting(date)

    batch_ids_list = variety_style

    data = [['n','n','n','n'] for n in range(len(batch_ids_list))]

    salads = ['Caravel_33cc (3 Week Acre)', 'Crystal_33cc (3 Week Acre)', 'Red Oakleaf_ 33cc (3 week Acre)', 'Red_romaine_33cc (3 Week Acre)']

    for i in range(len(batch_ids_list)):
        data[i][0] = batch_ids_list[i]
        data[i][1] = varieties[i].text
        data[i][2] = expected_plants[i].text

        if missing != []:
            for missed in missing:
                if missed[0] == batch_ids_list[i] and missed[1] == varieties[i].text:
                    data[i][3] = missed[2]
                    break
                elif varieties[i].text[0:4] == 'Pots':
                    data[i][3] = '4'
                elif data[i][1] in salads:
                    data[i][3] = data[i][2]
                else:
                    data[i][3] = '12'
            
        elif missing == []:
            if varieties[i].text[0:4] == 'Pots':
                data[i][3] = '4'
            elif data[i][1] in salads:
                    data[i][3] = data[i][2]
            else:
                data[i][3] = '12'

    clean_data = []

    for element in data:
        if any("Empty" in s for s in element) or any('Nursery' in s for s in element) or any('Crop' in s for s in element):
            continue
        else:
            clean_data.append(element)

    missing_input = [str(int(float(x[3]))) for x in clean_data]
    shrinkage_inputs = []

    for element in clean_data:
        if float(element[2]) == float(element[3]):
            shrinkage_inputs.append('0')
        else:
            formula = round((1 - (hps[element[1]]/100)) * (int(float(element[2])-float(element[3]))))
            shrinkage_inputs.append(formula)

    for i in range(len(missing_input)):
        missing_elements[i].clear
        missing_elements[i].send_keys(missing_input[i])
        shrinkage_elements[i].clear
        shrinkage_elements[i].send_keys(shrinkage_inputs[i])

    time.sleep(300)