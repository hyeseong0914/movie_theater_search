from django.http import request
from django.shortcuts import render, render_to_response, redirect, HttpResponseRedirect, HttpResponse

from .methods import *

app_name = 'movie_schedule'

def index(request):
    return render(request, "index.html", {})

def service(request):
    return render(request, 'service.html', {})


def search_daegu(request, html='daegu.html'):
    cgv_dict = {'대구': ['11', '0058'], '대구한일': ['11', '0147'], '대구현대': ['11', '0109'], '대구아카데미': ['11', '0185'], '대구수성': ['11', '0157'], '대구스타디움': ['11', '0108'],
                '대구월성': ['11', '0216'], '대구이시아': ['11', '0117'], '대구칠곡': ['11', '0071'], '구미': ['204', '0053'], '김천율곡': ['204', '0240'], '북포항': ['204', '0097'],
                '포항': ['204', '0045'], '안동': ['204', '0272']}

    megabox_dict = {'대구칠성로': '7022', '대구신세계': '7011', '대구이시아': '7012', '북대구': '7021', '경산하양': '7122', '경주': '7801', '구미강동': '7303', '김천': '7401',
                    '남포항': '7901', '문경': '7451', '안동': '7601'}

    lotte_dict = {'대구동성로': '5005', '대구광장': '5012', '경산': '5008', '경주': '9050', '구미프라임': '9001', '구미공단': '5013', '대구상인': '5016',
                  '대구성서': '5004', '대구율하': '5006', '포항': '5007', '구미센트럴': '9067', '대구만경': '9066', '대구칠곡': '9057', '영주': '9064'}

    if request.method == "POST":
        date = request.POST['date']

        cgv_string = cgv(request, cgv_dict, date)
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        megabox_string = megabox(request, megabox_dict, date, driver)
        lotte_string = lotte(request, lotte_dict, date, driver)
        driver.close()

        return render(request, html, {'date': date, 'cgv_string': cgv_string, 'megabox_string': megabox_string, 'lotte_string': lotte_string})
    else:
        return render(request, html, {})


def search_gwangju(request, html='gwangju.html'):

    cgv_dict = {'광주상무': '0193', '광주용봉': '0210', '광주첨단': '0218', '광주충장로': '0244', '광주터미널': '0090'}

    megabox_dict = {'광주충장로': '5011', '광주상무': '5021', '광주하남': '5061'}

    lotte_dict = {'광주백화점': '6001', '광주수완': '6004', '광주광산': '9065'}

    if request.method == "POST":
        date = request.POST['date']

        cgv_string = cgv(request, cgv_dict, date)
        megabox_string = megabox(request, megabox_dict, date)
        lotte_string = lotte(request, lotte_dict, date)

        return render(request, html, {'date': date, 'cgv_string': cgv_string, 'megabox_string': megabox_string,
                                      'lotte_string': lotte_string})
    else:
        return render(request, html, {})

def search_daejeon(request, html='daejeon.html'):

    cgv_dict = {'대전': '0007', '대전가오': '0154', '대전탐방': '0202', '대전터미널': '0127',
                '유성노은': '0206', '유성온천': '0209'}

    megabox_dict = {'대전': '3021'}

    lotte_dict = {'대전백화점': '4002', '대전둔산': '4006', '대전센트럴': '4008'}

    if request.method == "POST":
        date = request.POST['date']

        cgv_string = cgv(request, cgv_dict, date)
        megabox_string = megabox(request, megabox_dict, date)
        lotte_string = lotte(request, lotte_dict, date)

        return render(request, html, {'date': date, 'cgv_string': cgv_string, 'megabox_string': megabox_string,
                                      'lotte_string': lotte_string})
    else:
        return render(request, html, {})



def search_busan(request, html='busan.html'):
    cgv_dict = {'남포': '0065', '대연': '0061', '대한': '0151', '동래': '0042', '서면': '0005',
                '센텀시티': '0089', '아시아드': '0160', '정관': '0238', '하단': '0245', '해운대': '0253', '화명': '0159'}

    megabox_dict = {'부산극장': '6001', '부산대': '6906', '해운대': '6121'}

    lotte_dict = {'부산본점': '2004', '사상': '2005', '센텀시티': '2006', '오투': '2011', '해운대': '9059'}

    if request.method == "POST":
        date = request.POST['date']

        cgv_string = cgv(request, cgv_dict, date)
        megabox_string = megabox(request, megabox_dict, date)
        lotte_string = lotte(request, lotte_dict, date)

        return render(request, html, {'date': date, 'cgv_string': cgv_string, 'megabox_string': megabox_string,
                                      'lotte_string': lotte_string})
    else:
        return render(request, html, {})


