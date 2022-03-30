from statistics import mode
from django.db import models



# Create your models here.

## モデル(py) = テーブル(db)

""" コピペ用 """
### db_column='main_id'
### on_delete=models.CASCADE

"""仮パスワードテーブル"""
class L_lostPasswords(models.Model):

    # メールアドレス
    l_mail = models.EmailField(primary_key=True)

    # 仮パスワード
    l_password = models.TextField()

    # 論理削除フラグ
    l_is_deleted = models.BooleanField(default=False)

    class Meta:

        verbose_name_plural = '仮パスワード'

"""NFCテーブル"""
class N_nfcs(models.Model):

    # NFCローカルID
    n_nfc_local_id = models.AutoField(primary_key=True)

    # ユーザーID
    u_user_id = models.ForeignKey('U_users', db_column='u_user_id', on_delete=models.CASCADE)

    # NFC ID
    n_nfcid = models.CharField(max_length=255, unique=True)

    # 論理削除フラグ
    n_is_deleted = models.BooleanField(default=False)

    class Meta:

        verbose_name_plural = 'NFC'


"""住所テーブル"""
class A_addresses(models.Model):

    # 住所ID
    a_address_id = models.AutoField(primary_key=True)

    # ユーザーID
    u_user_id = models.OneToOneField('U_users', db_column='u_user_id', on_delete=models.CASCADE)

    # 郵便番号
    a_address_number = models.CharField(max_length=7)

    # 都道府県
    a_prefecture = models.CharField(max_length = 4)

    # 市区町村
    a_city = models.CharField(max_length = 255)

    # 番地
    a_number = models.TextField()

    # 建物部屋番号
    a_build = models.TextField(blank=True, default="")

    class Meta:

        verbose_name_plural = '住所'

"""ユーザーテーブル"""
class U_users(models.Model):

    # ユーザーID
    u_user_id = models.AutoField(primary_key=True)

    # 名前
    u_name = models.CharField(max_length=255)

    # 生年月日
    u_happy_lucky_birthday = models.DateField()

    # メールアドレス
    u_mail_address = models.EmailField(unique=True)

    # 電話番号
    u_phone_number = models.CharField(max_length=11, unique=True)

    # パスワード
    u_password = models.CharField(max_length=255)

    # 顔写真
    u_photo_of_face =  models.URLField(blank=True, unique=True, default="http://example.com")

    # ユーザ区分ID
    uc_id = models.ForeignKey('Uc_userclasses', db_column='uc_id', on_delete=models.CASCADE)

    # 論理削除フラグ
    u_is_deleted = models.BooleanField(default=False)

    # 作成日時
    u_created_onat = models.DateTimeField(auto_now_add=True)

    # 更新日時
    u_update_onat = models.DateTimeField(auto_now=True)

    class Meta:

        verbose_name_plural = 'ユーザー'
    
    def __str__(self):
        return self.u_name

"""ユーザー区分テーブル"""
class Uc_userclasses(models.Model):
    
    # ユーザー区分ID
    uc_id = models.AutoField(primary_key=True)

    # 区分名
    uc_name = models.CharField(max_length=3, unique=True)

    def __str__(self):
        return self.uc_name

    class Meta:

        verbose_name_plural = 'ユーザー区分'

"""入場テーブル"""
class En_enries(models.Model):

    # 入場ID
    en_entry_id = models.AutoField(primary_key=True)

    # チケットID
    t_ticket_id = models.OneToOneField('T_tickets', db_column='t_ticket_id', on_delete=models.CASCADE)

    # 入場時間
    en_entry_onat = models.DateTimeField(auto_now_add=True)

    class Meta:

        verbose_name_plural = '入場'


"""チケットテーブル"""
class T_tickets(models.Model):
    
    # チケットID
    t_ticket_id = models.AutoField(primary_key=True)
    
    # ユーザーID
    u_user_id = models.ForeignKey('U_users', db_column='u_user_id', on_delete=models.CASCADE)

    # イベントID
    e_event_id = models.ForeignKey('E_events', db_column='e_event_id', on_delete=models.CASCADE)

    # 座席情報ID
    ## チケット-座席情報の外部キーは座席情報に移行しました
    # s_seat_id = models.ForeignKey('S_seats', db_column='s_seat_id', on_delete=models.CASCADE, default= -1 )

    # 料金中間テーブルID
    ww_charge_id = models.ForeignKey('Ww_charges_ww', db_column='ww_charge_id', on_delete=models.CASCADE)

    # 販売日時
    t_sold_onat = models.DateTimeField(auto_now_add=True)

    # 体温
    t_temperature = models.DecimalField(max_digits=3, decimal_places=1, default= 00.0)

    # 論理削除フラグ
    t_is_deleted = models.BooleanField(default=False)

    class Meta:

        verbose_name_plural = 'チケット'


