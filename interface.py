# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 15:31:31 2021

@author: ZAAIM HALIM - Master MIDVI
"""

import wx
import bg_modeling as bgm

ALGO = ["Frame_differencing","Mean_filter","Median_filter","Running_average"]
class GUI(wx.Frame):

    def __init__(self, parent, title):
        super(GUI, self).__init__(parent, title=title)
        self.video = bgm.ReadVideo()
        self.video_source = ""
        self.video_path = ""
        self.btn_video_browse = ""
        self.algo = ""
        self.threshold = 10
        self.sliderNumFrame = ""
        self.numFrame = 15
        self.stop_btn = ""
        self.InitUI()
        self.Centre()

    def on_source_video_change(self, event):
        choice = self.video_source.GetValue()
        if choice == "webCam":
            self.btn_video_browse.Disable()
        else:
            self.btn_video_browse.Enable()


    def on_video_browse(self, event):
        openFileDialog = wx.FileDialog(self, "Open", "", "", "Video files (*.mp4)|*.avi",
                                       wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        openFileDialog.ShowModal()
        self.video_source.SetValue(openFileDialog.GetPath())
        self.video_path = openFileDialog.GetPath().replace('\\','\\\\')

    def on_algo_selected(self, event):
        self.algo = event.GetEventObject().GetValue()
        if self.algo == "Running_average" or self.algo == "Frame_differencing":
            self.sliderNumFrame.Disable()
        else:
            self.sliderNumFrame.Enable()

    def on_slider_scroll(self , event):
        self.threshold = event.GetEventObject().GetValue()

    def on_slider_scroll_numFrame(self , event):
        self.numFrame = event.GetEventObject().GetValue()

    def on_close(self, event):
        self.Close()

    def on_stop(self, event):
        self.video.release()
        self.video.cleanup()

    def on_run(self, event):
        print("Running ...")
        self.stop_btn.Enable()
        if self.video_source.GetValue() == "webCam":

            self.video.set_isFromWebCam(True)
        else:
            self.video.set_path(self.video_path)

        #if True:
           # wx.MessageBox('Pythonspot wxWidgets demo', 'Info', wx.OK | wx.ICON_INFORMATION)

        self.video.set_thresh(self.threshold)
        self.video.load()
        self.video.capture(operation=self.algo)


    def InitUI(self):

        panel = wx.Panel(self)

        sizer = wx.GridBagSizer(5, 5)


        video_text = wx.StaticText(panel, label="Video Source")
        sizer.Add(video_text, pos=(3, 0), flag=wx.LEFT|wx.TOP, border=10)

        self.video_source = wx.ComboBox(panel,value="From a file",
                                   choices=["From a file","webCam"])
        self.video_source.Bind(wx.EVT_COMBOBOX, self.on_source_video_change)
        sizer.Add(self.video_source,  pos=(3, 1), span=(1, 3),
            flag=wx.TOP|wx.EXPAND, border=5)

        self.btn_video_browse = wx.Button(panel, label="Browse...")
        sizer.Add(self.btn_video_browse, pos=(3, 4), flag=wx.TOP|wx.RIGHT, border=5)
        self.btn_video_browse.Bind(wx.EVT_BUTTON,self.on_video_browse)

        text2 = wx.StaticText(panel, label="Model Algo")
        sizer.Add(text2, pos=(2, 0), flag=wx.LEFT|wx.TOP, border=10)

        self.algo = wx.ComboBox(panel,choices=ALGO,value="choose an algo")
        sizer.Add(self.algo, pos=(2, 1), span=(1, 3), flag=wx.TOP|wx.EXPAND,
            border=5)
        self.algo.Bind(wx.EVT_COMBOBOX, self.on_algo_selected)


        text4 = wx.StaticText(panel, label="Threshold")
        sizer.Add(text4, pos=(4, 0), flag=wx.TOP|wx.LEFT, border=10)

        slider = wx.Slider(panel,value = 10, minValue = 1, maxValue = 100,
                       style = wx.SL_HORIZONTAL|wx.SL_LABELS)
        sizer.Add(slider, pos=(4, 1), span=(1, 3), flag=wx.TOP|wx.EXPAND,border=5)

        slider.Bind(wx.EVT_SLIDER,self.on_slider_scroll)


        text4 = wx.StaticText(panel, label="NumFrame")
        sizer.Add(text4, pos=(5, 0), flag=wx.TOP|wx.LEFT, border=10)

        self.sliderNumFrame = wx.Slider(panel,value = 15, minValue = 1, maxValue = 100,
                       style = wx.SL_HORIZONTAL|wx.SL_LABELS)
        sizer.Add(self.sliderNumFrame,pos=(5, 1), span=(1, 3), flag=wx.TOP|wx.EXPAND,border=5)

        self.sliderNumFrame.Bind(wx.EVT_SLIDER,self.on_slider_scroll_numFrame)

        self.stop_btn = wx.Button(panel, label="Stop")
        sizer.Add(self.stop_btn, pos=(7, 3))
        self.stop_btn.Bind(wx.EVT_BUTTON,self.on_stop)
        self.stop_btn.Disable()

        run_btn = wx.Button(panel, label='Run')
        sizer.Add(run_btn, pos=(7, 0), flag=wx.LEFT, border=10)
        run_btn.Bind(wx.EVT_BUTTON,self.on_run)


        quit_btn = wx.Button(panel, label="Quit")
        sizer.Add(quit_btn, pos=(7, 4), span=(1, 1),
            flag=wx.BOTTOM|wx.RIGHT, border=10)
        quit_btn.Bind(wx.EVT_BUTTON,self.on_close)

        sizer.AddGrowableCol(2)

        panel.SetSizer(sizer)
        sizer.Fit(self)


def main():

    app = wx.App()
    ex = GUI(None, title="background modeling")
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()