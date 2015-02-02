import tornado.httpserver
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application, url

import numpy as np
from io import BytesIO
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg

def ts_hist(x, y, title=None, xlabel=None, ylabel=None, bins=30, alpha=0.6, color='b'):
    fig = plt.figure(figsize=[12,6], facecolor='w')
    split = 0.1
    left = split + 0.05 + 0.01
    bottom = 0.05
    axScatter = plt.axes([left, 0.05, 1 - left - 0.01, 1 - bottom - 0.01])
    if title is not None:
        plt.title(title)
    axHisty = plt.axes([0.05, 0.05, split, 1 - bottom - 0.01])
    if xlabel is not None:
        axScatter.set_xlabel(xlabel)
    if ylabel is not None:
        axHisty.set_ylabel(ylabel)
    axScatter.yaxis.set_major_formatter(NullFormatter())
    axHisty.xaxis.set_major_formatter(NullFormatter())
    axScatter.plot(x, y, alpha=alpha, c=color)
    axScatter.grid()
    axScatter.set_xlim( (np.min(x), np.max(x)) )
    axScatter.set_ylim( (np.min(y), np.max(y)) )
    axHisty.hist(y, bins=bins, alpha=alpha, orientation='horizontal', color=color)
    lim = axHisty.get_xlim()
    axHisty.set_xlim((lim[1], lim[0]))
    axHisty.grid()
    axHisty.set_ylim( axScatter.get_ylim() )
    return fig

class MainHandler(RequestHandler):
    def get(self):
        self.write("""<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>html demo</title>
    <style>
        p {
            margin: 8px;
            font-size: 20px;
            color: blue;
            cursor: pointer;
        }
        b {
            text-decoration: underline;
        }
            button {
            cursor: pointer;
        }
    </style>
    <script src="//code.jquery.com/jquery-1.10.2.js"></script>
</head>
<body>
    <p class="click">
        <b>Click</b> to change the <span id="tag">html</span>
    </p>
    <div id="content-container">
    </div>
    <p>
        This <button name="nada">button</button> does nothing.
    </p>
    <script>
        $('.click').click(function() {

            // replace the contents of the div with the link text
            $('#content-container').html("");
            $('#content-container').html("<img src='ts-hist/this.png'>");

            // cancel the default action of the link by returning false
            return false;
        });
    </script>
</body>
</html>""")

class TSHistHandler(RequestHandler):
    def get(self, filename):
        N = 1000

        x = np.arange(N)
        fig = ts_hist(x, np.sin(x / 50) + 0.1 * np.random.randn(N))

        canvas = FigureCanvasAgg(fig)

        buf = BytesIO()
        canvas.print_png(buf)
        data = buf.getvalue()
        self.set_header("Content-type",  "image/png")
        self.set_header("Content-Length",  len(data))
        self.write(data)

def make_app():
    return Application([
        url(r"/", MainHandler),
        url(r"/ts-hist/(?P<filename>.+\.png)", TSHistHandler),
    ])

def main():
    app = make_app()
    server = tornado.httpserver.HTTPServer(app)
    server.bind(8880)
    server.start(0)  # forks one process per cpu
    IOLoop.current().start()

if __name__ == '__main__':
    main()