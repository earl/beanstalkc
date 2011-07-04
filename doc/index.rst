beanstalkc
==========

:mod:`beanstalkc` is a simple beanstalkd client library for Python.
`beanstalkd`_ is a simple, fast work queue service.

beanstalkc depends on `PyYAML`_, but there are ways to avoid this dependency.
See :ref:`Appendix A <tut-appendix-a>` of the tutorial for details.

beanstalkc is pure Python, and is compatible with `eventlet`_ and `gevent`_.

.. _beanstalkd: http://kr.github.com/beanstalkd/
.. _PyYAML: http://pyyaml.org/
.. _eventlet: http://eventlet.net/
.. _gevent: http://www.gevent.org/


Contents
========

.. toctree::
    :maxdepth: 2

    tutorial
    reference


Usage
=====

Here is a short example, to illustrate the flavour of :mod:`beanstalkc`::

    >>> import beanstalkc
    >>> beanstalk = beanstalkc.Connection(host='localhost', port=11300)
    >>> beanstalk.put('hey!')
    1
    >>> job = beanstalk.reserve()
    >>> job.body
    'hey!'
    >>> job.delete() 


License
=======

.. _Apache License, Version 2.0: http://www.apache.org/licenses/LICENSE-2.0

Copyright © 2008-2011, Andreas Bolka. Licensed under the `Apache License,
Version 2.0`_::

    Copyright 2008-2011 Andreas Bolka

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing,
    software distributed under the License is distributed on an "AS
    IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
    express or implied. See the License for the specific language
    governing permissions and limitations under the License.
