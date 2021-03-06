from django.urls import path
from . import views

app_name = 'papps'

urlpatterns = [
    path('', views.BaseIndex.as_view(), name='baseindex'),
    path('ai', views.BaseAi.as_view(), name='baseai'),
    path('can', views.BaseCan.as_view(), name='basecan'),
    path('child', views.BaseChild.as_view(), name='basechild'),
    path('detail', views.BaseDetail.as_view(), name='basedetail'),
    path('easy', views.BaseEasy.as_view(), name='baseeasy'),
    path('full', views.BaseFull.as_view(), name='basefull'),
    path('refull/<int:pk>', views.BaseReFull.as_view(), name='baserefull'),
    path('reorderdone', views.BaseReOrderDone.as_view(), name='basereorderdone'),
    path('payorderchangedone', views.BasePayOrderChangeDone.as_view(), name='basepayorderchangedone'),
    path('green', views.BaseGreen.as_view(), name='basegreen'),
    path('hometown', views.BaseHomeTown.as_view(), name='basehometown'),
    path('medical', views.BaseMedical.as_view(), name='basemedical'),
    path('insertdata', views.BaseInsertData.as_view(), name='baseinsertdata'),
    path('payorder/<token>/', views.BasePayOrder.as_view(), name='basepayorder'),
    path('payorderchange/<int:pk>', views.BasePayOrderChange.as_view(), name='basepayorderchange'),
    path('superuserpage', views.BaseSuperUserPage.as_view(), name='basesuperuserpage'),
    path('searchid', views.BaseSearchId.as_view(), name='basesearchid'),
    path('normaluserinfo', views.BaseNormalUserInfo.as_view(), name='basenormaluserinfo'),
    path('mypage/<int:pk>', views.BaseMyPage.as_view(), name='basemypage'),
    path('mypageedit/<int:pk>', views.BaseMyPageEdit.as_view(), name='basemypageedit'),
    path('mypageedit/user/<int:pk>', views.BaseMyPageEditUser.as_view(), name='basemypageedituser'),
    path('mypageedit/order/<int:pk>', views.BaseMyPageEditOrder.as_view(), name='basemypageeditorder'),
    path('mypageedit/inputadddata/<int:pk>', views.BaseMyPageEditInputAddData.as_view(), name='basemypageeditinputadddata'),
    path('inputaddcreate', views.BaseInputAddCreate.as_view(), name='baseinputaddcreate'),
    path('inputadddelete/<int:pk>', views.BaseInputAddDelete.as_view(), name='baseinputadddelete'),
    path('login', views.Login.as_view(), name='baselogin'),
    path('logout', views.Logout.as_view(), name='baselogout'),
    path('password_change', views.PasswordChange.as_view(), name='basepasswordchange'),
    path('password_change/done', views.PasswordChangeDone.as_view(), name='basepasswordchangedone'),
    path('password_reset/', views.PasswordReset.as_view(), name='basepasswordreset'),
    path('password_reset/done/', views.PasswordResetDone.as_view(), name='basepasswordresetdone'),
    path('password_reset/confirm/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='basepasswordresetconfirm'),
    path('password_reset/complete/', views.PasswordResetComplete.as_view(), name='basepasswordresetcomplete'),
    path('order', views.BaseOrder.as_view(), name='baseorder'),
    path('reorder/<int:pk>', views.BaseReOrder.as_view(), name='basereorder'),
    path('order2', views.BaseOrder2.as_view(), name='baseorder2'),
    path('order3', views.BaseOrder3.as_view(), name='baseorder3'),
    path('osoro', views.BaseOsoro.as_view(), name='baseosoro'),
    path('pets', views.BasePets.as_view(), name='basepets'),
    path('pv', views.BasePv.as_view(), name='basepv'),
    path('ai/ai1', views.BaseAiAi1.as_view(), name='baseai1ai1'),
    path('ai/aim1', views.BaseAiAim1.as_view(), name='baseai1aim1'),
    path('ai/aiw1', views.BaseAiAiw1.as_view(), name='baseai1aiw1'),
    path('ai/1/aim1', views.BaseAi1Aim1.as_view(), name='baseai1aim1'),
    path('ai/1/aim1d', views.BaseAi1Aim1d.as_view(), name='baseai1aim1d'),
    path('ai/1/aim1m', views.BaseAi1Aim1m.as_view(), name='baseai1aim1m'),
    path('ai/1/aim1m1', views.BaseAi1Aim1m1.as_view(), name='baseai1aim1m1'),
    path('ai/1/aiw1', views.BaseAi1Aiw1.as_view(), name='baseai1aiw1'),
    path('ai/1/aiw1d', views.BaseAi1Aiw1d.as_view(), name='baseai1aiw1d'),
    path('ai/1/aiw1m', views.BaseAi1Aiw1m.as_view(), name='baseai1aiw1m'),
    path('ai/1/aiw1m1', views.BaseAi1Aiw1m1.as_view(), name='baseai1aiw1m1'),
    path('ai/1/1/aim1', views.BaseAi11Aim1.as_view(), name='baseai11aim1'),
    path('ai/1/1/aim1n', views.BaseAi11Aim1n.as_view(), name='baseai11aim1n'),
    path('ai/1/1/aim1s', views.BaseAi11Aim1s.as_view(), name='baseai11aim1s'),
    path('ai/1/1/aiw1', views.BaseAi11Aiw1.as_view(), name='baseai11aiw1'),
    path('ai/1/1/aiw1n', views.BaseAi11Aiw1n.as_view(), name='baseai11aiw1n'),
    path('ai/1/1/aiw1s', views.BaseAi11Aiw1s.as_view(), name='baseai11aiw1s'),
    path('ai/2/ai1', views.BaseAi2Ai1.as_view(), name='baseai2ai1'),
    path('ai/2/ai2', views.BaseAi2Ai2.as_view(), name='baseai2ai2'),
    path('ai/2/ai3', views.BaseAi2Ai3.as_view(), name='baseai2ai3'),
    path('ai/2/ai4', views.BaseAi2Ai4.as_view(), name='baseai2ai4'),
    path('ai/2/ai5', views.BaseAi2Ai5.as_view(), name='baseai2ai5'),
    path('ai/2/aiw1', views.BaseAi2Aiw1.as_view(), name='baseai2aiw1'),
    path('ai/2/aiw2', views.BaseAi2Aiw2.as_view(), name='baseai2aiw2'),
    path('ai/2/aiw3', views.BaseAi2Aiw3.as_view(), name='baseai2aiw3'),
    path('ai/19/aim1_1', views.BaseAi19Aim1_1.as_view(), name='baseai19aim1_1'),
    path('ai/19/aim1', views.BaseAi19Aim1.as_view(), name='baseai19aim1'),
    path('ai/19/aiw1_1', views.BaseAi19Aiw1_1.as_view(), name='baseai19aiw1_1'),
    path('ai/19/aiw1', views.BaseAi19Aiw1.as_view(), name='baseai19aiw1'),
    path('ai/19/1/aim1', views.BaseAi191Aim1.as_view(), name='baseai191aim1'),
    path('ai/19/1/aim1d', views.BaseAi191Aim1d.as_view(), name='baseai191aim1d'),
    path('ai/19/1/aim1m', views.BaseAi191Aim1m.as_view(), name='baseai191aim1m'),
    path('ai/19/1/aim1m1', views.BaseAi191Aim1m1.as_view(), name='baseai191aim1m1'),
    path('ai/19/1/aiw1', views.BaseAi191Aiw1.as_view(), name='baseai191aiw1'),
    path('ai/19/1/aiw1d', views.BaseAi191Aiw1d.as_view(), name='baseai191aiw1d'),
    path('ai/19/1/aiw1m', views.BaseAi191Aiw1m.as_view(), name='baseai191aiw1m'),
    path('ai/19/1/aiw1m1', views.BaseAi191Aiw1m1.as_view(), name='baseai191aiw1m1'),
    path('ai/19/1/1/aim1', views.BaseAi1911Aim1.as_view(), name='baseai1911aim1'),
    path('ai/19/1/1/aim1n', views.BaseAi1911Aim1n.as_view(), name='baseai1911aim1n'),
    path('ai/19/1/1/aiw1', views.BaseAi1911Aiw1.as_view(), name='baseai1911aiw1'),
    path('ai/19/1/1/aiw1n', views.BaseAi1911Aiw1n.as_view(), name='baseai1911aiw1n'),
    path('ai/20/aim1', views.BaseAi20Aim1.as_view(), name='baseai20aim1'),
    path('ai/50/aim1', views.BaseAi50Aim1.as_view(), name='baseai50aim1'),
    path('ai/50/aiw1', views.BaseAi50Aiw1.as_view(), name='baseai50aiw1'),
    path('ai/ai/ai_order', views.BaseAiAiAiOrder.as_view(), name='baseaiaiai_order'),
    path('ai/aianser/acne', views.BaseAiAianserAcne.as_view(), name='baseaiaianseracne'),
    path('ai/aianser/aianser1', views.BaseAiAianserAianser1.as_view(), name='baseaiaianseraianser1'),
    path('ai/aianser/complete', views.BaseAiAianserComplete.as_view(), name='baseaiaiansercomplete'),
    path('ai/aianser/dha', views.BaseAiAianserDha.as_view(), name='baseaiaianserdha'),
    path('ai/aianser/diet', views.BaseAiAianserDiet.as_view(), name='baseaiaianserdiet'),
    path('ai/aianser/eye', views.BaseAiAianserEye.as_view(), name='baseaiaiansereye'),
    path('ai/aianser/hair', views.BaseAiAianserHair.as_view(), name='baseaiaianserhair'),
    path('ai/aianser/intestines', views.BaseAiAianserIntestines.as_view(), name='baseaiaianserintestines'),
    path('ai/aianser/joint', views.BaseAiAianserJoint.as_view(), name='baseaiaianserjoint'),
    path('ai/aianser/muscle', views.BaseAiAianserMuscle.as_view(), name='baseaiaiansermuscle'),
    path('ai/aianser/night', views.BaseAiAianserNight.as_view(), name='baseaiaiansernight'),
    path('ai/aianser/outside', views.BaseAiAianserOutside.as_view(), name='baseaiaianseroutside'),
    path('ai/aianser/rhythm', views.BaseAiAianserRhythm.as_view(), name='baseaiaianserrhythm'),
    path('ai/aianser/sake', views.BaseAiAianserSake.as_view(), name='baseaiaiansersake'),
    path('ai/aianser/skin', views.BaseAiAianserSkin.as_view(), name='baseaiaianserskin'),
    path('ai/aianser/sleep', views.BaseAiAianserSleep.as_view(), name='baseaiaiansersleep'),
    path('ai/aianser/stress', views.BaseAiAianserStress.as_view(), name='baseaiaianserstress'),
    path('order/easyorder/easy_order', views.BaseOrderEasyOrderEasyOrder.as_view(), name='baseordereasyordereasy_order'),
    path('order/easyorder/acne', views.BaseOrderEasyOrderAcne.as_view(), name='baseordereasyorderacne'),
    path('order/easyorder/complete', views.BaseOrderEasyOrderComplete.as_view(), name='baseordereasyordercomplete'),
    path('order/easyorder/dha', views.BaseOrderEasyOrderDha.as_view(), name='baseordereasyorderdha'),
    path('order/easyorder/diet', views.BaseOrderEasyOrderDiet.as_view(), name='baseordereasyorderdiet'),
    path('order/easyorder/eye', views.BaseOrderEasyOrderEye.as_view(), name='baseordereasyordereye'),
    path('order/easyorder/hair', views.BaseOrderEasyOrderHair.as_view(), name='baseordereasyorderhair'),
    path('order/easyorder/intestines', views.BaseOrderEasyOrderIntestines.as_view(), name='baseordereasyorderintestines'),
    path('order/easyorder/joint', views.BaseOrderEasyOrderJoint.as_view(), name='baseordereasyorderjoint'),
    path('order/easyorder/muscle', views.BaseOrderEasyOrderMuscle.as_view(), name='baseordereasyordermuscle'),
    path('order/easyorder/night', views.BaseOrderEasyOrderNight.as_view(), name='baseordereasyordernight'),
    path('order/easyorder/outside', views.BaseOrderEasyOrderOutside.as_view(), name='baseordereasyorderoutside'),
    path('order/easyorder/rhythm', views.BaseOrderEasyOrderRhythm.as_view(), name='baseordereasyorderrhythm'),
    path('order/easyorder/skin', views.BaseOrderEasyOrderSkin.as_view(), name='baseordereasyorderskin'),
    path('order/easyorder/sleep', views.BaseOrderEasyOrderSleep.as_view(), name='baseordereasyordersleep'),
    path('order/easyorder/stress', views.BaseOrderEasyOrderStress.as_view(), name='baseordereasyorderstress'),
]
