import re
from bs4 import BeautifulSoup
import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from django.shortcuts import render
from datetime import datetime


def cgv(request, cgv_dict, date):
    ################ CGV ################

    # 웹 페이지로부터 선택된 CGV 정보 가져오기
    cgv_theaters = request.POST.getlist('cgv[]')
    cgv = []
    cgv_url_list = []

    # 체크된 CGV 영화관
    for i in cgv_theaters:
        if i in cgv_dict:
            cgv.append(cgv_dict[i])

    # CGV 숫자로만 된 날짜 구하기
    time = ''
    for i in date:
        if i.isdigit():
            time += i

    # CGV URL 구하기
    for i in cgv:
        cgv_url = "http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?areacode="
        cgv_url += i[0] + '&theaterCode=' + i[1] + '&date=' + time + '&screencodes=&screenratingcode=&regioncode='
        cgv_url_list.append(cgv_url)

    movie_titles = []
    theaters = []
    movie_time = []
    date_list = []

    # CGV 영화정보 가져오기
    for i in cgv_url_list:
        r = urllib.request.urlopen(i)
        soup = BeautifulSoup(r, 'html.parser')

        movie_titles.append(getMovieTitles(soup))
        theaters.append(getTheaterType(soup))
        movie_time.append(getMovieTime(soup))
        date_list.append(getDates(soup))

    cgv_string = ''
    for x in range(len(cgv_theaters)):
        cgv_string += "<br><br><hr><h1>" + cgv_theaters[x] + "(CGV)" + ":</h1>"
        if date in date_list[x]:
            for y in range(len(movie_titles[x])):
                cgv_string += "<br><div class=\"title\"><h2>" + movie_titles[x][y] + ":</h2></div><br>"
                for j in range(len(theaters[x][y])):
                    cgv_string += "<div class=\"theater\"><h4>" + theaters[x][y][j] + ":</h4></div>"
                    for k in range(len(movie_time[x][y][j])):
                        cgv_string += "<div class=\"time\">" + movie_time[x][y][j][k] + "</div>"
                    cgv_string += "<br><br>"
        else:
            cgv_string += '<br><h2>현재 날짜에 상영화는 영화가 없습니다.</h2><br>'

    return(cgv_string)

def megabox(request, megabox_dict, date, driver):
    ################ 메가 박스 ################

    # 웹 페이지로부터 선택된 메가박스 정보 가져오기
    megabox_theaters = request.POST.getlist('megabox[]')
    region = request.POST['region']
    megabox = []
    megabox_url_list = []

    # 체크된 메가박스 영화관
    for i in megabox_theaters:
        if i in megabox_dict:
            megabox.append(megabox_dict[i])

    # 메가박스 URL 구하기
    for i in megabox:
        megabox_url = "http://www.megabox.co.kr/?menuId=theater-detail&region=" + region + "&cinema=" + i
        megabox_url_list.append(megabox_url)

    megabox_string = ''
    # 메가박스 영화 정보 가져오기
    if megabox_url_list:
        for k in range(len(megabox_url_list)):
            # driver.implicitly_wait(3)
            driver.get(megabox_url_list[k])
            playDate = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "playDate")))

            while (playDate.get_attribute('value') != date):
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@onclick=\"goday('next');\"]"))).click()
                playDate = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'playDate')))

            # 모든 것
            result = []

            try:
                things = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, 'lineheight_80')))

            except:
                megabox_string += "<br><br><hr><h1>" + megabox_theaters[k] + "(메가박스)" + ":</h1>"
                megabox_string += '<br><h2>현재 날짜에 상영화는 영화가 없습니다.</h2><br>'
                continue

            for thing in things:
                easy = thing.text.replace('\n', ' ')
                result.append(easy.split(' '))

            # 영화 제목 가져오기
            movie_titles = []
            titles = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.ID, 'th_theaterschedule_title')))
            for title in titles:
                if WebDriverWait(title, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'strong'))).text is not ' ':
                    movie_titles.append(WebDriverWait(title, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'strong'))).text)

            # 영화 상영관 가져오기
            theaters = []
            rooms = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.ID, "th_theaterschedule_room")))
            for room in rooms:
                theaters.append(room.text.replace('\n', ' '))
                # theaters.append(room.find_element_by_css_selector('div').text)

            # 영화 시작 시간 ~ 끝나는 시간 가져오기
            megabox_movie_time = []

            temps3 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//table[@class='movie_time_table v2']")))
            temps = WebDriverWait(temps3, 10).until(EC.presence_of_all_elements_located((By.XPATH, './/tr')))
            for i in temps:
                temps2 = WebDriverWait(i, 10).until(EC.presence_of_all_elements_located((By.XPATH, ".//span[@class='hover_time']")))
                temp_list = []
                for j in temps2:
                    temp_list.append(j.get_attribute('innerHTML'))
                megabox_movie_time.append(temp_list)

            # 영화 좌석 가져오기
            seats = []

            for i in result:
                temp2 = []
                for j in i:
                    if '/' in j and j.replace('/', '').isdigit():
                        temp2.append(j)
                    elif j == '매진':
                        temp2.append(j)
                seats.append(temp2)

            # 영화당 영화관 갯수 가져오기
            limit = ['15세관람가', '12세관람가', '전체관람가', '청소년관람불가']

            numbers = []
            temp_number = 1
            for i in range(0, len(result)):
                if i + 1 == len(result):
                    numbers.append(temp_number)
                    break
                if result[i + 1][0] in limit:
                    numbers.append(temp_number)
                    temp_number = 1
                else:
                    temp_number += 1

            # 영화 정보 String으로 옮기기
            temp = 0
            megabox_string += "<br><br><hr><h1>" + megabox_theaters[k] + "(메가박스)" + ":</h1>"
            if movie_titles:
                for x in range(len(movie_titles)):
                    megabox_string += "<br><div class=\"title\"><h2>" + movie_titles[x] + ":</h2></div><br>"
                    for z in range(temp, temp + numbers[x]):
                        megabox_string += "<div class=\"theater\"><h4>" + theaters[z] + ":</h4></div>"
                        for g in range(len(seats[z])):
                            megabox_string += "<div class=\"time\">" + megabox_movie_time[z][g] + " " + seats[z][g] + "  " + "</div>"
                        megabox_string += "<br><br>"
                    megabox_string += "\n"
                    temp += numbers[x]

            else:
                megabox_string += '<br><h2>현재 날짜에 상영화는 영화가 없습니다.</h2><br>'

    return(megabox_string)

