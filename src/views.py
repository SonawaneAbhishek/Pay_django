from django.shortcuts import render
import razorpay
from . models import Coffee
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def home(request):
    if request.method == 'POST':
        name=request.POST['name']
        amount=int(request.POST['amount'])*100   #bcoz razorpay 5000 ko 50 samajta ahe 4500 ko 45

        client = razorpay.Client(auth=("rzp_test_Ttklpm6wJm1RYx", "mRqy3h6aUYNGSpNDnp9xDAt2"))
        #to genrate payment id    
        payment = client.order.create({'amount': amount, 'currency': 'INR','payment_capture': '1'}) #payment capture is automatic kartpy ki manually kartoy te asta pan apan auto kartoy mahnun  1 detoy

        coffee =Coffee(name=name,amount=amount,payment_id=payment['id'])
        coffee.save()
        return render(request,'src/index.html',{'payment':payment})  

    return render(request,'src/index.html')

@csrf_exempt
def success(request):
    
    if request.method == 'POST':
        a=request.POST
        order_id=""
        for key ,val in a.items():
            if key == 'razorpay_order_id':
                order_id = val
                break
        
        user = Coffee.objects.filter(payment_id=order_id).first()
        user.paid = True
        user.save()
    return render(request , 'src/success.html')