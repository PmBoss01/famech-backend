from django.test import TestCase

from mechanics.models import MechanicProfile
from service_requests.models import Job, JobStatus, Request, RequestStatus
from service_requests.services import accept_job, complete_job, find_nearest_mechanics
from users.models import CustomUser, Role

ACCRA_LAT, ACCRA_LON = 5.6037, -0.1870


def make_mechanic(username, lat, lon, radius_km=15, available=True, verified=True):
    user = CustomUser.objects.create_user(username=username, password="x", role=Role.MECHANIC)
    return MechanicProfile.objects.create(
        user=user,
        business_name=username,
        latitude=lat,
        longitude=lon,
        service_radius_km=radius_km,
        is_available=available,
        is_verified=verified,
    )


class FindNearestMechanicsTests(TestCase):
    def test_orders_by_distance(self):
        far = make_mechanic("far", ACCRA_LAT + 0.05, ACCRA_LON + 0.05)
        near = make_mechanic("near", ACCRA_LAT + 0.01, ACCRA_LON + 0.01)

        results = list(find_nearest_mechanics(ACCRA_LAT, ACCRA_LON))

        self.assertEqual([r.id for r in results], [near.id, far.id])

    def test_excludes_unavailable_and_unverified(self):
        make_mechanic("unavailable", ACCRA_LAT, ACCRA_LON, available=False)
        make_mechanic("unverified", ACCRA_LAT, ACCRA_LON, verified=False)

        results = list(find_nearest_mechanics(ACCRA_LAT, ACCRA_LON))

        self.assertEqual(results, [])

    def test_excludes_outside_service_radius(self):
        make_mechanic("too_far", ACCRA_LAT + 1.0, ACCRA_LON + 1.0, radius_km=5)

        results = list(find_nearest_mechanics(ACCRA_LAT, ACCRA_LON))

        self.assertEqual(results, [])

    def test_coincident_coordinates_do_not_raise(self):
        mechanic = make_mechanic("coincident", ACCRA_LAT, ACCRA_LON)

        results = list(find_nearest_mechanics(ACCRA_LAT, ACCRA_LON))

        self.assertEqual([r.id for r in results], [mechanic.id])
        self.assertAlmostEqual(results[0].distance_km, 0.0, places=3)


class JobTransitionTests(TestCase):
    def setUp(self):
        self.owner = CustomUser.objects.create_user(username="owner", password="x", role=Role.OWNER)
        self.mechanic_a = make_mechanic("mech_a", ACCRA_LAT, ACCRA_LON)
        self.mechanic_b = make_mechanic("mech_b", ACCRA_LAT, ACCRA_LON)
        self.request = Request.objects.create(
            owner=self.owner, description="Flat tyre", latitude=ACCRA_LAT, longitude=ACCRA_LON
        )
        self.job_a = Job.objects.create(request=self.request, mechanic=self.mechanic_a.user)
        self.job_b = Job.objects.create(request=self.request, mechanic=self.mechanic_b.user)

    def test_accept_declines_sibling_jobs_and_updates_request(self):
        accept_job(self.job_a)
        self.job_b.refresh_from_db()
        self.request.refresh_from_db()

        self.assertEqual(self.job_a.status, JobStatus.ACCEPTED)
        self.assertEqual(self.job_b.status, JobStatus.DECLINED)
        self.assertEqual(self.request.status, RequestStatus.ACCEPTED)

    def test_complete_updates_request(self):
        accept_job(self.job_a)
        complete_job(self.job_a)
        self.request.refresh_from_db()

        self.assertEqual(self.job_a.status, JobStatus.COMPLETED)
        self.assertEqual(self.request.status, RequestStatus.COMPLETED)
