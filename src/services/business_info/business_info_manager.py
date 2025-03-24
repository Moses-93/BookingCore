from src.services.business_info.business_info_service import BusinessInfoService


class BusinessInfoManager:

    def __init__(self, business_info_service: BusinessInfoService):
        self.business_info_service = business_info_service
