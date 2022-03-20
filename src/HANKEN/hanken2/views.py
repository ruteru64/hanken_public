from email.policy import default
import json
from urllib import request
from django.shortcuts import render
from django.shortcuts import redirect
from django.http.response import JsonResponse
import requests
import csv
from django.http import HttpResponse
import io

from .models import A_addresses, E_events, N_nfcs, T_tickets, U_users, P_places, O_others, Cc_chargeclasses, Yy_eventtags, Ww_charges_ww, Sc_seatclasses, Zz_events_connect_tags_zz, C_charges, M_maxes, Oo_ticket_connect_charge_oo, Ti_ticketsinfos, S_seats
# テーブルのスペルミスってた()
from .models import En_enries as En_entries

import datetime
from django.utils import timezone

from django.db.models import Q

import hashlib

# メール関係
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# パスワード隠してみた
import os
from dotenv import load_dotenv

# メール関係
def make_email(sender_email="", password="", receiver_email="",  subject="", text=""):
    """
    Gmailでメールを送信する
    Args:
        sender_email (str) : 自分のGmailのメールアドレス。
        password (str) : アプリパスワード。Googleアカウントの設定で生成されたもの。
        receiver_email (str) :メールを送る相手のメールアドレス
        subject (str) : メールのタイトル
    """
    message = MIMEText(text)
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email


    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )


def send_email(subject = "", text = ""):
    # .envファイルの内容を読み込む
    load_dotenv()
    make_email(sender_email=os.environ['MAIL_ADDRESS'], password=os.environ['MAIL_PASSWORD'], receiver_email=os.environ['MAIL_ADDRESS'], subject = subject, text = text)

# 人気のイベント
def popevent():
    # 受付終了が今日よりあとのを取得
    # したかったけど日付型が意味不明だったので諦めました
    # eventids = T_tickets.objects.filter("ti_ticketsinfos__ti_end" == 1111-11-11).values("e_event_id_id")
    # eventids.extend(T_tickets.objects.filter("ti_ticketsinfos__ti_end" >= datetime.datetime.now().strftime('%Y-%m-%d')).values("e_event_id_id"))
    # print(eventids)
    eventids = T_tickets.objects.values("e_event_id_id")

    eventid_dic = {}
    for eventid in eventids:
        
        if eventid['e_event_id_id'] in eventid_dic.keys():
            eventid_dic[eventid['e_event_id_id']] += 1
        else:
            eventid_dic[eventid['e_event_id_id']] = 0
    
    eventid_dic2 = sorted(eventid_dic.items(), key=lambda x:x[1], reverse=True)
    # [(1, 85), (2, 60), (3, 20)]
    event_list = []
    number = 5
    count = len(eventid_dic2)
    if count < 5:
        number = count

    for i in range(number):
        tmp = datetime.timedelta(hours=9)
        event_dic = {}
        event_obj = E_events.objects.get(pk = eventid_dic2[i][0])
        event_dic["id"] = event_obj.e_event_id
        event_dic["name"] = event_obj.e_event_name
        event_dic["date"] = event_obj.e_start + tmp
        
        event_dic["place"] = P_places.objects.get(e_event_id_id = eventid_dic2[i][0]).p_prefecture
        # event_dic["place"] = placelist[0]["p_prefecture"]
        if event_dic["date"].strftime('%Y/%m/%d') == "1111/11/11":
            event_dic["date"] = "常時開催"
        event_list.append(event_dic)

    return event_list

# Create your views here.
def index(request):
    poplist = popevent()
    id = ''
    try:
        id = request.session['host_id']
        return render(request, 'index.html', {"user":id,"name":"host","poplist":poplist})
    except:
        try:
            id = request.session['member_id']
        except:
            id = ''
    return render(request, 'index.html', {"user":id,"name":"Home","poplist":poplist})

def login(request):
    try:
        request.session['host_id']
        return redirect("/homehost")
    except:
        try:
            request.session['member_id']
            return redirect("/")
        except:
            return render(request, 'login.html', {"user":"","name":"Login"})

def terms(request):
    return render(request,'terms.html',{})

def privacy(request):
    return render(request,"privacy.html",{})

def eventsearch(request):
    ##
     # TODO:3
     # 送られてきたパラメータをイベント名に含むイベントを検索する
     # (json{id:"",name:"",date:datetime,place:""})を返す。
     #パラメータはrequest.GET
     ##
    #パラメータ=検索ワード(request.GETで取ってこれる)を含んでいるイベントの情報(id?)を取ってくる
    event_object = E_events.objects.filter(e_event_name__contains=request.GET['eventname'])
    events = event_object.values('e_event_id', 'e_event_name', 'e_start', 'p_places__p_prefecture')
    length = len(events)
    
        
    
    #　一回辞書にして、jsonにしてくれる　length 中の｛｝の数のかず、イベントリストの中の｛｝の数を増やしていく
    prm = {'length':length}
    #'eventlist':[{'id':"1",'name':"event",'date':'datetime','place':"123"}, {}, {}]
    event_list = []
    for i in range(length):
        event_dicts = {}
        event_dicts['id'] = events[i]['e_event_id']
        event_dicts['name'] = events[i]['e_event_name']
        event_dicts['date'] = events[i]['e_start'].strftime('%Y-%m-%d')
        event_dicts['place'] = events[i]['p_places__p_prefecture']

        if event_dicts['date'] == "1111-11-11":
            event_dicts['date'] = '常時開催'
        event_list.append(event_dicts)
    prm["eventlist"] = event_list
    #eventlist の中の prm = prm['eventlist'][0]['id']
    #length を増やす
    #eventlist(リスト型)に、新たなイベント情報(辞書型)を追加する
    
    return JsonResponse(prm,safe=False)

