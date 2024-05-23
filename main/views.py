# 所用模型及表单
from .models import Flight, Ticket, Customer
from .forms import FlightForm, FlightEdit
# 路由、渲染、检错所需方法
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.db import IntegrityError
from django.http import JsonResponse

# 录入航班信息
def flight_create(request):
    if request.method == 'POST':
        flight_number = request.POST.get('flight_number')
        if Flight.objects.filter(flight_number=flight_number).exists():
            return JsonResponse({'success': False, 'error': '该航班信息已录入'})
        form = FlightForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
    else:
        form = FlightForm()
    return render(request, 'flight_form.html', {'form': form})

# 航班信息更新
def flight_edit(request, pk):
    flight = get_object_or_404(Flight, pk=pk)
    if request.method == 'POST':
        form = FlightEdit(request.POST, instance=flight)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('flight-list'))
    else:
        form = FlightEdit(instance=flight)
    return render(request, 'flight_edit.html', {'form': form})
    
# 删除航班
def delete_flight(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    if request.method == 'POST':
        flight.delete()
        for customer in Customer.objects.all():
            # Customer数据更新：检查客户是否还有其他票，如果没有则删除客户
            if not customer.tickets.exists():
                customer.delete()
        return redirect('flight-list')
    return render(request, 'flight_list.html', {'flights': Flight.objects.all()})

# 订票
def book_ticket(request):
    if request.method == 'POST':
        name          = request.POST.get('name')
        id_number     = request.POST.get('id_number')
        flight_number = request.POST.get('flight_number')
        seat_number   = request.POST.get('seat_number')
        
        try:
            flight = Flight.objects.get(flight_number=flight_number)
            if flight.available_seats > 0:
                customer, created = Customer.objects.get_or_create(name=name, id_number=id_number)
                
                # 检查座位号是否合法
                int_seat_number = int(seat_number)
                if int_seat_number < 1 or int_seat_number > flight.total_seats:
                    return JsonResponse({'success': False, 'error': '座位号不在容量范围内'})

                # 检查客户是否已经在该航班上有票
                if Ticket.objects.filter(flight=flight, customer=customer).exists():
                    return JsonResponse({'success': False, 'error': '乘客已预订过该航班'})
                
                # 检查座位是否已经被预订
                if Ticket.objects.filter(flight=flight, seat_number=seat_number).exists():
                    return JsonResponse({'success': False, 'error': '该座位已被预定'})
                
                # 创建该客户对应的票，并更改航班数据信息
                ticket = Ticket.objects.create(flight=flight, customer=customer, seat_number=seat_number)
                flight.booked_seats += 1
                flight.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': '该航班已满员'})
        except Flight.DoesNotExist:
            return JsonResponse({'success': False, 'error': '该航班不存在'})
        except ValueError:
            return JsonResponse({'success': False, 'error': '座号必须是一个数字'})
        except IntegrityError:
            return JsonResponse({'success': False, 'error': '有与该乘客身份证号相同的乘客存在，请检查乘客信息'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return render(request, 'book_ticket.html')

# 退票业务
def cancel_ticket(request):
    if request.method == 'POST':
        name          = request.POST.get('name')
        id_number     = request.POST.get('id_number')
        flight_number = request.POST.get('flight_number')
        
        try:
            # 获取客户和航班及其对应的票
            customer = Customer.objects.get(name=name, id_number=id_number)
            flight   = Flight.objects.get(flight_number=flight_number)
            ticket   = Ticket.objects.get(flight=flight, customer=customer)
            
            # Flight数据更新：获取航班并更新订票数
            flight.booked_seats -= 1
            flight.save()
            
            # Ticket数据更新：删除票
            ticket.delete()

            # Customer数据更新：检查客户是否还有其他票，如果没有则删除客户
            if not customer.tickets.exists():
                customer.delete()
            
            return JsonResponse({'success': True})
        except Customer.DoesNotExist:
            return JsonResponse({'success': False, 'error': '该乘客不存在'})
        except Flight.DoesNotExist:
            return JsonResponse({'success': False, 'error': '该航班不存在'})
        except Ticket.DoesNotExist:
            return JsonResponse({'success': False, 'error': '该乘客未预定此航班'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return render(request, 'cancel_ticket.html')


# 输出全部航班信息
def flight_list(request):
    flights = Flight.objects.all()
    return render(request, 'flight_list.html', {'flights': flights})

# 输出全部客户信息
def customer_list(request):
    customers = Customer.objects.prefetch_related('tickets__flight').all()
    for customer in customers:
        if not customer.tickets.exists():
                customer.delete()
    return render(request, 'customer_list.html', {'customers': customers})