def search_ulsan(request, html='ulsan.html'):
    cgv_url_list = []

    if request.method == "POST":
        date = request.POST['date']
        cgv_theaters = request.POST.getlist('cgv[]')
        areacode = request.POST['areacode']
        cgv = []

        cgv_dict = {'대구': '0058', '대구한일': '0147', '대구현대': '0109', '대구아카데미': '0185', '대구수성': '0157', '대구스타디움': '0108',
                    '대구월성': '0216', '대구이시아': '0117', '대구칠곡': '0071', '광주상무': '0193', '광주용봉': '0210', '광주첨단': '0218',
                    '광주충장로': '0244', '광주터미널': '0090', '대전': '0007', '대전가오': '0154', '대전탐방': '0202', '대전터미널': '0127',
                    '유성노은': '0206', '유성온천': '0209', '남포': '0065', '대연': '0061', '대한': '0151', '동래': '0042',
                    '서면': '0005', '센텀시티': '0089', '아시아드': '0160', '정관': '0238', '하단': '0245', '해운대': '0253', '화명': '0159',
                    '울산삼산': '0128'}

        for i in cgv_theaters:
            if i in cgv_dict:
                cgv.append(cgv_dict[i])

        time = ''
        for i in date:
            if i.isdigit():
                time += i

        for i in cgv:
            cgv_url = "http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?areacode="
            cgv_url += areacode + '&theaterCode=' + i + '&date=' + time + '&screencodes=&screenratingcode=&regioncode='
            cgv_url_list.append(cgv_url)

        movie_titles = []
        theaters = []
        movie_time = []
        date_list = []

        for i in cgv_url_list:
            r = urllib.request.urlopen(i)
            soup = BeautifulSoup(r, 'html.parser')

            movie_titles.append(getMovieTitles(soup))
            theaters.append(getTheaterType(soup))
            movie_time.append(getMovieTime(soup))
            date_list.append(getDates(soup))

        cgv_string = ''
        for x in range(len(cgv_theaters)):
            cgv_string += "<br><br><hr><h1>" + cgv_theaters[x] + ":</h1>"
            if date in date_list[x]:
                for y in range(len(movie_titles[x])):
                    cgv_string += "<br><div class=\"title\"><h3>" + movie_titles[x][y] + ":</h3></div>"
                    for j in range(len(theaters[x][y])):
                        cgv_string += "<div class=\"theater\"><h4>" + theaters[x][y][j] + " :</h4></div>"
                        for k in range(len(movie_time[x][y][j])):
                            cgv_string += "<div class=\"time\">" + movie_time[x][y][j][k] + "</div>"
            else:
                cgv_string += '<br><h2>현재 날짜에 상영화는 영화가 없습니다.</h2><br>'

        return render(request, html, {'date': date, 'cgv': cgv_url_list, 'titles': movie_titles, 'theaters': theaters,
                                      'time': movie_time, 'cgv_string': cgv_string})
    else:
        return render(request, html, {})


