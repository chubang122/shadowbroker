#!/usr/bin/python2.6
import code
import os
import sys

from fuzzbunch import env

"""
Set up core paths ok
配置核心路径

"""
(FB_FILE, FB_DIR, EDFLIB_DIR) = env.setup_core_paths( os.path.realpath(__file__))

""" 
Make sure our libraries are setup properly 
确认库配置正确
"""
#env.setup_lib_paths(os.path.abspath(__file__), EDFLIB_DIR)

"""
Plugin directories
定义拼接插件目录
"""
PAYLOAD_DIR = os.path.join(FB_DIR, "payloads")
EXPLOIT_DIR = os.path.join(FB_DIR, "exploits")
TOUCH_DIR   = os.path.join(FB_DIR, "touches")
IMPLANT_DIR = os.path.join(FB_DIR, "implants")
LP_DIR      = os.path.join(FB_DIR, "listeningposts")
EDE_DIR     = os.path.join(FB_DIR, "ede-exploits")
TRIGGER_DIR = os.path.join(FB_DIR, "triggers")
SPECIAL_DIR = os.path.join(FB_DIR, "specials")

"""
Fuzzbunch directories
"""
LOG_DIR    = os.path.join(FB_DIR, "logs")
FB_CONFIG = os.path.join(FB_DIR, "Fuzzbunch.xml")

from fuzzbunch.edfplugin import EDFPlugin
#from fuzzbunch.edeplugin import EDEPlugin
from fuzzbunch.fuzzbunch import Fuzzbunch
from fuzzbunch.pluginfinder import addplugins, PluginfinderError
from fuzzbunch import exception
from fuzzbunch.daveplugin import DAVEPlugin
from fuzzbunch.deployablemanager import DeployableManager

def do_interactive(fb):
    gvars = globals()
    gvars['quit'] = (lambda *x: fb.io.print_error("Press Ctrl-D to quit"))
    gvars['exit'] = gvars['quit']
    fb.io.print_warning("Dropping to Interactive Python Interpreter")
    fb.io.print_warning("Press Ctrl-D to exit")
    code.interact(local=gvars, banner="")
#主函数
def main(fb):
    #fb.printbanner()
    fb.cmdqueue.append("retarget")
    while 1:
        try:
            fb.cmdloop()
        except exception.Interpreter:
            do_interactive(fb)
        else:
            break

#加载插件
def load_plugins(fb):
    fb.io.pre_input(None)
    fb.io.print_msg("Loading Plugins")
    fb.io.post_input()
    addplugins(fb, "Exploit",       EXPLOIT_DIR, EDFPlugin)
    addplugins(fb, "Payload",       PAYLOAD_DIR, EDFPlugin)
    addplugins(fb, "Touch",         TOUCH_DIR,   EDFPlugin)
    addplugins(fb, "ImplantConfig", IMPLANT_DIR, EDFPlugin)
    addplugins(fb, "ListeningPost", LP_DIR,      EDFPlugin)
    addplugins(fb, "Special",       SPECIAL_DIR, DAVEPlugin, DeployableManager)
    #    addplugins(fb, "EDE-Exploit",   EDE_DIR,     EDEPlugin)
    #    addplugins(fb, "Trigger",       TRIGGER_DIR, EDFPlugin)

@exception.exceptionwrapped
def setup_and_run(config, fbdir, logdir):
    # Setup fb globally so that we can debug interactively if we want
    global fb
    fb = Fuzzbunch(config, fbdir, logdir)
    fb.printbanner()
    load_plugins(fb)
    main(fb)
#确认当前运行文件
if __name__ == "__main__":
    setup_and_run(FB_CONFIG, FB_DIR, LOG_DIR)
