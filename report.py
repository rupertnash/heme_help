"""Helpers for analyzing HemeLB's report files.

"""
from xml.etree import ElementTree
import numpy as np

class Timing(object):
    """Bundle up all the different timings"""
    def __init__(self, el):
        self.Name = el.find("name").text
        self.Local = float(el.find("local").text)
        self.Min = float(el.find("min").text)
        self.Max = float(el.find("max").text)
        self.Mean = float(el.find("mean").text)

        
class Report(object):
    def __init__(self, xml):
        self.Tree = xml
        return

    @classmethod
    def FromFile(cls, fn):
        xml = ElementTree.parse(fn)
        return cls(xml)

    @classmethod
    def FromString(cls, xml_text):
        xml = ElementTree.fromstring(xml_text)
        return cls(xml)
    
    @property
    def ConfigFile(self):
        return self.Tree.find("configuration/file").text
    
    @property
    def Cores(self):
        val = self.Tree.find("nodes/threads").text
        return int(val)
    
    @property
    def Steps(self):
        s = self.Tree.find("configuration/steps").text
        return int(s)
    
    @property
    def Sites(self):
        s = self.Tree.find("geometry/sites").text
        return int(s)

    @property
    def SiteDistribution(self):
        n = self.Cores
        dist = np.zeros(n, dtype=int)

        for el in self.Tree.iterfind("geometry/domain"):
            r = int(el.find("rank").text)
            s = int(el.find("sites").text)
            dist[r] = s
            continue
        
        return dist

    @property
    def Timings(self):
        timers = {}
        
        for el in self.Tree.iterfind("timings/timer"):
            t = Timing(el)
            timers[t.Name] = t
            continue

        return timers

    @property
    def SUPS(self):
        lbTime = self.Timings["Simulation total"].Max
        return self.Sites*self.Steps / lbTime
    
    @property
    def Overhead(self):
        return (self.Timings["Simulation total"].Mean - self.Timings["LB calc only"].Mean) / self.Timings["Simulation total"].Mean
    
    def __getattr__(self, attr):
        try:
            return self.Timings[attr]
        except KeyError:
            raise AttributeError("'Report' object has no attribute '" + attr + "'")
    
    pass

