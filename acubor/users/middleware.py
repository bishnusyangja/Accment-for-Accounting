from users.models import Role
from users.models import Company, TrackUserInfo
from ipware.ip import get_real_ip
from geoip import geolite2

class RoleMiddleware(object):
    def process_request(self, request):
        if not request.user.is_anonymous():
            roles = Role.objects.filter(user=request.user)
            if not request.user.currently_activated_company and len(roles):
                request.user.currently_activated_company = roles[0].company
                request.user.save()
            if len(roles):
                request.__class__.company = Company.objects.get(id=request.user.currently_activated_company.id)
                request.__class__.roles = Role.objects.filter(user=request.user,
                                                              company=request.user.currently_activated_company)
                groups = []
                for role in request.roles:
                    groups.append(role.group)
                request.__class__.groups = groups
            else:
                request.__class__.groups = []
                request.__class__.roles = []
                request.__class__.company = None
                #request.__class__.role = None


class IPFromRequestMiddleware(object):
    def process_request(self, request):
        ip = get_real_ip(request)
        if ip is not None:
            if len(TrackUserInfo.objects.filter(ipaddress=ip)) < 2:
                tracked_data, created = TrackUserInfo.objects.get_or_create(ipaddress=ip)
                temp_count = tracked_data.count
                temp_count += 1
                tracked_data.count = temp_count
                match = geolite2.lookup(str(ip))
                if match is not None:
                    tracked_data.country = match.country
                    tracked_data.continent = match.continent
                    tracked_data.timezone = match.timezone
                    tracked_data.latitude = match.location[0]
                    tracked_data.longitude = match.location[1]
                tracked_data.save()

