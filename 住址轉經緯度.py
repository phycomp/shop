from selenium webdriver import ChromeOptions
targetUrl = 'https://www.map.com.tw/'

def rtrv經緯():
  chrmOpts = ChromeOptions() #webdriver.
  browser = webdriver.Chrome(options=chrmOpts) #載入瀏覽器設定
  browser.get(targetUrl)

def 經緯度(addr):
  chrmOpts = ChromeOptions()    #webdriver.
  browser = Chrome(options=chrmOpts) #webdriver.
  browser.get(targetUrl)
  search = browser.find_element_by_id('searchWord')
  search.clear()
  search.send_keys(addr)
  browser.find_element_by_xpath("/html/body/form/div[10]/div[2]/img[2]").click()
  iframe = browser.find_element_by_class_name("winfoIframe")
  browser.switch_to.frame(iframe)
  co_btn = browser.find_element_by_xpath("/html/body/form/div[4]/table/tbody/tr[3]/td/table/tbody/tr/td[2]")
  co_btn.click()
  page_results = browser.find_element_by_xpath("/html/body/form/div[5]/table/tbody/tr[2]/td")
  coor = page_results.text.strip().split(" ")
  lat = coor[-1].split("：")[-1]
  lng = coor[0].split("：")[-1]
  browser.quit() #關閉網頁
  return lat, lng
