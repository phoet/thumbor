#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/thumbor/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com timehome@corp.globo.com

from preggy import expect

from thumbor.config import Config
from thumbor.importer import Importer

from tests.base import TestCase


class BaseMaxAgeFilterTestCase(TestCase):
    def get_fixture_path(self, name):
        return './tests/fixtures/%s' % name

    def get_config(self):
        return Config.load(self.get_fixture_path('max_age_conf.py'))

    def get_importer(self):
        importer = Importer(self.config)
        importer.import_modules()
        return importer


class MaxAgeFilterTestCase(BaseMaxAgeFilterTestCase):
    def test_max_age_filter_with_regular_image(self):
        response = self.fetch('/unsafe/smart/image.jpg', method='GET')
        expect(response.code).to_equal(200)
        expect(response.headers['Cache-Control']).to_equal('max-age=2,public')
        expect(response.headers).to_include('Expires')

    def test_max_age_url(self):
        response = self.fetch('/unsafe/filters:max_age(30)/image.jpg', method='GET')
        expect(response.code).to_equal(200)
        expect(response.headers['Cache-Control']).to_equal('max-age=30,public')
        expect(response.headers).to_include('Expires')


class MaxAgeDetectorFilterTestCase(BaseMaxAgeFilterTestCase):
    def get_config(self):
        config = super(MaxAgeDetectorFilterTestCase, self).get_config()
        config.DETECTORS = ['tests.fixtures.prevent_result_storage_detector']
        return config

    def test_max_age_filter_with_non_storaged_image(self):
        response = self.fetch('/unsafe/smart/image.jpg', method='GET')
        expect(response.code).to_equal(200)
        expect(response.headers['Cache-Control']).to_equal('max-age=1,public')
        expect(response.headers).to_include('Expires')


class MaxAgeErrorDectectorFilterTestCase(BaseMaxAgeFilterTestCase):
    def get_config(self):
        config = super(MaxAgeErrorDectectorFilterTestCase, self).get_config()
        config.DETECTORS = ['tests.fixtures.detection_error_detector']
        return config

    def test_with_detection_error_image(self):
        response = self.fetch('/unsafe/smart/image.jpg', method='GET')
        expect(response.code).to_equal(200)
        expect(response.headers['Cache-Control']).to_equal('max-age=1,public')
        expect(response.headers).to_include('Expires')
