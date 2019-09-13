# use selenium to get dynamically generated web content from
# options = webdriver.ChromeOptions()
# options.add_argument("--ignore-certificate-errors")
# options.add_argument("--incognito")
# options.add_argument("--headless")
# driver = webdriver.Chrome("/Users/shaheryariqbal/bin/chromedriver", options=options)
# driver.manage().timeouts().implicitlyWait()
#
# url = "https://www.calottery.com/play/draw-results"
#
# driver.get(url)
#
# date_selector = driver.find_elements_by_class_name("select-hotspot-date hotspot-validate-date")
#
# for x in range(len(date_selector)):
#     print(x)
#     driver.execute_script("arguments[0].setAttribute('value', '08/01/2019')")
#
# page_source = driver.page_source
#
# soup = BeautifulSoup(page_source, "html.parser")
# print(soup.prettify())

url = "https://www.calottery.com/play/draw-games/hot-spot/draw-detail?draw=2522220"

response = requests.get(url)

#create BeautifulSoup object to parse winning numbers
soup = BeautifulSoup(response.text, "html.parser")

all_win_nums = soup.find_all("li", class_="spot win")

#find sample average for random number generation
#get sum of sample means
sample_sum = 0
sample_avg = 0

for num in all_win_nums:
    #is in a list element
    print(num.string)
    sample_sum += int(num.string)

sample_avg = sample_sum / NUM_SPOTS_PLAYED

print("Sample sum: " + str(sample_sum))
print("Sample Avg: " + str(sample_avg))

# print(soup.prettify())
