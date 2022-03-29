from django.conf import settings
from django.views import generic
from django.views.generic.edit import FormView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView,
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
)
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.http import Http404, HttpResponseBadRequest
from django.template.loader import render_to_string
from django.core.mail import send_mail
from .forms import *
from .models import *

User = get_user_model()

class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser

class OnlySuperMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.is_superuser


''' Aiのフレーバー選択 '''
''' フレーバ選択 '''
class BaseAiAiAiOrder(generic.TemplateView):
    template_name = 'papps/ai/ai/ai_order.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def get(self, request, *args, **kwargs):
        self.naiyou = request.GET.get('naiyou')
        self.base = request.GET.get('base')
        self.seibun = request.GET.get('seibun')
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['naiyou'] = self.naiyou
        ctx['base'] = self.base
        ctx['seibun'] = self.seibun
        return ctx

''' Easyのフレーバー選択 '''
''' フレーバ選択 '''
class BaseOrderEasyOrderEasyOrder(generic.TemplateView):
    template_name = 'papps/order/easyorder/easy_order.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def get(self, request, *args, **kwargs):
        self.naiyou = request.GET.get('naiyou')
        self.base = request.GET.get('base')
        self.seibun = request.GET.get('seibun')
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['naiyou'] = self.naiyou
        ctx['base'] = self.base
        ctx['seibun'] = self.seibun
        return ctx

'''
（例）
naiyou=フルオーダー&&base=大豆&&seibun=ビタミンB|ビタミンC|コラーゲン|ヒアルロン酸|コエンザイム|カルシウム|イチョウ葉|ダイエットプラス|ロイヤルゼリー&&flavor=イチゴ&&other=個包装
'''
''' オーダー '''
class BaseOrder(generic.TemplateView):
    template_name = 'papps/order.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #税込みの金額
        self.prices = {
            'base': 1132,
            'flavor': 972,
            'seibun': 216,
            'other': 972,
            'send_price': 1,
        }
    
    def get(self, request, *args, **kwargs):
        self.naiyou = request.GET.get('naiyou')
        self.base = request.GET.get('base')
        self.flavor = request.GET.get('flavor')
        self.seibun = '' if request.GET.get('seibun') is None else request.GET.get('seibun')
        self.other = '' if request.GET.get('other') is None else request.GET.get('other')
        self.tm_send_price = '' if request.GET.get('send_price') is None else request.GET.get('send_price')
        return super().get(request, *args, **kwargs)

    def calc_base(self):
        return self.prices['base'];

    def calc_flavor(self):
        return self.prices['flavor'];

    def calc_seibun(self):
        if self.seibun == '':
            return 0
        else:
            if self.seibun == '追加しない':
                return 0
            elif '/' not in self.seibun:
                return self.prices['seibun']
            else:
                return len(self.seibun.split('/')) * self.prices['seibun']

    def calc_other(self):
        if self.other == '':
            return 0
        else:
            if self.other == '追加しない':
                return 0
            elif '/' not in self.other:
                return self.prices['other']
            else:
                return len(self.other.split('/')) * self.prices['other']

    def price_syoukei(self):
        return round(self.price_zeikomi() / 1.08)

    def price_zei(self):
        return round(self.price_syoukei() * 0.08);

    def price_zeikomi(self):
        return self.price_sougaku() + 2000

    def send_price(self):
        try:
            add_price = round(int(self.tm_send_price) * self.prices['send_price'])
            if add_price < 101:
                raise Exception()
            return add_price
        except:
            return 0

    def price_sougaku(self):
        return self.calc_base() + self.calc_flavor() + self.calc_seibun() + self.calc_other() + self.send_price()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['naiyou'] = self.naiyou
        ctx['base'] = self.base
        ctx['seibun'] = self.seibun
        ctx['flavor'] = self.flavor
        ctx['other'] = self.other
        ctx['send_price'] = self.send_price()
        ctx['syoukei'] = self.price_syoukei()
        ctx['zei'] = self.price_zei()
        ctx['zeikomi'] = self.price_zeikomi()
        ctx['sougaku'] = self.price_sougaku()
        return ctx


