# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc


###########################################################################
## Class sale_prediction
###########################################################################

class sale_prediction(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"食万净菜销量预测", pos=wx.DefaultPosition, size=wx.Size(1500, 650),
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetFont(wx.Font(16, 70, 90, 90, False, wx.EmptyString))
        self.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNTEXT))
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE))

        bSizer2 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticline6 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        bSizer2.Add(self.m_staticline6, 0, wx.EXPAND | wx.ALL, 5)

        self.title1 = wx.StaticText(self, wx.ID_ANY, u"#数据输入", wx.DefaultPosition, wx.DefaultSize, 0)
        self.title1.Wrap(-1)
        self.title1.SetFont(wx.Font(15, 70, 90, 92, False, "新宋体"))

        bSizer2.Add(self.title1, 0, wx.ALL, 5)

        self.m_staticText10 = wx.StaticText(self, wx.ID_ANY, u"选择历史销量数据和活动数据", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText10.Wrap(-1)
        self.m_staticText10.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNTEXT))
        self.m_staticText10.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INACTIVECAPTION))

        bSizer2.Add(self.m_staticText10, 0, wx.ALL, 5)

        self.file_pick1 = wx.FilePickerCtrl(self, wx.ID_ANY, u'C:\\Users\\yan.zy\\Desktop\\WorkStation\\2022-06-20 净菜销量预测\\input\\sale_data.xlsx', u"选择历史销量数据", u"*.*", wx.DefaultPosition,
                                            wx.Size(1400, -1), wx.FLP_DEFAULT_STYLE)
        bSizer2.Add(self.file_pick1, 0, wx.ALL, 5)

        self.file_pick2 = wx.FilePickerCtrl(self, wx.ID_ANY,
                                            u"C:\\Users\\yan.zy\\Desktop\\WorkStation\\2022-06-20 净菜销量预测\\input\\activity.xlsx",
                                            u"选择活动数据", u"*.xlsx", wx.DefaultPosition, wx.Size(1400, -1),
                                            wx.FLP_CHANGE_DIR | wx.FLP_DEFAULT_STYLE)
        bSizer2.Add(self.file_pick2, 0, wx.ALL, 5)

        self.title1_1 = wx.StaticText(self, wx.ID_ANY, u"输入预测天数", wx.DefaultPosition, wx.DefaultSize, 0)
        self.title1_1.Wrap(-1)
        self.title1_1.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INACTIVECAPTION))

        bSizer2.Add(self.title1_1, 0, wx.ALL, 5)

        self.m_textCtrl8 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer2.Add(self.m_textCtrl8, 0, wx.ALL, 5)

        self.button1 = wx.Button(self, wx.ID_ANY, u"Check", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer2.Add(self.button1, 0, wx.ALL, 5)

        self.m_staticline7 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        bSizer2.Add(self.m_staticline7, 0, wx.EXPAND | wx.ALL, 5)

        self.title2 = wx.StaticText(self, wx.ID_ANY, u"#数据训练及预测", wx.DefaultPosition, wx.Size(-1, -1), 0)
        self.title2.Wrap(-1)
        self.title2.SetFont(wx.Font(15, 70, 90, 92, False, "新宋体"))

        bSizer2.Add(self.title2, 0, wx.ALL, 5)

        self.button2 = wx.Button(self, wx.ID_ANY, u"开始训练及预测", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer2.Add(self.button2, 0, wx.ALL, 5)

        self.m_staticline8 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        bSizer2.Add(self.m_staticline8, 0, wx.EXPAND | wx.ALL, 5)

        self.m_staticText11 = wx.StaticText(self, wx.ID_ANY, u"#数据输出", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText11.Wrap(-1)
        self.m_staticText11.SetFont(wx.Font(15, 70, 90, 92, False, "新宋体"))

        bSizer2.Add(self.m_staticText11, 0, wx.ALL, 5)

        m_choice3Choices = [u"按照星期和天输出", u"按照天输出", u"按照星期输出"]
        self.m_choice3 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice3Choices, 0)
        self.m_choice3.SetSelection(0)
        bSizer2.Add(self.m_choice3, 0, wx.ALL, 5)

        self.m_staticText12 = wx.StaticText(self, wx.ID_ANY, u"数据输出文件夹", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText12.Wrap(-1)
        self.m_staticText12.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNTEXT))
        self.m_staticText12.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INACTIVECAPTION))

        bSizer2.Add(self.m_staticText12, 0, wx.ALL, 5)

        self.m_dirPicker1 = wx.DirPickerCtrl(self, wx.ID_ANY, u'C:\\Users\\yan.zy\\Desktop', u"Select a folder", wx.DefaultPosition,
                                             wx.Size(600, -1), wx.DIRP_DEFAULT_STYLE)
        bSizer2.Add(self.m_dirPicker1, 0, wx.ALL, 5)

        self.button3 = wx.Button(self, wx.ID_ANY, u"输出", wx.DefaultPosition, wx.DefaultSize, 0)
        self.button3.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))

        bSizer2.Add(self.button3, 0, wx.ALL, 5)

        self.SetSizer(bSizer2)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.button1.Bind(wx.EVT_BUTTON, self.DataCheck)
        self.button2.Bind(wx.EVT_BUTTON, self.PredictionCal)
        self.button3.Bind(wx.EVT_BUTTON, self.OutPut)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def DataCheck(self, event):
        event.Skip()

    def PredictionCal(self, event):
        event.Skip()

    def OutPut(self, event):
        event.Skip()


