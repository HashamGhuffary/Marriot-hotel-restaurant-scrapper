import csv
from time import sleep
import requests
import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

####################################################################################

Destination = 'Warsaw, Poland' # first try to input the city in the marriot site and then paste here the autocompleted text
start_date = '09/9/2019'
end_date = '09/29/2019'
room_count = '1'
numAdultsPerRoom = '1'

####################################################################################
parsed_des = urllib.parse.quote(Destination)
start_date_parse = urllib.parse.quote(start_date)
end_date_parse = urllib.parse.quote(end_date)

url = 'https://www.marriott.com/search/submitSearch.mi?roomTypeCode=&destinationAddress.region=&recordsPerPage=20&autoSuggestItemType=&destinationAddress.types=&propertyCode=&destinationAddress.stateProvinceShort=&isInternalSearch=true&destinationAddress.cityPopulation=&vsInitialRequest=false&searchType=InCity&destinationAddress.locality=&showAddressPin=&miniStoreFormSubmit=&destinationAddress.stateProvinceDisplayName=&destinationAddress.destinationPageDestinationAddress=&searchRadius=80467.2&singleSearchAutoSuggest=&destinationAddress.placeId=ChIJOwg_06VPwokRYv534QaPC8g&is-hotelsnearme-clicked=false&destinationAddress.addressline1=&for-hotels-nearme=Near&suggestionsPropertyCode=&pageType=&destinationAddress.name=&poiCity=&destinationAddress.countryShort=&poiName=&destinationAddress.address=&search-countryRegion=&collapseAccordian=is-hidden&singleSearch=true&destinationAddress.cityPopulationDensity=&destinationAddress.postalCode=&airportCode=&isTransient=true&destinationAddress.longitude=-73.980961&initialRequest=false&destinationAddress.website=&search-locality=&dimensions=0&keywords=&roomTypeCode=&propertyCode=&flexibleDateSearchRateDisplay=false&propertyName=&isSearch=true&marriottRewardsNumber=&isRateCalendar=false&incentiveType_Number=&incentiveType=&flexibleDateLowestRateMonth=&flexibleDateLowestRateDate=&marrOfferId=&multiRateClusterCodes=&isMultiRateSearch=&multiRateCorpCodesEntered=&lowestRegularRate=true&multiRateCorpCodes=&useMultiRateRewardsPoints=&js-location-nearme-values='
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

with open('Corporate_PRomo_SET_FOR_MARIOTT.csv', 'r') as f:
    reader = csv.reader(f)
    codes_list = list(reader)



def make_query(code_pased):
    Rate = []
    hotel_name_list = []
    hotel_adr_list = []
    hotel_dis_for_des_list = []

    payload = {'destinationAddress.destination': parsed_des, 'fromDate': start_date_parse, 'toDate': end_date_parse, 'roomCount': room_count, 'numAdultsPerRoom': numAdultsPerRoom, 'clusterCode': 'corp', 'corporateCode': code_pased } #'app': app_name, 'country': country_name}
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
    r = requests.get(url, params=payload, headers=headers)
    url_webdriver = str(r.url)
    print(url_webdriver)

    driver.get(url_webdriver)
    driver.get(url_webdriver)

    driver.implicitly_wait(3)

    try:
        hotel_names = driver.find_elements_by_xpath('//span[@class="l-property-name"]')
        hotel_addreses = driver.find_elements_by_xpath('//div[@class="l-s-col-4 l-m-col-8 l-l-col-12 l-m-col-last l-s-col-last t-font-s t-line-height-m m-hotel-address t-color-standard-90"]')

        outer_address_span = driver.find_elements_by_xpath('//span[@class="l-padding-left-quarter l-padding-right-quarter t-bg-standard-100 t-color-standard-20 border-radius-small"]')
        for m in outer_address_span:
            span_ele_distance = m.find_element_by_tag_name('span')
            hotel_dis_for_des_list.append(span_ele_distance.text)

        outer_price_div = driver.find_elements_by_xpath('//div[@class="js-button-text-wrapper  l-float-right  "]')
        for o in outer_price_div:
            try:
                rate_element = o.find_element_by_xpath('//div[@class="t-color-standard-100 t-line-height-m t-font-weight-semibold t-font-m l-float-left l-padding-top l-sold-out"]')
                Rate.append(rate_element.text)
            except:
                try:
                    avl_rate_element = o.find_element_by_xpath('//span[@class="t-price  m-display-block t-font-weight-bold"]')
                    Rate.append(avl_rate_element.text)
                except:
                    Rate.append('Unable to retrieve price')
            else:
                Rate.append(rate_element.text)
    except Exception as e:
        print(e)

    else:

        for hotelname, hoteladdreses in zip(hotel_names, hotel_addreses):
            hotel_name_list.append(hotelname.text)
            hotel_adr_list.append(hoteladdreses.text)

        with open('csv_data.csv', 'a') as f:
            thewriter = csv.writer(f)
            thewriter.writerow([code_pased, '', '', ''])
            for hotel_name_csv, hotel_addreses_csv, distance_csv, rate_csv in zip(hotel_name_list, hotel_adr_list, hotel_dis_for_des_list, Rate):
                thewriter.writerow([hotel_name_csv, hotel_addreses_csv, distance_csv, rate_csv])


if __name__ == '__main__':

    with open('csv_data.csv', 'w') as f:
        thewriter = csv.writer(f)
        thewriter.writerow(['Hotel Names / Codes', 'Address', 'Distance from destination', 'Rate/Price'])

    for i in codes_list:
        print(i)
        make_query(i)

    print('Code Finished')

