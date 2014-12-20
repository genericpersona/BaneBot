# -*- coding: utf-8 -*-

# Imports
from glob import glob
from importlib import import_module
import inspect
import json
import os
import platform
import shlex
import sys
import textwrap
import traceback

from twisted.internet import inotify, protocol, reactor
from twisted.python import filepath, log
from twisted.python.rebuild import rebuild
from twisted.words.protocols import irc

import plugins.PluginBase as pb
from utils.utf8 import decode, encode

# Constants
VERSION_NAME = 'BaneBot'
VERSION_NUM = '0.1'
VERSION_ENV = platform.platform()
SOURCE_URL = 'https://github.com/genericpersona/banebot'

class BaneBot(irc.IRCClient):
    versionName = VERSION_NAME
    versionNum = VERSION_NUM
    versionEnv = VERSION_ENV
    sourceURL = SOURCE_URL

    def __init__(self, net_conf):
        '''
        BaneBot constructor.

        Parameters
        ----------
            net_conf: dict
              Dictionary with network config information
        '''
        # Save all net_conf values as attributes
        for k, v in net_conf.iteritems():
            setattr(self, k, v)

        # For sending long lines of text
        # Maps a nickname to the text
        # left to send
        self._mored = {}

    def action(self, user, channel, data):
        '''Called when I see a user perform an action.
        '''
        # Treat it like a privmsg which might contain a command
        return self.privmsg(user, channel, data)

    def alterCollidedNick(self, nickname):
        return '`{}`'.format(nickname)

    def balanced(self, u, left, right):
        '''Return true if u has balanced
        left and right unicode characters.
        '''
        bal_stack = []
        for char in u:
            if char == left:
                bal_stack.insert(0, char)

            elif char == right:
                if not bal_stack:
                    return False

                bal_stack.pop(0)

        return len(bal_stack) == 0

    def connectionLost(self, reason):
        if self.logging:
            log.err('Connection lost: {!r}'.format(reason))
        irc.IRCClient.connectionLost(self, reason)

    def connectionMade(self):
        if self.logging:
            log.msg('Connection made to {}'.format(self.server))
        irc.IRCClient.connectionMade(self)

    def eval(self, expr):
        '''Evaluate an expression, which might contain
        nested expressions.
        '''
        # Evaluate each inner list
        for i in range(len(expr) - 1, -1, -1):
            if type(expr[i]) == list:
                expr[i] = self.eval(expr[i])
       
        self.cmnd, rest = expr[0].lstrip(self.fact.prefix), expr[1:]
        rest = [word for word in rest if word and not word.isspace()]

        if self.cmnd in self.fact.commands:
            response = self.fact.commands[self.cmnd](rest, self)

            if response:
              return encode(response)
            else:
              return u''
        else:
            return u''

    def getCommand(self, msg):
        '''
        Isolate the portion of a privmsg msg
        containing a command and its arguments for
        a command-based plugin.

        Return the isolated portion of the msg if a
        command is found, or an empty unicode object
        otherwise.
        '''
        # Command with a prefix at the start of the line
        if msg.startswith(self.fact.prefix):
            return msg.lstrip(self.fact.prefix)

        # Inline command with parenthesis
        elif msg.find(self.fact.inline_prefix) != -1:
            start = msg.find(self.fact.inline_prefix)
            end = msg.find(self.fact.inline_suffix)
            if end == -1:
                return u''

            return msg[start:end+1].\
                    lstrip(self.fact.inline_prefix).\
                    rstrip(self.fact.inline_suffix)

        # Inline command without parenthesis
        elif msg.find(self.fact.prefix) != -1:
            return msg[msg.find(self.fact.prefix):].lstrip(self.fact.prefix)

        # No command found
        else:
            return u''

    def irc_RPL_ENDOFWHO(self, *nargs):
      '''End of WHO reply
      '''
      if self.who_reply[0] is not None:
          nick = self.who_reply[-1][5]
          username = self.who_reply[-1][2]
          host = self.who_reply[-1][3]
          full = u'{} ({}@{})'.format(nick, username, host)
          reply = u'{} is online'.format(full)
      else:
          reply = u'{} is not online'.format(self.who_reply[-1])

      self.msg(self.channel if not self.pm else self.sender, encode(reply))

    def irc_RPL_WHOREPLY(self, *nargs):
      '''
      Handles WHO response
      '''
      self.who_reply = nargs

    def irc_unknown(self, prefix, command, params):
      '''
      Currently, just supports joining on invite.
      '''
      if command == 'INVITE':
          self.join(params[1])

    def joined(self, channel):
        if self.logging:
            log.msg('Joined {}'.format(channel))

    def kickedFrom(self, channel, kicker, message):
        if self.logging:
            log.msg('Kicked from {} by {} ({})'.format(channel, kicker, message))

        if self.fact.rejoin_after_kick:
            self.join(channel)

    def moreSend(self, to, msg):
        '''Sends a maximum amount of text at a time and stores the rest
        which can be sent with the more plugin.
        '''
        # Get the msg length to split up the text into lines
        lines = textwrap.wrap(msg, self.fact.max_line_len)
        lines = lines[:self.fact.max_more_lines]

        # Save it in the dict for the more plugin
        self._mored[self.sender] = lines

        # Get the next line to send
        line = lines.pop(0)

        # What to put at the end of the line
        suffix = u' \x02({} more messages)\x02'.format(len(lines)) if lines \
                    else u''

        # Send the message with the suffix
        if type(line) == str:
            line = unicode(line, "utf-8", errors="ignore")
        self.msg(to, encode(u'{}{}'.format(line, suffix)))

    def noticed(self, user, channel, message):
        '''Called when a NOTICE message is sent.
        '''
        if self.logging:
            log.msg('[{}] <{}> {}'.format(channel, user, encode(message)))

    def parse(self, msg):
        '''Return a list of unicode objects and/or lists of
        unicode objects.  The first unicode object in a list
        is the name of a command.  The remaining unicode
        objects are arguments.  An inner list represents another
        expression to be evaluated.
        '''
        # Make sure msg is balanced before proceeding
        if not self.balanced(msg, 
                self.fact.nested_prefix, self.fact.nested_suffix):
            raise SyntaxError(self.fact.unbalanced_error.\
                    format(self.fact.nested_prefix, self.fact.nested_suffix))

        # Because self.prefix gets stripped away, the parser
        # needs to enclose everything as a nested command or
        # only the first token encountered is returned
        return self.readFrom([self.fact.nested_prefix] + \
                             self.tokenize(msg) + \
                             [self.fact.nested_suffix])

    def privmsg(self, user, channel, msg):
        # Save needed information
        self.sender = user.split('!', 1)[0]
        self.channel = channel
        self.pm = channel == self.nickname
        self.error = False
        msg = decode(msg)

        cmnd = self.getCommand(msg)
        if cmnd:
            try:
              response = self.eval(self.parse(cmnd))
              if response:
                  return self.moreSend(\
                            self.sender if self.pm else channel, response)
            except pb.CommandError, ce:
              return self.msg(self.sender if ce.pm else channel,
                      encode(u'{}'.format(se)))
            except SyntaxError, se:
              return self.msg(self.sender if self.pm else channel, 
                      encode(u'{}'.format(se)))
            finally:
              # Log each command responded to
              if self.logging:
                log.msg('[{}] <{}> {}'.format(channel, user, encode(msg)))

        # Check the non-command plugins
        for name in self.fact.line_plugins:
            if self.fact.plugins[name].hasResponse(msg, self):
                self.msg(self.sender if self.pm else channel,
                            encode(self.response))

    def readFrom(self, tokens, depth=0):
        '''Read, and return, an expression, i.e., a list
        of unicode objects and/or other expressions, from
        a sequence of tokens.

        Taken from http://norvig.com/lis.py
        '''
        if not tokens:
            raise SyntaxError(self.eol_error)

        token = tokens.pop(0)
        if self.fact.nested_prefix == token:
            if depth == self.fact.max_nesting + 1:
                raise SyntaxError(self.fact.max_nesting_error.\
                                    format(self.fact.max_nesting))

            L = []
            while tokens[0] != self.fact.nested_suffix:
                L.append(self.readFrom(tokens, depth + 1))

            # Pop off the nested suffix
            tokens.pop(0)
            return L

        elif self.fact.nested_suffix == token:
            raise SyntaxError(self.fact.unexpected_error.\
                    format(self.fact.nested_suffix))

        else:
            return token

    def signedOn(self):
        # Auth with NickServ
        if hasattr(self, 'nickserv_pw'):
            self.msg('NickServ', 
                'IDENTIFY {}'.format(self.nickserv_pw))

        for channel in self.channels:
            self.join(channel)

    def tokenize(self, msg):
        '''Turn a msg into a list of tokens
        '''
        for replace in (self.fact.nested_prefix, self.fact.nested_suffix):
            msg = msg.replace(replace, u' {} '.format(replace))

        try:
            return shlex.split(msg)
        except ValueError:
            return msg.split()

