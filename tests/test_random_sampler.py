# Copyright 2022 D-Wave Systems Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import time
import unittest

import dimod
import dimod.testing

from dwave.samplers import RandomSampler


@dimod.testing.load_sampler_bqm_tests(RandomSampler)
class TestRandomSampler(unittest.TestCase):
    def test_initialization(self):
        sampler = RandomSampler()

        dimod.testing.assert_sampler_api(sampler)

        self.assertEqual(sampler.properties, {})

    def test_energies(self):
        bqm = dimod.BinaryQuadraticModel({0: 0.0, 1: 0.0, 2: 0.0},
                                         {(0, 1): -1.0, (1, 2): 1.0, (0, 2): 1.0},
                                         1.0,
                                         dimod.SPIN)
        sampler = RandomSampler()
        response = sampler.sample(bqm, num_reads=10)

        dimod.testing.assert_response_energies(response, bqm)

    def test_kwargs(self):
        bqm = dimod.BinaryQuadraticModel({}, {}, 0.0, dimod.SPIN)
        with self.assertWarns(dimod.exceptions.SamplerUnknownArgWarning):
            RandomSampler().sample(bqm, a=5, b=2)

    def test_time_limit(self):
        t = time.time()

        bqm = dimod.BinaryQuadraticModel({0: 0.0, 1: 0.0, 2: 0.0},
                                         {(0, 1): -1.0, (1, 2): 1.0, (0, 2): 1.0},
                                         1.0,
                                         dimod.SPIN)

        t = time.perf_counter()
        sampleset = RandomSampler().sample(bqm, num_reads=10, time_limit=.02)
        runtime = time.perf_counter() - t

        self.assertTrue(.01 < runtime < .04)

        dimod.testing.assert_sampleset_energies(sampleset, bqm)
        self.assertEqual(len(sampleset), 10)
        self.assertGreater(sampleset.info['num_drawn'], 1000)  # should be much much bigger