"""開催地テーブル"""
class P_places(models.Model):

    # 開催地ID
    p_place_id = models.AutoField(primary_key=True)
    
    # イベントID
    e_event_id = models.OneToOneField('E_events', db_column='e_event_id', on_delete=models.CASCADE)
    
    # 地方
    # p_region = models.CharField(max_length=10)

    # 都道府県
    p_prefecture = models.CharField(max_length = 5)

    # 市区町村
    p_city = models.CharField(blank=True, max_length = 255, default="0000000000")

    # 施設名
    p_build = models.CharField(max_length=255)

    # サイトURL
    p_url = models.URLField(blank=True, default="http://example.com")

    # 緯度
    p_ido = models.CharField(max_length=17, blank=True, default='99')

    # 経度
    p_kedo = models.CharField(max_length=18, blank=True, default='360')

    class Meta:

        verbose_name_plural = '開催地'


"""イベントテーブル"""
class E_events(models.Model):

    # イベントID
    e_event_id = models.AutoField(primary_key=True)

    # イベント名
    e_event_name = models.CharField(max_length=255)

    # 主催者
    e_host_name = models.CharField(max_length=255)

    # 概要
    e_outline = models.TextField()

    # 作成者ID
    u_user_id = models.ForeignKey('U_users', db_column='u_user_id', on_delete=models.CASCADE)

    # 開始日
    e_start = models.DateTimeField(default="1111-11-11 00:00", blank=True)

    # 終了日
    e_end = models.DateTimeField(default="1111-11-11 00:00", blank=True)

    # 広告有無
    e_advertisement_flag = models.BooleanField(default=False)

    # 開催地ID
    # p_place_id = models.ForeignKey('P_places', db_column='p_place_id', on_delete=models.CASCADE)

    # チケット情報ID
    # ti_ticketsinfo_id = models.ForeignKey('Ti_ticketsinfos', db_column='ti_ticketsinfo_id ', on_delete=models.CASCADE)

    # 論理削除フラグ
    e_is_deleted = models.BooleanField(default=False)

    # 作成日時
    e_created_onat = models.DateTimeField(auto_now_add=True)

    # 更新日時
    e_update_onat = models.DateTimeField(auto_now=True)

    class Meta:

        verbose_name_plural = 'イベント'


"""チケット情報テーブル"""
class Ti_ticketsinfos(models.Model):
    
    # チケット情報ID
    ti_ticketsinfo_id = models.AutoField(primary_key=True)

    # イベントID
    e_event_id = models.OneToOneField('E_events', db_column='e_event_id', on_delete=models.CASCADE, blank=True, default = -1)

    # 販売開始日
    ti_start = models.DateField(blank=True, default="1111-11-11")

    # 販売終了日
    ti_end = models.DateField(blank=True, default="1111-11-11")

    class Meta:

        verbose_name_plural = 'チケット情報'


"""座席情報テーブル"""
class S_seats(models.Model):

    # 座席情報ID
    s_seats_id = models.AutoField(primary_key=True)

    # チケットID
    t_ticket_id = models.OneToOneField('T_tickets', db_column='t_ticket_id', on_delete=models.CASCADE, null=True)

    # チケット情報ID
    ti_ticketsinfo_id = models.ForeignKey('Ti_ticketsinfos', db_column='ti_ticketsinfo_id', on_delete=models.CASCADE, default = -1)

    # 座席区分ID
    sc_id = models.ForeignKey('Sc_seatclasses', db_column='sc_id', on_delete=models.CASCADE, default = -1)

    # 座席位置
    s_place = models.CharField(max_length=255, default="0000-0000-0000")

    class Meta:

        verbose_name_plural = '座席情報'


"""その他テーブル"""
class O_others(models.Model):

    # その他ID
    o_other_id = models.AutoField(primary_key=True)

    # イベントID
    e_event_id = models.ForeignKey('E_events', db_column='e_event_id', on_delete=models.CASCADE)

    # 備考名
    o_name = models.CharField(max_length=10)

    # 詳細
    o_detail = models.TextField()

    class Meta:

        verbose_name_plural = 'その他'


