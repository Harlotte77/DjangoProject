from django.shortcuts import render


def data_statistics(request):
    """数据统计"""
    return render(request, "data_statistics.html")

def data_bar(request):
    """构造柱状图数据"""