''' 再オーダー '''
class BaseReOrder(OnlyYouMixin, BaseOrder):
    template_name = 'papps/reorder.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #2000引きは無し
        self.prices['base'] = 3132

    def get(self, request, *args, **kwargs):
        self.naiyou = request.GET.get('naiyou')
        self.base = request.GET.get('base')
        self.flavor = request.GET.get('flavor')
        self.seibun = '' if request.GET.get('seibun') is None else request.GET.get('seibun')
        self.other = '' if request.GET.get('other') is None else request.GET.get('other')
        return super().get(request, *args, **kwargs)

    def price_zeikomi(self):
        return self.price_sougaku()

    def post(self, request, *args, **kwargs):
        ctx = {
            'name': request.user.sei_name + request.user.mei_name,
            'id': request.user.id,
            'email': request.user.email,
            'naiyou': request.POST.get('naiyou'),
            'base': request.POST.get('base'),
            'seibun': request.POST.get('seibun'),
            'flavor': request.POST.get('flavor'),
            'other': request.POST.get('other'),
            'syoukei': request.POST.get('syoukei'),
            'zei': request.POST.get('zei'),
            'zeikomi': request.POST.get('zeikomi'),
            'sougaku': request.POST.get('sougaku'),
        }
        subject = render_to_string('papps/mail_template/re_order/subject.txt', ctx)
        message = render_to_string('papps/mail_template/re_order/message.txt', ctx)
        host_user = getattr(settings, 'EMAIL_HOST_USER', None)
        send_mail(
            subject, message, host_user, [host_user]
        )
        return redirect('papps:basereorderdone')


''' オーダー2 '''
class BaseOrder2(FormView):
    form_class = UserCreateForm
    template_name = 'papps/order2.html'
    success_url = reverse_lazy('papps:baseorder3')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def form_valid(self, form):
        self.request.session['protein_data'] = {
            'naiyou': self.request.GET.get('naiyou'),
            'base': self.request.GET.get('base'),
            'flavor': self.request.GET.get('flavor'),
            'seibun': '' if self.request.GET.get('seibun') is None else self.request.GET.get('seibun'),
            'other': '' if self.request.GET.get('other') is None else self.request.GET.get('other'),
            'syoukei': self.request.GET.get('syoukei'),
            'zei': self.request.GET.get('zei'),
            'zeikomi': self.request.GET.get('zeikomi'),
            'send_price': self.request.GET.get('send_price'),
            'sougaku': self.request.GET.get('sougaku'),
        }
        self.request.session['user_data'] = {
            'sei_name': form.cleaned_data['sei_name'],
            'mei_name': form.cleaned_data['mei_name'],
            'yubin_bangou': form.cleaned_data['yubin_bangou'],
            'jusyo': form.cleaned_data['jusyo'],
            'tel_bangou': form.cleaned_data['tel_bangou'],
            'email': form.cleaned_data['email'],
            'password': form.cleaned_data['password'],
        }
        return super().form_valid(form)    

''' オーダー3 '''
class BaseOrder3(generic.TemplateView):
    form_class = UserCreateForm
    template_name = 'papps/order3.html'

    def get(self, request, *args, **kwargs):
        if 'user_data' in request.session and 'protein_data' in request.session:
            return super().get(request, *args, **kwargs)
        else:
            request.session.clear()
            return redirect('papps:baseindex')
            

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if 'user_data' in self.request.session and 'protein_data' in self.request.session:
            session = self.request.session
            ctx['name'] = session['user_data']['sei_name'] + session['user_data']['mei_name']
            ctx['yubin_bangou'] = session['user_data']['yubin_bangou']
            ctx['jusyo'] = session['user_data']['jusyo']
            ctx['tel_bangou'] = session['user_data']['tel_bangou']
            ctx['email'] = session['user_data']['email']
        return ctx


class BaseInsertData(generic.TemplateView):
    form_class = UserCreateForm
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        if 'user_data' in self.request.session and 'protein_data' in self.request.session:
            user_data = request.session.pop('user_data')
            protein_data = request.session.pop('protein_data')
            uq = User.objects.create_user(
                sei_name = user_data['sei_name'],
                mei_name = user_data['mei_name'],
                yubin_bangou = user_data['yubin_bangou'],
                jusyo = user_data['jusyo'],
                tel_bangou = user_data['tel_bangou'],
                email = user_data['email'],
                password = user_data['password'],
            )
            oq = Order.objects.create(
                user_id = uq.pk,
                naiyou = protein_data['naiyou'],
                base = protein_data['base'],
                flavor = protein_data['flavor'],
                seibun = protein_data['seibun'],
                other = protein_data['other'],
                syoukei = protein_data['syoukei'],
                zei = protein_data['zei'],
                zeikomi = protein_data['zeikomi'],
                send_price = protein_data['send_price'],
                sougaku = protein_data['sougaku'],
            )
            request.session.clear()
            user = authenticate(email=user_data['email'], password=user_data['password'])
            if user is not None:
                return redirect('papps:basepayorder', token=dumps(uq.pk))
            else:
                return redirect('papps:baseindex')
        else:
            request.session.clear()
            return redirect('papps:baseindex')