def make_hash(password):
    password = bytes(password, 'utf-8')
    hashpw = hashlib.sha256(password).hexdigest()
    return hashpw

def login_m(request):
    if 'id' in request.POST and 'password' in request.POST:
        id = request.POST['id']
        pw = make_hash(request.POST['password'])
        ## 
        # TODO:4
        # idでかつpasswordを持つユーザーがいるか確認する
        # もしいないなら"/login"へ
        # いるかつ一般ユーザーなら"/"へ
        # ホストユーザーなら"/homehost"へ
        ##

        # データーベースにメアド, pwが登録されているか.
        user = U_users.objects.filter(u_mail_address = id, u_password = pw)
        isUser = user.exists()

        if not isUser:
            return redirect("/login")

        isHost = user.values('uc_id')
        
        if isHost[0]['uc_id'] == 2:
            request.session['host_id'] = id
            return redirect("/homehost")
        else:
            request.session['member_id'] = id
            return redirect("/")

    else:
        return redirect("/login")


def getEvent(id):
    ##
     # TODO:6
     # idのイベントの詳細を取得する
     # 返り値は{id:"",name:"",state:"",date:"",host:"",detail:""}
     ##
     # このidはイベントidのこと
    tmp = datetime.timedelta(hours=9)
    dic = {}
    dic["id"] = id
    event = E_events.objects.get(pk = id)
    temp1 = P_places.objects.filter(e_event_id_id = id)
    dic["name"] = event.e_event_name
    dic["state"] = temp1[0].p_prefecture

    dic["date"] = event.e_start + tmp

    dic["host"] = event.e_host_name
    dic["detail"] = event.e_outline
    dic["url"] = temp1[0].p_url

    dic["xyzFlag"] = 1
    if temp1[0].p_ido == "":
        dic["xyzFlag"] = 0

    if dic["date"].strftime('%Y/%m/%d') == "1111/11/11":
            dic["date"] = "常時開催"

    event = dic
    # event = [{'id':'1','state':'tokyo',"date":'2020',"host":"ruteru","detail":"いろいろやるよ"}]

    '''マップ用'''
    place_dic = {'ido':temp1[0].p_ido, 'kedo':temp1[0].p_kedo, 'name':temp1[0].p_build}
    return event, place_dic
    
def status_render(s_null, s_count):
    wariai = s_null / s_count
    if wariai == 0:
        return "売り切れ"
    elif wariai >= 0.1:
        return "空席有"
    else:
        return "残り僅か"

