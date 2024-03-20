import logging
import traceback

from rest_framework import status, generics
from rest_framework.response import Response
from .serializers import UpdateRedisSerializer, RedisOmniServicesSerializer
from menus.menu_builder import update_redis_menus, update_redis_omni_services
from menus.menu_builder.exceptions import MenuGenerationException

logger = logging.getLogger('CountryApiLogger')


class UpdateRedisCacheView(generics.GenericAPIView):
    serializer_class = UpdateRedisSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        shortcode = serializer.validated_data['shortCode']
        logger.debug(f'{shortcode}-|ShortCode|Starting to update menus')
        try:
            menus = update_redis_menus(shortcode=shortcode)
        except MenuGenerationException as e:
            log_msg = f"UpdateRedisCacheView|Error is:{traceback.format_exc()}"
            logger.error(log_msg)
            http_status = status.HTTP_500_INTERNAL_SERVER_ERROR
            response_data = {
                "statusCode": "99",
                "message": "Server error",
                "status": False,
            }
            return Response(data=response_data, status=http_status)
        if menus != None and type(menus) != str:
            logger.info(f'{shortcode}-|Shortcode|Finished updating menus successfully')
            response_data = {
                "status": True,
                "statusCode": "00",
                "message": "Menus updated successfully",
                "menus": menus,
            }
        else:
            logger.info(f'{shortcode}-|Shortcode|Menus not updated successfully')
            response_data = {
                "status": False,
                "statusCode": "99",
                "message": "Menus not updated",
                "menus": menus,
            }

        return Response(data=response_data, status=status.HTTP_200_OK)


class UpdateRedisOmniServicesView(generics.GenericAPIView):
    serializer_class = RedisOmniServicesSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        shortcode = serializer.validated_data['shortCode']
        error_resp = {
                "statusCode": "99",
                "message": "Server error",
                "status": False,
            }
        logger.debug(f'{shortcode}-|ShortCode|Starting to update omni services')
        try:
            omni_services = update_redis_omni_services(shortcode=shortcode)
            logger.info(f'{len(omni_services)} Omni Services updated')
        except Exception as e:
            log_msg = f"UpdateRedisOmniServicesView|Error is:{traceback.format_exc()}"
            logger.error(log_msg)
            http_status = status.HTTP_500_INTERNAL_SERVER_ERROR
            return Response(data=error_resp, status=http_status)
        if omni_services != None:
            logger.info(f'{shortcode}-|Shortcode|Finished updating Omni Services successfully')
            response_data = {
                "status": True,
                "statusCode": "00",
                "message": "Omni Services updated successfully",
                "omni_services": omni_services,
            }
        else:
            logger.info(f'{shortcode}-|Shortcode|Omni Services not updated successfully')
            response_data = error_resp
        return Response(data=response_data, status=status.HTTP_200_OK)