''' 支払情報登録 '''
class BasePayOrder(generic.TemplateView):
    template_name = 'papps/payorder.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                oq = Order.objects.get(user_id=user_pk)
                ctx['sougaku'] = oq.sougaku.replace('円', '')
                ctx['zeikomi'] = oq.zeikomi.replace('円', '')
        return ctx


''' 支払情報変更 '''
class BasePayOrderChange(OnlyYouMixin, generic.TemplateView):
    template_name = 'papps/payorderchange.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['dumps_id'] = dumps(kwargs['pk'])
        return ctx

    def post(self, request, *args, **kwargs):
        try:
            user_pk = loads(request.POST.get('dumps_id'), max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            uq = User.objects.get(pk=user_pk)
            ctx = {
                'protocol': request.scheme,
                'domain': request.get_host(),
                'name': uq.sei_name + uq.mei_name,
                'email': uq.email,
                'dumps_id': dumps(user_pk),
            }
            subject = render_to_string('papps/mail_template/pay_order_change/subject.txt', ctx)
            message = render_to_string('papps/mail_template/pay_order_change/message.txt', ctx)
            host_user = getattr(settings, 'EMAIL_HOST_USER', None)
            send_mail(
                subject, message, host_user, [host_user]
            )
            return redirect('papps:basepayorderchangedone')
        


''' マイページ '''
class BaseMyPage(OnlyYouMixin, generic.TemplateView):
    template_name = 'papps/mypage.html'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if User.objects.filter(pk=kwargs['pk']).exists() and Order.objects.filter(user_id=kwargs['pk']).exists():
            user_data = User.objects.get(pk=kwargs['pk'])
            order_data = Order.objects.get(user_id=kwargs['pk'])
            ctx['user_id'] = user_data.id
            ctx['dumps_id'] = dumps(user_data.id)
            ctx['name'] = user_data.sei_name + user_data.mei_name
            ctx['yubin_bangou'] = user_data.yubin_bangou
            ctx['jusyo'] = user_data.jusyo
            ctx['tel_bangou'] = user_data.tel_bangou
            ctx['email'] = user_data.email
            ctx['naiyou'] = '' if order_data.naiyou is None else order_data.naiyou
            ctx['base'] = '' if order_data.base is None else order_data.base
            ctx['flavor'] = '' if order_data.flavor is None else order_data.flavor
            ctx['seibun'] = '' if order_data.seibun is None else order_data.seibun
            ctx['other'] = '' if order_data.other is None else order_data.other
            ctx['sougaku'] = order_data.sougaku

            iad_data = {}
            for obj in raw_queryset_normal(Order.select_inputadddata(self.kwargs['pk'])):
                iad_data[obj['name']] = obj['data']
            ctx['iad_data'] = iad_data
            return ctx
        else:
            raise Http404('idと紐づくユーザが存在しません')


''' スーパーユーザーページ '''
class BaseSuperUserPage(OnlySuperMixin, generic.TemplateView):
    template_name = 'papps/superuserpage.html'


''' 一般ユーザ一覧ページ '''
class BaseNormalUserInfo(OnlySuperMixin, generic.TemplateView):
    template_name = 'papps/normaluserinfo.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        users = User.objects.filter(is_superuser=False)
        ctx['data'] = raw_queryset_normal(User.select_normaluserdata())
        return ctx



''' マイページ編集 '''
class BaseMyPageEdit(OnlySuperMixin, generic.TemplateView):
    form_useredit_class = UserEditForm
    form_orderedit_class = OrderEditForm
    form_inputadddata_class = InputAddDataForm
    
    template_name = 'papps/mypageedit.html'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        try:
            ctx = super().get_context_data(**kwargs)
            edit_user = User.objects.get(pk=self.kwargs['pk'])
            ctx['user_name'] = edit_user.sei_name + edit_user.mei_name
            
            user_data = User.objects.get(pk=self.kwargs['pk'])
            ctx['useredit_form'] = self.form_useredit_class(
                initial = {
                    'yubin_bangou': user_data.yubin_bangou,
                    'jusyo': user_data.jusyo,
                    'tel_bangou': user_data.tel_bangou,
                    'email': user_data.email,
                }
            )
            order_data = Order.objects.get(user_id=self.kwargs['pk'])
            ctx['orderedit_form'] = self.form_orderedit_class(
                initial = order_data.__dict__
            )

            iad_data = {}
            for obj in raw_queryset_normal(Order.select_inputadddata(self.kwargs['pk'])):
                iad_data[obj['temp_id']] = obj['data']

            print(len(iad_data))
            ctx['inputadddata_form'] = self.form_inputadddata_class(
                initial = iad_data
            )
            ctx['inputadd_cnt'] = len(InputAdd.objects.all())
            return ctx
        except Exception:
            raise Http404('idと紐づくユーザが存在しません')


''' マイページ編集（ユーザ） '''
class BaseMyPageEditUser(OnlySuperMixin, generic.TemplateView):
    form_class = UserEditForm
    template_name = 'papps/mypageedit.html'

    def post(self, request, *args, **kwargs):
        uq = User.objects.get(pk=self.kwargs['pk'])
        form = self.form_class(request.POST, instance=uq)

        if form.is_valid():    
            form.save()
        return redirect('papps:basemypageedit', pk=self.kwargs['pk'])


''' マイページ編集（オーダー） '''
class BaseMyPageEditOrder(OnlySuperMixin, generic.TemplateView):
    form_class = OrderEditForm
    template_name = 'papps/mypageedit.html'

    def post(self, request, *args, **kwargs):
        oq = Order.objects.get(user_id=self.kwargs['pk'])
        form = self.form_class(request.POST, instance=oq)

        if form.is_valid():
            form.save()
        return redirect('papps:basemypageedit', pk=self.kwargs['pk'])


''' マイページ編集（InputAddData） '''
class BaseMyPageEditInputAddData(OnlySuperMixin, generic.TemplateView):
    form_class = InputAddDataForm
    template_name = 'papps/mypageedit.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            iaq = InputAdd.objects.all()
            if len(iaq) != 0:
                if Order.objects.filter(user_id=self.kwargs['pk']).exists():
                    order_id = Order.objects.get(user_id=self.kwargs['pk']).id
                    #  inputadddataのidのディクショナリ
                    iadval_obj = {}
                    iaid_obj = {}
                    for q in iaq:
                        iadval_obj[q.temp_id] = form.cleaned_data[q.temp_id]
                        iaid_obj[q.temp_id] = InputAdd.objects.get(temp_id=q.temp_id).id

                    for k in iaid_obj:
                        InputAddData.objects.update_or_create(
                            order_id = order_id,
                            inputadd_id = iaid_obj[k],
                            defaults = {
                                'data': iadval_obj[k],
                            }
                        )
        
        return redirect('papps:basemypageedit', pk=self.kwargs['pk'])


''' 項目登録 '''
class BaseInputAddCreate(OnlySuperMixin, FormView):
    form_class = InputAddForm
    template_name = 'papps/inputadd.html'
    success_url = reverse_lazy('papps:baseinputaddcreate')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['inputadddata'] = InputAdd.objects.all()
        return ctx

    def form_valid(self, form):
        InputAdd.objects.create(
            temp_id = InputAdd.insert_tempid(),
            name = form.cleaned_data['name'],
        )
        return super().form_valid(form)


''' 項目削除 '''
class BaseInputAddDelete(OnlySuperMixin, generic.TemplateView):
    template_name = 'papps/inputadd.html'
    success_url = reverse_lazy('papps:baseinputaddcreate')

    def get(self, request, *args, **kwargs):
        InputAdd.objects.filter(id=self.kwargs['pk']).delete()
        InputAddData.objects.filter(inputadd_id=self.kwargs['pk']).delete()
        return redirect('papps:baseinputaddcreate')


''' ID検索 '''
class BaseSearchId(OnlySuperMixin, FormView):
    form_class = SearchIdForm
    template_name = 'papps/searchid.html'
    success_url = reverse_lazy('papps:basesearchid')

    def form_valid(self, form):
        ctx = {
            'form': form,
            'user_id': '存在しません',
        }
        if User.objects.filter(email=form.cleaned_data['email']).exists():
            user_id = User.objects.get(email=form.cleaned_data['email']).id
            ctx['user_id'] = user_id
            return render(self.request, self.template_name, ctx)
        return render(self.request, self.template_name, ctx)


''' ログイン '''   
class Login(LoginView):
    
    form_class = LoginForm
    template_name = 'papps/login.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        response.set_cookie('uid', str(form.get_user().pk), getattr(settings, 'SESSION_COOKIE_AGE', None))
        return response

    def get_success_url(self):
        if self.request.user.is_superuser:
            return reverse('papps:basesuperuserpage')
        else:
            return reverse('papps:basemypage', kwargs={'pk': self.request.user.pk})


''' ログアウト '''
class Logout(LogoutView):
    template_name = 'papps/logout.html'

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        response.delete_cookie('uid')
        return response


class PasswordChange(PasswordChangeView):
    """パスワード変更ビュー"""
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('papps:basepasswordchangedone')
    template_name = 'papps/password_change.html'


class PasswordChangeDone(PasswordChangeDoneView):
    """パスワード変更しました"""
    template_name = 'papps/password_change_done.html'

    def get(self, request, **kwargs):
        logout(request)
        return super().get(request, **kwargs)


class PasswordReset(PasswordResetView):
    """パスワード変更用URLの送付ページ"""
    subject_template_name = 'papps/mail_template/password_reset/subject.txt'
    email_template_name = 'papps/mail_template/password_reset/message.txt'
    template_name = 'papps/password_reset_form.html'
    form_class = MyPasswordResetForm
    success_url = reverse_lazy('papps:basepasswordresetdone')


class PasswordResetDone(PasswordResetDoneView):
    """パスワード変更用URLを送りましたページ"""
    template_name = 'papps/password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    """新パスワード入力ページ"""
    form_class = MySetPasswordForm
    success_url = reverse_lazy('papps:basepasswordresetcomplete')
    template_name = 'papps/password_reset_confirm.html'


class PasswordResetComplete(PasswordResetCompleteView):
    """新パスワード設定しましたページ"""
    template_name = 'papps/password_reset_complete.html'


class BaseIndex(generic.TemplateView):
    template_name = 'papps/index.html'

class BaseAi(generic.TemplateView):
    template_name = 'papps/ai.html'

class BaseCan(generic.TemplateView):
    template_name = 'papps/can.html'

class BaseChild(generic.TemplateView):
    template_name = 'papps/child.html'

class BaseDetail(generic.TemplateView):
    template_name = 'papps/detail.html'

class BaseEasy(generic.TemplateView):
    template_name = 'papps/easy.html'

class BaseFull(generic.TemplateView):
    template_name = 'papps/full.html'

''' 再オーダー '''
class BaseReFull(OnlyYouMixin, generic.TemplateView):
    template_name = 'papps/refull.html'

class BaseReOrderDone(generic.TemplateView):
    template_name = 'papps/reorder_done.html'

class BasePayOrderChangeDone(generic.TemplateView):
    template_name = 'papps/payorder_done.html'

class BaseGreen(generic.TemplateView):
    template_name = 'papps/green.html'

class BaseHomeTown(generic.TemplateView):
    template_name = 'papps/hometown.html'

class BaseMedical(generic.TemplateView):
    template_name = 'papps/medical.html'

class BaseOsoro(generic.TemplateView):
    template_name = 'papps/osoro.html'

class BasePets(generic.TemplateView):
    template_name = 'papps/pets.html'

class BasePv(generic.TemplateView):
    template_name = 'papps/pv.html'

''' ディレクトリai '''
class BaseAiAi1(generic.TemplateView):
    template_name = 'papps/ai/ai1.html'

class BaseAiAim1(generic.TemplateView):
    template_name = 'papps/ai/aim1.html'

class BaseAiAiw1(generic.TemplateView):
    template_name = 'papps/ai/aiw1.html'


''' ディレクトリ1 '''
class BaseAi1Aim1(generic.TemplateView):
    template_name = 'papps/ai/1/aim1.html'

class BaseAi1Aim1d(generic.TemplateView):
    template_name = 'papps/ai/1/aim1d.html'

class BaseAi1Aim1m(generic.TemplateView):
    template_name = 'papps/ai/1/aim1m.html'

class BaseAi1Aim1m1(generic.TemplateView):
    template_name = 'papps/ai/1/aim1m1.html'

class BaseAi1Aiw1(generic.TemplateView):
    template_name = 'papps/ai/1/aiw1.html'

class BaseAi1Aiw1d(generic.TemplateView):
    template_name = 'papps/ai/1/aiw1d.html'

class BaseAi1Aiw1m(generic.TemplateView):
    template_name = 'papps/ai/1/aiw1m.html'

class BaseAi1Aiw1m1(generic.TemplateView):
    template_name = 'papps/ai/1/aiw1m1.html'

class BaseAi11Aim1(generic.TemplateView):
    template_name = 'papps/ai/1/1/aim1.html'

class BaseAi11Aim1n(generic.TemplateView):
    template_name = 'papps/ai/1/1/aim1n.html'

class BaseAi11Aim1s(generic.TemplateView):
    template_name = 'papps/ai/1/1/aim1s.html'

class BaseAi11Aiw1(generic.TemplateView):
    template_name = 'papps/ai/1/1/aiw1.html'

class BaseAi11Aiw1n(generic.TemplateView):
    template_name = 'papps/ai/1/1/aiw1n.html'

class BaseAi11Aiw1s(generic.TemplateView):
    template_name = 'papps/ai/1/1/aiw1s.html'

''' ディレクトリ2 '''
class BaseAi2Ai1(generic.TemplateView):
    template_name = 'papps/ai/2/ai1.html'

class BaseAi2Ai2(generic.TemplateView):
    template_name = 'papps/ai/2/ai2.html'

class BaseAi2Ai3(generic.TemplateView):
    template_name = 'papps/ai/2/ai3.html'

class BaseAi2Ai4(generic.TemplateView):
    template_name = 'papps/ai/2/ai4.html'

class BaseAi2Ai5(generic.TemplateView):
    template_name = 'papps/ai/2/ai5.html'

class BaseAi2Aiw1(generic.TemplateView):
    template_name = 'papps/ai/2/aiw1.html'

class BaseAi2Aiw2(generic.TemplateView):
    template_name = 'papps/ai/2/aiw2.html'

class BaseAi2Aiw3(generic.TemplateView):
    template_name = 'papps/ai/2/aiw3.html'

''' ディレクトリ19 '''
class BaseAi19Aim1_1(generic.TemplateView):
    template_name = 'papps/ai/19/aim1_1.html'

class BaseAi19Aim1(generic.TemplateView):
    template_name = 'papps/ai/19/aim1.html'

class BaseAi19Aiw1_1(generic.TemplateView):
    template_name = 'papps/ai/19/aiw1_1.html'

class BaseAi19Aiw1(generic.TemplateView):
    template_name = 'papps/ai/19/aiw1.html'

''' ディレクトリ19 / 1 '''
class BaseAi191Aim1(generic.TemplateView):
    template_name = 'papps/ai/19/1/aim1.html'

class BaseAi191Aim1d(generic.TemplateView):
    template_name = 'papps/ai/19/1/aim1d.html'

class BaseAi191Aim1m(generic.TemplateView):
    template_name = 'papps/ai/19/1/aim1m.html'

class BaseAi191Aim1m1(generic.TemplateView):
    template_name = 'papps/ai/19/1/aim1m1.html'

class BaseAi191Aiw1(generic.TemplateView):
    template_name = 'papps/ai/19/1/aiw1.html'

class BaseAi191Aiw1d(generic.TemplateView):
    template_name = 'papps/ai/19/1/aiw1d.html'

class BaseAi191Aiw1m(generic.TemplateView):
    template_name = 'papps/ai/19/1/aiw1m.html'

class BaseAi191Aiw1m1(generic.TemplateView):
    template_name = 'papps/ai/19/1/aiw1m1.html'

''' ディレクトリ19 / 1 / 1 '''
class BaseAi1911Aim1(generic.TemplateView):
    template_name = 'papps/ai/19/1/1/aim1.html'

class BaseAi1911Aim1n(generic.TemplateView):
    template_name = 'papps/ai/19/1/1/aim1n.html'

class BaseAi1911Aiw1(generic.TemplateView):
    template_name = 'papps/ai/19/1/1/aiw1.html'

class BaseAi1911Aiw1n(generic.TemplateView):
    template_name = 'papps/ai/19/1/1/aiw1n.html'

''' ディレクトリ20 '''
class BaseAi20Aim1(generic.TemplateView):
    template_name = 'papps/ai/20/aim1.html'

''' ディレクトリ50 '''
class BaseAi50Aim1(generic.TemplateView):
    template_name = 'papps/ai/50/aim1.html'

class BaseAi50Aiw1(generic.TemplateView):
    template_name = 'papps/ai/50/aiw1.html'

''' ディレクトリaianser '''
class BaseAiAianserAcne(generic.TemplateView):
    template_name = 'papps/ai/aianser/acne.html'

class BaseAiAianserAianser1(generic.TemplateView):
    template_name = 'papps/ai/aianser/aianser1.html'

class BaseAiAianserComplete(generic.TemplateView):
    template_name = 'papps/ai/aianser/complete.html'

class BaseAiAianserDha(generic.TemplateView):
    template_name = 'papps/ai/aianser/dha.html'

class BaseAiAianserDiet(generic.TemplateView):
    template_name = 'papps/ai/aianser/diet.html'

class BaseAiAianserEye(generic.TemplateView):
    template_name = 'papps/ai/aianser/eye.html'

class BaseAiAianserHair(generic.TemplateView):
    template_name = 'papps/ai/aianser/hair.html'

class BaseAiAianserIntestines(generic.TemplateView):
    template_name = 'papps/ai/aianser/intestines.html'

class BaseAiAianserJoint(generic.TemplateView):
    template_name = 'papps/ai/aianser/joint.html'

class BaseAiAianserMuscle(generic.TemplateView):
    template_name = 'papps/ai/aianser/muscle.html'

class BaseAiAianserNight(generic.TemplateView):
    template_name = 'papps/ai/aianser/night.html'

class BaseAiAianserOutside(generic.TemplateView):
    template_name = 'papps/ai/aianser/outside.html'

class BaseAiAianserRhythm(generic.TemplateView):
    template_name = 'papps/ai/aianser/rhythm.html'

class BaseAiAianserSake(generic.TemplateView):
    template_name = 'papps/ai/aianser/sake.html'

class BaseAiAianserSkin(generic.TemplateView):
    template_name = 'papps/ai/aianser/skin.html'

class BaseAiAianserSleep(generic.TemplateView):
    template_name = 'papps/ai/aianser/sleep.html'

class BaseAiAianserStress(generic.TemplateView):
    template_name = 'papps/ai/aianser/stress.html'

''' ディレクトリorder '''
class BaseOrderEasyOrderAcne(generic.TemplateView):
    template_name = 'papps/order/easyorder/acne.html'

class BaseOrderEasyOrderComplete(generic.TemplateView):
    template_name = 'papps/order/easyorder/complete.html'

class BaseOrderEasyOrderDha(generic.TemplateView):
    template_name = 'papps/order/easyorder/dha.html'

class BaseOrderEasyOrderDiet(generic.TemplateView):
    template_name = 'papps/order/easyorder/diet.html'

class BaseOrderEasyOrderEye(generic.TemplateView):
    template_name = 'papps/order/easyorder/eye.html'

class BaseOrderEasyOrderHair(generic.TemplateView):
    template_name = 'papps/order/easyorder/hair.html'

class BaseOrderEasyOrderIntestines(generic.TemplateView):
    template_name = 'papps/order/easyorder/intestines.html'

class BaseOrderEasyOrderJoint(generic.TemplateView):
    template_name = 'papps/order/easyorder/joint.html'

class BaseOrderEasyOrderMuscle(generic.TemplateView):
    template_name = 'papps/order/easyorder/muscle.html'

class BaseOrderEasyOrderNight(generic.TemplateView):
    template_name = 'papps/order/easyorder/night.html'

class BaseOrderEasyOrderOutside(generic.TemplateView):
    template_name = 'papps/order/easyorder/outside.html'

class BaseOrderEasyOrderRhythm(generic.TemplateView):
    template_name = 'papps/order/easyorder/rhythm.html'

class BaseOrderEasyOrderSkin(generic.TemplateView):
    template_name = 'papps/order/easyorder/skin.html'

class BaseOrderEasyOrderSleep(generic.TemplateView):
    template_name = 'papps/order/easyorder/sleep.html'

class BaseOrderEasyOrderStress(generic.TemplateView):
    template_name = 'papps/order/easyorder/stress.html'


