def getTicketlist(id):
    ##
     # TODO:19
     # idのイベントの詳細を取得する
     # 返り値は{id:"",name:"",status:"",name:"",plice:"",detail:""}
     # 'status' の凝り10%以上の時空席有,以下残り僅か,0なし
     ##
    
    # idはイベントID

    # 料金中間テーブルでイベントの料金形態が分かる
    ## 料金中間テーブルから[{料金中間テーブルID:1, 料金区分:大人, 座席区分:S席, 料金:1000}, {料金中間テーブルID:2, 料金区分:子供, 座席区分:S席, 料金:1000}]を取得
    plan_list = Ww_charges_ww.objects.filter(e_event_id_id = id).order_by("sc_id_id").values("ww_charge_id", "cc_id_id", "sc_id_id", "c_charge_id")

    

    # チケット情報IDを取得
    ticketinfoid = Ti_ticketsinfos.objects.get(pk = id).ti_ticketsinfo_id
    # 定員数の辞書[{座席区分:N, 定員:S}, {座席区分:Y, 定員:Z}]
    capacity_dic = M_maxes.objects.filter(ti_ticketsinfo_id_id = ticketinfoid).values('sc_id_id', 'm_capacity')
    ticket = []
    for plan in plan_list:
        temp_dic = {}
        # plan == {'ww_charge_id': 1, 'cc_id_id': 2, 'sc_id_id': 1, 'c_charge_id': 2}
        # # イベントの座席数
        for cap in capacity_dic:
            if cap["sc_id_id"] == plan['sc_id_id']:
                s_count = cap["m_capacity"]
                break
        # 定員が0(制限なし)の場合
        if s_count == 0:
            temp_dic["status"] = "販売中"
        # もし座席情報があるなら(イベントが指定席制なら)
        elif  S_seats.objects.filter(ti_ticketsinfo_id_id = ticketinfoid).exists():
            # 空席
            s_null = S_seats.objects.filter(ti_ticketsinfo_id_id = ticketinfoid, t_ticket_id_id__isnull=True).count()
            temp_dic["status"] = status_render(s_null, s_count)

        # 指定席ではないがチケット販売数に制限を設ける場合
        elif s_count:
            # チケットの売り上げ枚数
            ticket_sold = T_tickets.objects.filter(e_event_id_id = id).count()
            temp_dic["status"] = status_render(s_count - ticket_sold, s_count)

        else:
            temp_dic["status"] = "販売中"
        temp_dic["name"] = Sc_seatclasses.objects.get(pk = plan["sc_id_id"]).sc_name
        if temp_dic["name"] == "":
            temp_dic["name"] = "同じよ～ん"
        
        temp_dic["people"] = Cc_chargeclasses.objects.get(pk = plan["cc_id_id"]).cc_name
        temp_dic["plice"] = C_charges.objects.get(pk = plan["c_charge_id"]).c_charge

        temp_dic["id"] = plan["ww_charge_id"]
        seat_obj = S_seats.objects.filter(ti_ticketsinfo_id_id = ticketinfoid, sc_id_id = plan["sc_id_id"], t_ticket_id__isnull=True)
        
        # 席指定があればどんどん追加
        # if seat_obj.exists:
        #     temp_dic["seats"] = []
        #     for seat_one in seat_obj:
        #         seat_dic = {'seatid':seat_one.s_seats_id, 'seat':seat_one.s_place}
        #         temp_dic["seats"].append(seat_dic)


        ticket.append(temp_dic)

    '''表用'''
    # すごい無駄なことしてるかも...

    # 料金区分です
    th_list =[]
    sc_list = []
    sc_temp = 0
    cc_temp = []
    sc_count = -1
    for plan in plan_list:
        if not plan["cc_id_id"] in cc_temp:
            th_list.append(Cc_chargeclasses.objects.get(pk = plan["cc_id_id"]).cc_name)
            cc_temp.append(plan["cc_id_id"])
        # 座席区分IDがなければ追加
        if plan["sc_id_id"] != sc_temp:
            cc_list = []
            sc_count += 1
            sc_temp = plan["sc_id_id"]
            sc_dic = {"s_name":Sc_seatclasses.objects.get(pk = plan["sc_id_id"]).sc_name}
            sc_list.append(sc_dic)
            cc_dic ={"c_name":Cc_chargeclasses.objects.get(pk = plan["cc_id_id"]).cc_name, "plice":C_charges.objects.get(pk = plan["c_charge_id"]).c_charge}
            cc_list.append(cc_dic)
            sc_list[sc_count]["cc"] = cc_list
        else:
            cc_dic ={"c_name":Cc_chargeclasses.objects.get(pk = plan["cc_id_id"]).cc_name, "plice":C_charges.objects.get(pk = plan["c_charge_id"]).c_charge}
            sc_list[sc_count]["cc"].append(cc_dic)
    # event["name"] = E_events.objects.get(pk = id).e_event_name
    # event["plice"] = 


    # ticket = []
    # ticket.append = event
    # neme: 1等席 people: 大人
    # ticket = [{'id':'1','status':'残り僅か','name':'いいやつ', 'people': '大人', 'plice':'3500', 'seats':[{'seatid':1, 'seat':'S-1'}, {'seatid':2, 'seat':'S-2'}]}]
    return ticket, th_list, sc_list

def event(request):
    if 'id' in request.GET:
        event, placeDic = getEvent(request.GET['id'])
        ticketlist, th_list, sc_list = getTicketlist(request.GET['id'])
        othersList = O_others.objects.filter(e_event_id_id = request.GET['id']).values("o_name", "o_detail")
    else:
        return redirect('/')
    try:
        return render(request, 'event.html', {"user":request.session['member_id'],"name":"event","event":event,"ticketlist":ticketlist, "otherslist":othersList, "thlist":th_list, "sclist":sc_list, 'place_json': json.dumps(placeDic)})
    except:
        try:
            return render(request, 'event.html', {"user":request.session['host_id'],"name":"host","event":event, "otherslist":othersList, "thlist":th_list, "sclist":sc_list, 'place_json': json.dumps(placeDic)})
        except:
            return render(request, 'event.html', {"user":"","name":"event","event":event, "otherslist":othersList, "thlist":th_list, "sclist":sc_list, 'place_json': json.dumps(placeDic)})

def register(request):
    id = ''
    try:
        id = request.session['member_id']
    except:
        return render(request,'register.html',{"user":"","name":"register"})
    return redirect('/')