def lotte(request, lotte_dict, date, driver):
    lotte_theaters = request.POST.getlist('lotte[]')
    detailDivisionCode = request.POST['detailDivisionCode']
    lotte = []
    lotte_url_list = []

    month = {
        '01': "January",
        '02': "February",
        '03': "March",
        '04': "April",
        '05': "May",
        '06': "June",
        '07': "July",
        '08': "August",
        '09': "September",
        '10': "October",
        '11': "November",
        '12': "December"
    }

    # 날짜 영어 달일로 바꾸기
    text_date = ''
    if date is not None:
        text_date += month[date[5:7]]
        if date[8:9] == '0':
            text_date += date[9:10]
        else:
            text_date += date[8:10]

    # 체크된 롯데시네마 영화관
    for i in lotte_theaters:
        if i in lotte_dict:
            lotte.append(lotte_dict[i])

    # 롯데시네마 URL 구하기
    for i in lotte:
        lotte_url = "http://www.lottecinema.co.kr/LCHS/Contents/Cinema/Cinema-Detail.aspx?divisionCode=1&detailDivisionCode=" + detailDivisionCode + "&cinemaID="+ i
        lotte_url_list.append(lotte_url)

    lotte_string = ''
    if lotte_url_list:
        for k in range(len(lotte_url_list)):
            # driver.implicitly_wait(3)
            driver.get(lotte_url_list[k])

            # 선택한 날짜 클릭하기
            label_value = "//label[@for='" + text_date + "']"
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, label_value))).click()
            time.sleep(2)


            # 모든 것
            number_theaters = []
            temp_class = "//div[@class='time_aType time" + lotte_dict[lotte_theaters[k]] + "']"
            try:
                temps = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, temp_class)))
            except:
                lotte_string += "<br><br><hr><h1>" + lotte_theaters[k] + "(롯데시네마)" + ":</h1>"
                lotte_string += '<br><h2>현재 날짜에 상영화는 영화가 없습니다.</h2><br>'
                continue
            for i in WebDriverWait(temps, 10).until(EC.presence_of_all_elements_located((By.XPATH, ".//dl"))):
                number_theaters.append(
                    len(WebDriverWait(i, 10).until(EC.presence_of_all_elements_located((By.XPATH, ".//dd")))))
            # 한개의 영화당 섹션의 갯수

            # 영화제목 구하기
            movie_titles = []
            for i in WebDriverWait(temps, 10).until(EC.presence_of_all_elements_located((By.XPATH, ".//dt"))):
                movie_titles.append(i.text[2:])

            lines = []
            times = []
            tech = []
            theaters = []
            seats = []

            for i in WebDriverWait(temps, 10).until(EC.presence_of_all_elements_located((By.XPATH, ".//dd"))):
                lines.append(i.text.split('\n'))
                times_temp = []
                tech_temp = []
                theaters_temp = []
                seats_temp = []
                # 영화 시간 구하기
                for j in WebDriverWait(i, 10).until(
                        EC.presence_of_all_elements_located((By.XPATH, ".//span[@class='clock']"))):
                    ending_time = WebDriverWait(j, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'span'))).get_attribute('innerHTML').replace(
                        ' ', '')
                    times_temp.append(j.text.replace('조조', '').replace('심야', '') + ending_time)
                # 영상 기술 Ex) 2D, 3D, 4D
                for j in WebDriverWait(i, 10).until(
                        EC.presence_of_all_elements_located((By.XPATH, ".//ul[@class='cineD1']"))):
                    tech_temp.append(j.text.replace('\n', ' '))
                # 영상관 구하기
                for j in WebDriverWait(i, 10).until(
                        EC.presence_of_all_elements_located((By.XPATH, ".//span[@class='cineD2']"))):
                    theaters_temp.append(j.text)
                # 남은 좌석 구하기
                for j in WebDriverWait(i, 10).until(
                        EC.presence_of_all_elements_located((By.XPATH, ".//span[@class='ppNum']"))):
                    seats_temp.append(j.text.replace(' ', '').replace('석', ''))

                tech.append(tech_temp)
                times.append(times_temp)
                theaters.append(theaters_temp)
                seats.append(seats_temp)

            temp = 0
            lotte_string += "<br><br><hr><h1>" + lotte_theaters[k] + "(롯데시네마)" + ":</h1>"
            if movie_titles:
                for i in range(len(movie_titles)):
                    lotte_string += "<br><div class=\"title\"><h2>" + movie_titles[i] + ":</h2></div><br>"
                    for j in range(temp, temp+number_theaters[i]):
                        lotte_string += "<div class=\"theater\"><h4>" + tech[j][0] + ":</h4></div>"
                        for k in range(len(theaters[j])):
                            lotte_string += "<div class=\"time\">" + theaters[j][k] + " " + times[j][k] + " " + seats[j][k] + "  " + "</div>"
                        lotte_string += "<br><br>"
                    temp += number_theaters[i]
    return lotte_string