def search_incheon(request, html='incheon.html'):
    cgv_url_list = []

    if request.method == "POST":
        date = request.POST['date']
        cgv_theaters = request.POST.getlist('cgv[]')
        areacode = request.POST['areacode']
        cgv = []

        cgv_dict = {'대구': '0058', '대구한일': '0147', '대구현대': '0109', '대구아카데미': '0185', '대구수성': '0157', '대구스타디움': '0108',
                    '대구월성': '0216', '대구이시아': '0117', '대구칠곡': '0071', '광주상무': '0193', '광주용봉': '0210', '광주첨단': '0218',
                    '광주충장로': '0244', '광주터미널': '0090', '대전': '0007', '대전가오': '0154', '대전탐방': '0202', '대전터미널': '0127',
                    '유성노은': '0206', '유성온천': '0209', '남포': '0065', '대연': '0061', '대한': '0151', '동래': '0042',
                    '서면': '0005', '센텀시티': '0089', '아시아드': '0160', '정관': '0238', '하단': '0245', '해운대': '0253', '화명': '0159',
                    '울산삼산': '0128', '계양': '0043', '남주안': '0198', '부평':  '0021', '연수역': '0247', '인천': '0002', '인천공항': '0118',
                    '인천논현': '0254', '인천연수': '0258', '주안역': '0027', '청라': '0235'}

        for i in cgv_theaters:
            if i in cgv_dict:
                cgv.append(cgv_dict[i])

        time = ''
        for i in date:
            if i.isdigit():
                time += i

        for i in cgv:
            cgv_url = "http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?areacode="
            cgv_url += areacode + '&theaterCode=' + i + '&date=' + time + '&screencodes=&screenratingcode=&regioncode='
            cgv_url_list.append(cgv_url)

        movie_titles = []
        theaters = []
        movie_time = []
        date_list = []

        for i in cgv_url_list:
            r = urllib.request.urlopen(i)
            soup = BeautifulSoup(r, 'html.parser')

            movie_titles.append(getMovieTitles(soup))
            theaters.append(getTheaterType(soup))
            movie_time.append(getMovieTime(soup))
            date_list.append(getDates(soup))

        cgv_string = ''
        for x in range(len(cgv_theaters)):
            cgv_string += "<br><br><hr><h1>" + cgv_theaters[x] + ":</h1>"
            if date in date_list[x]:
                for y in range(len(movie_titles[x])):
                    cgv_string += "<br><div class=\"title\"><h3>" + movie_titles[x][y] + ":</h3></div>"
                    for j in range(len(theaters[x][y])):
                        cgv_string += "<div class=\"theater\"><h4>" + theaters[x][y][j] + " :</h4></div>"
                        for k in range(len(movie_time[x][y][j])):
                            cgv_string += "<div class=\"time\">" + movie_time[x][y][j][k] + "</div>"
            else:
                cgv_string += '<br><h2>현재 날짜에 상영화는 영화가 없습니다.</h2><br>'

        return render(request, html, {'date': date, 'cgv': cgv_url_list, 'titles': movie_titles, 'theaters': theaters,
                                      'time': movie_time, 'cgv_string': cgv_string})
    else:
        return render(request, html, {})


def search_seoul(request, html='seoul.html'):
    cgv_url_list = []

    if request.method == "POST":
        date = request.POST['date']
        cgv_theaters = request.POST.getlist('cgv[]')
        areacode = request.POST['areacode']
        cgv = []

        cgv_dict = {'강남': '0056', '강변': '0001', '건대입구': '0229', '구로': '0010', '군자': '0095', '대학로': '0063',
                    '동대문': '0252', '명동': '0009', '명동역': '0105', '목동': '0011', '미아': '0057', '불광': '0030',
                    '상봉': '0046', '성신여대입구': '0083', '송파': '0088', '수유': '0276', '신촌아트레온': '0150', '압구정': '0040',
                    '여의도': '0112', '영등포': '0059', '왕십리': '0074', '용산아이파크몰': '0013', '중계': '0131', '천호': '0199',
                    '청담씨네시티': '0107', '피카디리1958': '0223', '하계':'0164', '홍대':'0191'}

        for i in cgv_theaters:
            if i in cgv_dict:
                cgv.append(cgv_dict[i])

        time = ''
        for i in date:
            if i.isdigit():
                time += i

        for i in cgv:
            cgv_url = "http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?areacode="
            cgv_url += areacode + '&theaterCode=' + i + '&date=' + time + '&screencodes=&screenratingcode=&regioncode='
            cgv_url_list.append(cgv_url)

        movie_titles = []
        theaters = []
        movie_time = []
        date_list = []

        for i in cgv_url_list:
            r = urllib.request.urlopen(i)
            soup = BeautifulSoup(r, 'html.parser')

            movie_titles.append(getMovieTitles(soup))
            theaters.append(getTheaterType(soup))
            movie_time.append(getMovieTime(soup))
            date_list.append(getDates(soup))

        cgv_string = ''
        for x in range(len(cgv_theaters)):
            cgv_string += "<br><br><hr><h1>" + cgv_theaters[x] + ":</h1>"
            if date in date_list[x]:
                for y in range(len(movie_titles[x])):
                    cgv_string += "<br><div class=\"title\"><h3>" + movie_titles[x][y] + ":</h3></div>"
                    for j in range(len(theaters[x][y])):
                        cgv_string += "<div class=\"theater\"><h4>" + theaters[x][y][j] + " :</h4></div>"
                        for k in range(len(movie_time[x][y][j])):
                            cgv_string += "<div class=\"time\">" + movie_time[x][y][j][k] + "</div>"
            else:
                cgv_string += '<br><h2>현재 날짜에 상영화는 영화가 없습니다.</h2><br>'

        return render(request, html, {'date': date, 'cgv': cgv_url_list, 'titles': movie_titles, 'theaters': theaters,
                                      'time': movie_time, 'cgv_string': cgv_string})
    else:
        return render(request, html, {})