def register_m(request):
    if 'id' in request.POST and 'password' in request.POST and 'repassword' in request.POST and 'name' in request.POST and 'bath' in request.POST and 'phone' in request.POST and 'NFC' in request.POST and 'address' in request.POST and 'prefer' in request.POST and 'city' in request.POST and 'number' in request.POST and 'build' in request.POST:
        id = request.POST['id']
        ps = request.POST['password']
        rps = request.POST['repassword']
        name = request.POST['name']
        bath = request.POST['bath']
        phone = request.POST['phone']
        nfc = request.POST['NFC']
        address = request.POST['address']
        prefer = request.POST['prefer']
        city = request.POST['city']
        number = request.POST['number']
        build = request.POST['build']

        # 空欄ダメだよー
        if "" in [id, ps, rps, name, bath, phone, nfc, address, prefer, city, number]:
            return redirect("/register")
        
        # 電話番号かぶりサヨナラ
        if U_users.objects.filter(u_phone_number = phone).exists():
            return redirect("/register")
        
        # NFCかぶりサヨナラ
        if N_nfcs.objects.filter(n_nfcid = nfc).exists():
            return redirect("/register")
        
        # メアドかぶりサヨナラ
        if U_users.objects.filter(u_mail_address = id).exists():
            return redirect("/register")
        

        elif ps == rps:
            ##
            # TODO:8
            # 受け取ったログイン情報をDBに登録する
            ##
            hashps = make_hash(ps) 

            
            '''顔面用(仮)いつか消す'''
            temp = ("https://" + id)

            # データーベースにぶち込む
            ## ユーザーテーブル
            userid = U_users.objects.create(u_name = name, u_happy_lucky_birthday = bath, u_mail_address = id, u_phone_number = phone, u_password = hashps, uc_id_id = 1, u_photo_of_face = temp)
            ## NFCテーブル
            N_nfcs.objects.create(u_user_id_id = userid.u_user_id, n_nfcid = nfc)
            ## 住所テーブル
            A_addresses.objects.create(u_user_id_id = userid.u_user_id, a_address_number = address, a_prefecture = prefer, a_city = city, a_number = number, a_build = build)

            # もし希望なら運営にメールを送る
            try:
                if request.POST['mail'] == 'plz':
                    title = f'購入者アカウント希望【{ userid.u_user_id }:{ name }】'
                    text = f'''
                    ユーザーID: { userid.u_user_id }
                    名前: { name }
                    メールアドレス: { id }
                    電話番号: { phone }
                    郵便番号: { address }
                    住所: { prefer }{ city }{ number }{ build }
                    備考:{ request.POST["detail"] }
                    '''
                    send_email(subject = title, text = text)
            except:
                pass

            return redirect("/login")
        else:
            return redirect("/register")
    else:
        return redirect("/register")

def myevent(request):
    id = ''
    try:
        id = request.session['member_id']
    except:
        return redirect('/')
    ##
     # TODO:9
     # ユーザーの持っているチケットのイベントをすべて取得する
     # 取得する内容は{"id":0,"name":"","place":"","date":""}
     # これをリストにし取得する
     ##
    
    list = []

    # セッションのメアドからDBのユーザIDを調べる
    user = U_users.objects.get(u_mail_address = id).u_user_id
    # そのユーザIDの入ってるイベントをリスト型で抽出
    events = T_tickets.objects.filter(u_user_id = user).values('e_event_id_id')

    # チケットの数だけぶん回す
    for event_id in events:

        # イベントID
        eventid = event_id.get("e_event_id_id")

        # 辞書を作る
        dic = {}
        dic["id"] = eventid
        dic["name"] = E_events.objects.get(pk = eventid).e_event_name
        temp1 = P_places.objects.filter(e_event_id_id = eventid)
        dic["place"] = temp1[0].p_prefecture
        dic["date"] = (E_events.objects.get(pk = eventid).e_start).strftime("%Y-%m-%d")
        if dic["date"] == "1111-11-11":
            dic["date"] = "常時開催"


        # 辞書をリストに追加
        list.append(dic)




    # list = ({"id":0,"name":"COD","place":"tokyo","date":"0201"},{"id":2,"name":"CS50","place":"tokyo","date":"0228"}) # ダミーデータのため後々消す



    return render(request,'myevent.html',{"user":id,"name":"myevent","eventlist":list})

def myticket(request):
    id = ''
    try:
        id = request.session['member_id']
    except:
        return redirect('/')
    ##
     # TODO:10
     # ユーザーの持っているチケットをすべて取得する
     # 取得する内容は{"id":0,"name":"","place":"","date":"","seat":"A20"}
     # これをリストにし取得する
     ##
    user = U_users.objects.get(u_mail_address = id).u_user_id
    # 配列[<T_table 1>, <t_table 2>]
    tickets = T_tickets.objects.filter(u_user_id_id = user)

    list = []
    for i in tickets:
        eventid = i.e_event_id_id
        ticketid = i.pk
        events = E_events.objects.get(pk=eventid)
        event = {}
        event["id"] = eventid
        event["name"] = events.e_event_name
        event["place"] = events.p_places.p_prefecture
        event["date"] = (events.e_start).strftime("%Y-%m-%d")
        if event["date"] == "1111-11-11":
            event["date"] = "常時開催"
        temp = S_seats.objects.filter(t_ticket_id_id = ticketid)
        if temp.exists():
            event["seat"] = temp[0].s_place
        else:
            event["seat"] = "" 
        list.append(event)

    # list = ({"id":0,"name":"COD","place":"tokyo","date":"0201","seat":"A20"},{"id":2,"name":"CS50","place":"tokyo","date":"0228","seat":"A22"}) # ダミーデータのため後々消す
    return render(request,'myticket.html',{"user":id,"name":"myticket","ticketlist":list})

