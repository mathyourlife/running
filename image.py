from io import BytesIO
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg

fig = Figure(figsize=[4,4])
ax = fig.add_axes([.1,.1,.8,.8])
ax.scatter([1,2], [3,4])
canvas = FigureCanvasAgg(fig)

# write image data to a string buffer and get the PNG image bytes
buf = BytesIO()
canvas.print_png(buf)
data = buf.getvalue()

# pseudo-code for generating the http response from your
# webserver, and writing the bytes back to the browser.
# replace this with corresponding code for your web framework
headers = {
    'Content-Type': 'image/png',
    'Content-Length': len(data)
}
response.write(200, 'OK', headers, data)