class BaneBotFactory(protocol.ClientFactory):
    encoding = 'utf-8'

    def __init__(self, config, network):
      # Save the config and needed directories
      for k, v in config.iteritems():
          setattr(self, k, v)
      self.config_dir = os.path.join(self.base_dir, 'config/')
      self.plugins_dir = os.path.join(self.base_dir, 'plugins/')
      self.plugins_config = os.path.join(self.config_dir, 'plugins/')

      if self.logging:
          mode = 'a' if self.log_append else 'w'
          log.startLogging(open(self.log_file, mode), setStdout=False)

      # Save the networks to connect to
      self.network = network

      # Load plugins 
      self.plugins = {}
      self.commands = {}
      self.line_plugins = set()
      self.loadPlugins()

      # Set-up auto-reloading of plugins
      self.setupAutoReloading()

    def buildProtocol(self, addr):
        '''
        Set up the correct relationship b/w a BaneBot
        instance and the BaneBotFactory.
        '''
        bb = BaneBot(self.network)

        bb.fact = self
        bb.logging = self.logging

        return bb

    def clientConnectionLost(self, connector, reason):
        if self.logging:
            log.err('Connection lost: {!r}'.format(reason))
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        if self.logging:
            log.err('Connection failed: {!r}'.format(reason))
        reactor.stop()

    def loadPluginObject(self, module, reloading=False):
        for name, value in inspect.getmembers(module, inspect.isclass):
            if issubclass(value, pb.PluginBase):
                try:
                    plugin_config = os.path.join(self.plugins_config, '{}.conf'.format(name))
                    plugin_config = json.loads(open(plugin_config).read())
                except:
                    plugin_config = {}

                if plugin_config.get('disabled', False):
                    continue

                if reloading and name in sys.modules:
                    reload(sys.modules[name])
                self.plugins[name] = value(plugin_config)
                if self.logging:
                    log.msg('Loaded plugin object: {}'.format(name))

                if hasattr(self.plugins[name], 'commands'):
                    for k, v in self.plugins[name].commands().iteritems():
                        if k in self.commands and not reloading:
                            log.err('[Error]: Duplicate command named {}'.format(k))
                            quit('Duplicate command named {}'.format(k))
                        else:
                            self.commands[k] = v

                if issubclass(value, pb.LinePlugin):
                    self.line_plugins.add(name)

    def loadPluginObjects(self):
        for module in self.modules.values():
            self.loadPluginObject(module)

    def loadPlugins(self):
        # Get a list of all .py files in the plugins directory
        plugins = [ f.split('/')[-1] \
                    for f in glob('{}*.py'.format(self.plugins_dir)) \
                    if not f.endswith('__init__.py') and \
                       not f.endswith('PluginBase.py') 
                  ]

        # Import all the plugins and save a mapping of name to module
        self.modules = { os.path.join(self.plugins_dir, plugin): \
                         import_module('plugins.{}'.format(os.path.splitext(plugin)[0])) \
                         for plugin \
                         in plugins
                       }

        # Create objects for all plugin classes
        self.loadPluginObjects()

    def reloadPluginModule(self, stuff, filepath, mask):
        # Get the actual filepath
        afpath = os.path.abspath(filepath.path).replace('.conf', '.py')

        # See if we need to reload a plugin, load a new plugin, or ignore
        if mask == inotify.IN_MODIFY and afpath in self.modules:
            try:
                self.modules[afpath] = rebuild(self.modules[afpath])
                self.loadPluginObject(self.modules[afpath], reloading=True)
                if self.logging:
                    log.msg('Reloaded {}'.format(filepath))
            except:
                if self.logging:
                    log.err('Failed to reload {} | {} | {}'.\
                            format( filepath
                                  , sys.exc_info()[0]
                                  , traceback.format_exc()
                                  )
                           )

        elif mask == inotify.IN_CREATE and afpath.endswith('.py'):
            plugin = afpath.split('/')[-1].rstrip('.py')
            self.modules[afpath] = import_module('plugins.{}'.format(plugin))

        else:
            return

    def setupAutoReloading(self):
        notifier = inotify.INotify()
        notifier.startReading()
        notifier.watch(filepath.FilePath(self.plugins_dir), callbacks=[self.reloadPluginModule])
        notifier.watch(filepath.FilePath(self.plugins_config), callbacks=[self.reloadPluginModule])