def editingmypage(request):
    id = ''
    try:
        id = request.session['member_id']
    except:
        try:
            id = request.session['host_id']
        except:
            return redirect('/')
    
    ## TODO: userlist
    user_list = U_users.objects.filter(u_mail_address = id).values("u_user_id", "u_name", "u_happy_lucky_birthday", "u_phone_number", "u_update_onat")
    dic = user_list[0]
    nfcs = N_nfcs.objects.filter(u_user_id = dic["u_user_id"], n_is_deleted = False)
    dic["nfc"] = nfcs[0].n_nfcid
    address_list = A_addresses.objects.filter(u_user_id_id = dic["u_user_id"]).values("a_address_number", "a_prefecture", "a_city", "a_number", "a_build")
    dic.update(address_list[0])
    dic["mail"] = id


    return render(request,'editingmypage.html',{"user":id,"name":"editingmypage", "userlist":dic})

def editingmypage_m(request):
    id = ''
    try:
        id = request.session['member_id']
    except:
        try:
            id = request.session['host_id']
        except:
            return redirect('/')
    


    mail = request.POST['mail']
    ps = request.POST['password']
    psr = request.POST['repassword']
    hashps = make_hash(ps)
    phone = request.POST['phone']
    nfc = request.POST['nfc']
    address = request.POST['address']
    prefer = request.POST['prefer']
    city = request.POST['city']
    number = request.POST['number']
    build = request.POST['build']

    user_obj = U_users.objects.filter(u_mail_address = id)
    userid = user_obj[0].u_user_id
    mynfclist = N_nfcs.objects.filter(u_user_id_id = userid).values("n_nfcid", "n_is_deleted")

    flag = 0

    if not N_nfcs.objects.filter(n_nfcid = nfc).exists():
        products = N_nfcs.objects.filter(u_user_id_id=userid)
        products.update(n_is_deleted=True)
        N_nfcs.objects.create(u_user_id_id = userid, n_nfcid = nfc)
    else:
        for i in mynfclist:
            if i["n_nfcid"] == nfc:
                # 論理削除がFlase= 消されてない:つまり今のNFCと同じ
                if not i["n_is_deleted"]:
                    flag = 1
    if flag != 1:
        return redirect('/editingmypage')

    # メアドが自分以外の人に使われていたらbye
    u_temp1 = U_users.objects.filter(u_mail_address = mail)
    if u_temp1.exists():
        if u_temp1[0].u_user_id != userid:
            return redirect('/editingmypage')

    # 電話番号が自分以外の人に使われてたらbye
    u_temp2 = U_users.objects.filter(u_phone_number = phone)
    if u_temp2.exists():
        if u_temp2[0].u_user_id != userid:
            return redirect('/editingmypage')

    if ps == psr:

        '''処理を書く'''
        userObj = U_users.objects.get(pk=userid)


        hashps = make_hash(ps)

        mail_flag = 0
        
        if userObj.u_password != hashps:
            userObj.u_password = hashps
        
        if userObj.u_mail_address != mail:
            userObj.u_mail_address = mail
            mail_flag = 1
        
        if userObj.u_phone_number != phone:
            userObj.u_phone_number = phone

        userObj.save()

        jushoObj = A_addresses.objects.get(u_user_id_id = userid)
        jushoObj.a_address_number = address
        jushoObj.a_prefecture = prefer
        jushoObj.a_city = city
        jushoObj.a_number = number
        jushoObj.a_build = build

        jushoObj.save()

        if mail_flag == 1:
            try:
                del request.session['member_id']
                return redirect('/login')
            except:
                try:
                    del request.session['host_id']
                    return redirect('/login')
                except: 
                    pass
                    return redirect('/')
        return redirect('/mypage')
    else:
        return redirect('/editingmypage')

def mypage(request):
    id = ''
    try:
        id = request.session['member_id']
    except:
        return redirect('/')
    ##
     # TODO:11
     # ユーザーの情報を取得する
     # 取得する内容は{"id":0,"name":"","place":"","date":"","seat":"A20"}
     # これをリストにし取得する
     ##
    
    # temp = U_users.objects.get(u_mail_address = id).values("u_name", "u_happy_lucky_birthday", "u_phone_number")
    temp = U_users.objects.filter(u_mail_address = id).values("u_user_id", "u_name", "u_happy_lucky_birthday", "u_phone_number")
    list = {"id":temp[0]["u_user_id"], "name":temp[0]["u_name"], "bath":temp[0]["u_happy_lucky_birthday"], "phone":temp[0]["u_phone_number"]}

    # list = {"id":"0","name":"いくら","bath":"20000101","phone":"0120112233445"}
    return render(request,'mypage.html',{"user":id,"name":"mypage","userlist":list})

