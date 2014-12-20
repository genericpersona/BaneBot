# -*- coding: utf-8 -*-

'''
This plugin is lifted from supybot.
'''

###
# Copyright (c) 2002-2004, Jeremiah Fincher
# Copyright (c) 2008-2009, James McCoy
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
###

import cmath
import math
import re
import types

from twisted.python import log

import plugins.PluginBase as pb

class Math(pb.CommandPlugin):
  def __init__(self, conf):
    super(Math, self).__init__(conf)

    self.forbidden = re.compile('[_[\]]')
    self.buildMathEnv()

    self._mathRe = re.compile(r'((?:(?<![A-Fa-f\d)])-)?'
                              r'(?:0x[A-Fa-f\d]+|'
                              r'0[0-7]+|'
                              r'\d+\.\d+|'
                              r'\.\d+|'
                              r'\d+\.|'
                              r'\d+))') 

  def buildMathEnv(self):
    self._mathEnv = {'__builtins__': types.ModuleType('__builtins__'), 'i': 1j}
    self._mathEnv.update(math.__dict__)
    self._mathEnv.update(cmath.__dict__)
    self._mathEnv['sqrt'] = Math._sqrt
    self._mathEnv['cbrt'] = Math._cbrt
    self._mathEnv['abs'] = abs
    self._mathEnv['max'] = max
    self._mathEnv['min'] = min
    self._mathSafeEnv = dict([(x,y) for x,y in self._mathEnv.items() \
                              if x not in ['factorial']])

  def commands(self):
    return { 'calc': self.calc
           }

  def calc(self, args, irc):
    '''(calc <math expression>) -- Lifted from supybot.
    '''
    expr = ' '.join(args)
    try:
        expr = str(expr)
    except UnicodeEncodeError:
        return 'No Unicode allowed in math expressions.'

    if self.forbidden.match(expr):
        return 'No underscores or brackets allowed in math expressions.'

    if 'lambda' in expr:
        return 'lambda is not allowed in math expressions.'

    expr = self._mathRe.sub(Math.handleMatch, expr.lower())
    try:
        log.msg('evaluating %q from %s', expr, irc.sender)
        x = complex(eval(expr, self._mathSafeEnv, self._mathSafeEnv))
        return self._complexToString(x)
    except OverflowError:
        maxFloat = math.ldexp(0.9999999999999999, 1024)
        return 'The answer exceeded %s or so.' % maxFloat
    except TypeError:
        return 'Something in there wasn\'t a valid number.'
    except NameError as e:
        return '%s is not a defined function.' % str(e).split()[1]
    except Exception as e:
        return str(e)

  def _complexToString(self, x):
    realS = self._floatToString(x.real)
    imagS = self._floatToString(x.imag)
    if imagS == '0':
        return realS
    elif imagS == '1':
        imagS = '+i'
    elif imagS == '-1':
        imagS = '-i'
    elif x.imag < 0:
        imagS = '%si' % imagS
    else:
        imagS = '+%si' % imagS
    if realS == '0' and imagS == '0':
        return '0'
    elif realS == '0':
        return imagS.lstrip('+')
    elif imagS == '0':
        return realS
    else:
        return '%s%s' % (realS, imagS)

  def _floatToString(self, x):
    if -1e-10 < x < 1e-10:
        return '0'
    elif -1e-10 < int(x) - x < 1e-10:
        return str(int(x))
    else:
        return str(x) 

  @staticmethod
  def handleMatch(m):
    s = m.group(1)
    if s.startswith('0x'):
        i = int(s, 16)
    elif s.startswith('0') and '.' not in s:
        try:
            i = int(s, 8)
        except ValueError:
            i = int(s)
    else:
        i = float(s)

    x = complex(i)
    if x.imag == 0:
        x = x.real
        # Need to use string-formatting here instead of str() because
        # use of str() on large numbers loses information:
        # str(float(33333333333333)) => '3.33333333333e+13'
        # float('3.33333333333e+13') => 33333333333300.0
        return '%.16f' % x
    return str(x)

  @staticmethod
  def _sqrt(n):
    if isinstance(n, complex) or n < 0:
        return cmath.sqrt(n)
    else:
        return math.sqrt(n)

  @staticmethod
  def _cbrt(n):
    return math.pow(n, 1.0/3)
