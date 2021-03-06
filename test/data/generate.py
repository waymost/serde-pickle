# Copyright (c) 2015-2017 Georg Brandl.  Licensed under the Apache License,
# Version 2.0 <LICENSE-APACHE or http:#www.apache.org/licenses/LICENSE-2.0>
# or the MIT license <LICENSE-MIT or http:#opensource.org/licenses/MIT>, at
# your option. This file may not be copied, modified, or distributed except
# according to those terms.

"""Generate Pickle test cases for the test suite."""

# Run this with both Python 2.x and 3.x to generate all test files.

import sys
try:
    import cPickle as pickle
except ImportError:
    import pickle

longish = 10000000000 * 10000000000  # > 64 bits

# A test object that generates all the types supported, with HashableValue
# and normal Value variants.
test_object = {
    None: None,
    False: (False, True),
    10: 100000,
    longish: longish,
    1.0: 1.0,
    b"bytes": b"bytes",
    u"string": u"string",
    (1, 2): (1, 2, 3),
    frozenset((42, 0)): frozenset((42, 0)),
    (): [
        [1, 2, 3],
        set([42, 0]),
        {}
    ]
}

# Generate test file depending on protocol and Python major version.
major = sys.version_info[0]
max_proto = {2: 2, 3: 4}[major]
for proto in range(max_proto + 1):
    with open('tests_py%d_proto%d.pickle' % (major, proto), 'wb') as fp:
        pickle.dump(test_object, fp, proto)

# Do all else with Python 3 only.
if major == 2:
    sys.exit()

# Generate recursive structure.
rec_list = []
rec_list.append(([rec_list], ))
for proto in range(max_proto + 1):
    with open('test_recursive_proto%d.pickle' % proto, 'wb') as fp:
        pickle.dump(rec_list, fp, proto)
