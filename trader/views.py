# from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from gcapp.forms import *
from django.http import HttpResponse
from gcapp.models import *
from django.utils.timezone import datetime
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from goconnekt import settings

from django.views.decorators.csrf import csrf_exempt

# to round decimals
TWOPLACES = decimal.Decimal(10) ** -2


def get_default_context(request):
    context = {}

    my_user = MyUser.morph_user(request.user)
    context['my_user'] = my_user

    context['hotels'] = Hotel.objects.all()

    if request.GET.get('message') == "register_email_sent":
        context['message'] = "We sent you a confirmation email."

    elif request.GET.get('message') == 'activation_ok':
        context['message'] = "Your account has been activated. You're welcome to login."

    elif request.GET.get('message') == 'message_sent':
        context['message'] = "Your email has been sent!"

    elif request.GET.get('message') == 'reset_email_sent':
        context['message'] = "We sent you an email to confirm your password reset."

    context['hostname'] = settings.hostname

    return context

@csrf_exempt
def home(request):
    context = get_default_context(request)

    if request.method == 'POST':
        form = ContactForm(data=request.POST)
        if form.is_valid():
            send_mail("Urgent help request from Contact Us form " + form.cleaned_data['subject'],
                      "From %s (%s)\n%s" % (form.cleaned_data['name'], form.cleaned_data['email'], form.cleaned_data['message']),
                      "help@goconnekt.com",
                      ["merwan@telegraphtechnologies.com", "jeff@telegraphtechnologies.com"],
                      fail_silently=False)
            context = get_default_context(request)

        else:
            print 'not valid'
            print form.cleaned_data['subject'] ,form.cleaned_data['name'], form.cleaned_data['message']
            # just return the form with errors
            context['message'] = "Please enter a valid email address"

    return render(request, "gcapp/index.html", context)


def book_now(request):
    if not request.user.is_authenticated():
        return render(request, "gcapp/index.html", {'open_login': True})

    context = get_default_context(request)
    my_user = MyUser.morph_user(request.user)

    if request.POST:
        form = CustomerReservationForm(data=request.POST)
        payment_method = request.POST.get('payment_method')
        if form.is_valid() and form.cleaned_data['agree'] and payment_method:
            r = form.save(commit=False)
            r.user = my_user
            reserved_device = Device.get_available_devices(r.hotel, r.start_date, r.end_date)[0]
            r.device = reserved_device

            r.expected_cost = 0
            r.deposit_amount = r.calculate_deposit_amount()
            reservation.agree = True
            r.save()

            MyLog.log_from_request(r, "agreed", request)

            # add the coupon and use it to calculate the promised cost...
            coupon_code = form.cleaned_data['coupon_code']
            if coupon_code:
                coupon = Coupon.objects.filter(code=coupon_code).first()
                r.coupons.add(coupon)
            r.expected_cost = r.calculate_total_cost()
            r.save()

            # keep track of the reservation being booked so it can be aborted
            my_user.reservation_being_booked = r
            my_user.save()

            # from contract page
            payment = Payment.create_payment_for_method(r, payment_method)

            currency = 'USD'
            expected_cost = Decimal(r.expected_cost)
            deposit_amount = r.calculate_deposit_amount()
            redirect_url = request.build_absolute_uri(reverse('payment', kwargs={'payment_id':payment.id}))
            cancel_url = request.build_absolute_uri()
            notification_url = reverse('payment_callback', kwargs={'payment_id':payment.id})

            url = payment.make_invoice(expected_cost, deposit_amount, currency, redirect_url, cancel_url, notification_url)

            return redirect(url)

        else:
            print "there were some errors in the book now form"

    else:
        # i'd rather not abort, so they can hit forward. i'd rather just have expiration...
        # my_user.abort_current_reservation()
        if my_user.is_employed_anywhere():
            hotels_worked = my_user.hotels.all()
            form = CustomerReservationForm(hotel_queryset=hotels_worked)

        else:
            form = CustomerReservationForm()

    context['show_room_charge_payment'] = my_user.is_employed_anywhere()
    context['form'] = form
    return render(request, "gcapp/book_now.html", context)


