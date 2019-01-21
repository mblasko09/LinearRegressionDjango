from django.http import HttpResponse
from django.shortcuts import render
from matplotlib import figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
import io, csv
import matplotlib.pyplot as plt
import numpy as np

def upload_csv(request):
    data = {}
    x_y_values = []
    val = ""
    if "GET" == request.method:
        return render(request, "plane/upload_csv.html", data)
    elif request.POST and request.FILES:
        # gets uploaded csv and parses data
        csvfile = request.FILES['csv_file'].read().decode('utf-8-sig')
        for el in csvfile:
            if el != ',' and el != '\r':
                val += el
            else:
                x_y_values.append(val)
                val = ""
        x_y_values.append(val)
        # first half of list (of coordinates) are x values, second are y values
        mid = int(len(x_y_values)/2)
        x = np.array(list(map(float, x_y_values[:mid])))
        y = np.array(list(map(float, x_y_values[mid:])))

        # number of points
        n = np.size(x)
        # x, y vec means
        m_x, m_y = np.mean(x), np.mean(y)
        # cross deviation/deviation for x
        SS_xy = np.sum(y*x) - n*m_y*m_x
        SS_xx = np.sum(x*x) - n*m_x*m_x
        # regression coefficients
        b_1 = SS_xy / SS_xx
        b_0 = m_y - b_1*m_x
        b = [b_0, b_1]
        # predicted vector
        y_pred = b[0] + b[1]*x

        plt.plot(x, y_pred, color='b')
        plt.plot(x, y, 'bo')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.xlim(min(x)-.5*min(x), max(x)+.5*max(x))
        plt.ylim(min(y)-.5*min(x), max(y)+.5*max(y))
        f = figure.Figure()
        FigureCanvasAgg(f)
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close(f)
        response = HttpResponse(buf.getvalue(), content_type='image/png')
        return response
