import numpy as np
from matplotlib import pyplot
from .report import Report, Timing

def Time(name, which='Mean'):
    if which == 'Nonlocal':
        def getter(run):
            t = run.Timings[name]
            sum = t.Mean * run.Cores
            nlSum = sum - t.Local
            return nlSum / (run.Cores - 1) / run.Steps
    else:
        getter = lambda run: getattr(run.Timings[name], which) / run.Steps
        pass
    getter.label = name
    return getter

class Plotter(object):
    DEFAULT_COLOURS = ['b', 'r', 'c', 'k']
    DEFAULT_POINTS = ['s', 'x', 'o', 'v']
    DEFUALT_FORMATS = np.add.outer(np.array(DEFAULT_COLOURS,dtype=object), DEFAULT_POINTS).flatten().tolist()
    
    def __init__(self, report_map, fmt_map=None, lbl_map=None):
        self.report_map = report_map
        
        if fmt_map is None:
            self.fmt_map = {}
            for i, k in enumerate(sorted(report_map.keys())):
                self.fmt_map[k] = self.DEFAULT_FORMATS[i]
        else:
            self.fmt_map = fmt_map

        self.lbl_map = lbl_map
        return

    def GetFmt(self, series_name):
        """Override this to have a custom mapping from report series to plot style.
        """
        return self.fmt_map[series_name]

    def GetLbl(self, series_name):
        """Override this to have a custom mapping from report series to label.
        """
        if self.lbl_map is None:
            return series_name
        
        return self.lbl_map[series_name]
    
    def __call__(self, xfunc='Cores', yfunc=None, xlabel=None, ylabel=None, axes=None, legend_loc=None):
        """Iterate over all the Runs, plotting the data specified by xfunc and yfunc.
    
        axes - The axes on which to create the plot. If omitted, a new figure
               will be created with log-log axes
           
        xfunc - Either:
                - A string, which must correspond to an attribute of the
                  Run object, that value then being plotted
                or:
                - A function, which when called with a Run as its only 
                  argument, will give the value to be plotted
                Has a default of 'Cores'
        
        yfunc - As above but has no default.
    
        xlabel - A string for the xlabel of the plot - if omitted and xfunc 
                 is a string, that value will be used
    
        ylabel - As above

        legend_loc - matplotlib legend location specification string or None (which implies no legend)
        """
        if isinstance(xfunc, str):
            xattr = xfunc
            xfunc = lambda run: getattr(run, xattr)
            if xlabel is None:
                xlabel = xattr
        else:
            if xlabel is None:
                try:
                    xlabel = xfunc.label
                except AttributeError:
                    pass
                pass
            pass
        
        if yfunc is None:
            raise ValueError("No 'yfunc' specified!")
        
        if isinstance(yfunc, str):
            yattr = yfunc
            yfunc = lambda run: getattr(run, yattr)
            if ylabel is None:
                ylabel = yattr
        else:
            if ylabel is None:
                try:
                    ylabel = yfunc.label
                except AttributeError:
                    pass
                pass
            pass

        plots = []
        if axes is None:
            fig = pyplot.figure()
            axes = fig.add_subplot(1,1,1)
            axes.set_xscale('log')
            axes.set_yscale('log')

        # Ensure we put them in the right order!
        for run_type, runs in self.report_map.iteritems():
            xs = np.array(map(xfunc, runs))
            ys = np.array(map(yfunc, runs))
            fmt = self.GetFmt(run_type)
            lbl = self.GetLbl(run_type)
            plots.append(axes.plot(xs, ys, fmt, label=lbl)[0])

        if xlabel is not None:
            axes.set_xlabel(xlabel)

        if ylabel is not None:
            axes.set_ylabel(ylabel)
        if legend_loc is not None:
            leg = axes.legend(loc=legend_loc)
        return plots