# rename this to change_book_now_form
def availability(request):
    hotel = Hotel.objects.get(name=request.GET['hotel'])
    # tz_info = pytz.timezone(hotel.timezone_name)
    start_date = datetime.strptime(request.GET['start_date'], '%m/%d/%Y').date()
    end_date = datetime.strptime(request.GET['end_date'], '%m/%d/%Y').date()
    pricing_plan_id = request.GET.get('pricing_plan')
    coupon_code = request.GET.get('coupon_code')

    error = None
    msg_level = None
    device_available = False
    duration_days = None
    expected_cost_text = None
    deposit_amount_text = None

    tz_info = pytz.timezone(hotel.timezone_name)
    today_in_hotel_tz = tz_info.normalize(timezone.now()).date()

    if start_date < today_in_hotel_tz:
        error = 'You selected a pickup date before today!'
        msg_level = 'ERROR'

    elif end_date < start_date:
        error = 'Please ensure the drop-off date is after the pick-up date!'
        msg_level = 'ERROR'

    elif not pricing_plan_id:
        error = "Please choose a pricing plan to see if we have a device that fits."
        msg_level = 'ERROR'

    else:
        duration = (end_date - start_date + timezone.timedelta(days=1))
        duration_days = duration.days
        available_devices = Device.get_available_devices(hotel, start_date, end_date)
        device_available = len(available_devices) > 0

        pricing_plan = PricingPlan.objects.get(id=pricing_plan_id)
        expected_cost = pricing_plan.calculate_total_cost(duration)

        if coupon_code:
            coupon = Coupon.objects.filter(code=coupon_code).first()
            if not coupon:
                error = "That coupon code is invalid!"
                msg_level = 'ERROR'
            elif not coupon.is_valid(pricing_plan, duration):
                error = "Your reservation does not satisfy the requirements for the coupon!"
                msg_level = 'ERROR'
            else:
                error = coupon.name
                msg_level = 'INFO'
                expected_cost -= coupon.calculate_discount(pricing_plan, duration)
        expected_cost_text = '%s %s' % (expected_cost.quantize(TWOPLACES), 'USD')

        if not device_available:
            logging.warning("There were no devices available at hotel %s from %s to %s", hotel.name, str(start_date), str(end_date))
            error = "There's no device available for the selected dates. Please try other dates."
            msg_level = 'ERROR'
        else:
            deposit_amount = available_devices[0].loss_fee
            deposit_amount_text = '%s %s' % (deposit_amount.quantize(TWOPLACES), 'USD')

    data = {
        'error': error,
        'msg_level': msg_level,
        'device_available': device_available,
        'duration': duration_days,
        'expected_cost_text': expected_cost_text,
        'deposit_amount_text': deposit_amount_text,
    }

    return HttpResponse(json.dumps(data), content_type="application/json")


def payment_callback(request):
    print str(request.POST)


def payment(request, payment_id):
    # don't call this variable payment! the name of the method is payment
    p = get_object_or_404(Payment, id=payment_id)
    context = get_default_context(request)

    # needed, e.g., because paypal requires you to finalize a transaction with some args they send you...
    kwargs = dict(request.REQUEST)

    p.update_payment_status(**kwargs)
    p.reservation.send_confirmation_email()

    # activate the device
    time_period = p.reservation.get_time_period()
    print 'time period is:', time_period
    if time_period == 'current':
            comm_status = p.reservation.device.check_status()
            print 'comm status is:', comm_status
            if comm_status == 'suspend' or comm_status is None:
                print 'resuming...'
                p.reservation.device.resume()

    context['hotel'] = p.reservation.hotel
    context['reservation'] = p.reservation
    context['payment'] = p

    return render(request, "gcapp/payment.html", context)


def account(request):
    context = get_default_context(request)

    my_user = MyUser.morph_user(request.user)
    customer_reservations = Reservation.objects.filter(user=my_user).order_by('start_date')
    current_reservations = []
    upcoming_reservations = []
    previous_reservations = []
    for r in customer_reservations:
        if r.end_date < timezone.datetime.now().date():
            previous_reservations.append(r)
        elif r.start_date <= timezone.datetime.now().date() and r.end_date >= timezone.datetime.now().date():
            current_reservations.append(r)
        elif r.start_date > timezone.datetime.now().date():
            upcoming_reservations.append(r)

    context['current_reservations'] = current_reservations
    context['upcoming_reservations'] = upcoming_reservations
    context['previous_reservations'] = previous_reservations

    return render(request, "gcapp/account.html", context)


