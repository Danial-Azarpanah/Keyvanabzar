import ghasedakpack

sms = ghasedakpack.Ghasedak("c24ff1b633a6e59dfdb9a5229be300bf1a122ca2fdf17ee3083a346b3d8864e6")
sms.verification({'receptor': '09149055726', 'type': '1', 'template': 'otpcode', 'param1': '1234'})