def homehost(request):
    id = ''
    try:
        id = request.session['host_id']
    except:
        return redirect('/')
    return render(request,'homehost.html',{"user":id,"name":"host"})

def hostevent(request):
    id = ''
    try:
        id = request.session['host_id']
    except:
        return redirect('/')
    ##
     # TODO:12-1
     # 主催者がホストのイベントをすべて取得する
     # 取得する内容は{"id":0,"name":"","place":"","date":""}
     # これをリストにし取得する
     ##
    '''ここから'''
    user = U_users.objects.get(u_mail_address = id).u_user_id
    list = E_events.objects.filter(u_user_id_id = user).values("e_event_id", "e_event_name", "p_places__p_prefecture", "e_start")
    # list = ({"id":0,"name":"COD","place":"tokyo","date":"0201"},{"id":2,"name":"CS50","place":"tokyo","date":"0228"}) # ダミーデータのため後々消す

    '''ここまで'''
    return render(request,'hostevent.html',{"user":id,"name":"host","eventlist":list})

def hostnfc(request):
    ##
     # TODO:12-2
     # 主催者がホストのイベントをすべて取得する
     # 取得する内容は{"id":0,"name":"","place":"","date":""}
     # これをリストにし取得する
     ##
    id = ''
    try:
        id = request.session['host_id']
    except:
        return redirect('/')
        
    '''ここから'''
    user = U_users.objects.get(u_mail_address = id).u_user_id
    list = E_events.objects.filter(u_user_id_id = user).values("e_event_id", "e_event_name", "p_places__p_prefecture", "e_start")
    # list = ({"id":0,"name":"COD","place":"tokyo","date":"0201"},{"id":2,"name":"CS50","place":"tokyo","date":"0228"}) # ダミーデータのため後々消す

    '''ここまで'''
    return render(request,'hostnfc.html',{"user":id,"name":"host","eventlist":list})

def hostnfcget(request):
    uid = ''
    try:
        uid = request.session['host_id']
    except:
        return redirect('/')
    id = ''
    if 'id' in request.GET:
        id = str(int(request.GET['id']) + 8635)
    return render(request,'hostnfcget.html',{"user":uid,"name":"host","id":id})

def hostnfcget_a(request):
    """hostnfcget_gと同じ"""
     # 入力されたNFCをGET
    nfcid = request.GET['nfc']

    # イベントIDをGET
    eventid = str(int(request.GET['id']) - 8635)
    
    # NFCテーブルにNFCがあるか探す
    prm = {"wasentry":0}
    nfcObj = N_nfcs.objects
    if nfcObj.filter(n_nfcid = nfcid, n_is_deleted = False).exists():
        userid = nfcObj.get(n_nfcid = nfcid).u_user_id_id
        prm["isnfc"] = 1
        # 今回のイベントのチケットを持っているか
        ticketObj = T_tickets.objects
        if ticketObj.filter(e_event_id_id = eventid, u_user_id_id = userid).exists():
            ticketid = ticketObj.get(e_event_id_id = eventid, u_user_id_id = userid).t_ticket_id
            entruObj = En_entries.objects
            if not entruObj.filter(t_ticket_id_id = ticketid).exists():
                entruObj.create(t_ticket_id_id = ticketid)
                prm["isticket"] = 1
            else:
                prm["wasentry"] = 1
        else:
            prm["isticket"] = 0
    else:
        prm["isnfc"] = 0
        prm["isticket"] = 0


    # prm = {"isnfc": 1, "isticket": 1}
    return JsonResponse(prm,safe=False)

def hostnfcget_g(request):
    id = ''
    try:
        id = request.session['host_id']
    except:
        return redirect('/')
    ##
     # TODO:13
     # GETでNFCidを受け取りその内容をdbに登録登録できたのであればjson({isnfc:True,isticket:True})を返す
     # もしticketを持っていない場合json({isnfc:True,isticket:False})を返す
     ##
    
    # 登録=入場時間記録
    
    # 入力されたNFCをGET
    nfcid = request.GET['nfc']

    # イベントIDをGET
    eventid = str(int(request.GET['id']) - 8635)
    
    # NFCテーブルにNFCがあるか探す
    prm = {"wasentry":0}
    nfcObj = N_nfcs.objects
    if nfcObj.filter(n_nfcid = nfcid, n_is_deleted = False).exists():
        userid = nfcObj.get(n_nfcid = nfcid).u_user_id_id
        prm["isnfc"] = 1
        # 今回のイベントのチケットを持っているか
        ticketObj = T_tickets.objects
        if ticketObj.filter(e_event_id_id = eventid, u_user_id_id = userid).exists():
            ticketid = ticketObj.get(e_event_id_id = eventid, u_user_id_id = userid).t_ticket_id
            entruObj = En_entries.objects
            if not entruObj.filter(t_ticket_id_id = ticketid).exists():
                entruObj.create(t_ticket_id_id = ticketid)
                prm["isticket"] = 1
            else:
                prm["wasentry"] = 1
        else:
            prm["isticket"] = 0
    else:
        prm["isnfc"] = 0
        prm["isticket"] = 0


    # prm = {"isnfc": 1, "isticket": 1}
    return JsonResponse(prm,safe=False)

