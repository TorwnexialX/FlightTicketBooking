from django.db import models

'''
models之间关系示意：
Flight 1 --- * Ticket
1 Customer --- * Ticket
确保每个座位都唯一对应一个客户，防止两个客户买到同一个座位，同时便于管理和查询航班、座位和客户的信息。
'''


class Flight(models.Model):
    flight_number = models.CharField(max_length=20, unique=True)  # 航班号
    plane_number = models.CharField(max_length=20)  # 飞机型号
    departure = models.CharField(max_length=100)  # 出发地
    arrival = models.CharField(max_length=100)  # 目的地
    depart_time = models.DateTimeField() # 出发时间
    arrive_time = models.DateTimeField() # 到达时间
    total_seats = models.IntegerField()  # 总座位数
    booked_seats = models.IntegerField(default=0)  # 订票数

    @property
    def available_seats(self):
        # 计算余票数
        return self.total_seats - self.booked_seats

    def __str__(self):
        return f"{self.flight_number}"

class Ticket(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='seats')  # 航班号
    seat_number = models.CharField(max_length=4)  # 座位号
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='tickets', null=True)  # 客户
    # 由于 Customer 模型定义在 Ticket 模型之后，所以用字符串 'Customer' 来引用目标模型。
    # 一个ForeignKey字段可以是非空的，而另一个却不能是非空的

    class Meta:
        unique_together = ('flight', 'seat_number')

    def __str__(self):
        return f"{self.flight.flight_number} - Seat {self.seat_number}"

class Customer(models.Model):
    name = models.CharField(max_length=100)  # 客户姓名
    id_number = models.CharField(max_length=20, unique=True)  # 身份证号

    def __str__(self):
        return f"{self.name} - {self.id_number}"