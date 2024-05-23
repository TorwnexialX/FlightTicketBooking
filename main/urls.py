from django.urls import path
from .views import flight_create, flight_edit, book_ticket, cancel_ticket, delete_flight, flight_list, customer_list

urlpatterns = [
    path('', flight_list),  
    path('flights/', flight_list, name='flight-list'),                            # 显示全部航班信息
    path('flights/new/', flight_create, name='flight-create'),                    # 创建新的航班
    path('flights/edit/<int:pk>/', flight_edit, name='flight-edit'),              # 修改航班信息
    path('flights/<int:flight_id>/delete/', delete_flight, name='delete-flight'), # 删除航班信息
    path('customers/', customer_list, name='customer-list'),                      # 显示全部客户信息
    path('book_ticket/', book_ticket, name='book-ticket'),                        # 订票业务
    path('cancel_ticket/', cancel_ticket, name='cancel-ticket'),                  # 退票业务
]
