#!/usr/bin/env python

import math
import sys
import time
import wx
import numpy as np
import sounddevice as sd
import json

def convertNumpyGSToBitmap( ary, final_scale = None ):
    color_ary = np.zeros( (ary.shape[0], ary.shape[1], 3), 'uint8' )
    aryu = ary.astype('uint8')
    color_ary[:,:,0] = aryu
    color_ary[:,:,1] = aryu
    color_ary[:,:,2] = aryu
    image = wx.Image(ary.shape[1],ary.shape[0], color_ary.tostring())
    if not final_scale is None:
        image.Rescale(final_scale[0], final_scale[1])
    wxBitmap = image.ConvertToBitmap()       # OR:  wx.BitmapFromImage(image)
    return wxBitmap

def findPeak(signal, oversample, pkval=0.4):
    ffts = np.fft.fft(signal)
    ffts = np.concatenate((ffts[0:ffts.size//2],np.zeros(ffts.size*(oversample-1)),ffts[ffts.size//2+1:ffts.size]))
    ffts = np.abs(np.fft.ifft(ffts))
    ind1 = np.argmax(ffts>(0.5*np.max(ffts)))
    ind = min(max(1,np.argmax(ffts>=(pkval*np.max(ffts)))),ffts.size-2)
    ind = ind + (ffts[ind-1]-ffts[ind+1])/(2.0*(ffts[ind+1]+ffts[ind-1]-2*ffts[ind]))
    ind = ind / oversample
    return ind

def cosineWindow(sig):
    return sig*np.sin(np.linspace(0,math.pi,sig.size))
    
def generateChirp(samplerate, freq1, freq2, numsamples, amplitude, channel):
    n = np.arange(numsamples)
    ch = (((freq1 / samplerate) * n + ((freq2 - freq1) / (2.0 * numsamples * samplerate)) * n  * n))
    ch = np.cos(2.0*np.pi*ch)*amplitude
    #ch = cosineWindow(ch)
    ch = ch.reshape(numsamples, 1)
    if channel == -1:
        ch = np.column_stack((ch, ch))
    elif channel > 0:
        zr = np.zeros((numsamples, 1))
        ch = np.column_stack((ch, zr) if (channel == 1) else (zr, ch))
    return ch

def playTone(samplerate, freq, numsamples, amplitude):
    samples = generateChirp(samplerate, freq, freq, numsamples, amplitude, -1)
    playSound(samples)
    
def getAudioConf():
    cfg = wx.FileConfig.Get()
    cfg.SetPath("/AudioConf")
    return cfg

def getCalibration():
    cfg = wx.FileConfig.Get()
    cfg.SetPath("/Calibration")
    return cfg
    
def playSound(sample):
    devno_output=getAudioConf().ReadInt("audio_devno_output7",0)
    sample_rate = getAudioConf().ReadInt("sample_rate",44100)
    sample_number = getAudioConf().ReadInt("sample_number_output",100000)
    if devno_output == 0:
        return
    snddv = OSoundDevice(devno_output-1, sample_rate)
    snddv.PlaySound(sample)
    return
    
def captureSound(channel_no): 
    devno_input = getAudioConf().ReadInt("audio_devno_micinput",0)
    channelno_input = getAudioConf().ReadInt("audio_channelno_micinput",0)
    channelno_feedback = getAudioConf().ReadInt("audio_channelno_micinput",0)
    sample_rate = getAudioConf().ReadInt("sample_rate",44100)
    sample_number_output = getAudioConf().ReadInt("sample_number_output",100000)
    sample_number_input = getAudioConf().ReadInt("sample_number_input",200000)
    minimum_frequency = getAudioConf().ReadInt("min_frequency",100)
    maximum_frequency = getAudioConf().ReadInt("max_frequency",15000)
    if devno_input == 0 or channelno_input == 0 or channelno_feedback == 0:
         wx.MessageDialog(None, "Input Channels Not Defined", "Error", wx.OK|wx.STAY_ON_TOP|wx.CENTRE).ShowModal()
         return None
    if channel_no == 1:
        devno_output=getAudioConf().ReadInt("audio_devno_outputleft",0)
        channelno_output=getAudioConf().ReadInt("audio_channelno_outputleft",0)
    else:
        devno_output=getAudioConf().ReadInt("audio_devno_outputright",0)
        channelno_output=getAudioConf().ReadInt("audio_channelno_outputright",0)
    if devno_output == 0 or channelno_output == 0:
         wx.MessageDialog(None, "Output Channel Not Defined", "Error", wx.OK|wx.STAY_ON_TOP|wx.CENTRE).ShowModal()
         return None
    snddv = IOSoundDevice(devno_output-1, devno_input-1, sample_rate)
    ch = generateChirp(snddv.output_samplerate, minimum_frequency, maximum_frequency, sample_number_output, 1.0, channelno_output)
    samp = snddv.PlaySound(ch, sample_number_input)
    sig = np.fft.fft(cosineWindow(samp[:,0]))*np.conj(np.fft.fft(cosineWindow(samp[:,1])))
    sig = np.conj(sig) if channelno_input == 2 else sig
    sig = np.fft.ifft(sig)
    timelen = sample_number_input / sample_rate 
    return samp, sig, timelen
        
class SelectAudioDeviceDialog(wx.Dialog):
    def __init__(self, *args, **kw):
        super(SelectAudioDeviceDialog, self).__init__(*args, **kw) 
        self.dev = {}
        self.dev['deviceno'] = -1
        self.dev['channelno'] = -1
        self.dev['desc'] = ''
    
    def AudioDeviceSelection(self):
        return self.dev
    
    def InitUI(self,outputCh=True):
        dvs = sd.query_devices()
        panel = wx.Panel(self)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.listbox = wx.ListBox(panel)
        hbox.Add(self.listbox, wx.ID_ANY, wx.EXPAND | wx.ALL, 20)
        self.listbox.Append("00/00: NONE")
        countdevices = 0
        n = 0
        for x in dvs:
            n = n + 1
            channels = x['max_output_channels'] if outputCh else x['max_input_channels']
            for ch in range(0, channels):
                countdevices = countdevices + 1
                cht = "{0:02d}/{1:02d}: {2}".format(n,ch+1,x['name'])
                self.listbox.Append(cht)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.OnSelected)
        panel.SetSizer(hbox)
        self.SetSize((600,400))
        self.SetTitle('Select Output Channel' if outputCh else 'Select Input Channel')
        self.Centre()
        
    def OnSelected(self, event):
        sel = self.listbox.GetSelection()
        self.dev['desc'] = self.listbox.GetString(sel)
        try:
            self.dev['deviceno'] = int(self.dev['desc'][0:2])
            self.dev['channelno'] = int(self.dev['desc'][3:5])
        except Exception as e:
            print('Exception='+type(e).__name__+': '+str(e))        
        self.Close()
   
class OSoundDevice():
    def __init__(self, output_device, sample_rate):
        self.output_current_device = output_device
        output_dvs = sd.query_devices(self.output_current_device, 'output')
        self.output_samplerate = output_dvs['default_samplerate'] if sample_rate is None else sample_rate
        
    def PlaySound(self,sound):
        def output_callback(outdata, frames, time, status):
            if status:
                print(status, file=sys.stderr)
            lastframe = min(output_callback.index + frames, sound.shape[0])
            nsamples = lastframe - output_callback.index
            if nsamples == 0:
                output_callback.terminate = True
            if nsamples > 0:
                outdata[0:nsamples] = sound[output_callback.index:output_callback.index+nsamples].reshape(nsamples, -1)
            if nsamples < frames:
                outdata[nsamples:frames] = 0
            output_callback.index = lastframe
        output_callback.index = 0
        output_callback.terminate = False
        try:
            with sd.OutputStream(device=self.output_current_device, channels=2, callback=output_callback, samplerate=self.output_samplerate):
                while not output_callback.terminate:
                    time.sleep(0.05)
        except Exception as e:
            print('Exception='+type(e).__name__+': '+str(e))
        return

        
class IOSoundDevice():
    def __init__(self, output_device, input_device, sample_rate):
        self.output_current_device = output_device
        self.input_current_device = input_device
        output_dvs = sd.query_devices(self.output_current_device, 'output')
        self.output_samplerate = output_dvs['default_samplerate'] if sample_rate is None else sample_rate
        input_dvs = sd.query_devices(self.input_current_device, 'input')
        self.input_samplerate = input_dvs['default_samplerate'] if sample_rate is None else sample_rate
        
    def PlaySound(self,sound,insamples):
        def input_callback(indata, frames, time, status):
            if status:
                print(status, file=sys.stderr)
            lastframe = min(input_callback.index + frames, insamples)
            nsamples = lastframe - input_callback.index
            if nsamples == 0:
                input_callback.terminate = True
            if nsamples > 0:
                input_callback.inary[input_callback.index:input_callback.index+nsamples] = indata[0:nsamples].reshape(nsamples, -1)
            input_callback.index = lastframe
        input_callback.index = 0
        input_callback.terminate = False
        input_callback.inary = np.zeros((insamples,2))
        def output_callback(outdata, frames, time, status):
            if status:
                print(status, file=sys.stderr)
            lastframe = min(output_callback.index + frames, sound.shape[0])
            nsamples = lastframe - output_callback.index
            if nsamples == 0:
                output_callback.terminate = True
            if nsamples > 0:
                outdata[0:nsamples] = sound[output_callback.index:output_callback.index+nsamples].reshape(nsamples, -1)
            if nsamples < frames:
                outdata[nsamples:frames] = 0
            output_callback.index = lastframe
        output_callback.index = 0
        output_callback.terminate = False
        try:
            with sd.OutputStream(device=self.output_current_device, channels=2, callback=output_callback, samplerate=self.output_samplerate):
                with sd.InputStream(device=self.input_current_device, channels=2, callback=input_callback, samplerate=self.input_samplerate):
                    while not input_callback.terminate:
                        time.sleep(0.05)
        except Exception as e:
            print('Exception='+type(e).__name__+': '+str(e))
        return input_callback.inary

        
class AudioSamplingConfigurePanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        super(AudioSamplingConfigurePanel,self).__init__(*args, **kwargs)

        gs = wx.GridSizer(9, 3, 0, 0)
        
        cfg = getAudioConf()
        self.sample_rate = cfg.ReadInt("sample_rate",44100)
        self.sample_number_output = cfg.ReadInt("sample_number_output",100000)
        self.sample_number_input = cfg.ReadInt("sample_number_input",200000)
        self.minimum_frequency = cfg.ReadInt("min_frequency",100)
        self.maximum_frequency = cfg.ReadInt("max_frequency",15000)
        self.accumulated_exponent = cfg.ReadInt("accumulated_exponent",100)
        self.null_delay = cfg.ReadInt("null_delay",0)
        self.after_delay = cfg.ReadInt("after_delay",0)
        self.save_interval = cfg.ReadInt("save_interval",100)
        
        self.sample_rate_slider, self.sample_rate_slider_val = self.SetupSlider(gs, "Sample Rate", 44100, 96000, self.OnSampleRateSliderScroll, self.sample_rate)
        self.SetSampleRateValue(self.sample_rate)
        
        self.sample_number_output_slider, self.sample_number_output_slider_val = self.SetupSlider(gs, "Number of Output Samples", 10000, 200000, self.OnSampleNumberOutputSliderScroll, self.sample_number_output)
        self.SetSampleNumberOutputValue(self.sample_number_output)

        self.sample_number_input_slider, self.sample_number_input_slider_val = self.SetupSlider(gs, "Number of Input Samples", 40000, 200000, self.OnSampleNumberInputSliderScroll, self.sample_number_input)
        self.SetSampleNumberInputValue(self.sample_number_input)

        self.min_frequency_slider, self.min_frequency_slider_val = self.SetupSlider(gs, "Minimum frequency (Hz)", 100, 40000, self.OnMinFrequencySliderScroll, self.minimum_frequency)
        self.SetMinFrequencyValue(self.minimum_frequency)

        self.max_frequency_slider, self.max_frequency_slider_val = self.SetupSlider(gs, "Maximum frequency (Hz)", 1000, 40000, self.OnMaxFrequencySliderScroll, self.maximum_frequency)
        self.SetMaxFrequencyValue(self.maximum_frequency)

        self.accumulated_exponent_slider, self.accumulated_exponent_slider_val = self.SetupSlider(gs, "Accumulated Exponent", 25, 400, self.OnAccumulatedExponentSliderScroll, self.accumulated_exponent)
        self.SetAccumulatedExponentValue(self.accumulated_exponent)
        
        self.null_delay_slider, self.null_delay_slider_val = self.SetupSlider(gs, "Null Delay (us)", 0, 10000, self.OnNullDelaySliderScroll, self.null_delay)
        self.SetNullDelayValue(self.null_delay)

        self.after_delay_slider, self.after_delay_slider_val = self.SetupSlider(gs, "After Delay (ms)", 0, 100, self.OnAfterDelaySliderScroll, self.after_delay)
        self.SetAfterDelayValue(self.after_delay)

        self.save_interval_slider, self.save_interval_slider_val = self.SetupSlider(gs, "Save Interval (ms)", 1, 1000, self.OnSaveIntervalSliderScroll, self.save_interval)
        self.SetSaveIntervalValue(self.save_interval)

        self.SetSizer(gs)
        
    def SetupSlider(self, gs, typelabel, rang_low, rang_high, binder, val):
        gs.Add(wx.StaticText(self,label=typelabel),0, wx.EXPAND)
        slider = wx.Slider(self, -1)
        slider.SetRange(rang_low,rang_high)
        gs.Add(slider, 0, wx.EXPAND)
        slider.Bind(wx.EVT_SLIDER, binder)
        slider_val = wx.StaticText(self,label=str(val))
        gs.Add(slider_val, 0, wx.EXPAND)
        return slider, slider_val        
        
    def OnSampleRateSliderScroll(self, e):
        value = self.sample_rate_slider.GetValue()
        self.SetSampleRateValue(value)

    def OnSampleNumberOutputSliderScroll(self, e):
        value = self.sample_number_output_slider.GetValue()
        self.SetSampleNumberOutputValue(value)

    def OnSampleNumberInputSliderScroll(self, e):
        value = self.sample_number_input_slider.GetValue()
        self.SetSampleNumberInputValue(value)

    def OnMaxFrequencySliderScroll(self, e):
        value = self.max_frequency_slider.GetValue()
        self.SetMaxFrequencyValue(value)    

    def OnMinFrequencySliderScroll(self, e):
        value = self.min_frequency_slider.GetValue()
        self.SetMinFrequencyValue(value)    

    def OnAccumulatedExponentSliderScroll(self, e):
        value = self.accumulated_exponent_slider.GetValue()
        self.SetAccumulatedExponentValue(value)    

    def OnNullDelaySliderScroll(self, e):
        value = self.null_delay_slider.GetValue()
        self.SetNullDelayValue(value)    

    def OnAfterDelaySliderScroll(self, e):
        value = self.after_delay_slider.GetValue()
        self.SetAfterDelayValue(value)    

    def OnSaveIntervalSliderScroll(self, e):
        value = self.save_interval_slider.GetValue()
        self.SetSaveIntervalValue(value)    
        
    def SetSampleRateValue(self, value):
        if value < 46000:
            value = 44100
        elif value < 60000:
            value = 48000
        elif value < 92000:
            value = 88200
        else:
            value = 96000
        self.sample_rate = value
        getAudioConf().WriteInt("sample_rate", value)
        self.sample_rate_slider.SetValue(value)
        self.sample_rate_slider_val.SetLabel(str(value))
        
    def SetSampleNumberOutputValue(self, value):
        value = ((value+1000) // 2000)*2000
        getAudioConf().WriteInt("sample_number_output", value)
        self.sample_number_output_slider.SetValue(value)
        self.sample_number_output_slider_val.SetLabel(str(value))

    def SetSampleNumberInputValue(self, value):
        value = ((value+1000) // 2000)*2000
        getAudioConf().WriteInt("sample_number_input", value)
        self.sample_number_input_slider.SetValue(value)
        self.sample_number_input_slider_val.SetLabel(str(value))

    def SetMinFrequencyValue(self, value):
        value = ((value+50) // 100)*100
        getAudioConf().WriteInt("min_frequency", value)
        self.min_frequency_slider.SetValue(value)
        self.min_frequency_slider_val.SetLabel(str(value))

    def SetMaxFrequencyValue(self, value):
        value = ((value+500) // 1000)*1000
        getAudioConf().WriteInt("max_frequency", value)
        self.max_frequency_slider.SetValue(value)
        self.max_frequency_slider_val.SetLabel(str(value))

    def SetAccumulatedExponentValue(self, value):
        getAudioConf().WriteInt("accumulated_exponent", value)
        self.accumulated_exponent_slider.SetValue(value)
        self.accumulated_exponent_slider_val.SetLabel(str(value))

    def SetNullDelayValue(self, value):
        getAudioConf().WriteInt("null_delay", value)
        self.null_delay_slider.SetValue(value)
        self.null_delay_slider_val.SetLabel(str(value))

    def SetAfterDelayValue(self, value):
        getAudioConf().WriteInt("after_delay", value)
        self.after_delay_slider.SetValue(value)
        self.after_delay_slider_val.SetLabel(str(value))

    def SetSaveIntervalValue(self, value):
        getAudioConf().WriteInt("save_interval", value)
        self.save_interval_slider.SetValue(value)
        self.save_interval_slider_val.SetLabel(str(value))
        
class AudioSourceConfigurePanel(wx.Panel):
    AUDIOCHANNELS = [ "Mic Input", "Feedback Input", "Output Left", "Output Right", 
        "Output_3", "Output_4", "Output_5", "Output_6", "Output Speaker" ]
    DEVNOARY = [ "audio_devno_micinput", "audio_devno_feedbackinput", "audio_devno_outputleft", 
        "audio_devno_outputright", "audio_devno_output3", "audio_devno_output4",
        "audio_devno_output5", "audio_devno_output6", "audio_devno_output7" ]
    CHANNELNOARY = [ "audio_channelno_micinput", "audio_channelno_feedbackinput", "audio_channelno_outputleft",
        "audio_channelno_outputright", "audio_channelno_output3", "audio_channelno_output4",
        "audio_channelno_output5", "audio_channelno_output6", "audio_channelno_output7" ] 
    def __init__(self, *args, **kwargs):
        super(AudioSourceConfigurePanel,self).__init__(*args, **kwargs)
       
        cfg = getAudioConf()
        gs = wx.GridSizer(len(self.AUDIOCHANNELS), 4, 0, 0)
        self.textary = []
        self.devnoary = []
        self.channelnoary = []
        self.buttonary = []
        for n in range(0,len(self.AUDIOCHANNELS)):
            tx = wx.StaticText(self,label=self.AUDIOCHANNELS[n]+':')
            self.textary.append(tx)
            gs.Add(tx, 0, wx.EXPAND)
            tx = wx.StaticText(self,label=str(cfg.ReadInt(self.DEVNOARY[n],0)))
            self.devnoary.append(tx)
            gs.Add(tx, 0, wx.EXPAND)
            tx = wx.StaticText(self,label=str(cfg.ReadInt(self.CHANNELNOARY[n],0)))
            self.channelnoary.append(tx)
            gs.Add(tx, 0, wx.EXPAND)
            tx = wx.Button(self, label="Change")
            self.Bind(wx.EVT_BUTTON, self.OnButtonClicked, id=tx.GetId())
            self.buttonary.append(tx)
            gs.Add(tx, 0, wx.EXPAND)
        self.SetSizer(gs)
        
    def OnButtonClicked(self, e):
        for n in range(0,len(self.buttonary)):
            if e.GetId() == self.buttonary[n].GetId():
                dialog = SelectAudioDeviceDialog(None)
                dialog.InitUI(self.AUDIOCHANNELS[n][0:1] == 'O')
                dialog.ShowModal()
                sel = dialog.AudioDeviceSelection()
                dialog.Destroy()
                if sel['deviceno'] >= 0:
                    self.devnoary[n].SetLabel(str(sel['deviceno']))
                    self.channelnoary[n].SetLabel(str(sel['channelno']))
                    wx.FileConfig.Get().SetPath("/AudioConf")
                    wx.FileConfig.Get().WriteInt(self.DEVNOARY[n],sel['deviceno'])
                    wx.FileConfig.Get().WriteInt(self.CHANNELNOARY[n],sel['channelno'])
                    
class ConfigureDialog(wx.Dialog):
    def __init__(self, *args, **kwargs):
        super(ConfigureDialog,self).__init__(*args, **kwargs)

        p = wx.Panel(self)
        nb = wx.Notebook(p)
        
        audioSourceConfigurePanel = AudioSourceConfigurePanel(nb)
        nb.AddPage(audioSourceConfigurePanel, "Audio Sources")

        audioSamplingConfigurePanel = AudioSamplingConfigurePanel(nb)
        nb.AddPage(audioSamplingConfigurePanel, "Audio Sampling")
        
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        p.SetSizer(sizer);
        self.SetSize((500,400))
        self.SetTitle('Configuration')
        self.Centre()
        
class GraphPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        super(GraphPanel,self).__init__(*args, **kwargs)
        colourDatabase = wx.ColourDatabase()
        self.lineColour = colourDatabase.Find(u"BLACK")
        self.backgroundColour = colourDatabase.Find(u"WHITE")
        self.data_array = None
        self.data_array_is_changed = False
        self.start_val = 0.0
        self.end_val = 1.0
        self.min_val = 0.0
        self.max_val = 1.0
        self.current_width = 0
        self.round_to = 1.0
        self.zoom = 1.0
        self.powscal = 0.5
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.font = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.NORMAL) 
        self.SetData(np.linspace(1,50,5000), 1.0)

    def SetData(self, data_array, end_val):
        self.end_val = end_val
        self.data_array = data_array
        self.data_array_is_changed = True
        self.Refresh()
        
    def SetZoom(self, zoomval):
        self.zoom = min(max(zoomval,0.001),1.0)
        self.data_array_is_changed = True
        self.Refresh()
        
    def OnPaint(self,e):
        width, height = self.GetSize()
        dc = wx.PaintDC(self)
        dc.SetPen(wx.Pen(self.lineColour))
        dc.SetBrush(wx.Brush(self.backgroundColour))
        dc.DrawRectangle(0, 0, width-1, height-1)
        dc.SetFont(self.font) 
        dc.DrawText("{0:.3f}".format((self.start_val)),3,0.5*height)
        txt = "{0:.3f}".format((self.start_val + (self.end_val - self.start_val) * self.zoom))
        dc.DrawText(txt,width - dc.GetTextExtent(txt).GetWidth() - 3, 0.5*height)        
        if self.data_array is None:
            return
        ary_width = int(width//2)*2
        if self.data_array_is_changed or ary_width != self.current_width:
            self.data_array_is_changed = False
            self.current_width = ary_width
            nary = max(width, int(self.data_array.size * self.zoom))
            self.data_array_zoomed = self.data_array[0:nary]
            ffta = np.fft.fft(self.data_array_zoomed)
            ffta = np.concatenate((ffta[:ary_width//2],ffta[ffta.size-ary_width//2:]))
            self.show_array = np.power(np.abs(np.fft.ifft(ffta))*(ary_width/self.data_array_zoomed.size),self.powscal)
            self.max_val = math.ceil(np.max(self.show_array)/self.round_to)*self.round_to
            self.min_val = math.floor(np.min(self.show_array)/self.round_to)*self.round_to
        dc.DrawText("{0:.3f}".format(self.max_val), 3, 3)
        txt = "{0:.3f}".format(self.min_val)
        dc.DrawText(txt,3, height - dc.GetTextExtent(txt).GetHeight() - 3)        
        pts = (self.show_array-self.min_val)/(self.max_val - self.min_val) * (-height) + height - 1
        pts_list = []
        scalf = width / pts.size
        for n in range(0, pts.size):
            pts_list.append((scalf*n,pts[n]))
        dc.DrawLines(pts_list)

    def OnSize(self, e):
        self.Refresh()
        
class SpeakerPanel(wx.Panel):    
    def __init__(self, *args, **kwargs):
        super(SpeakerPanel,self).__init__(*args, **kwargs)
        
        self.left_speaker_on = False
        self.right_speaker_on = False
        self.speakersizehorizontal = 0.05
        self.speakersizevertical = 0.05
        self.speakerverticalplacement = 0.9
        self.speakerfromcenter = 0.15
        self.microphonex = 0.0
        self.microphoney = 0.0
        self.reflections = np.zeros((800,600))
        self.background = np.zeros((10,10))+255
        self.background_width = -1
        self.background_height = -1
        colourDatabase = wx.ColourDatabase()
        self.lineColour = colourDatabase.Find(u"RED")
        self.backgroundColour = colourDatabase.Find(u"WHITE")
        self.speakerColour = colourDatabase.Find(u"PINK")
        self.microphoneColour = colourDatabase.Find(u"MAROON")
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)

    def DrawProportionalLine(self, x1, y1, x2, y2):
        width, height = self.GetSize()
        dc = wx.PaintDC(self)
        dc.DrawLine(x1*width, y1*height, x2*width, y2*height)

    def DrawProportionalRectangle(self, x1, y1, rectwidth, rectheight):
        width, height = self.GetSize()
        dc = wx.PaintDC(self)
        dc.DrawRectangle(x1*width, y1*height, rectwidth*width, rectheight*height)        

    def DrawProportionalEllipse(self, x1, y1, rectwidth, rectheight):
        width, height = self.GetSize()
        dc = wx.PaintDC(self)
        dc.DrawEllipse(x1*width, y1*height, rectwidth*width, rectheight*height)        

    def DrawProportionalEllipticArc(self, x1, y1, rectwidth, rectheight, angle1, angle2):
        width, height = self.GetSize()
        dc = wx.PaintDC(self)
        dc.DrawEllipticArc(x1*width, y1*height, rectwidth*width, rectheight*height, angle1, angle2)        
        
    def DrawSpeaker(self, fracx, fracy, playing=False):
        dc = wx.PaintDC(self)
        dc.SetPen(wx.Pen(self.lineColour))
        dc.SetBrush(wx.Brush(self.speakerColour))
        self.DrawProportionalRectangle(fracx-0.25*self.speakersizehorizontal,
            fracy,0.5*self.speakersizehorizontal,0.5*self.speakersizevertical)
        self.DrawProportionalLine(fracx-0.5*self.speakersizehorizontal,
            fracy-0.5*self.speakersizevertical,fracx+0.5*self.speakersizehorizontal,
            fracy-0.5*self.speakersizevertical)
        self.DrawProportionalLine(fracx-0.5*self.speakersizehorizontal,
            fracy-0.5*self.speakersizevertical,fracx-0.25*self.speakersizehorizontal,
            fracy)
        self.DrawProportionalLine(fracx+0.5*self.speakersizehorizontal,
            fracy-0.5*self.speakersizevertical,fracx+0.25*self.speakersizehorizontal,
            fracy)
        if playing:
            dc.SetBrush(wx.TRANSPARENT_BRUSH)
            self.DrawProportionalEllipticArc(fracx-0.9*self.speakersizehorizontal,
                fracy-0.9*self.speakersizevertical,1.8*self.speakersizehorizontal,
                1.8*self.speakersizevertical, 45, 135)
            self.DrawProportionalEllipticArc(fracx-1.2*self.speakersizehorizontal,
                fracy-1.2*self.speakersizevertical,2.4*self.speakersizehorizontal,
                2.4*self.speakersizevertical, 45, 135)            
            
    def DrawMicrophone(self, fracx, fracy):
        dc = wx.PaintDC(self)
        dc.SetPen(wx.Pen(self.lineColour))
        dc.SetBrush(wx.Brush(self.speakerColour))
        self.DrawProportionalRectangle(fracx-0.125*self.speakersizehorizontal,
            fracy,0.25*self.speakersizehorizontal,0.5*self.speakersizevertical)
        dc.SetBrush(wx.Brush(self.microphoneColour))
        self.DrawProportionalEllipse(fracx-0.2*self.speakersizehorizontal,
            fracy-0.5*self.speakersizevertical, 0.4*self.speakersizehorizontal,
            0.6*self.speakersizevertical)
        dc.SetPen(wx.Pen(self.backgroundColour))
        self.DrawProportionalLine(fracx-0.15*self.speakersizehorizontal,
            fracy-0.25*self.speakersizevertical,fracx+0.15*self.speakersizehorizontal,
            fracy-0.25*self.speakersizevertical)
   
    def SetBackground(self, background):
        self.background = background.real.copy()
        self.background_width = -1
        self.Refresh()
   
    def SetSpeakers(self, left_speaker_on, right_speaker_on):
        self.left_speaker_on = left_speaker_on
        self.right_speaker_on = right_speaker_on
        self.Refresh()
        
    def SetMicrophonePosition(self, posx, posy):
        self.microphonex = posx
        self.microphoney = posy
        self.Refresh()
        
    def OnPaint(self,e):
        width, height = self.GetSize()
        dc = wx.PaintDC(self)

        if self.background_width != width or self.background_height != height:
            self.background_width = width
            self.background_height = height
            self.bt = convertNumpyGSToBitmap( self.background, (width, height) )
        dc.DrawBitmap(self.bt, 0, 0)
        dc.SetPen(wx.Pen(self.lineColour))
        dc.SetBrush(wx.Brush(self.backgroundColour))
        #dc.DrawRectangle(0, 0, width-1, height-1)
        self.DrawSpeaker(0.5 - self.speakerfromcenter, self.speakerverticalplacement,self.left_speaker_on)
        self.DrawSpeaker(0.5 + self.speakerfromcenter, self.speakerverticalplacement,self.right_speaker_on)
        micx = 0.5 - self.microphonex * self.speakerfromcenter
        micy = self.speakerverticalplacement - self.microphoney * self.speakerfromcenter
        self.DrawMicrophone(micx,micy)
                
    def OnSize(self, e):
        self.Refresh()

    def ClearReflections(self):
        self.reflections = np.zeros(self.reflections.shape)
        ary = np.zeros((10,10))+255
        self.SetBackground(ary)                
        
    def AddToReflections(self, dlymap):
        cfg = getAudioConf()
        accumulated_exponent = cfg.ReadInt("accumulated_exponent",100) * 0.01
        self.reflections = self.reflections + np.power(np.abs(dlymap),accumulated_exponent)
        dlymap = np.power(np.abs(self.reflections),1.0 / accumulated_exponent)
        ary = (dlymap-np.max(dlymap))*(255/(np.min(dlymap)-np.max(dlymap)))
        self.SetBackground(ary)        
        
    def AddReflections(self, reflection, channel):
        if channel == 1 or channel < 0:
            dlymap = reflection.ComputeMap(1, self.speakerfromcenter, self.speakerverticalplacement, self.reflections.shape)
            self.AddToReflections(dlymap)
        if channel == 2 or channel < 0:
            dlymap = reflection.ComputeMap(2, self.speakerfromcenter, self.speakerverticalplacement, self.reflections.shape)
            self.AddToReflections(dlymap)
                    
class Reflection():
    def __init__(self):
        self.par = {}

    def SetReflection(self, sample_rate, left_samples, right_samples):
        cfg = getAudioConf()
        self.par = {}
        save_interval = cfg.ReadInt("save_interval",100)*0.001
        cal = getCalibration()
        left_micro_left_speaker_peak = cal.ReadDouble("left_micro_left_speaker_peak",0.0)
        left_micro_right_speaker_peak = cal.ReadDouble("left_micro_right_speaker_peak",0.0)
        right_micro_left_speaker_peak = cal.ReadDouble("right_micro_left_speaker_peak",0.0)
        right_micro_right_speaker_peak = cal.ReadDouble("right_micro_right_speaker_peak",0.0)
        if (left_micro_left_speaker_peak == 0.0 or left_micro_right_speaker_peak == 0.0 or
            right_micro_left_speaker_peak == 0.0 or right_micro_right_speaker_peak == 0.0):
            return
        x0 = ((right_micro_left_speaker_peak - left_micro_left_speaker_peak) + 
             (left_micro_right_speaker_peak - right_micro_right_speaker_peak)) / 4.0
        inter_speaker_delay = x0
        left_delay = findPeak(left_samples,2) / sample_rate
        right_delay = findPeak(right_samples,2) / sample_rate 
        left_num_samples = int((save_interval + left_delay) * sample_rate)
        right_num_samples = int((save_interval + right_delay) * sample_rate)
        self.left_samples = left_samples[0:left_num_samples]
        self.right_samples = right_samples[0:right_num_samples]
        left_delay = left_delay - left_micro_left_speaker_peak
        right_delay = right_delay - right_micro_right_speaker_peak
        x = (right_delay*right_delay-left_delay*left_delay)/(4.0*x0)
        y = math.sqrt(max((left_delay*left_delay+right_delay*right_delay-2.0*x*x-2.0*x0*x0)/2,0.0))
        self.par['left_built_in_delay'] = left_micro_left_speaker_peak
        self.par['right_built_in_delay'] = right_micro_right_speaker_peak
        self.par['sample_rate'] = sample_rate
        self.par['inter_speaker_delay'] = x0
        self.par['left_delay'] = left_delay
        self.par['right_delay'] = right_delay
        self.par['x'] = x
        self.par['y'] = y        

    def GetSampleRate(self):
        return self.par['sample_rate']
        
    def GetLeftSamples(self):
        return self.left_samples
        
    def GetRightSamples(self):
        return self.right_samples
        
    def GetLeftDelay(self):
        return self.par['left_delay']
        
    def GetRightDelay(self):
        return self.par['right_delay']
        
    def GetMicrophonePosition(self):
        return self.par['x'], self.par['y']
        
    def GetInterSpeakerDelay(self):
        return self.par['inter_speaker_delay']
        
    def GetLeftBuiltInDelay(self):
        return self.par['left_built_in_delay']
        
    def GetRightBuiltInDelay(self):
        return self.par['right_built_in_delay']

    def ComputeMap(self, channel, speakerfromcenter, speakerverticalplacement, mapshape):
        cfg = getAudioConf()
        null_delay = cfg.ReadInt("null_delay",0) * 1e-6
        after_delay = cfg.ReadInt("after_delay",0) * 1e-3
        built_in_delay = self.GetLeftBuiltInDelay() if channel == 1 else self.GetRightBuiltInDelay()
        signal = self.GetLeftSamples() if channel == 1 else self.GetRightSamples()
        scalx = self.GetInterSpeakerDelay() / speakerfromcenter 
        xpos = np.linspace(-0.5 * scalx, 0.5 * scalx, mapshape[1])
        ypos = np.linspace(-scalx*speakerverticalplacement,scalx-scalx*speakerverticalplacement,mapshape[0])
        xv, yv = np.meshgrid(xpos,ypos)
        micx, micy = self.GetMicrophonePosition()
        micx = -micx
        micy = -micy
        if channel == 1:
            posdly = (np.sqrt(np.square(xv-micx)+np.square(yv-micy)) +
                      np.sqrt(np.square(xv+scalx*speakerfromcenter)+np.square(yv))) + built_in_delay
            dist = math.sqrt((scalx*speakerfromcenter+micx)*(scalx*speakerfromcenter+micx)+micy*micy)
        else:
            posdly = (np.sqrt(np.square(xv-micx)+np.square(yv-micy)) +
                      np.sqrt(np.square(xv-scalx*speakerfromcenter)+np.square(yv))) + built_in_delay
            dist = math.sqrt((scalx*speakerfromcenter-micx)*(scalx*speakerfromcenter-micx)+micy*micy)
        if null_delay > 0 or after_delay > 0:
            if null_delay > 0 and after_delay > 0:
                posdlyblank = np.logical_and(posdly > (built_in_delay + dist + null_delay),posdly < (built_in_delay + dist + after_delay))
            elif null_delay > 0:
                posdlyblank = posdly > (built_in_delay + dist + null_delay)
            else:
                posdlyblank = posdly < (built_in_delay + dist + after_delay)
            posdly = posdly * posdlyblank + posdlyblank - 1.0
        dlymap = np.interp(posdly,np.linspace(0,signal.size/self.GetSampleRate(),signal.size),signal, left=0.0, right=0.0)
        return dlymap
        
    def WriteToStream(self, file):
        success = True
        try:            
            parstr = json.dumps(self.par)
            file.write(parstr.encode())
            file.write(b'\n')
            np.save(file, self.left_samples)
            np.save(file, self.right_samples)
        except Exception as e:
            print(repr(e))
        return success    

    def ReadFromStream(self, file):
        success = True
        try:          
            lstr = file.readline(-1)
            self.par = json.loads(lstr.decode())
            self.left_samples = np.load(file)
            self.right_samples = np.load(file)
        except Exception as e:
            print(repr(e))
        return success    
        
class ReflectionList():
    def __init__(self):
        self.reflections = []
        self.header = {}
        self.header['program'] = 'Audiomapper'
        
    def AddReflection(self, sample_rate, left_samples, right_samples):
        reflection = Reflection()
        reflection.SetReflection(sample_rate, left_samples, right_samples)
        self.reflections.append(reflection)
        return reflection
        
    def SaveStream(self, file):
        success = True
        try:
            self.header['reflections'] = len(self.reflections)
            headerstr = json.dumps(self.header)
            file.write(headerstr.encode())
            file.write(b'\n')
            for ref in self.reflections:
                if not ref.WriteToStream(file):
                    success = False
        except Exception as e:
            print(repr(e))
        return success
    
    def LoadStream(self, file):
        success = True
        try:
           lstr = file.readline(-1)
           self.header = json.loads(lstr.decode())
           for n in range(0,self.header['reflections']):
                reflection = Reflection()
                if not reflection.ReadFromStream(file):
                    success = False
                self.reflections.append(reflection)
        except Exception as e:
            print(repr(e))
            success = False
        return success

    def RemoveReflections(self, n):
        while len(self.reflections)>0 and n>0:
            self.reflections.pop(len(self.reflections)-1)
            n=n-1
        
    def RefreshMap(self, speakerPanel):
        speakerPanel.ClearReflections()
        for ref in self.reflections:
            speakerPanel.AddReflections(ref, -1)    
        
class AudioMapperFrame(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(AudioMapperFrame,self).__init__(*args, **kwargs)

        self.reflectionList = ReflectionList()
        self.changedReflections = False
        
        self.panel = wx.Panel(self)
        self.speakerPanel = SpeakerPanel(self.panel)
        
        self.leftGraphPanel = GraphPanel(self.panel)
        self.rightGraphPanel = GraphPanel(self.panel)
        
        self.graphPanelSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.graphPanelSizer.Add(self.leftGraphPanel, 1, wx.EXPAND | wx.ALL, 5)
        self.graphPanelSizer.Add(self.rightGraphPanel, 1, wx.EXPAND | wx.ALL, 5)
                
        self.frameSizer = wx.BoxSizer(wx.VERTICAL)
        self.speakerPanel.SetBackgroundColour('#ffffff')
        self.frameSizer.Add(self.speakerPanel, 4, wx.EXPAND | wx.ALL, 5)
        self.frameSizer.Add(self.graphPanelSizer, 1, wx.EXPAND | wx.ALL, 5)
        self.panel.SetSizer(self.frameSizer)
        
        self.buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sampleButton = wx.Button(self.panel, label=u"Sample")
        self.buttonSizer.Add(self.sampleButton, 0, wx.FIXED_MINSIZE|wx.ALL, 5)
        self.Bind(wx.EVT_BUTTON, self.SampleButtonClicked, id=self.sampleButton.GetId())
        
        self.addSignalCheck = wx.CheckBox(self.panel, label="Add Signal")
        self.buttonSizer.Add(self.addSignalCheck, 0, wx.FIXED_MINSIZE|wx.ALL, 5)

        self.delayStaticText = wx.StaticText(self.panel,label="")
        self.buttonSizer.Add(self.delayStaticText, 1, wx.EXPAND|wx.ALIGN_TOP|wx.ALL, 5)
        
        self.zoomSlider = wx.Slider(self.panel,-1)
        self.zoomSlider.SetRange(1,1000)
        self.zoomSlider.SetValue(1000)
        self.buttonSizer.Add(self.zoomSlider, 1, wx.EXPAND|wx.ALL, 5)
        self.zoomSlider.Bind(wx.EVT_SLIDER, self.ZoomSliderMoved)

        self.frameSizer.Add(self.buttonSizer, 0, wx.EXPAND|wx.ALL, 5)
        
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        newMapItem = fileMenu.Append(wx.ID_NEW, '&New Map', 'New Map')
        openMapItem = fileMenu.Append(wx.ID_OPEN, '&Open Map', 'Open Map')
        saveMapItem = fileMenu.Append(wx.ID_SAVE, '&Save Map', 'Save Map')
        quitItem = fileMenu.Append(wx.ID_EXIT, '&Quit', 'Quit Application')
        menubar.Append(fileMenu, '&File')
        self.Bind(wx.EVT_MENU, self.OnNewMap, newMapItem)
        self.Bind(wx.EVT_MENU, self.OnOpenMap, openMapItem)
        self.Bind(wx.EVT_MENU, self.OnSaveMap, saveMapItem)
        self.Bind(wx.EVT_MENU, self.OnQuit, quitItem)
        configurationMenu = wx.Menu()
        configureItem = configurationMenu.Append(wx.ID_ANY, '&Configure', 'Configure')
        calibrateItem = configurationMenu.Append(wx.ID_ANY, '&Calibrate', 'Calibrate Microphone')
        menubar.Append(configurationMenu, '&Configuration')        
        processingMenu = wx.Menu()
        multipleReflectionsItem = processingMenu.Append(wx.ID_ANY, '&Multiple Reflections', 'Multiple Reflections')        
        reprocessItem = processingMenu.Append(wx.ID_ANY, '&Reprocess', 'Reprocess')
        removeLastReflection = processingMenu.Append(wx.ID_ANY, '&Remove Last Reflection', 'Remove Last Reflection')
        menubar.Append(processingMenu, '&Acquire')        
        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self.OnCalibrate, calibrateItem)
        self.Bind(wx.EVT_MENU, self.OnConfigure, configureItem)
        self.Bind(wx.EVT_MENU, self.OnMultipleReflections, multipleReflectionsItem)
        self.Bind(wx.EVT_MENU, self.OnReprocess, reprocessItem)
        self.Bind(wx.EVT_MENU, self.OnRemoveLastReflection, removeLastReflection)
        self.SetSize((800,600))
        self.SetTitle('Audiomapper')
        self.Centre()
        

    def OnCalibrate(self, e):
        cfg = getAudioConf()
        sample_rate = cfg.ReadInt("sample_rate",44100)
        wx.MessageDialog(None, "Place microphone next to left speaker\nand point at left speaker", "Calibrate", wx.OK|wx.STAY_ON_TOP|wx.CENTRE).ShowModal()
        leftch, leftx, left_timelen = self.PlayFromSpeaker(1)
        left_micro_left_speaker_peak = findPeak(leftx,2) / sample_rate
        wx.MessageDialog(None, "Place microphone next to left speaker\nand point at right speaker", "Calibrate", wx.OK|wx.STAY_ON_TOP|wx.CENTRE).ShowModal()
        leftch, leftx, left_timelen = self.PlayFromSpeaker(2)
        left_micro_right_speaker_peak = findPeak(leftx,2) / sample_rate
        wx.MessageDialog(None, "Place microphone next to right speaker\nand point at right speaker", "Calibrate", wx.OK|wx.STAY_ON_TOP|wx.CENTRE).ShowModal()
        rightch, rightx, right_timelen = self.PlayFromSpeaker(2)
        right_micro_right_speaker_peak = findPeak(rightx,2) / sample_rate
        wx.MessageDialog(None, "Place microphone next to right speaker\nand point at left speaker", "Calibrate", wx.OK|wx.STAY_ON_TOP|wx.CENTRE).ShowModal()
        rightch, rightx, right_timelen = self.PlayFromSpeaker(1)
        right_micro_left_speaker_peak = findPeak(rightx,2) / sample_rate
        cal = getCalibration()
        cal.WriteFloat("left_micro_left_speaker_peak",left_micro_left_speaker_peak)
        cal.WriteFloat("left_micro_right_speaker_peak",left_micro_right_speaker_peak)
        cal.WriteFloat("right_micro_left_speaker_peak",right_micro_left_speaker_peak)
        cal.WriteFloat("right_micro_right_speaker_peak",right_micro_right_speaker_peak)
        strn = ("From left speaker to left microphone delay {0:.4g} ms\n"+
                "From right speaker to left microphone delay {1:.4g} ms\n"+
                "From left speaker to right microphone delay {2:.4g} ms\n"+
                "From right speaker to right microphone delay {3:.4g} ms\n"+
                "Inter speaker delay at left speaker {4:.4g} ms\n"+
                "Inter speaker delay at right speaker {5:.4g} ms\n").format(
                left_micro_left_speaker_peak*1000.0,
                left_micro_right_speaker_peak*1000.0,
                right_micro_left_speaker_peak*1000.0,
                right_micro_right_speaker_peak*1000.0,
                (right_micro_left_speaker_peak-left_micro_left_speaker_peak)*1000.0,
                (left_micro_right_speaker_peak-right_micro_right_speaker_peak)*1000.0)
        wx.MessageDialog(None, strn, "Calibrate complete", wx.OK|wx.STAY_ON_TOP|wx.CENTRE).ShowModal()
              
    def OnConfigure(self, e):
        dialog = ConfigureDialog(self)
        dialog.ShowModal()
        dialog.Destroy()

    def CheckUnsaved(self, message, windowtitle):
        result = wx.ID_YES
        if self.changedReflections:
            dialog = wx.MessageDialog(None, message, windowtitle, wx.YES_NO | wx.ICON_QUESTION)
            result = dialog.ShowModal()
            dialog.Destroy()
        return result
        
    def OnQuit(self, e):
        result = self.CheckUnsaved("Do you want to quit with unsaved map?",'Quit?')
        if result == wx.ID_YES:
            self.Close()
        
    def OnNewMap(self, e):
        result = self.CheckUnsaved("Do you want to erase the unsaved map?",'New Map')
        if result == wx.ID_YES:
            self.speakerPanel.ClearReflections()
            self.reflectionList = ReflectionList()
            self.changedReflections = False
            
    def OnReprocess(self, e):
        self.reflectionList.RefreshMap(self.speakerPanel)
            
    def OnOpenMap(self, e):
        result = self.CheckUnsaved("Do you want to lose the unsaved map?",'Open Map')
        if result !=wx.ID_YES:
            return
        with wx.FileDialog(self, "Open Map", wildcard="AMAP files (*.amap)|*.amap",style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'rb') as file:
                    self.changedReflections = False
                    self.reflectionList = ReflectionList()
                    self.reflectionList.LoadStream(file)
                    self.reflectionList.RefreshMap(self.speakerPanel)
            except IOError:
                wx.MessageDialog(None, "Unable to open file to load", "Error", wx.OK|wx.STAY_ON_TOP|wx.CENTRE).ShowModal()
                            
    def OnSaveMap(self, e):
        with wx.FileDialog(self, "Save Map", wildcard="AMAP files (*.amap)|*.amap", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'wb') as file:
                    self.reflectionList.SaveStream(file)
                    self.changedReflections = False
            except IOError:
                wx.MessageDialog(None, "Unable to open file to save", "Error", wx.OK|wx.STAY_ON_TOP|wx.CENTRE).ShowModal()
                                    
            
    def ZoomSliderMoved(self, e):
        zoomv = self.zoomSlider.GetValue() * self.zoomSlider.GetValue() * 1.0e-6
        self.leftGraphPanel.SetZoom(zoomv)
        self.rightGraphPanel.SetZoom(zoomv)
        
    def PlayFromSpeaker(self, output_no):
        self.speakerPanel.SetSpeakers(True,False) if output_no == 1 else self.speakerPanel.SetSpeakers(False,True) 
        wx.Yield()
        signal, corr, timelen = captureSound(output_no)
        self.speakerPanel.SetSpeakers(False,False)
        wx.Yield()        
        return signal, corr, timelen

    def OnRemoveLastReflection(self, e):
        self.changedReflections = True
        self.reflectionList.RemoveReflections(1)
        self.reflectionList.RefreshMap(self.speakerPanel)
        
    def OnMultipleReflections(self, e):
        dialog = wx.MessageDialog(None, "Do you want to start multiple reflection acquisition?",'Multiple Reflections',wx.YES_NO | wx.ICON_QUESTION)
        result = dialog.ShowModal()
        if result == wx.ID_YES:
            self.addSignalCheck.SetValue(True)
            while self.addSignalCheck.GetValue():
                playTone(44100, 1000, 44100, 0.2)
                playTone(44100, 500, 44100, 0.2)
                playTone(44100, 750, 44100, 0.2)
                wx.Yield()
                if self.addSignalCheck.GetValue():
                    self.AcquireReflection()
                wx.Yield()
        dialog.Destroy()
        
    def SampleButtonClicked(self, e):
        self.AcquireReflection()

    def AcquireReflection(self):
        cfg = getAudioConf()
        sample_rate = cfg.ReadInt("sample_rate",44100)
        leftch, leftx, left_timelen = self.PlayFromSpeaker(1)
        self.leftGraphPanel.SetData(np.abs(leftx),left_timelen)
        rightch, rightx, right_timelen = self.PlayFromSpeaker(2)
        self.rightGraphPanel.SetData(np.abs(rightx), right_timelen)
        reflection = self.reflectionList.AddReflection(sample_rate, leftx, rightx)

        x, y = reflection.GetMicrophonePosition()
        x0 = reflection.GetInterSpeakerDelay()
        self.speakerPanel.SetMicrophonePosition(x/x0,y/x0)
        if self.addSignalCheck.GetValue():
            self.speakerPanel.AddReflections(reflection, -1)
        strn = ("Left delay {0:.4g} ms\nRight delay {1:.4g} ms").format(reflection.GetLeftDelay()*1000.0,reflection.GetRightDelay()*1000.0)
        self.delayStaticText.SetLabel(strn)        
        self.changedReflections = True
            
def main():
    app = wx.App()
    fileConfig = wx.FileConfig(appName="AudioMapper",vendorName="RLDM", style=wx.CONFIG_USE_LOCAL_FILE)
    wx.FileConfig.Set(fileConfig)
    frame = AudioMapperFrame(None, title='Audiomapper')
    frame.Show()
    app.MainLoop()
    
        
if __name__=='__main__':
    main()
   