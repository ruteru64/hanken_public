from django.contrib import admin


# Register your models here.
from .models import U_users
admin.site.register(U_users)

from .models import N_nfcs
admin.site.register(N_nfcs)

from .models import A_addresses
admin.site.register(A_addresses)

from .models import Uc_userclasses
admin.site.register(Uc_userclasses)

from .models import En_enries
admin.site.register(En_enries)

from .models import T_tickets
admin.site.register(T_tickets)

from .models import P_places
admin.site.register(P_places)

from .models import E_events
admin.site.register(E_events)

from .models import Ti_ticketsinfos
admin.site.register(Ti_ticketsinfos)

from .models import S_seats
admin.site.register(S_seats)

from .models import O_others
admin.site.register(O_others)

from .models import Zz_events_connect_tags_zz
admin.site.register(Zz_events_connect_tags_zz)

from .models import C_charges
admin.site.register(C_charges)

from .models import M_maxes
admin.site.register(M_maxes)

from .models import Oo_ticket_connect_charge_oo
admin.site.register(Oo_ticket_connect_charge_oo)

from .models import Yy_eventtags
admin.site.register(Yy_eventtags)

from .models import Ww_charges_ww
admin.site.register(Ww_charges_ww)

from .models import Sc_seatclasses
admin.site.register(Sc_seatclasses)

from .models import Cc_chargeclasses
admin.site.register(Cc_chargeclasses)