def genticket(request):
    id = ''
    try:
        id = request.session['host_id']
    except:
        return redirect('/')

    return render(request,'genticket.html',{"user":id,"name":"host"})
    

def logout(request):
    try:
        del request.session['member_id']
    except:
        try:
            del request.session['host_id']
        except:
            pass
    return redirect('/')

import re
def genticket_m(request):
    id = ''
    try:
        id = request.session['host_id']
    except:
        return redirect('/')
    # print('name' in request.POST, 'hostname' in request.POST, 'detail' in request.POST, 'prefer' in request.POST, 'institution' in request.POST)
    if 'name' in request.POST and 'hostname' in request.POST and 'detail' in request.POST and 'prefer' in request.POST and 'institution' in request.POST:
        ##
         # TODO:16
         # POSTで受け取った値をDBへ登録する
         # CSVを展開する
         ##
        
        #POSTから変数を受け取る
        name = request.POST['name']
        host = request.POST['hostname']
        detail = request.POST['detail']
        startDate = request.POST['startDate']
        endDate = request.POST['endDate']
        prefecture = request.POST['prefer']
        ti_start = request.POST['tiStart']
        ti_end = request.POST['tiEnd']
        city = request.POST['city']
        institution = request.POST['institution']
        url = request.POST['url']
        xyz = request.POST['xyz']
        
        ido = ""
        kedo = ""
        if not xyz == '':
            temp = xyz.split(',')
            ido = temp[0].replace(' ','')
            kedo = temp[1].replace(' ','')


        # 期間不正排除
        if not ti_start < ti_end:
            return redirect('/genticket')
        if not startDate < endDate:
            return redirect('/genticket')
        if endDate < ti_end:
            return redirect('/genticket')

        if startDate == '':
            startDate = "1111-11-11 11:11"
        if endDate == '':
            endDate = "1111-11-11 11:11"
        if ti_start == '':
            ti_start = "1111-11-11"
        if ti_end == '':
            ti_end = "1111-11-11"
        
        # 


        # startDate = startDate.replace('T', ' ')
        # endDate = endDate.replace('T', ' ')


        # print("日付型", startDate, type(startDate))
        # DBへ登録
        
        # イベントテーブルのレコード生成と同時に自動生成された主キーを取得し、それを開催地テーブルのイベントIDにぶち込む案
        # eventid = E_events.objects.create(e_event_name = name, e_host_name = host, e_outline = detail, e_start = startDate, e_end = endDate).get('e_event_id')
        
        # __付けたらテーブルまたいで取得できるらしいから生成もできる説
        # P_places.objects.create(e_events__e_event_name = name, e_events__e_host_name = host, e_events__e_outline = detail,p_prefecture = prefecture, e_events__e_start = startDate, e_events__e_end = endDate, p_city = city, p_build = institution, p_url = url, p_ido = ido, p_kedo = kedo)
        user = U_users.objects.get(u_mail_address = id).u_user_id
        # イベントテーブル
        eventid = E_events.objects.create(e_event_name = name, e_host_name = host, e_outline = detail, e_start = startDate, e_end = endDate, u_user_id_id = user).e_event_id
        # 開催地テーブル
        P_places.objects.create(e_event_id_id = eventid, p_prefecture = prefecture, p_city = city, p_build = institution, p_url = url, p_ido = ido, p_kedo = kedo)
        # eventid = E_events.objects.latest("e_created_onat").e_event_id
        # print("イベントID", eventid, type(eventid))

        # チケット情報テーブル
        ticketsinfoid = Ti_ticketsinfos.objects.create(e_event_id_id = eventid, ti_start = ti_start, ti_end = ti_end).ti_ticketsinfo_id
        
        # その他テーブル     
        titleList= []
        bodyList= []
        # request.POST.items()でPOSTで送られてきた全てを取得。
        for i in request.POST.items():
        # name属性のtitle_から始まるものをtitleListに追加
            if re.match(r'title_*',i[0]):
                titleList.append(i[1])
            if re.match(r'body_*',i[0]):
                bodyList.append(i[1])
        # titleListの要素数分をぶん回す
        for i in range(len(titleList)):
            # DBに追加
            # print(titleList[i], bodyList[i])
            O_others.objects.create(e_event_id_id = eventid, o_name = titleList[i], o_detail = bodyList[i])


        
        # 料金CSV
        if 'plice' in request.FILES:
            data = io.TextIOWrapper(request.FILES['plice'].file, encoding='utf-8')
            csv_content = csv.reader(data)
            scidID = []
            for i in csv_content:
                # ['座席区分', '料金区分', '値段']
                # 座席区分テーブル, なければ追加
                obj_2, created_2 = Sc_seatclasses.objects.get_or_create(sc_name = i[0])
                scid = obj_2.sc_id
                # 料金区分テーブル, なければ追加
                obj_1, created_1 = Cc_chargeclasses.objects.get_or_create(cc_name = i[1])
                ccid = obj_1.cc_id
                # 料金テーブル
                chargeid = C_charges.objects.create(ti_ticketsinfo_id_id = ticketsinfoid, c_charge = i[2    ]).c_charge_id
                # 料金中間テーブル
                Ww_charges_ww.objects.create(cc_id_id = ccid, sc_id_id = scid, c_charge_id_id = chargeid, e_event_id_id = eventid)

                #使用するsheetリストを作る
                if not scid in scidID:
                    scidID.append(scid)

            sheetList = {}
            # 定員テーブル
            for i in scidID:
                sheetList[i] = M_maxes.objects.create(ti_ticketsinfo_id_id = ticketsinfoid, sc_id_id = i).m_capacity_id

            # print("SheetList 席区分:定員", sheetList)
            # 座席CSV
            # print("ファイルいるかな" ,'sheet' in request.FILES, 'plice' in request.FILES)
            if 'sheet' in request.FILES:
                data = io.TextIOWrapper(request.FILES['sheet'].file, encoding='utf-8')
                csv_content = csv.reader(data)
                for i in csv_content:
                    # ['座席区分', '座席位置']
                    # 座席区分IDを取得
                    
                    sc_id = Sc_seatclasses.objects.get(sc_name = i[0]).sc_id
                    # 座席情報テーブル
                    S_seats.objects.create(ti_ticketsinfo_id_id = ticketsinfoid, sc_id_id = sc_id, s_place = i[1])

                # 定員を更新
                for i in scidID:
                    cap = S_seats.objects.filter(ti_ticketsinfo_id_id = ticketsinfoid, sc_id_id = i).count()
                    temp = M_maxes.objects.get(pk = sheetList[i])
                    temp.m_capacity = cap
                    temp.save()

        return redirect('/homehost')
    else:
        return redirect('/')


 

