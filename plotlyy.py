import plotly.tools as to
import plotly.graph_objs as go
from plotly.offline import plot
from random import randint
from collections import OrderedDict
from plotly import tools
import re
from screeninfo import get_monitors


class Plot:
    def __init__(self):
        self.first = []
        self.second = []
        self.third = []
        self.fourth = []
        self.total_elements = 10
        self.total_values = 8
        self.iterations = range(5, 5 * self.total_values + 1, 5)
        self.layout = None
        self.subplots_title = []
        self.memory_dict = OrderedDict()
        self.show_legend = False
        self.offset = 80

    @staticmethod
    def set_credentials_file():
        to.set_credentials_file(username='karandeep7', api_key='EUSyFaGFeFaiAmxcqVf0')

    def generate_random_data(self):
        for i in range(self.total_values):
            self.first.append(randint(5000, 20000))
            self.second.append(randint(25000, 35000))
            self.third.append(randint(2000, 7000))
            self.fourth.append(randint(45000, 60000))

        self.memory_dict = OrderedDict(
            {'Native Alloc': self.first,
             'Native Heap': self.second,
             'Dalvik Alloc': self.third,
             'Dalvik Heap': self.fourth
             })

    def get_trace(self, memory_name, memory_data):
        trace = go.Scatter(
            x=self.iterations,
            y=memory_data,
            name=memory_name,
        )
        return trace

    @staticmethod
    def get_screen_resolution():
        default_resolution = [1366, 768]
        resolution = None
        for m in get_monitors():
            resolution = str(m)
            break
        if resolution:
            return re.findall(r'.*\((\d+)x(\d+).*', resolution)[0]
        else:
            return default_resolution

    def get_all_traces(self):
        all_traces = []
        for i in range(self.total_elements):
            for memory_name, memory_data in self.memory_dict.items():
                all_traces.append(self.get_trace(memory_name, memory_data))
            self.subplots_title.append('Memory Variation {}'.format(i + 1))

        fig = tools.make_subplots(rows=self.total_elements, cols=1, subplot_titles=self.subplots_title)
        for annotation in fig.layout.annotations:
            annotation.font['size'] = 20

        trace_row = 1
        for trace_index, trace in enumerate(all_traces):
            fig.append_trace(trace, trace_row, 1)
            if ((trace_index + 1) % 4) == 0:
                fig['layout']['xaxis{}'.format(trace_row)].update(title='Iterations')
                fig['layout']['yaxis{}'.format(trace_row)].update(title='Memory Consumption (KB)')
                trace_row += 1

        width, height = map(int, Plot.get_screen_resolution())
        if self.show_legend:
            fig['layout'].update(width=width - self.offset, height=height * self.total_elements, title='Memory Report',
                                 showlegend=self.show_legend)
        else:
            fig['layout'].update(width=width, height=height * self.total_elements, title='Memory Report',
                                 showlegend=self.show_legend)

        fig['layout']['title']['font']['size'] = 28

        plot(fig, filename='memory_dump.html', auto_open=True)


def main():
    p = Plot()
    p.generate_random_data()
    p.get_all_traces()


if __name__ == '__main__':
    main()
