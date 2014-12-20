# -*- coding: utf-8 -*-

import plugins.PluginBase as pb

class About(pb.CommandPlugin):
  ABOUT = 'Based on BaneBot by genericpersona.'
  def __init__(self, conf):
    super(About, self).__init__(conf)

  def commands(self):
    return { 'about': self.about 
           }

  def about(self, args, irc):
    '''About the bot.
    '''
    return self.ABOUT