def getMovieTitles(soup):
    movieTitles = []
    temp = soup.find_all('div', class_='info-movie')
    for i in temp:
        movieTitles.append(i.a.strong.text.strip())
    return movieTitles


def getTheaterType(soup):
    # theaterTypes = []
    # temp = soup.find_all('div', class_='col-times')
    # for i in temp:
    #     temp_list = []
    #     for j in i.find_all('div', class_='info-hall'):
    #         temp_list.append(j.ul.li.text.strip())
    #     theaterTypes.append(temp_list)
    # return theaterTypes
    theaterTypes = []
    temp = soup.find_all('div', class_='col-times')
    for i in temp:
        temp_list = []
        for j in i.find_all('div', class_='info-hall'):
            temp_list2 = str(j.ul.text).replace(" ", "").replace("\r", "").split("\n")
            for k in temp_list2:
                if len(k) == 0:
                    temp_list2.remove(k)
            temp_str = temp_list2[0] + " " + temp_list2[1] + " " + temp_list2[2] + " " + temp_list2[3]
            temp_list.append(temp_str)
        theaterTypes.append(temp_list)
    return theaterTypes


def getMovieTime(soup):
    movieTime = []
    temp = soup.find_all('div', class_='col-times')
    for i in temp:
        temp_list1 = []
        for j in i.find_all('div', class_='info-timetable'):
            temp_list2 = []
            for k in j.ul.find_all('li'):
                a = k.find('a')
                temp_string = ''
                if a is None:
                    temp_string = k.em.text + ' 마감'
                else:
                    if 'onclick' in a.attrs:
                        temp_string = k.em.text + ' 준비중'
                    else:
                        temp_string = k.text[:5] + "~" + k.a.attrs['data-playendtime'][:2] + ":" + \
                                      k.a.attrs['data-playendtime'][2:] + " &#160" + k.text[5:] + "\n"
                temp_list2.append(temp_string)
            temp_list1.append(temp_list2)
        movieTime.append(temp_list1)
    return movieTime


def getDates(soup):
    temp = soup.find_all('div', class_='day')
    date_list = []
    for i in temp:
        link = i.a.attrs['href']
        date = re.search('\d{8}', link).group(0)
        date = date[:4] + '-' + date[4:6] + '-' + date[6:]
        date_list.append(date)
    return date_list