def pay(request):
    try:
        id = request.session['member_id']
    except:
        return redirect('/')
    return render(request,'pay.html',{"user":id,"name":"pay"})

import payjp

def pay_m(request):
    ## 
     # TODO:18
     # 決済処理が完了したときチケットを登録する
     # 決済処理が完了したときリダイレクトさせる
     ##
    if 'id' in request.GET:
        #料金中間テーブルIDを取得し、料金idを使って料金テーブルとjoinして値段をchargeAmount(新変数)に代入
        chargeid = Ww_charges_ww.objects.get(pk=request.GET['id']).c_charge_id_id
        chargeAmount = C_charges.objects.get(pk=chargeid).c_charge
        if chargeAmount > 0:
            payjp.api_key = "sk_test_9969d1219460ecdd40f02304"
            charge = payjp.Charge.create(
                amount=chargeAmount,
                card=request.POST['id'],
                currency='jpy',
            )
            if 'status' in charge:
                prm = {"err": charge['message']}
            else:
                ccid = Ww_charges_ww.objects.get(pk=request.GET['id']).ww_charge_id
                eventid = Ww_charges_ww.objects.get(pk=request.GET['id']).e_event_id_id
                user_obj = U_users.objects.filter(u_mail_address = request.session['member_id'])
                userid = user_obj[0].u_user_id
                ticketid = T_tickets.objects.create(e_event_id_id=eventid, u_user_id_id=userid, ww_charge_id_id =ccid)
                '''席指定'''
                # if request.GET['seatid'] != "":
                #    S_seats.objects.get(pk = request.GET['seatid']).t_ticket_id_id = ticketid
                prm = {"err": "Ok"}
        else:
            ccid = Ww_charges_ww.objects.get(pk=request.GET['id']).ww_charge_id
            eventid = Ww_charges_ww.objects.get(pk=request.GET['id']).e_event_id_id
            user_obj = U_users.objects.filter(u_mail_address = request.session['member_id'])
            userid = user_obj[0].u_user_id
            ticketid = T_tickets.objects.create(e_event_id_id=eventid, u_user_id_id=userid, ww_charge_id_id =ccid)
            '''席指定'''
            # if request.GET['seatid'] != "":
            #    S_seats.objects.get(pk = request.GET['seatid']).t_ticket_id_id = ticketid
            prm = {"err": "Ok"}
    else:
        prm = {"err": "idが無効です"}
    
    return JsonResponse(prm,safe=False)