"""イベントタグ中間テーブル"""
class Zz_events_connect_tags_zz(models.Model):

    # イベント中間テーブルID(複合主キーダメとか言われたんで)
    zz_event_id = models.AutoField(primary_key=True)

    # イベントID
    e_event_id = models.ForeignKey('E_events', db_column='e_event_id', on_delete=models.CASCADE)

    # イベントタグID
    yy_eventtag_id = models.ForeignKey('Yy_eventtags', db_column='yy_eventtag_id', on_delete=models.CASCADE)

    class Meta:

        verbose_name_plural = 'イベントタグ中間テーブル'


"""料金テーブル"""
class C_charges(models.Model):

    # 料金ID
    c_charge_id = models.AutoField(primary_key=True)

    # チケット情報ID
    ti_ticketsinfo_id = models.ForeignKey('Ti_ticketsinfos', db_column='ti_ticketsinfo_id', on_delete=models.CASCADE)

    # 値段
    c_charge = models.PositiveIntegerField()

    class Meta:

        verbose_name_plural = '料金'


"""定員テーブル"""
class M_maxes(models.Model):
    
    # 定員ID
    m_capacity_id = models.AutoField(primary_key=True)

    # チケット情報ID
    ti_ticketsinfo_id = models.ForeignKey('Ti_ticketsinfos', db_column='ti_ticketsinfo_id', on_delete=models.CASCADE)

    # 座席区分ID
    sc_id = models.ForeignKey('Sc_seatclasses', db_column='sc_id', on_delete=models.CASCADE, default = -1)

    # 定員数
    m_capacity = models.PositiveIntegerField(blank=True, default = 0)

    class Meta:

        verbose_name_plural = '定員'


"""チケット料金中間テーブル"""
class Oo_ticket_connect_charge_oo(models.Model):

    # チケット中間テーブルID(複合主キーダメとか言われたんで)
    oo_ticket_id = models.AutoField(primary_key=True)

    # 料金区分ID
    cc_id = models.ForeignKey('cc_chargeclasses', db_column='cc_id', on_delete=models.CASCADE)

    # チケットID
    t_ticket_id = models.ForeignKey('T_tickets', db_column='t_ticket_id', on_delete=models.CASCADE)

    class Meta:

        verbose_name_plural = 'チケット料金中間テーブル'


"""イベントタグテーブル"""
class Yy_eventtags(models.Model):

    # イベントタグID
    yy_eventtag_id = models.AutoField(primary_key=True)

    # タグ名
    yy_name = models.CharField(max_length=50, unique=True)

    class Meta:

        verbose_name_plural = 'イベントタグ'
    
    def __str__(self):
        return self.yy_name


"""料金中間テーブル"""
class Ww_charges_ww(models.Model):

    # 料金中間テーブルID
    ww_charge_id = models.AutoField(primary_key=True)

    # 料金区分ID
    cc_id = models.ForeignKey('cc_chargeclasses', db_column='cc_id', on_delete=models.CASCADE)

    # 座席区分ID
    sc_id = models.ForeignKey('Sc_seatclasses', db_column='sc_id', on_delete=models.CASCADE, default = -1)

    # 料金ID
    c_charge_id = models.ForeignKey('C_charges', db_column='c_charge_id', on_delete=models.CASCADE)

    # イベントID
    e_event_id = models.ForeignKey('E_events', db_column='e_event_id', on_delete=models.CASCADE)

    class Meta:

        verbose_name_plural = '料金中間テーブル'


"""座席区分テーブル"""
class Sc_seatclasses(models.Model):

    # 座席区分ID
    sc_id = models.AutoField(primary_key=True)

    # 座席区分名
    sc_name = models.CharField(max_length=10, unique=True)

    class Meta:

        verbose_name_plural = '座席区分'

    def __str__(self):
        return self.sc_name


"""料金区分テーブル"""
class Cc_chargeclasses(models.Model):
    
    # 料金区分
    cc_id = models.AutoField(primary_key=True)

    # 料金区分名
    cc_name = models.CharField(max_length=10, unique=True)

    class Meta:

        verbose_name_plural = '料金区分'
    
    def __str__(self):
        return self.cc_name
