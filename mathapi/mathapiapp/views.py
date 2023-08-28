from django.shortcuts import render
from django.http import JsonResponse
from .models import Operation

def index(request):
    endpoints = [
        '/',
        '/history',
        '/5/plus/3',
        '/3/minus/5',
        '/3/minus/5/plus/8',
        '/3/into/5/plus/8/into/6',
    ]
    return render(request, 'index.html', {'endpoints': endpoints})

def history(request):
    history_entries = Operation.objects.all().order_by('-id')[:20]
    history_data = [{'question': entry.question, 'answer': entry.answer} for entry in history_entries]
    return render(request, 'history.html', {'history': history_data})

def calculate(request, calculation):
    segments = calculation.split('/')
    
    if len(segments) < 3 or len(segments) % 2 != 1:
        response_data = {'error': 'Invalid input format'}
        return JsonResponse(response_data, status=400)

    result = float(segments[0])
    operation_str = str(result)

    for i in range(1, len(segments) - 1, 2):
        operator = segments[i]
        operand = float(segments[i + 1])

        if operator in ('plus', 'minus', 'into'):
            operation_str += f" {operator} {operand}"

            if operator == 'plus':
                result += operand
            elif operator == 'minus':
                result -= operand
            elif operator == 'into':
                result *= operand
        else:
            response_data = {'error': 'Invalid operator'}
            return JsonResponse(response_data, status=400)

    Operation.objects.create(question=operation_str, answer=result)

    response_data = {'question': operation_str, 'answer': result}
    return JsonResponse(response_data)
