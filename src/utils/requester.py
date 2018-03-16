import logging
from json import JSONDecodeError

import requests
from time import sleep
from multiprocessing.pool import ThreadPool


logger = logging.getLogger('Requester')


class Requester:
    """ service request wrapper """
    max_retries = 3
    retry_delay = 0
    timeout = 15

    _max_thread_count = 50

    @staticmethod
    def networked(func, max_retries=max_retries, delay=retry_delay):
        """ Network error retries wrapper"""
        retry_count = 0
        network_exception = None

        while retry_count < max_retries:
            try:
                return func()
            except requests.RequestException as exc:
                network_exception = exc
                logger.warning('Network error(retry #%d): %s', retry_count, exc)

            if retry_count:
                sleep(delay)
            retry_count += 1

        raise network_exception

    @classmethod
    def request_for_map_use(cls, request_args: dict):

        if 'timeout' not in request_args:
            request_args['timeout'] = cls.timeout
        try:
            response = cls.networked(lambda: requests.request(**request_args))
        except requests.RequestException:
            return request_args, None

        response.close()
        return request_args, response

    @classmethod
    def request(cls, request_args: dict, session=None):
        """
        On request error returns None
        """
        if 'timeout' not in request_args:
            request_args['timeout'] = cls.timeout
        try:
            if session:
                response = cls.networked(lambda: session.request(**request_args))
            else:
                response = cls.networked(lambda: requests.request(**request_args))
        except requests.RequestException:
            return None

        response.close()
        return response

    @staticmethod
    def parse_response(response):
        """
        If response is None, returns 503 status
        """
        if response is None:
            return 503, {'detail': 'service is not available'}
        try:
            response_data = response.json()
        except JSONDecodeError:
            response_data = {'detail': response.text.strip()}
        return response.status_code, response_data

    @classmethod
    def request_and_parse(cls, request_args: dict, session=None):

        response = cls.request(request_args, session)
        status_code, response_data = cls.parse_response(response)

        return status_code, response_data

    @classmethod
    def async_requests_and_parse(cls, request_tasks: list) -> list:
        """
        :return: list of tuples [(request_args, http_status, response_data), ...]
        """

        responses = cls.async_requests(request_tasks)

        result = []
        for request_args, response in responses:
            http_status, response_data = Requester.parse_response(response)
            result.append((request_args, http_status, response_data))

        return result

    @classmethod
    def async_requests(cls, request_tasks: list) -> list:
        thread_count = min(cls._max_thread_count, len(request_tasks))
        pool = ThreadPool(thread_count)
        responses = pool.map(cls.request_for_map_use, request_tasks)
        pool.terminate()
        return responses
