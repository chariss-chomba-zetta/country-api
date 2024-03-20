import json
import os.path
from abc import ABC, abstractmethod

from django.conf import settings

from menus.models import OmniService, UssdMenu

REPORT_BY_OMNI_SERVICE_BASE_FILENAME = 'report_by_omni_service'
REPORT_BY_RELATED_NODES_BASE_FILENAME = 'report_by_related_nodes'
EMPTY_SUFFIX = '___empty'


class BaseServiceLayerChecker(ABC):
    omni_services_base_url = 'http://ussd:8092'  # change that to match urls accordingly

    def __init__(self):
        super().__init__()
        self.assets_folder = os.path.join(settings.BASE_DIR, 'data_assets', 'checks', 'service_layer')
        self.service_layer_urls_file = os.path.join(self.assets_folder, 'service_layer_urls.txt')

        self.service_layer_endpoints = self.get_service_layer_endpoints()

    def save_to_json(self, filename, obj):
        result_file = os.path.join(self.assets_folder, filename)
        with open(result_file, 'w') as json_file:
            json.dump(obj, json_file)
            json_file.close()

    def get_service_layer_endpoints(self):
        with open(self.service_layer_urls_file, 'r') as f:
            lines = f.readlines()
            endpoints = {f'{self.omni_services_base_url}{line.split()[0]}': line.split()[1] for line in lines}
            f.close()
        return endpoints

    @abstractmethod
    def report_all(self):
        pass


class CheckServiceLayerEndpointsForCurrentCountry(BaseServiceLayerChecker):
    def __init__(self, omni_services_base_url=None):
        super().__init__()
        if omni_services_base_url is not None:
            self.omni_services_base_url = omni_services_base_url

        self.omni_services_by_endpoint = self.get_all_omni_services_per_endpoint()
        self.all_menus_by_omni_service = self.get_all_menus_by_omni_service_as_objects()

    def get_all_omni_services_per_endpoint(self):
        omni_services = {}
        for endpoint in self.service_layer_endpoints:
            omni_services[endpoint] = list(OmniService.objects.filter(url__exact=endpoint))
        return omni_services

    def get_all_menus_by_omni_service_as_objects(self):
        result_dict = {}
        for endpoint in self.service_layer_endpoints:
            result_dict[endpoint] = {}
            for omni_service in self.omni_services_by_endpoint[endpoint]:
                result_dict[endpoint][omni_service] = list(UssdMenu.objects.filter(omni_service=omni_service))
        return result_dict

    def report_by_omni_service(self, save_json_file=True, only_empty=False):
        result_dict = {}
        for endpoint, views in self.omni_services_by_endpoint.items():
            if only_empty and bool(views):
                continue
            view_names = [str(view) for view in views]
            result_dict[endpoint] = view_names

        if save_json_file:
            filename = f'{settings.COUNTRY_CODE}___{REPORT_BY_OMNI_SERVICE_BASE_FILENAME}'
            if only_empty:
                filename += EMPTY_SUFFIX
            filename += '.json'
            self.save_to_json(filename=filename, obj=result_dict)

        return result_dict

    def report_by_related_nodes(self, save_json_file=True, only_empty=False):
        result_dict = {}
        for endpoint in self.omni_services_by_endpoint:
            for omni_service in self.all_menus_by_omni_service[endpoint]:
                views = self.all_menus_by_omni_service[endpoint][omni_service]
                for view in views:
                    next_screen_views = UssdMenu.objects.filter(next_screen=view)
                    temp_menus = [str(temp_view) for temp_view in next_screen_views]
                    if only_empty and bool(temp_menus):
                        continue

                    result_dict[endpoint] = {}
                    temp_dict = {
                        'next_screen': str(view.next_screen),
                        'menus_that_points_to_this_menu': temp_menus,
                    }

                    result_dict[endpoint][str(view)] = temp_dict

        if save_json_file:
            filename = f'{settings.COUNTRY_CODE}___{REPORT_BY_RELATED_NODES_BASE_FILENAME}'
            if only_empty:
                filename += EMPTY_SUFFIX
            filename += '.json'
            self.save_to_json(filename=filename, obj=result_dict)

        return result_dict

    def report_all(self):
        self.report_by_omni_service(only_empty=False)
        self.report_by_omni_service(only_empty=True)

        self.report_by_related_nodes(only_empty=False)
        self.report_by_related_nodes(only_empty=True)


class CheckOverallEmptyServiceLayerEndpoints(BaseServiceLayerChecker):
    def __init__(self):
        super().__init__()
        self._reversed_country_list = {d_val: d_key for d_key, d_val in settings.SUPPORTED_COUNTRIES.items()}
        self._reports_by_omni_service = self._read_report_by_omni_service_files()
        self._reports_by_related_nodes = self._read_report_by_related_nodes_files()

    def _read_report_by_omni_service_files(self):
        result_data = {}
        for country_code in list(settings.SUPPORTED_COUNTRIES.keys()):
            filename = f'{country_code}___{REPORT_BY_OMNI_SERVICE_BASE_FILENAME}{EMPTY_SUFFIX}.json'
            with open(os.path.join(self.assets_folder, filename)) as file:
                result_data[country_code] = json.load(file)
                file.close()

        return result_data

    def _read_report_by_related_nodes_files(self):
        result_data = {}
        for country_code in list(settings.SUPPORTED_COUNTRIES.keys()):
            filename = f'{country_code}___{REPORT_BY_RELATED_NODES_BASE_FILENAME}{EMPTY_SUFFIX}.json'
            with open(os.path.join(self.assets_folder, filename)) as file:
                result_data[country_code] = json.load(file)
                file.close()

        return result_data

    def report_by_omni_service(self, save_json_file=True):
        result_dict = {}
        for url in self.service_layer_endpoints:
            temp_check = {url in self._reports_by_omni_service[country] for country in settings.SUPPORTED_COUNTRIES}
            if False not in temp_check and len(temp_check) == 1:
                result_dict[url] = self.service_layer_endpoints[url]

        if save_json_file:
            filename = f'OVERALL___{REPORT_BY_OMNI_SERVICE_BASE_FILENAME}.json'
            self.save_to_json(filename=filename, obj=result_dict)
        return result_dict

    def report_by_related_nodes(self, save_json_file=True):
        result_dict = {}
        for url in self.service_layer_endpoints:
            checker = {url in self._reports_by_related_nodes[country] for country in settings.SUPPORTED_COUNTRIES}
            if False not in checker and len(checker) == 1:
                result_dict[url] = self.service_layer_endpoints[url]

        if save_json_file:
            filename = f'OVERALL___{REPORT_BY_RELATED_NODES_BASE_FILENAME}.json'
            self.save_to_json(filename=filename, obj=result_dict)

        return result_dict

    def report_all(self):
        self.report_by_omni_service()
        self.report_by_related_nodes()
