"""
In this file, find the functions that actually trigger the sound generators.

graa doesn't use it's own sound generation, but different backends, as seen below.

"""
import datetime, time, threading, atexit, os, fnmatch
from pythonosc import osc_message_builder
import scsynth_client as scsc

scsynth_client = scsc.UDPClient("127.0.0.1", 57110, 54442)

scsynth_client.sendMsg("/g_new", 1, 0, 0)

def nois(*args, **kwargs):
    """
    Play a white noise (with SC).
    """    
    gain = float(kwargs.get("gain", 0.5))    
    sus = args[0]
    attack = kwargs.get("a", max(4, min(50, sus*0.25)));
    decay = kwargs.get("d", 0);
    release = kwargs.get("r", max(4, min(50, sus*0.1)));
    rev = kwargs.get("rev", 0.0)
    pan = float((kwargs.get("pan", 0.5) * 2) - 1) 
    sus = sus - attack - decay - release
    if sus <= 0:
        log.action("nois duration too short!")
    synth_name = "noise"
    if(rev > 0.0):
        synth_name = "noiserev"
    # send message
    scsynth_client.sendMsg("/s_new", synth_name, -1, 0, 1, "gain", gain, "a", attack, "d", decay, "s", sus, "r", release, "rev", rev, "pan", pan)
# end noiz()

# dict mapping samplename to bufnum
class sampl_info:
    graa_samples = {}
    sample_root = "/home/nik/REPOSITORIES/thenemin/samples"
    bufnum = 0

def free_samples():
    for sample in sampl_info.graa_samples:
        scsynth_client.sendMsg("/b_free", sampl_info.graa_samples[sample])

atexit.register(free_samples)

def sampl(*args, **kwargs):
    """
    Play a sample or a part of it (with SC).
    """
    folder = str(args[0])
    name = str(args[1])
    sample_id = folder + ":" + name
    speed = float(kwargs.get("speed", 1.0))
    rev = float(kwargs.get("rev", 0.0))
    pan = float((kwargs.get("pan", 0.5) * 2) - 1)
    cutoff = float(kwargs.get("cutoff", 20000))
    gain = float(kwargs.get("gain", 1.0))
    start = float(kwargs.get("start", 0.0))
    a_ms = kwargs.get("a", 4)
    r_ms = kwargs.get("r", 4)
    l_ms = kwargs.get("length", 0) - a_ms - r_ms
    release = float(r_ms / 1000)
    attack = float(a_ms / 1000)
    length = float(l_ms / 1000)
    if rev > 0.0:
        if length > 0.0:
            synth_name="grainrev"
        else:
            synth_name="samplrev"
    else:
        if length > 0.0:
            synth_name="grain"
        else:
            synth_name="sampl"
    #print(synth_name + ":" + str(length))
    if sample_id not in sampl_info.graa_samples:
        sample_path = sampl_info.sample_root + "/" + folder + "/" + name + ".wav"
        # create buffer on scsynth
        scsynth_client.sendMsg("/b_allocRead", sampl_info.bufnum, sample_path)
        sampl_info.graa_samples[sample_id] = sampl_info.bufnum
        sampl_info.bufnum += 1
    scsynth_client.sendMsg("/s_new", synth_name, -1, 0, 1, "bufnum", sampl_info.graa_samples[sample_id], "speed", speed, "rev", rev, "pan", pan, "cutoff", cutoff, "gain", gain, "start", start, "length", length)
# end sampl()

def buzz(*args, **kwargs):
    """
    Play a buzz bass synth sound (with SC).
    """
    freq = args[0]    
    gain = float(kwargs.get("gain", 0.5))    
    sus = args[1]
    attack = kwargs.get("a", max(4, min(30, sus*0.1))) / 1000
    decay = kwargs.get("d", max(4, min(30, sus*0.25))) / 1000
    release = kwargs.get("r", max(4, min(50, sus*0.1))) / 1000
    sus = (sus - attack - decay - release) / 1000
    rev = kwargs.get("rev", 0.0)
    cutoff = kwargs.get("cutoff", freq)
    if type(cutoff) is gnote:
        cutoff = cutoff.pitch.frequency
    pan = float((kwargs.get("pan", 0.5) * 2) - 1) 
    if sus <= 0:
        log.action("sine duration too short!")    
    if rev > 0.0:
        synth_name="buzzrev"
    else:
        synth_name="buzz"    
    scsynth_client.sendMsg("/s_new", synth_name, -1, 0, 1, "freq", freq, "gain", gain, "a", attack, "d", decay, "s", sus, "r", release, "rev", rev, "pan", pan, "cutoff", cutoff)
# end buzz()

def sqr(*args, **kwargs):
    """
    Play a sqr bass synth sound (with SC).
    """
    freq = None
    if type(args[0]) is gnote:
        freq = args[0].pitch.frequency
    else:
        freq = args[0]    
    gain = float(kwargs.get("gain", 0.5))    
    sus = args[1]
    attack = kwargs.get("a", max(4, min(30, sus*0.1))) / 1000
    decay = kwargs.get("d", max(4, min(30, sus*0.25))) / 1000
    release = kwargs.get("r", max(4, min(50, sus*0.1))) / 1000
    sus = (sus - attack - decay - release) / 1000
    rev = kwargs.get("rev", 0.0)
    cutoff = kwargs.get("cutoff", freq)
    if type(cutoff) is gnote:
        cutoff = cutoff.pitch.frequency
    pan = float((kwargs.get("pan", 0.5) * 2) - 1) 
    if sus <= 0:
        log.action("sine duration too short!")
    if rev > 0.0:
        synth_name="sqrrev"
    else:
        synth_name="sqr"    
    scsynth_client.sendMsg("/s_new", synth_name, -1, 0, 1, "freq", freq, "gain", gain, "a", attack, "d", decay, "s", sus, "r", release, "rev", rev, "pan", pan, "cutoff", cutoff)
# end sqr()
